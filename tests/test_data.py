#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Testing for Delorean
"""

from unittest import TestCase, main
from datetime import tzinfo, datetime, date, timedelta
from copy import deepcopy

from pytz import timezone
import delorean


class GenericUTC(tzinfo):
    """GenericUTC"""
    ZERO = timedelta(0)

    def utcoffset(self, dt):
        return self.ZERO

    def tzname(self, dt):
        return "GenericUTC"

    def dst(self, dt):
        return self.ZERO

UTC = "UTC"
utc = timezone(UTC)
generic_utc = GenericUTC()
est = timezone("US/Eastern")


class DeloreanTests(TestCase):

    def setUp(self):
        self.naive_dt = datetime(2013, 1, 3, 4, 31, 14, 148546)
        self.do = delorean.Delorean(datetime=self.naive_dt, timezone="UTC")

    def test_initialize_from_datetime_naive(self):
        self.assertRaises(delorean.DeloreanInvalidTimezone, delorean.Delorean, datetime=self.naive_dt)

    def test_initialize_with_tzinfo_generic(self):
        self.aware_dt_generic = datetime(2013, 1, 3, 4, 31, 14, 148546, tzinfo=generic_utc)
        do = delorean.Delorean(datetime=self.aware_dt_generic)
        self.assertTrue(type(do) is delorean.Delorean)

    def test_initialize_with_tzinfo_pytz(self):
        self.aware_dt_pytz = datetime(2013, 1, 3, 4, 31, 14, 148546, tzinfo=utc)
        do = delorean.Delorean(datetime=self.aware_dt_pytz)
        self.assertTrue(type(do) is delorean.Delorean)

    def test_truncation_hour(self):
        self.do.truncate('hour')
        self.assertEqual(self.do.naive(), datetime(2013, 1, 3, 4, 0))

    def test_truncation_second(self):
        self.do.truncate('second')
        self.assertEqual(self.do.naive(), datetime(2013, 1, 3, 4, 31, 14, 0))

    def test_truncation_minute(self):
        self.do.truncate('minute')
        self.assertEqual(self.do.naive(), datetime(2013, 1, 3, 4, 31, 0, 0))

    def test_truncation_day(self):
        self.do.truncate('day')
        self.assertEqual(self.do.naive(), datetime(2013, 1, 3, 0, 0, 0, 0))

    def test_truncation_month(self):
        self.do.truncate('month')
        self.assertEqual(self.do.naive(), datetime(2013, 1, 1, 0, 0, 0, 0))

    def test_truncation_year(self):
        self.do.truncate('year')
        self.assertEqual(self.do.naive(), datetime(2013, 1, 1, 0, 0, 0, 0))

    def test_date(self):
        self.assertEqual(self.do.date, date(2013, 1, 3))

    def test_datetime(self):
        self.assertEqual(self.do.naive(), datetime(2013, 1, 3, 4, 31, 14, 148546))

    def test_naive(self):
        dt1 = delorean.Delorean()
        dt_naive = dt1.naive()
        self.assertEqual(dt_naive.tzinfo, None)

    def test_naive_timezone(self):
        dt1 = delorean.Delorean(timezone="US/Eastern").truncate('second').naive()
        dt2 = delorean.Delorean().truncate('second').naive()
        self.assertEqual(dt2, dt1)
        self.assertEqual(dt1.tzinfo, None)

    def test_localize(self):
        dt = datetime.today()
        utc = timezone("UTC")
        dt = delorean.localize(dt, "UTC")
        self.assertEqual(dt.tzinfo, utc)

    def test_failure_truncation(self):
        self.assertRaises(ValueError, self.do.truncate, "century")

    def test_normalize(self):
        dt1 = delorean.Delorean()
        dt2 = delorean.Delorean(timezone="US/Eastern")
        dt1.truncate('minute')
        dt2.truncate('minute')
        dt_normalized = delorean.normalize(dt1.datetime, "US/Eastern")
        self.assertEqual(dt2.datetime, dt_normalized)

    def test_normalize_failure(self):
        naive_datetime = datetime.today()
        self.assertRaises(ValueError, delorean.normalize, naive_datetime, "US/Eastern")

    def test_localize_failure(self):
        dt1 = delorean.localize(datetime.utcnow(), "UTC")
        self.assertRaises(ValueError, delorean.localize, dt1, "UTC")

    def test_timezone(self):
        utc = timezone('UTC')
        do_timezone = delorean.Delorean().timezone()
        self.assertEqual(utc, do_timezone)

    def test_datetime_timezone_default(self):
        do = delorean.Delorean()
        do.truncate('minute')
        dt1 = delorean.datetime_timezone(UTC)
        self.assertEqual(dt1.replace(second=0, microsecond=0), do.datetime)

    def test_datetime_timezone(self):
        do = delorean.Delorean(timezone="US/Eastern")
        do.truncate("minute")
        dt1 = delorean.datetime_timezone(tz="US/Eastern")
        self.assertEqual(dt1.replace(second=0, microsecond=0), do.datetime)

    def test_parse(self):
        do = delorean.parse('Thu Sep 25 10:36:28 BRST 2003')
        dt1 = utc.localize(datetime(2003, 9, 25, 10, 36, 28))
        self.assertEqual(do.datetime, dt1)

    def test_parse_with_utc_year_fill(self):
        do = delorean.parse('Thu Sep 25 10:36:28')
        dt1 = utc.localize(datetime(date.today().year, 9, 25, 10, 36, 28))
        self.assertEqual(do.datetime, dt1)

    def test_parse_with_timezone_year_fill(self):
        do = delorean.parse('Thu Sep 25 10:36:28')
        dt1 = utc.localize(datetime(date.today().year, 9, 25, 10, 36, 28))
        self.assertEqual(do.datetime, dt1)
        self.assertEqual(do._tz, "UTC")

    def test_move_namedday(self):
        dt_next = datetime(2013, 1, 4, 4, 31, 14, 148546, tzinfo=utc)
        dt_next_2 = datetime(2013, 1, 11, 4, 31, 14, 148546, tzinfo=utc)
        dt_last = datetime(2012, 12, 28, 4, 31, 14, 148546, tzinfo=utc)
        dt_last_2 = datetime(2012, 12, 21, 4, 31, 14, 148546, tzinfo=utc)

        d_obj_next = self.do.next_friday()
        d_obj_next_2 = self.do.next_friday(2)
        d_obj_last = self.do.last_friday()
        d_obj_last_2 = self.do.last_friday(2)

        self.assertEqual(dt_next, d_obj_next.datetime)
        self.assertEqual(dt_last, d_obj_last.datetime)
        self.assertEqual(dt_next_2, d_obj_next_2.datetime)
        self.assertEqual(dt_last_2, d_obj_last_2.datetime)

    def test_move_namedday_function(self):
        dt_next = datetime(2013, 1, 4, 4, 31, 14, 148546, tzinfo=utc)
        dt_last = datetime(2012, 12, 28, 4, 31, 14, 148546, tzinfo=utc)

        d_obj_next = delorean.move_datetime_namedday(self.do.datetime, 'next', 'friday')
        d_obj_last = delorean.move_datetime_namedday(self.do.datetime, 'last', 'friday')

        self.assertEqual(dt_next, d_obj_next)
        self.assertEqual(dt_last, d_obj_last)

    def test_move_week(self):
        dt_next = datetime(2013, 1, 10, 4, 31, 14, 148546, tzinfo=utc)
        dt_next_2 = datetime(2013, 1, 17, 4, 31, 14, 148546, tzinfo=utc)
        dt_last = datetime(2012, 12, 27, 4, 31, 14, 148546, tzinfo=utc)
        dt_last_2 = datetime(2012, 12, 20, 4, 31, 14, 148546, tzinfo=utc)

        d_obj_next = self.do.next_week()
        d_obj_next_2 = self.do.next_week(2)
        d_obj_last = self.do.last_week()
        d_obj_last_2 = self.do.last_week(2)

        self.assertEqual(dt_next, d_obj_next.datetime)
        self.assertEqual(dt_last, d_obj_last.datetime)
        self.assertEqual(dt_next_2, d_obj_next_2.datetime)
        self.assertEqual(dt_last_2, d_obj_last_2.datetime)

    def test_move_week_function(self):
        dt_next = datetime(2013, 1, 10, 4, 31, 14, 148546, tzinfo=utc)
        dt_last = datetime(2012, 12, 27, 4, 31, 14, 148546, tzinfo=utc)

        d_obj_next = delorean.move_datetime_week(self.do.datetime, 'next', 1)
        d_obj_last = delorean.move_datetime_week(self.do.datetime, 'last', 1)

        self.assertEqual(dt_next, d_obj_next)
        self.assertEqual(dt_last, d_obj_last)

    def test_move_month(self):
        dt_next = datetime(2013, 2, 3, 4, 31, 14, 148546, tzinfo=utc)
        dt_next_2 = datetime(2013, 3, 3, 4, 31, 14, 148546, tzinfo=utc)
        dt_last = datetime(2012, 12, 3, 4, 31, 14, 148546, tzinfo=utc)
        dt_last_2 = datetime(2012, 11, 3, 4, 31, 14, 148546, tzinfo=utc)

        d_obj_next = self.do.next_month()
        d_obj_next_2 = self.do.next_month(2)
        d_obj_last = self.do.last_month()
        d_obj_last_2 = self.do.last_month(2)

        self.assertEqual(dt_next, d_obj_next.datetime)
        self.assertEqual(dt_last, d_obj_last.datetime)
        self.assertEqual(dt_next_2, d_obj_next_2.datetime)
        self.assertEqual(dt_last_2, d_obj_last_2.datetime)

    def test_move_month_function(self):
        dt_next = datetime(2013, 2, 3, 4, 31, 14, 148546, tzinfo=utc)
        dt_last = datetime(2012, 12, 3, 4, 31, 14, 148546, tzinfo=utc)

        d_obj_next = delorean.move_datetime_month(self.do.datetime, 'next', 1)
        d_obj_last = delorean.move_datetime_month(self.do.datetime, 'last', 1)

        self.assertEqual(dt_next, d_obj_next)
        self.assertEqual(dt_last, d_obj_last)

    def test_move_day_function(self):
        dt_next = datetime(2013, 1, 4, 4, 31, 14, 148546, tzinfo=utc)
        dt_last = datetime(2013, 1, 2, 4, 31, 14, 148546, tzinfo=utc)

        d_obj_next = delorean.move_datetime_day(self.do.datetime, 'next', 1)
        d_obj_last = delorean.move_datetime_day(self.do.datetime, 'last', 1)

        self.assertEqual(dt_next, d_obj_next)
        self.assertEqual(dt_last, d_obj_last)

    def test_move_year(self):
        dt_next = datetime(2014, 1, 3, 4, 31, 14, 148546, tzinfo=utc)
        dt_next_2 = datetime(2015, 1, 3, 4, 31, 14, 148546, tzinfo=utc)
        dt_last = datetime(2012, 1, 3, 4, 31, 14, 148546, tzinfo=utc)
        dt_last_2 = datetime(2011, 1, 3, 4, 31, 14, 148546, tzinfo=utc)

        d_obj_next = self.do.next_year()
        d_obj_next_2 = self.do.next_year(2)
        d_obj_last = self.do.last_year()
        d_obj_last_2 = self.do.last_year(2)

        self.assertEqual(dt_next, d_obj_next.datetime)
        self.assertEqual(dt_last, d_obj_last.datetime)
        self.assertEqual(dt_next_2, d_obj_next_2.datetime)
        self.assertEqual(dt_last_2, d_obj_last_2.datetime)

    def test_move_year_function(self):
        dt_next = datetime(2014, 1, 3, 4, 31, 14, 148546, tzinfo=utc)
        dt_last = datetime(2012, 1, 3, 4, 31, 14, 148546, tzinfo=utc)

        d_obj_next = delorean.move_datetime_year(self.do.datetime, 'next', 1)
        d_obj_last = delorean.move_datetime_year(self.do.datetime, 'last', 1)

        self.assertEqual(dt_next, d_obj_next)
        self.assertEqual(dt_last, d_obj_last)

    def test_move_hour(self):
        dt_next   = datetime(2013, 1, 3, 5, 31, 14, 148546, tzinfo=utc)
        dt_next_2 = datetime(2013, 1, 3, 6, 31, 14, 148546, tzinfo=utc)
        dt_last = datetime(2013, 1, 3, 3, 31, 14, 148546, tzinfo=utc)
        dt_last_2 = datetime(2013, 1, 3, 2, 31, 14, 148546, tzinfo=utc)

        d_obj_next = self.do.next_hour()
        d_obj_next_2 = self.do.next_hour(2)
        d_obj_last = self.do.last_hour()
        d_obj_last_2 = self.do.last_hour(2)

        self.assertEqual(dt_next, d_obj_next.datetime)
        self.assertEqual(dt_last, d_obj_last.datetime)
        self.assertEqual(dt_next_2, d_obj_next_2.datetime)
        self.assertEqual(dt_last_2, d_obj_last_2.datetime)

    def test_move_hour_function(self):
        dt_next = datetime(2013, 1, 3, 5, 31, 14, 148546, tzinfo=utc)
        dt_last = datetime(2013, 1, 3, 3, 31, 14, 148546, tzinfo=utc)

        d_obj_next = delorean.move_datetime_hour(self.do.datetime, 'next', 1)
        d_obj_last = delorean.move_datetime_hour(self.do.datetime, 'last', 1)

        self.assertEqual(dt_next, d_obj_next)
        self.assertEqual(dt_last, d_obj_last)

    def test_move_minute(self):
        dt_next   = datetime(2013, 1, 3, 4, 32, 14, 148546, tzinfo=utc)
        dt_next_2 = datetime(2013, 1, 3, 4, 33, 14, 148546, tzinfo=utc)
        dt_last = datetime(2013, 1, 3, 4, 30, 14, 148546, tzinfo=utc)
        dt_last_2 = datetime(2013, 1, 3, 4, 29, 14, 148546, tzinfo=utc)

        d_obj_next = self.do.next_minute()
        d_obj_next_2 = self.do.next_minute(2)
        d_obj_last = self.do.last_minute()
        d_obj_last_2 = self.do.last_minute(2)

        self.assertEqual(dt_next, d_obj_next.datetime)
        self.assertEqual(dt_last, d_obj_last.datetime)
        self.assertEqual(dt_next_2, d_obj_next_2.datetime)
        self.assertEqual(dt_last_2, d_obj_last_2.datetime)

    def test_move_minute_function(self):
        dt_next = datetime(2013, 1, 3, 4, 32, 14, 148546, tzinfo=utc)
        dt_last = datetime(2013, 1, 3, 4, 30, 14, 148546, tzinfo=utc)

        d_obj_next = delorean.move_datetime_minute(self.do.datetime, 'next', 1)
        d_obj_last = delorean.move_datetime_minute(self.do.datetime, 'last', 1)

        self.assertEqual(dt_next, d_obj_next)
        self.assertEqual(dt_last, d_obj_last)

    def test_move_minute(self):
        dt_next   = datetime(2013, 1, 3, 4, 31, 15, 148546, tzinfo=utc)
        dt_next_2 = datetime(2013, 1, 3, 4, 31, 16, 148546, tzinfo=utc)
        dt_last = datetime(2013, 1, 3, 4, 31, 13, 148546, tzinfo=utc)
        dt_last_2 = datetime(2013, 1, 3, 4, 31, 12, 148546, tzinfo=utc)

        d_obj_next = self.do.next_second()
        d_obj_next_2 = self.do.next_second(2)
        d_obj_last = self.do.last_second()
        d_obj_last_2 = self.do.last_second(2)

        self.assertEqual(dt_next, d_obj_next.datetime)
        self.assertEqual(dt_last, d_obj_last.datetime)
        self.assertEqual(dt_next_2, d_obj_next_2.datetime)
        self.assertEqual(dt_last_2, d_obj_last_2.datetime)

    def test_move_second_function(self):
        dt_next = datetime(2013, 1, 3, 4, 31, 15, 148546, tzinfo=utc)
        dt_last = datetime(2013, 1, 3, 4, 31, 13, 148546, tzinfo=utc)

        d_obj_next = delorean.move_datetime_second(self.do.datetime, 'next', 1)
        d_obj_last = delorean.move_datetime_second(self.do.datetime, 'last', 1)

        self.assertEqual(dt_next, d_obj_next)
        self.assertEqual(dt_last, d_obj_last)

    def test_range_count(self):
        """
        tests the range method with count used
        """
        count = list(delorean.stops(delorean.DAILY, count=5))
        self.assertEqual(len(count), 5)

    def test_range_with_start(self):
        dates1 = []
        for do in delorean.stops(delorean.DAILY, count=5, start=datetime.utcnow()):
            do.truncate('minute')
            dates1.append(do)
        do = delorean.Delorean().truncate('minute')
        dates2 = []
        for x in range(5):
            dates2.append(do.next_day(x))
        self.assertEqual(dates1, dates2)

    def test_range_with_start_and_stop(self):
        dates1 = []
        tomorrow = datetime.utcnow() + timedelta(days=1)
        for do in delorean.stops(delorean.DAILY, start=datetime.utcnow(), stop=tomorrow):
            do.truncate('minute')
            dates1.append(do)
        do = delorean.Delorean().truncate('minute')
        dates2 = []
        for x in range(2):
            dates2.append(do.next_day(x))
        self.assertEqual(dates1, dates2)

    def test_range_with_interval(self):
        dates1 = []
        for do in delorean.stops(delorean.DAILY, interval=2, count=3, start=datetime.utcnow()):
            do.truncate('minute')
            dates1.append(do)
        do = delorean.Delorean().truncate('minute')
        dates2 = []
        for x in range(6):
            if (x % 2) == 0:
                dates2.append(do.next_day(x))
        self.assertEqual(dates1, dates2)

    def test_delorean_with_datetime(self):
        dt = datetime.utcnow()
        d = delorean.Delorean(datetime=dt, timezone=UTC)
        dt = utc.localize(dt)
        self.assertEqual(dt, d._dt)
        self.assertEqual(UTC, d._tz)

    def test_delorean_with_timezone(self):
        dt = datetime.utcnow()
        d = delorean.Delorean(datetime=dt, timezone=UTC)
        d = d.shift("US/Eastern")
        dt = utc.localize(dt)
        dt = est.normalize(dt)
        self.assertEqual(dt, d._dt)
        self.assertEqual(est, timezone(d._tz))

    def test_delorean_with_only_timezone(self):
        dt = datetime.utcnow()
        dt = utc.localize(dt)
        dt = est.normalize(dt)
        dt = dt.replace(second=0, microsecond=0)
        d = delorean.Delorean(timezone="US/Eastern")
        d.truncate('minute')
        self.assertEqual(est, timezone(d._tz))
        self.assertEqual(dt, d._dt)

    def testparse_with_timezone(self):
        d1 = delorean.parse("2011/01/01 00:00:00 -0700")
        d2 = datetime(2011, 1, 1, 7, 0)
        d2 = utc.localize(d2)
        self.assertEqual(d2, d1.datetime)
        self.assertEqual(utc, timezone(d1._tz))

    def test_shift_failure(self):
        self.assertRaises(delorean.DeloreanInvalidTimezone, self.do.shift, "US/Westerrn")

    def test_datetime_localization(self):
        dt1 = self.do.datetime
        dt2 = delorean.Delorean(dt1).datetime
        self.assertEquals(dt1, dt2)

    def test_localize_datetime(self):
        dt = datetime.utcnow()
        tz = timezone("US/Pacific")
        dt = tz.localize(dt)
        d = delorean.Delorean(dt)
        d2 = d.shift('US/Pacific')

        self.assertEquals(d._tz, "US/Pacific")
        self.assertEquals(d.datetime, dt)
        self.assertEqual(d.datetime, d2.datetime)

    def test_lt(self):
        dt1 = self.do
        dt2 = delorean.Delorean()
        self.assertTrue(dt1 < dt2)

    def test_gt(self):
        dt1 = self.do
        dt2 = delorean.Delorean()
        self.assertTrue(dt2 > dt1)

    def test_ge(self):
        dt = datetime.utcnow()
        dt1 = delorean.Delorean(dt, timezone="UTC")
        dt2 = delorean.Delorean(dt, timezone="UTC")
        dt3 = self.do
        self.assertTrue(dt2 >= dt1)
        self.assertTrue(dt1 >= dt3)

    def test_le(self):
        dt = datetime.utcnow()
        dt1 = delorean.Delorean(dt, timezone="UTC")
        dt2 = delorean.Delorean(dt, timezone="UTC")
        dt3 = self.do
        self.assertTrue(dt2 <= dt1)
        self.assertTrue(dt3 <= dt2)

    def test_epoch(self):
        unix_time = self.do.epoch()
        self.assertEqual(unix_time, 1357187474.148546)

    def test_epoch_creation(self):
        do = delorean.epoch(1357187474.148546)
        self.assertEqual(self.do, do)

    def test_not_equal(self):
        d = delorean.Delorean()
        self.assertNotEqual(d, None)

    def test_equal(self):
        d1 = delorean.Delorean()
        d2 = deepcopy(d1)
        self.assertEqual(d1, d2)
        self.assertFalse(d1 != d2, 'Overloaded __ne__ is not correct')

    def test_timezone_delorean_to_datetime_to_delorean_utc(self):
        d1 = delorean.Delorean()
        d2 = delorean.Delorean(d1.datetime)

        #these deloreans should be the same
        self.assertEqual(d1.next_day(1), d2.next_day(1))
        self.assertEqual(d2.last_week(), d2.last_week())
        self.assertEqual(d1.timezone(), d2.timezone())
        self.assertEqual(d1, d2)

    def test_timezone_delorean_to_datetime_to_delorean_non_utc(self):
        """Test if when you create Delorean object from Delorean's datetime
        it still behaves the same
        """
        d1 = delorean.Delorean(timezone='America/Chicago')
        d2 = delorean.Delorean(d1.datetime)

        #these deloreans should be the same
        self.assertEqual(d1.next_day(1), d2.next_day(1))
        self.assertEqual(d2.last_week(), d2.last_week())
        self.assertEqual(d1.timezone(), d2.timezone())
        self.assertEqual(d1, d2)

if __name__ == '__main__':
    main()
