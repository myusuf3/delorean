#!/usr/bin/env python

"""
Test for testing the data model for delorean.
"""

import unittest

class Delorean(unittest.TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class DeloreanDatetimeTest(unittest.TestCase):
    pass

class DeloreanDate(unittest.TestCase):
    pass
