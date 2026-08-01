#!/usr/bin/env python

"""
Implementation-neutral behaviour tests for Delorean.

These describe what delorean does in terms that do not name a timezone
library: the instant a value represents, its UTC offset, its timezone name,
and its type. They are the regression net for the move from pytz to
`zoneinfo`, so nothing here may assert on pytz objects, pytz-specific
`repr()` output, or object identity against a particular timezone
implementation.

`delorean_tests.py` remains the implementation-level suite. This file is the
contract that must hold before and after the migration.
"""

import unittest
from datetime import date, datetime, timedelta, timezone, tzinfo
from unittest import mock
from zoneinfo import ZoneInfo

import delorean

EASTERN = "US/Eastern"

# 12:00 on these two days sits either side of a daylight saving transition, so
# the same wall clock resolves to a different offset and abbreviation.
WINTER_NAIVE = datetime(2013, 1, 15, 12, 0)
WINTER_UTC = datetime(2013, 1, 15, 17, 0, tzinfo=timezone.utc)
SUMMER_NAIVE = datetime(2013, 7, 15, 12, 0)
SUMMER_UTC = datetime(2013, 7, 15, 16, 0, tzinfo=timezone.utc)

# 02:30 never happens on this date; the clocks jump 02:00 EST -> 03:00 EDT.
SPRING_GAP_NAIVE = datetime(2013, 3, 10, 2, 30)
# 01:30 happens twice on this date, first as EDT and then again as EST.
FALL_AMBIGUOUS_NAIVE = datetime(2013, 11, 3, 1, 30)


def utc_instant(do):
    """The instant a Delorean represents, free of any timezone machinery."""
    return do.datetime.astimezone(timezone.utc)


class TimezoneTypes(unittest.TestCase):
    """What `.timezone` and `.datetime` hand back to a caller."""

    def test_timezone_is_a_tzinfo(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=EASTERN)

        self.assertIsInstance(do.timezone, tzinfo)

    def test_named_zone_is_identified_by_its_name(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=EASTERN)

        self.assertEqual(str(do.timezone), EASTERN)

    def test_utc_is_identified_as_utc(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone="UTC")

        self.assertEqual(str(do.timezone), "UTC")

    def test_datetime_is_aware(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=EASTERN)

        self.assertIsNotNone(do.datetime.tzinfo)
        self.assertIsNotNone(do.datetime.utcoffset())

    def test_naive_strips_the_timezone(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=EASTERN)

        self.assertIsNone(do.naive.tzinfo)

    def test_naive_is_the_utc_reading(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=EASTERN)

        self.assertEqual(do.naive, WINTER_UTC.replace(tzinfo=None))

    def test_date_is_a_date(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=EASTERN)

        self.assertEqual(do.date, date(2013, 1, 15))

    def test_accepts_a_zoneinfo_object(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=ZoneInfo(EASTERN))

        self.assertEqual(utc_instant(do), WINTER_UTC)

    def test_accepts_a_stdlib_fixed_offset(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=timezone(timedelta(hours=-5)))

        self.assertEqual(utc_instant(do), WINTER_UTC)


class OffsetsAndNames(unittest.TestCase):
    """Offsets and abbreviations, which are the observable part of a zone."""

    def test_standard_time_offset(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=EASTERN)

        self.assertEqual(do.datetime.utcoffset(), timedelta(hours=-5))
        self.assertEqual(do.datetime.tzname(), "EST")

    def test_daylight_time_offset(self):
        do = delorean.Delorean(SUMMER_NAIVE, timezone=EASTERN)

        self.assertEqual(do.datetime.utcoffset(), timedelta(hours=-4))
        self.assertEqual(do.datetime.tzname(), "EDT")

    def test_wall_clock_is_preserved_when_localizing(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=EASTERN)

        self.assertEqual(do.datetime.replace(tzinfo=None), WINTER_NAIVE)

    def test_instant_is_correct_when_localizing(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=EASTERN)

        self.assertEqual(utc_instant(do), WINTER_UTC)


class Parsing(unittest.TestCase):
    def test_offset_string_keeps_its_offset(self):
        do = delorean.parse("2015-01-01 00:01:02 -0800")

        self.assertEqual(do.datetime.utcoffset(), timedelta(hours=-8))
        self.assertEqual(
            utc_instant(do), datetime(2015, 1, 1, 8, 1, 2, tzinfo=timezone.utc)
        )

    def test_offset_string_timezone_is_a_tzinfo(self):
        do = delorean.parse("2015-01-01 00:01:02 -0800")

        self.assertIsInstance(do.timezone, tzinfo)
        self.assertEqual(do.timezone.utcoffset(None), timedelta(hours=-8))

    def test_utc_designator_is_utc(self):
        do = delorean.parse("2013-09-30T15:34:00.000Z")

        self.assertEqual(do.datetime.utcoffset(), timedelta(0))
        self.assertEqual(
            utc_instant(do), datetime(2013, 9, 30, 15, 34, tzinfo=timezone.utc)
        )

    def test_timezone_less_string_assumes_utc(self):
        do = delorean.parse("2015-02-04T16:33:21")

        self.assertEqual(do.datetime.utcoffset(), timedelta(0))
        self.assertEqual(str(do.timezone), "UTC")

    def test_assumed_timezone_is_applied(self):
        do = delorean.parse("2015-02-04T16:33:21", assume_timezone=EASTERN)

        self.assertEqual(do.datetime.utcoffset(), timedelta(hours=-5))
        self.assertEqual(str(do.timezone), EASTERN)

    def test_assumed_timezone_accepts_a_zoneinfo_object(self):
        do = delorean.parse("2015-02-04T16:33:21", assume_timezone=ZoneInfo(EASTERN))

        self.assertEqual(do.datetime.utcoffset(), timedelta(hours=-5))

    def test_assumed_timezone_is_ignored_when_the_string_has_one(self):
        do = delorean.parse("2015-01-01 00:01:02 -0800", assume_timezone=EASTERN)

        self.assertEqual(do.datetime.utcoffset(), timedelta(hours=-8))

    def test_timezone_argument_overrides_the_parsed_offset(self):
        do = delorean.parse("2015-01-01 00:01:02 -0500", timezone="US/Pacific")

        self.assertEqual(
            do.datetime.replace(tzinfo=None), datetime(2015, 1, 1, 0, 1, 2)
        )
        self.assertEqual(do.datetime.utcoffset(), timedelta(hours=-8))

    def test_strict_mode_rejects_a_timezone_less_string(self):
        with self.assertRaises(delorean.DeloreanInvalidDatetime):
            delorean.parse("2015-02-04T16:33:21", assume_timezone=None)

    def test_strict_mode_error_is_a_value_error(self):
        with self.assertRaises(ValueError):
            delorean.parse("2015-02-04T16:33:21", assume_timezone=None)

    def test_unreadable_string_is_a_value_error(self):
        with self.assertRaises(ValueError):
            delorean.parse("asd")


class DaylightSavingTieBreaks(unittest.TestCase):
    """
    How delorean resolves local times that are missing or duplicated.

    2.0 follows the standard library: a naive datetime carries ``fold=0``, so a
    duplicated local time means the first of its two occurrences, and a missing
    one is read against the offset in force before the transition. The gap
    answers match the pytz era exactly; the ambiguous ones deliberately do not.
    """

    def test_shifting_across_a_transition_keeps_the_wall_clock(self):
        do = delorean.Delorean(datetime(2013, 3, 9, 7, 0), timezone=EASTERN)

        shifted = do.next_day()
        self.assertEqual(
            shifted.datetime.replace(tzinfo=None), datetime(2013, 3, 10, 7, 0)
        )
        self.assertEqual(shifted.datetime.tzname(), "EDT")

    def test_nonexistent_local_time_resolves_to_standard_time(self):
        do = delorean.Delorean(SPRING_GAP_NAIVE, timezone=EASTERN)

        self.assertEqual(do.datetime.tzname(), "EST")
        self.assertEqual(
            utc_instant(do), datetime(2013, 3, 10, 7, 30, tzinfo=timezone.utc)
        )

    def test_ambiguous_local_time_takes_the_first_occurrence(self):
        do = delorean.Delorean(FALL_AMBIGUOUS_NAIVE, timezone=EASTERN)

        self.assertEqual(do.datetime.tzname(), "EDT")
        self.assertEqual(
            utc_instant(do), datetime(2013, 11, 3, 5, 30, tzinfo=timezone.utc)
        )

    def test_parse_resolves_a_nonexistent_local_time_the_same_way(self):
        do = delorean.parse("2013-03-10T02:30:00", assume_timezone=EASTERN)

        self.assertEqual(do.datetime.tzname(), "EST")

    def test_parse_resolves_an_ambiguous_local_time_the_same_way(self):
        do = delorean.parse("2013-11-03T01:30:00", assume_timezone=EASTERN)

        self.assertEqual(do.datetime.tzname(), "EDT")


class Shifting(unittest.TestCase):
    def test_shift_preserves_the_instant(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=EASTERN)
        before = utc_instant(do)

        do.shift("US/Pacific")

        self.assertEqual(utc_instant(do), before)

    def test_shift_changes_the_wall_clock_and_zone(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=EASTERN)

        do.shift("US/Pacific")

        self.assertEqual(do.datetime.replace(tzinfo=None), datetime(2013, 1, 15, 9, 0))
        self.assertEqual(str(do.timezone), "US/Pacific")

    def test_shift_to_an_unknown_zone_raises(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=EASTERN)

        with self.assertRaises(delorean.DeloreanInvalidTimezone):
            do.shift("Not/AZone")

    def test_named_day_shift_moves_a_week(self):
        do = delorean.Delorean(datetime(2013, 1, 20, 19, 41), timezone="UTC")

        self.assertEqual(
            do.next_tuesday().datetime.replace(tzinfo=None),
            datetime(2013, 1, 22, 19, 41),
        )

    def test_fractional_second_shift_moves_a_fraction(self):
        do = delorean.Delorean(datetime(2013, 1, 20, 0, 0, 0), timezone="UTC")

        self.assertEqual(
            do.next_second(0.5).datetime.replace(tzinfo=None),
            datetime(2013, 1, 20, 0, 0, 0, 500000),
        )

    def test_non_integer_shift_of_a_calendar_unit_raises(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone="UTC")

        with self.assertRaises(TypeError):
            do.next_month(1.5)


class MonthEndShifts(unittest.TestCase):
    def test_shift_into_a_shorter_month_clamps(self):
        do = delorean.Delorean(datetime(2015, 1, 31), timezone="UTC")

        self.assertEqual(do.next_month().datetime.date(), date(2015, 2, 28))

    def test_a_count_is_measured_from_the_original_date(self):
        do = delorean.Delorean(datetime(2015, 1, 31), timezone="UTC")

        self.assertEqual(do.next_month(2).datetime.date(), date(2015, 3, 31))

    def test_repeated_shifts_accumulate_the_clamp(self):
        do = delorean.Delorean(datetime(2015, 1, 31), timezone="UTC")

        self.assertEqual(
            do.next_month().next_month().datetime.date(), date(2015, 3, 28)
        )

    def test_leap_day_clamps_on_a_year_shift(self):
        do = delorean.Delorean(datetime(2024, 2, 29), timezone="UTC")

        self.assertEqual(do.next_year().datetime.date(), date(2025, 2, 28))


class PeriodBoundaries(unittest.TestCase):
    def setUp(self):
        self.do = delorean.Delorean(datetime(2015, 5, 15, 14, 30), timezone=EASTERN)

    def test_boundaries_return_delorean_objects(self):
        for name in (
            "start_of_day",
            "end_of_day",
            "start_of_month",
            "end_of_month",
            "start_of_year",
            "end_of_year",
            "midnight",
        ):
            with self.subTest(boundary=name):
                self.assertIsInstance(getattr(self.do, name), delorean.Delorean)

    def test_start_of_day_is_local_midnight(self):
        self.assertEqual(
            self.do.start_of_day.datetime.replace(tzinfo=None), datetime(2015, 5, 15)
        )

    def test_end_of_day_is_the_last_microsecond(self):
        self.assertEqual(
            self.do.end_of_day.datetime.replace(tzinfo=None),
            datetime(2015, 5, 15, 23, 59, 59, 999999),
        )

    def test_end_of_month_knows_month_length(self):
        self.assertEqual(
            self.do.end_of_month.datetime.date(),
            date(2015, 5, 31),
        )

    def test_end_of_month_knows_leap_years(self):
        do = delorean.Delorean(datetime(2024, 2, 15), timezone="UTC")

        self.assertEqual(do.end_of_month.datetime.date(), date(2024, 2, 29))

    def test_year_boundaries(self):
        self.assertEqual(self.do.start_of_year.datetime.date(), date(2015, 1, 1))
        self.assertEqual(self.do.end_of_year.datetime.date(), date(2015, 12, 31))

    def test_boundaries_keep_the_timezone(self):
        self.assertEqual(str(self.do.start_of_day.timezone), EASTERN)

    def test_boundaries_leave_the_original_untouched(self):
        before = utc_instant(self.do)

        self.do.start_of_day

        self.assertEqual(utc_instant(self.do), before)


class Arithmetic(unittest.TestCase):
    def test_adding_a_timedelta_moves_the_instant(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=EASTERN)

        self.assertEqual(
            utc_instant(do + timedelta(hours=1)), WINTER_UTC + timedelta(hours=1)
        )

    def test_subtracting_a_timedelta_moves_the_instant(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=EASTERN)

        self.assertEqual(
            utc_instant(do - timedelta(hours=1)), WINTER_UTC - timedelta(hours=1)
        )

    def test_subtracting_two_delorean_objects_gives_a_timedelta(self):
        first = delorean.Delorean(WINTER_NAIVE, timezone=EASTERN)
        second = delorean.Delorean(WINTER_NAIVE + timedelta(hours=3), timezone=EASTERN)

        self.assertEqual(second - first, timedelta(hours=3))

    def test_equality_is_by_instant_not_by_zone(self):
        pacific = delorean.Delorean(datetime(2015, 1, 1), timezone="US/Pacific")
        utc = delorean.Delorean(datetime(2015, 1, 1, 8), timezone="UTC")

        self.assertEqual(pacific, utc)

    def test_ordering_is_by_instant(self):
        earlier = delorean.Delorean(WINTER_NAIVE, timezone=EASTERN)
        later = delorean.Delorean(WINTER_NAIVE + timedelta(hours=1), timezone=EASTERN)

        self.assertLess(earlier, later)
        self.assertGreater(later, earlier)


class EpochRoundTrip(unittest.TestCase):
    def test_epoch_is_seconds_since_1970(self):
        do = delorean.Delorean(datetime(1970, 1, 1), timezone="UTC")

        self.assertEqual(do.epoch, 0.0)

    def test_timestamp_matches_the_utc_instant(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=EASTERN)

        self.assertEqual(do.timestamp, WINTER_UTC.timestamp())

    def test_from_timestamp_round_trips(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=EASTERN)

        self.assertEqual(utc_instant(delorean.from_timestamp(do.timestamp)), WINTER_UTC)

    def test_epoch_alias_round_trips(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=EASTERN)

        self.assertEqual(utc_instant(delorean.epoch(do.epoch)), WINTER_UTC)


class Helpers(unittest.TestCase):
    def test_localize_with_a_zone_name(self):
        dt = delorean.localize(WINTER_NAIVE, EASTERN)

        self.assertEqual(dt.utcoffset(), timedelta(hours=-5))
        self.assertEqual(dt.replace(tzinfo=None), WINTER_NAIVE)

    def test_localize_with_a_zoneinfo_object(self):
        dt = delorean.localize(WINTER_NAIVE, ZoneInfo(EASTERN))

        self.assertEqual(dt.utcoffset(), timedelta(hours=-5))

    def test_normalize_converts_to_the_target_zone(self):
        dt = delorean.normalize(WINTER_UTC, EASTERN)

        self.assertEqual(dt.replace(tzinfo=None), WINTER_NAIVE)
        self.assertEqual(dt.utcoffset(), timedelta(hours=-5))

    def test_normalize_with_a_zoneinfo_object(self):
        dt = delorean.normalize(WINTER_UTC, ZoneInfo(EASTERN))

        self.assertEqual(dt.replace(tzinfo=None), WINTER_NAIVE)

    def test_normalize_accepts_a_datetime_delorean_produced(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=ZoneInfo("UTC"))

        dt = delorean.normalize(do.datetime, EASTERN)

        self.assertEqual(dt.utcoffset(), timedelta(hours=-5))

    def test_normalize_rejects_a_naive_datetime(self):
        with self.assertRaises(ValueError):
            delorean.normalize(WINTER_NAIVE, EASTERN)

    def test_datetime_timezone_returns_an_aware_datetime(self):
        dt = delorean.datetime_timezone(EASTERN)

        self.assertIsNotNone(dt.tzinfo)


class Ranges(unittest.TestCase):
    def test_daily_range_counts_and_steps(self):
        stops = list(
            delorean.range_daily(start=datetime(2013, 1, 1), count=3, timezone=EASTERN)
        )

        self.assertEqual(len(stops), 3)
        self.assertEqual(
            [do.datetime.date() for do in stops],
            [date(2013, 1, 1), date(2013, 1, 2), date(2013, 1, 3)],
        )

    def test_range_carries_the_timezone(self):
        stops = list(
            delorean.range_daily(start=datetime(2013, 1, 1), count=1, timezone=EASTERN)
        )

        self.assertEqual(str(stops[0].timezone), EASTERN)
        self.assertEqual(stops[0].datetime.utcoffset(), timedelta(hours=-5))

    def test_stops_yields_delorean_objects(self):
        stops = list(
            delorean.stops(
                delorean.DAILY, count=2, timezone=EASTERN, start=datetime(2013, 1, 1)
            )
        )

        self.assertTrue(all(isinstance(do, delorean.Delorean) for do in stops))

    def test_stops_rejects_an_aware_start(self):
        with self.assertRaises(delorean.DeloreanInvalidDatetime):
            list(delorean.stops(delorean.DAILY, count=1, start=WINTER_UTC))


class Errors(unittest.TestCase):
    def test_unknown_zone_name_is_rejected(self):
        with self.assertRaises(Exception) as caught:
            delorean.Delorean(WINTER_NAIVE, timezone="Not/AZone")

        self.assertNotIsInstance(caught.exception, AttributeError)

    def test_naive_datetime_without_a_timezone_is_rejected(self):
        with self.assertRaises(delorean.DeloreanInvalidTimezone):
            delorean.Delorean(WINTER_NAIVE)

    def test_non_datetime_is_rejected(self):
        with self.assertRaises(ValueError):
            delorean.Delorean("not a datetime", timezone="UTC")

    def test_invalid_shift_name_raises_attribute_error(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone="UTC")

        with self.assertRaises(AttributeError):
            do.sideways_day()

    def test_invalid_shift_name_is_not_reported_by_hasattr(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone="UTC")

        self.assertFalse(hasattr(do, "next_bogus"))


class CurrentTime(unittest.TestCase):
    def test_utcnow_is_utc(self):
        self.assertEqual(delorean.utcnow().datetime.utcoffset(), timedelta(0))

    def test_now_uses_the_local_zone(self):
        with mock.patch(
            "delorean.interface.get_localzone", return_value=ZoneInfo(EASTERN)
        ):
            do = delorean.now()

        self.assertEqual(str(do.timezone), EASTERN)

    def test_now_accepts_an_explicit_zone(self):
        self.assertEqual(str(delorean.now(EASTERN).timezone), EASTERN)

    def test_classmethod_utcnow_is_utc(self):
        self.assertEqual(delorean.Delorean.utcnow().datetime.utcoffset(), timedelta(0))


class Presentation(unittest.TestCase):
    def test_repr_round_trips(self):
        namespace = {"Delorean": delorean.Delorean, "datetime": __import__("datetime")}
        try:  # pytz disappears with the migration; the test must not.
            namespace["pytz"] = __import__("pytz")
        except ImportError:
            pass
        namespace["zoneinfo"] = __import__("zoneinfo")

        for do in (
            delorean.Delorean(WINTER_NAIVE, timezone=EASTERN),
            delorean.Delorean(WINTER_NAIVE, timezone="UTC"),
            delorean.parse("2015-01-01 00:01:02 -0800"),
        ):
            with self.subTest(value=repr(do)):
                self.assertEqual(eval(repr(do), namespace), do)

    def test_repr_names_the_class(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=EASTERN)

        self.assertTrue(repr(do).startswith("Delorean("))

    def test_format_datetime_uses_the_local_reading(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=EASTERN)

        self.assertIn("12:00", do.format_datetime(locale="en_US"))

    def test_humanize_returns_a_string(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=EASTERN)

        self.assertIsInstance(do.humanize(), str)

    def test_truncate_clears_smaller_units(self):
        do = delorean.Delorean(datetime(2013, 1, 15, 12, 34, 56), timezone=EASTERN)

        self.assertEqual(
            do.truncate("hour").datetime.replace(tzinfo=None), datetime(2013, 1, 15, 12)
        )

    def test_replace_keeps_the_timezone(self):
        do = delorean.Delorean(WINTER_NAIVE, timezone=EASTERN)

        replaced = do.replace(hour=1)

        self.assertEqual(str(replaced.timezone), EASTERN)
        self.assertEqual(replaced.datetime.hour, 1)


if __name__ == "__main__":
    unittest.main()
