#!/usr/bin/env python

"""
Test for testing the data model for delorean.
"""
from delorean import Delorean
from datetime import datetime
from unittest import TestCase, main


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

    def test_naive(self):
        dt1 = Delorean()
        dt1.naive()
        self.assertEqual(dt1.datetime.tzinfo, None)


if __name__ == '__main__':
    main()
