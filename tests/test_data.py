#!/usr/bin/env python

"""
Test for testing the data model for delorean.
"""
from delorean import Delorean, datetime_timezone, localize, normalize
from datetime import datetime, date
from unittest import TestCase, main
from pytz import timezone


class DeloreanTests(TestCase):

    def setUp(self):
        date1 = datetime(2013, 1, 3, 4, 31, 14, 148546)
        self.do = Delorean(dt=date1)

    def test_truncation_hour(self):
        """
        Tests that truncate always works
        """
        self.do.truncate('hour')
        self.assertEqual(self.do.datetime, datetime(2013, 1, 3, 4, 0))

    def test_truncation_second(self):
        """
        Tests that truncate always works
        """
        self.do.truncate('second')
        self.assertEqual(self.do.datetime, datetime(2013, 1, 3, 4, 31, 14, 0))

    def test_truncation_minute(self):
        """
        Tests that truncate always works
        """
        self.do.truncate('minute')
        self.assertEqual(self.do.datetime, datetime(2013, 1, 3, 4, 31, 0, 0))

    def test_truncation_day(self):
        """
        Tests that truncate always works
        """
        self.do.truncate('day')
        self.assertEqual(self.do.datetime, datetime(2013, 1, 3, 0, 0, 0, 0))

    def test_truncation_month(self):
        """
        Tests that truncate always works
        """
        self.do.truncate('month')
        self.assertEqual(self.do.datetime, datetime(2013, 1, 1, 0, 0, 0, 0))

    def test_truncation_year(self):
        """
        Tests that truncate always works
        """
        self.do.truncate('year')
        self.assertEqual(self.do.datetime, datetime(2013, 1, 1, 0, 0, 0, 0))

    def test_date(self):
        self.do.date()
        self.assertEqual(self.do.date(), date(2013, 1, 3))

    def test_datetime(self):
        self.assertEqual(self.do.datetime, datetime(2013, 1, 3, 4, 31, 14, 148546))

    def test_naive(self):
        dt1 = Delorean()
        dt1.naive()
        self.assertEqual(dt1.datetime.tzinfo, None)

    def test_localize(self):
        dt = datetime.today()
        utc = timezone("UTC")
        dt = localize(dt, "UTC")
        self.assertEqual(dt.tzinfo, utc)

    def test_normalize(self):
        dt1 = Delorean()
        dt2 = Delorean(tz="US/Eastern")
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
        do = Delorean(tz="US/Eastern")
        do.truncate("minute")
        dt1 = datetime_timezone(tz="US/Eastern")
        self.assertEqual(dt1.replace(second=0, microsecond=0), do.datetime)


if __name__ == '__main__':
    main()
