#!/usr/bin/env python


import os
import sys
import unittest
from datetime import timedelta, datetime, time, date, tzinfo

from delorean import Delorean

sys.path.append(os.getcwd())


class DeloreanTests(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_tomorrow(self):
        d=Delorean()
        current_date = d.date()
        time_delta = timedelta(days=1)
        d.tomorrow()
        self.assertTrue(d, current_date+time_delta)

    def test_date(self):
        d=Delorean()
        datetimeutc = datetime.utcnow()
        self.assertEqual(d.date(), datetimeutc.date())
    
    def test_time(self):
        pass
    

    def test_date_timetravel(self, days=1, weeks=1):
        d=Delorean()
        sample = datetime(2002,10,10)
        d.utcdatetime = sample
        current_date = d.date()
        current_date = current_date + timedelta(days=1, weeks=1)
        d.timetravel(days=1, weeks=1)
        self.assertEqual(d.date(), current_date)
    
    def test_time_timtravel(self, seconds=1, minutes=1, microseconds=100):
        d = Delorean()
        sample = datetime(2011, 10, 10, 1, 33, 4, 121940)
        d.utcdatetime = sample
        current_time = d.datetime()
        current_time = current_time + timedelta(seconds=1, minutes=1, microseconds=100)
        d.timetravel(seconds=1, minutes=1, microseconds=100)
        self.assertEqual(d.time(), current_time.time())


    def test_future(self):
        pass



if __name__ == '__main__':
	unittest.main()
