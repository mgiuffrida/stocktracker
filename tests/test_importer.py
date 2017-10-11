#!/usr/bin/env python2

"""
Tests for importer module.
"""

import datetime
import unittest
from decimal import Decimal as D

from stocktracker import importer
from stocktracker import transactions


class TestTDAmeritradeImporter(unittest.TestCase):
    def setUp(self):
        super(TestTDAmeritradeImporter, self).setUp()
        self.addTypeEqualityFunc(transactions.Transfer, self._assert_txn_equal)
        self.addTypeEqualityFunc(transactions.Interest, self._assert_txn_equal)
        self.addTypeEqualityFunc(transactions.Buy, self._assert_txn_equal)
        self.addTypeEqualityFunc(transactions.Sell, self._assert_txn_equal)
        self.addTypeEqualityFunc(transactions.Dividend, self._assert_txn_equal)
        self.addTypeEqualityFunc(transactions.CapGain, self._assert_txn_equal)
        self.addTypeEqualityFunc(transactions.SecurityTransfer,
                                 self._assert_txn_equal)

    def _assert_txn_equal(self, lhs, rhs, msg):
        self.assertDictEqual(lhs.__dict__, rhs.__dict__, msg)

    def test_import(self):
        td_importer = importer.TDAmeritradeImporter(
            'tests/test_data/td_ameritrade.csv')
        td_importer.do_import()
        self.assertEqual(len(td_importer.transactions), 10)
        self.assertEqual(td_importer.transactions[0],
                         transactions.Transfer(datetime.date(2008, 1, 1),
                                               D('400')))
        self.assertEqual(td_importer.transactions[1],
                         transactions.Interest(datetime.date(2008, 1, 31),
                                               D('0.02')))
        self.assertEqual(td_importer.transactions[2],
                         transactions.Interest(datetime.date(2008, 2, 1),
                                               D('0.01')))
        self.assertEqual(
            td_importer.transactions[3],
            transactions.Buy(datetime.date(2008, 3, 19), 'FOO', D('21'),
                             D('1.2345'), D('9.99'), D('35.91'), False))
        self.assertEqual(
            td_importer.transactions[4],
            transactions.Sell(datetime.date(2008, 4, 1), 'FOO', D('19'),
                              D('2.34'), D('10'), D('34.46')))
        self.assertEqual(
            td_importer.transactions[5],
            transactions.Dividend(datetime.date(2008, 5, 3), 'FOO', D('0.12'),
                                  False, False))
        self.assertEqual(
            td_importer.transactions[6],
            transactions.Dividend(datetime.date(2008, 5, 3), 'FOO', D('0.80'),
                                  True, False))
        self.assertEqual(
            td_importer.transactions[7],
            transactions.CapGain(datetime.date(2008, 5, 3), 'FOO', D('5.43'),
                                 True, False))
        self.assertEqual(
            td_importer.transactions[8],
            transactions.SecurityTransfer(datetime.date(2008, 9, 15), 'FOO',
                                          D('-2')))
        self.assertEqual(
            td_importer.transactions[9],
            transactions.Transfer(datetime.date(2008, 12, 31), D('-400')))
