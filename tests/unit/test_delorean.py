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
        d=Delorean()
        print d
        datetimeutc = datetime.utcnow()
        print datetimeutc
        self.assertEqual(d.time(), datetimeutc.time())
    

    def test_timetravel(self, days=1, weeks=1):
        d=Delorean()
        current_datetime = d.date()
        current_datetime = current_datetime + timedelta(days=1, weeks=1)
        d.timetravel(days=1, weeks=1)
        self.assertEqual(d.date(), current_datetime)
        

    def test_future(self):
        pass



if __name__ == '__main__':
	unittest.main()
