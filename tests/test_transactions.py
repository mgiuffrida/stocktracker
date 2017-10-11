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

    def test_comparisons(self):
        # Similar transactions compare by identity.
        transfer1 = transactions.Transfer(date(2015, 1, 1), D('1'))
        transfer1_2 = transactions.Transfer(date(2015, 1, 1), D('1'))
        self.assertEqual(transfer1, transfer1)
        self.assertNotEqual(transfer1, transfer1_2)

        # Only date is used to compare dissimilar transactions.
        transfers = [
            transactions.Transfer(date(2015, 1, 2), D('1')),
            transactions.Transfer(date(2015, 1, 3), D('0')),
            transactions.Transfer(date(2015, 1, 4), D('3')),
            transactions.Transfer(date(2015, 1, 5), D('2')),
        ]
        for i in xrange(0, len(transfers)):
            for j in xrange(i + 1, len(transfers)):
                self.assertLess(transfers[i], transfers[j])
                self.assertLessEqual(transfers[i], transfers[j])
                self.assertGreater(transfers[j], transfers[i])
                self.assertGreaterEqual(transfers[j], transfers[i])

    # TODO: Test other Transaction types.
