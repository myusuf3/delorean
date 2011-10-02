#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

    def test_today(self):
        pass

    def test_future(self):
        pass
    
    def test_date(self):
    	pass



if __name__ == '__main__':
	unittest.main()
