#!/usr/bin/env python2

"""
Tests for utility module.
"""

import datetime
import unittest

from stocktracker import utility


class TestUtility(unittest.TestCase):
    def test_dates(self):
        self.assertEqual(utility.from_js_date('2017-01-10T01:12:45.678Z'),
                         datetime.date(2017, 1, 10))
