#!/usr/bin/env python2

"""
Tests for importer module.
"""

from decimal import Decimal as D
import datetime
import unittest

from stocktracker import importers
from stocktracker import transactions


class TestImporters(unittest.TestCase):
    def setUp(self):
        super(TestImporters, self).setUp()
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

    def _verify_transactions(self, importer):
        self.assertEqual(importer.transactions[0],
                         transactions.Transfer(datetime.date(2008, 1, 1),
                                               D('400')))
        self.assertEqual(importer.transactions[1],
                         transactions.Interest(datetime.date(2008, 1, 31),
                                               D('0.02')))
        self.assertEqual(importer.transactions[2],
                         transactions.Interest(datetime.date(2008, 2, 1),
                                               D('0.01')))
        self.assertEqual(
            importer.transactions[3],
            transactions.Buy(datetime.date(2008, 3, 19), 'FOO', D('21'),
                             D('1.2345'), D('9.99'), D('35.91'), False))
        self.assertEqual(
            importer.transactions[4],
            transactions.Sell(datetime.date(2008, 4, 1), 'FOO', D('19'),
                              D('2.34'), D('10'), D('34.46')))
        self.assertEqual(
            importer.transactions[5],
            transactions.Dividend(datetime.date(2008, 5, 3), 'FOO', D('0.12'),
                                  False, False))
        self.assertEqual(
            importer.transactions[6],
            transactions.Dividend(datetime.date(2008, 5, 3), 'FOO', D('0.80'),
                                  True, False))
        self.assertEqual(
            importer.transactions[7],
            transactions.CapGain(datetime.date(2008, 5, 3), 'FOO', D('5.43'),
                                 True, False))
        self.assertEqual(
            importer.transactions[8],
            transactions.SecurityTransfer(datetime.date(2008, 9, 15), 'FOO',
                                          D('-2')))
        self.assertEqual(
            importer.transactions[9],
            transactions.Transfer(datetime.date(2008, 12, 31), D('-400')))

        self.assertEqual(len(importer.transactions), 10)

    def test_td_ameritrade(self):
        td_importer = importers.TDAmeritradeImporter(
            'tests/test_data/td_ameritrade.csv')
        td_importer.do_import()
        self._verify_transactions(td_importer)

    def test_csv(self):
        csv_importer = importers.CSVImporter('tests/test_data/st.csv')
        csv_importer.do_import()
        self._verify_transactions(csv_importer)
