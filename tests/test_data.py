#!/usr/bin/env python

"""
Test for testing the data model for delorean.
"""
from unittest import TestCase, main
from datetime import datetime, date

from pytz import timezone
from delorean import Delorean, datetime_timezone, localize, normalize, capture
from delorean.data import (move_datetime_day, move_datetime_week,
                           move_datetime_month, move_datetime_year,
                           move_datetime_namedday)

utc = timezone("UTC")


class DeloreanTests(TestCase):

    def setUp(self):
        date1 = datetime(2013, 1, 3, 4, 31, 14, 148546)
        self.do = Delorean(datetime=date1, timezone="UTC")

    def test_truncation_hour(self):
        """
        Tests that truncate always works
        """
        self.do.truncate('hour')
        self.assertEqual(self.do.naive(), datetime(2013, 1, 3, 4, 0))

    def test_truncation_second(self):
        """
        Tests that truncate always works
        """
        self.do.truncate('second')
        self.assertEqual(self.do.naive(), datetime(2013, 1, 3, 4, 31, 14, 0))

    def test_truncation_minute(self):
        """
        Tests that truncate always works
        """
        self.do.truncate('minute')
        self.assertEqual(self.do.naive(), datetime(2013, 1, 3, 4, 31, 0, 0))

    def test_truncation_day(self):
        """
        Tests that truncate always works
        """
        self.do.truncate('day')
        self.assertEqual(self.do.naive(), datetime(2013, 1, 3, 0, 0, 0, 0))

    def test_truncation_month(self):
        """
        Tests that truncate always works
        """
        self.do.truncate('month')
        self.assertEqual(self.do.naive(), datetime(2013, 1, 1, 0, 0, 0, 0))

    def test_truncation_year(self):
        """
        Tests that truncate always works
        """
        self.do.truncate('year')
        self.assertEqual(self.do.naive(), datetime(2013, 1, 1, 0, 0, 0, 0))

    def test_date(self):
        self.do.date()
        self.assertEqual(self.do.date(), date(2013, 1, 3))

    def test_datetime(self):
        self.assertEqual(self.do.naive(), datetime(2013, 1, 3, 4, 31, 14, 148546))

    def test_naive(self):
        dt1 = Delorean()
        dt_naive = dt1.naive()
        self.assertEqual(dt_naive.tzinfo, None)

    def test_localize(self):
        dt = datetime.today()
        utc = timezone("UTC")
        dt = localize(dt, "UTC")
        self.assertEqual(dt.tzinfo, utc)

    def test_normalize(self):
        dt1 = Delorean()
        dt2 = Delorean(timezone="US/Eastern")
        dt1.truncate('minute')
        dt2.truncate('minute')
        dt_normalized = normalize(dt1.datetime, "US/Eastern")
        self.assertEqual(dt2.datetime, dt_normalized)

    def test_normalize_failure(self):
        naive_datetime = datetime.today()
        self.assertRaises(ValueError, normalize, naive_datetime, "US/Eastern")

    def test_localize_failure(self):
        dt1 = localize(datetime.utcnow(), "UTC")
        self.assertRaises(ValueError, localize, dt1, "UTC")

    def test_timezone(self):
        utc = timezone('UTC')
        do_timezone = Delorean().timezone()
        self.assertEqual(utc, do_timezone)

    def test_datetime_timezone_default(self):
        do = Delorean()
        do.truncate('minute')
        dt1 = datetime_timezone()
        self.assertEqual(dt1.replace(second=0, microsecond=0), do.datetime)

    def test_datetime_timezone(self):
        do = Delorean(timezone="US/Eastern")
        do.truncate("minute")
        dt1 = datetime_timezone(tz="US/Eastern")
        self.assertEqual(dt1.replace(second=0, microsecond=0), do.datetime)

    def test_parse(self):
        do = capture('Thu Sep 25 10:36:28 BRST 2003')
        dt1 = utc.localize(datetime(2003, 9, 25, 10, 36, 28))
        self.assertEqual(do.datetime, dt1)

    def test_parse_with_utc_year_fill(self):
        do = capture('Thu Sep 25 10:36:28')
        dt1 = utc.localize(datetime(2013, 9, 25, 10, 36, 28))
        self.assertEqual(do.datetime, dt1)

    def test_parse_with_timezeon_year_fill(self):
        do = capture('Thu Sep 25 10:36:28', timezone="US/Eastern")
        est = timezone("US/Eastern")
        dt1 = est.localize(datetime(2013, 9, 25, 10, 36, 28))
        self.assertEqual(do.datetime, dt1)
        self.assertEqual(do._tz, "US/Eastern")

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

        d_obj_next = move_datetime_namedday(self.do.datetime, 'next', 'friday')
        d_obj_last = move_datetime_namedday(self.do.datetime, 'last', 'friday')

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

        d_obj_next = move_datetime_week(self.do.datetime, 'next', 1)
        d_obj_last = move_datetime_week(self.do.datetime, 'last', 1)

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

        d_obj_next = move_datetime_month(self.do.datetime, 'next', 1)
        d_obj_last = move_datetime_month(self.do.datetime, 'last', 1)

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

        d_obj_next = move_datetime_year(self.do.datetime, 'next', 1)
        d_obj_last = move_datetime_year(self.do.datetime, 'last', 1)

        self.assertEqual(dt_next, d_obj_next)
        self.assertEqual(dt_last, d_obj_last)

    def test_range_count(self):
        """
        tests the range method with count used
        """
        pass

    def test_range_with_start(self):
        pass

    def test_range_with_start_and_stop(self):
        pass

    def test_range_with_interval(self):
        pass

    def test_delorean(self):
        pass


if __name__ == '__main__':
    main()
