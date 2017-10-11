#!/usr/bin/env python2

"""
Tests for transactions module.
"""
from decimal import Decimal as D
import unittest

from datetime import date

from stocktracker import transactions


class TestTransactions(unittest.TestCase):
    def test_dividend(self):
        dividend = transactions.Dividend(date(2015, 2, 5), 'GOOG', D('100.10'),
                                         True, False)
        self.assertEqual(
            repr(dividend),
            '''Dividend(datetime.date(2015, 2, 5), 'GOOG', '''
            '''Decimal('100.10'), True, False)''')

        dividend.reinvested = True
        self.assertEqual(str(dividend),
                         '2015-02-05  Dividend of $100.10 from GOOG '
                         '(qualified) - reinvested')

        dividend.qualified = False
        self.assertEqual(
            str(dividend),
            '2015-02-05  Dividend of $100.10 from GOOG - reinvested')

        dividend.reinvested = False
        self.assertEqual(str(dividend),
                         '2015-02-05  Dividend of $100.10 from GOOG')

    # TODO: Test other Transaction types.
