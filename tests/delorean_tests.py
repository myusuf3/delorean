#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Testing for Delorean
"""

import unittest

from copy import deepcopy
from datetime import date
from datetime import datetime
from datetime import timedelta
from datetime import tzinfo

import mock
import pytz

from dateutil.tz import tzlocal
from dateutil.tz import tzoffset

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
generic_utc = GenericUTC()
est = pytz.timezone("US/Eastern").localize(datetime.utcnow()).tzinfo


class DeloreanTests(unittest.TestCase):
    def setUp(self):
        self.naive_dt = datetime(2013, 1, 3, 4, 31, 14, 148540)
        self.do = delorean.Delorean(datetime=self.naive_dt, timezone="UTC")

    def test_date_failure(self):
        dt = date(2013, 5, 6)
        self.assertRaises(ValueError, delorean.Delorean, dt)

    def test_initialize_from_datetime_naive(self):
        self.assertRaises(delorean.DeloreanInvalidTimezone, delorean.Delorean, datetime=self.naive_dt)

    def test_initialize_with_tzinfo_generic(self):
        aware_dt_generic = datetime(2013, 1, 3, 4, 31, 14, 148540, tzinfo=generic_utc)
        do = delorean.Delorean(datetime=aware_dt_generic)
        self.assertTrue(isinstance(do, delorean.Delorean))

    def test_initialize_with_tzinfo_pytz(self):
        aware_dt_pytz = datetime(2013, 1, 3, 4, 31, 14, 148540, tzinfo=pytz.utc)
        do = delorean.Delorean(datetime=aware_dt_pytz)
        self.assertTrue(isinstance(do, delorean.Delorean))

    def test_initialize_with_invalid_datetime(self):
        self.assertRaises(ValueError, delorean.Delorean, '2015-01-01')

    def test_initialize_with_naive_datetime_with_pytz_timezone(self):
        dt = datetime(2015, 1, 1)
        do = delorean.Delorean(dt, timezone=pytz.utc)

        dt = pytz.utc.localize(dt)
        self.assertEqual(do.datetime, dt)
        self.assertEqual(do.timezone, pytz.utc)

    def test_initialize_with_naive_datetime_with_dateutil_timezone(self):
        dt = datetime(2015, 1, 1)
        tz = tzoffset(None, -22500)
        do = delorean.Delorean(dt, timezone=tz)

        utcoffset = tz.utcoffset(None)
        total_seconds = (
            (utcoffset.microseconds + (utcoffset.seconds + utcoffset.days * 24 * 3600) * 10 ** 6) / 10 ** 6)
        tz = pytz.FixedOffset(total_seconds / 60)
        dt = tz.localize(dt)
        self.assertEqual(do.datetime, dt)
        self.assertEqual(do.timezone, tz)

    def test_initialize_with_naive_datetime_with_string_timezone(self):
        dt = datetime(2015, 1, 1)
        tz_str = 'US/Pacific'
        tz = pytz.timezone(tz_str)
        do = delorean.Delorean(dt, timezone=tz_str)
        tz = tz.localize(datetime(2015, 1, 1)).tzinfo

        dt = tz.localize(dt)
        self.assertEqual(do.datetime, dt)
        self.assertEqual(do.timezone, tz)

    def test_initialize_with_naive_datetime_without_timezone(self):
        self.assertRaises(delorean.DeloreanInvalidTimezone, delorean.Delorean, datetime(2015, 1, 1))

    def test_initialize_with_datetime_with_timezone(self):
        dt = pytz.utc.localize(datetime(2015, 1, 1))
        do = delorean.Delorean(dt, timezone=pytz.timezone('US/Pacific'))

        self.assertEqual(do.datetime, dt)
        self.assertEqual(do.timezone, pytz.utc)

    def test_initialize_with_datetime_without_timezone(self):
        dt = pytz.utc.localize(datetime(2015, 1, 1))
        do = delorean.Delorean(dt)

        self.assertEqual(do.datetime, dt)
        self.assertEqual(do.timezone, pytz.utc)

    @mock.patch('delorean.dates.datetime_timezone')
    def test_initialize_without_datetime_with_pytz_timezone(self, mock_datetime_timezone):
        tz = pytz.timezone('US/Pacific')
        dt = tz.localize(datetime(2015, 1, 1))
        tz = dt.tzinfo
        mock_datetime_timezone.return_value = dt

        do = delorean.Delorean(timezone=tz)
        self.assertEqual(do.datetime, dt)
        self.assertEqual(do.timezone, tz)

    @mock.patch('delorean.dates.datetime_timezone')
    def test_initialize_without_datetime_with_dateutil_timezone(self, mock_datetime_timezone):
        tz = tzoffset(None, -22500)
        dt = datetime(2015, 1, 1, tzinfo=tz)

        utcoffset = tz.utcoffset(None)
        total_seconds = (
            (utcoffset.microseconds + (utcoffset.seconds + utcoffset.days * 24 * 3600) * 10 ** 6) / 10 ** 6)

        tz = pytz.FixedOffset(total_seconds / 60)
        dt = tz.normalize(dt)
        mock_datetime_timezone.return_value = dt

        do = delorean.Delorean(timezone=tz)
        self.assertEqual(do.datetime, dt)
        self.assertEqual(do.timezone, tz)

    @mock.patch('delorean.dates.datetime_timezone')
    def test_initialize_without_datetime_with_string_timezone(self, mock_datetime_timezone):
        tz_str = 'US/Pacific'
        tz = pytz.timezone(tz_str)
        dt = tz.localize(datetime(2015, 1, 1))
        tz = dt.tzinfo
        mock_datetime_timezone.return_value = dt

        do = delorean.Delorean(timezone=tz_str)
        self.assertEqual(do.datetime, dt)
        self.assertEqual(do.timezone, tz)

    @mock.patch('delorean.dates.datetime_timezone')
    def test_initialize_without_datetime_without_timezone(self, mock_datetime_timezone):
        dt = pytz.utc.localize(datetime(2015, 1, 1))
        mock_datetime_timezone.return_value = dt

        do = delorean.Delorean()
        self.assertEqual(do.datetime, dt)
        self.assertEqual(do.timezone, pytz.utc)

    def test_truncation_hour(self):
        self.do.truncate('hour')
        self.assertEqual(self.do.naive, datetime(2013, 1, 3, 4, 0))

    def test_midnight(self):
        dt = self.do.midnight
        self.assertEqual(dt, datetime(2013, 1, 3, 0, 0, 0, tzinfo=pytz.utc))

    def test_start_of_day(self):
        dt = self.do.start_of_day
        self.assertEqual(dt, datetime(2013, 1, 3, 0, 0, 0, 0, tzinfo=pytz.utc))

    def test_end_of_day(self):
        dt = self.do.end_of_day
        self.assertEqual(dt, datetime(2013, 1, 3, 23, 59, 59, 999999, tzinfo=pytz.utc))

    def test_truncation_second(self):
        self.do.truncate('second')
        self.assertEqual(self.do.naive, datetime(2013, 1, 3, 4, 31, 14, 0))

    def test_truncation_minute(self):
        self.do.truncate('minute')
        self.assertEqual(self.do.naive, datetime(2013, 1, 3, 4, 31, 0, 0))

    def test_truncation_day(self):
        self.do.truncate('day')
        self.assertEqual(self.do.naive, datetime(2013, 1, 3, 0, 0, 0, 0))

    def test_truncation_month(self):
        self.do.truncate('month')
        self.assertEqual(self.do.naive, datetime(2013, 1, 1, 0, 0, 0, 0))

    def test_truncation_year(self):
        self.do.truncate('year')
        self.assertEqual(self.do.naive, datetime(2013, 1, 1, 0, 0, 0, 0))

    def test_date(self):
        self.assertEqual(self.do.date, date(2013, 1, 3))

    def test_datetime(self):
        self.assertEqual(self.do.naive, datetime(2013, 1, 3, 4, 31, 14, 148540))

    def test_naive(self):
        dt1 = delorean.Delorean()
        dt_naive = dt1.naive
        self.assertEqual(dt_naive.tzinfo, None)

    def test_naive_timezone(self):
        dt1 = delorean.Delorean(timezone="US/Eastern").truncate('minute').naive
        dt2 = delorean.Delorean().truncate('minute').naive
        self.assertEqual(dt2, dt1)
        self.assertEqual(dt1.tzinfo, None)

    def test_localize(self):
        dt = datetime.today()
        dt = delorean.localize(dt, "UTC")
        self.assertEqual(dt.tzinfo, pytz.utc)

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
        do_timezone = delorean.Delorean().timezone
        self.assertEqual(pytz.utc, do_timezone)

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
        dt1 = pytz.utc.localize(datetime(2003, 9, 25, 10, 36, 28))
        self.assertEqual(do.datetime, dt1)

    def test_parse_default(self):
        do = delorean.parse('2016-07-01T11:00:00+02:00', dayfirst=False)
        dt1 = delorean.Delorean(datetime=datetime(2016, 7, 1, 11, 0), timezone=pytz.FixedOffset(120))
        self.assertEqual(do.datetime, dt1.datetime)

    def test_parse_with_invalid_datetime_string(self):
        self.assertRaises(ValueError, delorean.parse, 'asd')

    def test_parse_with_utc_year_fill(self):
        do = delorean.parse('Thu Sep 25 10:36:28')
        dt1 = pytz.utc.localize(datetime(date.today().year, 9, 25, 10, 36, 28))
        self.assertEqual(do.datetime, dt1)

    def test_parse_with_timezone_year_fill(self):
        do = delorean.parse('Thu Sep 25 10:36:28')
        dt1 = pytz.utc.localize(datetime(date.today().year, 9, 25, 10, 36, 28))
        self.assertEqual(do.datetime, dt1)
        self.assertEqual(do.timezone.tzname(None), "UTC")

    def test_parse_with_fixed_offset_timezone(self):
        tz = pytz.FixedOffset(-480)
        dt = tz.localize(datetime(2015, 1, 1))
        dt_str = dt.strftime('%Y-%m-%d %H:%M:%S %z')

        do = delorean.parse(dt_str)
        self.assertEqual(do.datetime, dt)
        self.assertEqual(do.timezone, tz)

    @mock.patch('delorean.interface.get_localzone')
    def test_parse_with_tzlocal_timezone(self, mock_get_local_zone):
        tz = pytz.timezone('US/Eastern')
        mock_get_local_zone.return_value = tz
        dt = datetime(2015, 1, 1, tzinfo=tzlocal())
        dt_str = dt.strftime('%Y-%m-%d %H:%M:%S %Z')
        dt = dt.replace(tzinfo=None)
        dt = tz.localize(dt)
        tz = dt.tzinfo

        do = delorean.parse(dt_str)
        self.assertEqual(do.datetime, dt)
        self.assertEqual(do.timezone, tz)

    @mock.patch('delorean.interface.get_localzone')
    def test_parse_with_tzutc_timezone(self, mock_get_localzone):
        mock_get_localzone.return_value = pytz.utc
        dt = pytz.utc.localize(datetime(2015, 1, 1))
        dt_str = dt.strftime('%Y-%m-%d %H:%M:%S %Z')

        do = delorean.parse(dt_str)
        self.assertEqual(do.datetime, dt)
        self.assertEqual(do.timezone, pytz.utc)

    def test_parse_with_timezone_parameter(self):
        tz = pytz.timezone('US/Pacific')
        dt = tz.localize(datetime(2015, 1, 1))
        tz = dt.tzinfo
        dt_str = dt.strftime('%Y-%m-%d %H:%M:%S')

        do = delorean.parse(dt_str, timezone='US/Pacific')
        self.assertEqual(do.datetime, dt)
        self.assertEqual(do.timezone, tz)

    def test_parse_with_overriding_timezone_parameter(self):
        tz = pytz.timezone('US/Pacific')
        dt = tz.localize(datetime(2015, 1, 1))
        tz = dt.tzinfo
        dt_str = dt.strftime('%Y-%m-%d %H:%M:%S -0500')

        do = delorean.parse(dt_str, timezone='US/Pacific')
        self.assertEqual(do.datetime, dt)
        self.assertEqual(do.timezone, tz)

    def test_move_namedday(self):
        dt_next = datetime(2013, 1, 4, 4, 31, 14, 148540, tzinfo=pytz.utc)
        dt_next_2 = datetime(2013, 1, 11, 4, 31, 14, 148540, tzinfo=pytz.utc)
        dt_last = datetime(2012, 12, 28, 4, 31, 14, 148540, tzinfo=pytz.utc)
        dt_last_2 = datetime(2012, 12, 21, 4, 31, 14, 148540, tzinfo=pytz.utc)

        d_obj_next = self.do.next_friday()
        d_obj_next_2 = self.do.next_friday(2)
        d_obj_last = self.do.last_friday()
        d_obj_last_2 = self.do.last_friday(2)

        self.assertEqual(dt_next, d_obj_next.datetime)
        self.assertEqual(dt_last, d_obj_last.datetime)
        self.assertEqual(dt_next_2, d_obj_next_2.datetime)
        self.assertEqual(dt_last_2, d_obj_last_2.datetime)

    def test_move_namedday_function(self):
        dt_next = datetime(2013, 1, 4, 4, 31, 14, 148540, tzinfo=pytz.utc)
        dt_last = datetime(2012, 12, 28, 4, 31, 14, 148540, tzinfo=pytz.utc)

        d_obj_next = delorean.move_datetime_namedday(self.do.datetime, 'next', 'friday')
        d_obj_last = delorean.move_datetime_namedday(self.do.datetime, 'last', 'friday')

        self.assertEqual(dt_next, d_obj_next)
        self.assertEqual(dt_last, d_obj_last)

    def test_move_week(self):
        dt_next = datetime(2013, 1, 10, 4, 31, 14, 148540, tzinfo=pytz.utc)
        dt_next_2 = datetime(2013, 1, 17, 4, 31, 14, 148540, tzinfo=pytz.utc)
        dt_last = datetime(2012, 12, 27, 4, 31, 14, 148540, tzinfo=pytz.utc)
        dt_last_2 = datetime(2012, 12, 20, 4, 31, 14, 148540, tzinfo=pytz.utc)

        d_obj_next = self.do.next_week()
        d_obj_next_2 = self.do.next_week(2)
        d_obj_last = self.do.last_week()
        d_obj_last_2 = self.do.last_week(2)

        self.assertEqual(dt_next, d_obj_next.datetime)
        self.assertEqual(dt_last, d_obj_last.datetime)
        self.assertEqual(dt_next_2, d_obj_next_2.datetime)
        self.assertEqual(dt_last_2, d_obj_last_2.datetime)

    def test_move_week_function(self):
        dt_next = datetime(2013, 1, 10, 4, 31, 14, 148540, tzinfo=pytz.utc)
        dt_last = datetime(2012, 12, 27, 4, 31, 14, 148540, tzinfo=pytz.utc)

        d_obj_next = delorean.move_datetime_week(self.do.datetime, 'next', 1)
        d_obj_last = delorean.move_datetime_week(self.do.datetime, 'last', 1)

        self.assertEqual(dt_next, d_obj_next)
        self.assertEqual(dt_last, d_obj_last)

    def test_move_month(self):
        dt_next = datetime(2013, 2, 3, 4, 31, 14, 148540, tzinfo=pytz.utc)
        dt_next_2 = datetime(2013, 3, 3, 4, 31, 14, 148540, tzinfo=pytz.utc)
        dt_last = datetime(2012, 12, 3, 4, 31, 14, 148540, tzinfo=pytz.utc)
        dt_last_2 = datetime(2012, 11, 3, 4, 31, 14, 148540, tzinfo=pytz.utc)

        d_obj_next = self.do.next_month()
        d_obj_next_2 = self.do.next_month(2)
        d_obj_last = self.do.last_month()
        d_obj_last_2 = self.do.last_month(2)

        self.assertEqual(dt_next, d_obj_next.datetime)
        self.assertEqual(dt_last, d_obj_last.datetime)
        self.assertEqual(dt_next_2, d_obj_next_2.datetime)
        self.assertEqual(dt_last_2, d_obj_last_2.datetime)

    def test_move_month_function(self):
        dt_next = datetime(2013, 2, 3, 4, 31, 14, 148540, tzinfo=pytz.utc)
        dt_last = datetime(2012, 12, 3, 4, 31, 14, 148540, tzinfo=pytz.utc)

        d_obj_next = delorean.move_datetime_month(self.do.datetime, 'next', 1)
        d_obj_last = delorean.move_datetime_month(self.do.datetime, 'last', 1)

        self.assertEqual(dt_next, d_obj_next)
        self.assertEqual(dt_last, d_obj_last)

    def test_move_day_function(self):
        dt_next = datetime(2013, 1, 4, 4, 31, 14, 148540, tzinfo=pytz.utc)
        dt_last = datetime(2013, 1, 2, 4, 31, 14, 148540, tzinfo=pytz.utc)

        d_obj_next = delorean.move_datetime_day(self.do.datetime, 'next', 1)
        d_obj_last = delorean.move_datetime_day(self.do.datetime, 'last', 1)

        self.assertEqual(dt_next, d_obj_next)
        self.assertEqual(dt_last, d_obj_last)

    def test_move_year(self):
        dt_next = datetime(2014, 1, 3, 4, 31, 14, 148540, tzinfo=pytz.utc)
        dt_next_2 = datetime(2015, 1, 3, 4, 31, 14, 148540, tzinfo=pytz.utc)
        dt_last = datetime(2012, 1, 3, 4, 31, 14, 148540, tzinfo=pytz.utc)
        dt_last_2 = datetime(2011, 1, 3, 4, 31, 14, 148540, tzinfo=pytz.utc)

        d_obj_next = self.do.next_year()
        d_obj_next_2 = self.do.next_year(2)
        d_obj_last = self.do.last_year()
        d_obj_last_2 = self.do.last_year(2)

        self.assertEqual(dt_next, d_obj_next.datetime)
        self.assertEqual(dt_last, d_obj_last.datetime)
        self.assertEqual(dt_next_2, d_obj_next_2.datetime)
        self.assertEqual(dt_last_2, d_obj_last_2.datetime)

    def test_move_year_function(self):
        dt_next = datetime(2014, 1, 3, 4, 31, 14, 148540, tzinfo=pytz.utc)
        dt_last = datetime(2012, 1, 3, 4, 31, 14, 148540, tzinfo=pytz.utc)

        d_obj_next = delorean.move_datetime_year(self.do.datetime, 'next', 1)
        d_obj_last = delorean.move_datetime_year(self.do.datetime, 'last', 1)

        self.assertEqual(dt_next, d_obj_next)
        self.assertEqual(dt_last, d_obj_last)

    def test_move_hour(self):
        dt_next = datetime(2013, 1, 3, 5, 31, 14, 148540, tzinfo=pytz.utc)
        dt_next_2 = datetime(2013, 1, 3, 6, 31, 14, 148540, tzinfo=pytz.utc)
        dt_last = datetime(2013, 1, 3, 3, 31, 14, 148540, tzinfo=pytz.utc)
        dt_last_2 = datetime(2013, 1, 3, 2, 31, 14, 148540, tzinfo=pytz.utc)

        d_obj_next = self.do.next_hour()
        d_obj_next_2 = self.do.next_hour(2)
        d_obj_last = self.do.last_hour()
        d_obj_last_2 = self.do.last_hour(2)

        self.assertEqual(dt_next, d_obj_next.datetime)
        self.assertEqual(dt_last, d_obj_last.datetime)
        self.assertEqual(dt_next_2, d_obj_next_2.datetime)
        self.assertEqual(dt_last_2, d_obj_last_2.datetime)

    def test_move_hour_function(self):
        dt_next = datetime(2013, 1, 3, 5, 31, 14, 148540, tzinfo=pytz.utc)
        dt_last = datetime(2013, 1, 3, 3, 31, 14, 148540, tzinfo=pytz.utc)

        d_obj_next = delorean.move_datetime_hour(self.do.datetime, 'next', 1)
        d_obj_last = delorean.move_datetime_hour(self.do.datetime, 'last', 1)

        self.assertEqual(dt_next, d_obj_next)
        self.assertEqual(dt_last, d_obj_last)

    def test_move_minute(self):
        dt_next = datetime(2013, 1, 3, 4, 32, 14, 148540, tzinfo=pytz.utc)
        dt_next_2 = datetime(2013, 1, 3, 4, 33, 14, 148540, tzinfo=pytz.utc)
        dt_last = datetime(2013, 1, 3, 4, 30, 14, 148540, tzinfo=pytz.utc)
        dt_last_2 = datetime(2013, 1, 3, 4, 29, 14, 148540, tzinfo=pytz.utc)

        d_obj_next = self.do.next_minute()
        d_obj_next_2 = self.do.next_minute(2)
        d_obj_last = self.do.last_minute()
        d_obj_last_2 = self.do.last_minute(2)

        self.assertEqual(dt_next, d_obj_next.datetime)
        self.assertEqual(dt_last, d_obj_last.datetime)
        self.assertEqual(dt_next_2, d_obj_next_2.datetime)
        self.assertEqual(dt_last_2, d_obj_last_2.datetime)

    def test_move_minute_function(self):
        dt_next = datetime(2013, 1, 3, 4, 32, 14, 148540, tzinfo=pytz.utc)
        dt_last = datetime(2013, 1, 3, 4, 30, 14, 148540, tzinfo=pytz.utc)

        d_obj_next = delorean.move_datetime_minute(self.do.datetime, 'next', 1)
        d_obj_last = delorean.move_datetime_minute(self.do.datetime, 'last', 1)

        self.assertEqual(dt_next, d_obj_next)
        self.assertEqual(dt_last, d_obj_last)

    def test_move_shift_minute(self):
        dt_next = datetime(2013, 1, 3, 4, 31, 15, 148540, tzinfo=pytz.utc)
        dt_next_2 = datetime(2013, 1, 3, 4, 31, 16, 148540, tzinfo=pytz.utc)
        dt_last = datetime(2013, 1, 3, 4, 31, 13, 148540, tzinfo=pytz.utc)
        dt_last_2 = datetime(2013, 1, 3, 4, 31, 12, 148540, tzinfo=pytz.utc)

        d_obj_next = self.do.next_second()
        d_obj_next_2 = self.do.next_second(2)
        d_obj_last = self.do.last_second()
        d_obj_last_2 = self.do.last_second(2)

        self.assertEqual(dt_next, d_obj_next.datetime)
        self.assertEqual(dt_last, d_obj_last.datetime)
        self.assertEqual(dt_next_2, d_obj_next_2.datetime)
        self.assertEqual(dt_last_2, d_obj_last_2.datetime)

    def test_move_second_function(self):
        dt_next = datetime(2013, 1, 3, 4, 31, 15, 148540, tzinfo=pytz.utc)
        dt_last = datetime(2013, 1, 3, 4, 31, 13, 148540, tzinfo=pytz.utc)

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
        dt = pytz.utc.localize(dt)
        self.assertEqual(dt, d._dt)
        self.assertEqual(pytz.utc, d.timezone)

    def test_delorean_with_timezone(self):
        dt = datetime.utcnow()
        d = delorean.Delorean(datetime=dt, timezone=UTC)
        d = d.shift("US/Eastern")
        dt = pytz.utc.localize(dt).astimezone(est)
        dt = est.normalize(dt)
        self.assertEqual(dt, d.datetime)
        self.assertEqual(est, d.timezone)

    def test_delorean_with_only_timezone(self):
        dt = datetime.utcnow()
        dt = pytz.utc.localize(dt)
        dt = est.normalize(dt)
        dt = dt.replace(second=0, microsecond=0)
        d = delorean.Delorean(timezone="US/Eastern")
        d.truncate('minute')
        self.assertEqual(est, d.timezone)
        self.assertEqual(dt, d._dt)

    def test_shift_failure(self):
        self.assertRaises(delorean.DeloreanInvalidTimezone, self.do.shift, "US/Westerrn")

    def test_datetime_localization(self):
        dt1 = self.do.datetime
        dt2 = delorean.Delorean(dt1).datetime
        self.assertEqual(dt1, dt2)

    def test_localize_datetime(self):
        dt = datetime.utcnow()
        tz = pytz.timezone("US/Pacific")
        dt = tz.localize(dt)
        d = delorean.Delorean(dt)
        d2 = d.shift('US/Pacific')

        self.assertEqual(d.timezone.tzname(None), "US/Pacific")
        self.assertEqual(d.datetime, dt)
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
        unix_time = self.do.epoch
        self.assertEqual(unix_time, 1357187474.148540)

    def test_epoch_creation(self):
        do = delorean.epoch(1357187474.148540)
        self.assertEqual(self.do, do)

    def test_not_equal(self):
        d = delorean.Delorean()
        self.assertNotEqual(d, None)

    def test_equal(self):
        d1 = delorean.Delorean()
        d2 = deepcopy(d1)
        self.assertEqual(d1, d2)
        self.assertFalse(d1 != d2, 'Overloaded __ne__ is not correct')

        d1 = delorean.Delorean(datetime(2015, 1, 1), timezone='US/Pacific')
        d2 = delorean.Delorean(datetime(2015, 1, 1, 8), timezone='UTC')
        self.assertEqual(d1, d2)

    def test_repr_string_timezone(self):
        import datetime
        from delorean import Delorean

        d1 = Delorean(datetime.datetime(2015, 1, 1), timezone='US/Pacific')
        d2 = eval(repr(d1))

        self.assertEqual(d1, d2)

        d3 = Delorean(d1.datetime, timezone='UTC')
        d4 = eval(repr(d3))

        self.assertEqual(d1, d4)

    def test_repr_pytz_timezone(self):
        import datetime
        from delorean import Delorean
        d1 = Delorean(datetime.datetime(2015, 1, 1), timezone='US/Pacific')
        d2 = eval(repr(d1))

        self.assertEqual(d1, d2)
        self.assertEqual(d1.datetime, d2.datetime)
        self.assertEqual(d1.timezone, d2.timezone)

    def test_repr_fixed_offset_timezone(self):
        import datetime
        from delorean import Delorean

        tz = pytz.timezone('US/Pacific')
        dt = tz.localize(datetime.datetime(2015, 1, 1))
        dt_str = dt.strftime('%Y-%m-%d %H:%M:%S %z')

        d1 = delorean.parse(dt_str)
        d2 = eval(repr(d1))

        self.assertEqual(d1, d2)
        self.assertEqual(d1.datetime, d2.datetime)
        self.assertEqual(d1.timezone, d2.timezone)

    def test_timezone_delorean_to_datetime_to_delorean_utc(self):
        d1 = delorean.Delorean()
        d2 = delorean.Delorean(d1.datetime)

        # these deloreans should be the same
        self.assertEqual(d1.next_day(1), d2.next_day(1))
        self.assertEqual(d2.last_week(), d2.last_week())
        self.assertEqual(d1.timezone, d2.timezone)
        self.assertEqual(d1, d2)

    def test_timezone_delorean_to_datetime_to_delorean_non_utc(self):
        """Test if when you create Delorean object from Delorean's datetime
        it still behaves the same
        """
        d1 = delorean.Delorean(timezone='America/Chicago')
        d2 = delorean.Delorean(d1.datetime)

        # these deloreans should be the same
        self.assertEqual(d1.next_day(1), d2.next_day(1))
        self.assertEqual(d2.last_week(), d2.last_week())
        self.assertEqual(d1.timezone, d2.timezone)
        self.assertEqual(d1, d2)

    def test_stops_bymonth(self):
        """Test if create stops, checks bymonth, bymonthday, count
        and start parameters work properly
        """
        days = list(delorean.interface.stops(
            delorean.MONTHLY,
            bymonth=(1, 4, 7, 10),
            bymonthday=15,
            count=4,
            start=datetime(datetime.now().year, 1, 1))
        )
        year = datetime.now().year
        day = 15
        dt1 = datetime(year, 1, day)
        dt4 = datetime(year, 4, day)
        dt7 = datetime(year, 7, day)
        dt10 = datetime(year, 10, day)

        self.assertTrue(len(days) == 4)
        dl1 = delorean.Delorean(datetime=dt1, timezone='UTC')
        self.assertEqual(days[0], dl1)

        dl4 = delorean.Delorean(datetime=dt4, timezone='UTC')
        self.assertEqual(days[1], dl4)

        dl7 = delorean.Delorean(datetime=dt7, timezone='UTC')
        self.assertEqual(days[2], dl7)

        dl10 = delorean.Delorean(datetime=dt10, timezone='UTC')
        self.assertEqual(days[3], dl10)

    def test_timedelta_arithmetic(self):
        hour = timedelta(hours=1)
        d = delorean.parse("2014/06/02 10:00:00 -0700")
        hour_before = delorean.parse("2014/06/02 09:00:00 -0700")
        hour_after = delorean.parse("2014/06/02 11:00:00 -0700")
        self.assertEqual(d + hour, hour_after)
        self.assertEqual(d - hour, hour_before)
        self.assertEqual(hour_after - d, hour)

    @mock.patch('delorean.Delorean.now')
    def test_humanize_past(self, mock_now):
        mock_now.return_value = delorean.Delorean(datetime(2015, 1, 2), timezone='US/Pacific')

        do = delorean.Delorean(datetime(2015, 1, 1), timezone='US/Pacific')
        self.assertEqual(do.humanize(), 'a day ago')

    @mock.patch('delorean.Delorean.now')
    def test_humanize_future(self, mock_now):
        mock_now.return_value = delorean.Delorean(datetime(2014, 12, 31), timezone='US/Pacific')

        do = delorean.Delorean(datetime(2015, 1, 1), timezone='US/Pacific')
        self.assertEqual(do.humanize(), 'a day from now')

    def test_replace(self):
        do = delorean.Delorean(datetime(2015, 1, 1), timezone='US/Pacific')
        dt = do.datetime

        # Check if parts are okay
        self.assertEqual(do.replace(hour=8).datetime.hour, 8)
        self.assertEqual(do.replace(minute=23).datetime.minute, 23)
        self.assertEqual(do.replace(second=45).datetime.second, 45)

        # Asserts on datetimes
        self.assertEqual(do.replace(hour=8).datetime, dt.replace(hour=8))
        self.assertEqual(do.replace(minute=38).datetime, dt.replace(minute=38))
        self.assertEqual(do.replace(second=48).datetime, dt.replace(second=48))

        # Test that the timezone does not change
        self.assertEqual(do.replace(second=45).timezone, do.timezone)

        # Test the datetime
        eight_hours_late = dt + timedelta(hours=8)
        self.assertEqual(do.replace(hour=8).datetime, eight_hours_late)


if __name__ == '__main__':
    unittest.main()
