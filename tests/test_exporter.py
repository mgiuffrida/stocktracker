#!/usr/bin/env python2

"""
Tests for exporter module.
"""

import csv
import datetime
import StringIO
import unittest
from decimal import Decimal as D

from stocktracker import exporter
from stocktracker import transactions


class TestCSVExporter(unittest.TestCase):
    def test_export(self):
        csv_exporter = exporter.CSVExporter('test_file.csv')

        txn_list = transactions.TransactionList([
            transactions.Dividend(
                datetime.date(2008, 1, 1), 'FOO', D('0.01'), False, False),
            transactions.Dividend(
                datetime.date(2008, 12, 31), 'BAR', D('1.2345'), True, False),
            transactions.Transfer(datetime.date(2008, 1, 2), D('400')),
            transactions.Transfer(datetime.date(2008, 1, 3), D('-800')),
            transactions.Interest(datetime.date(2008, 1, 3), D('0.02')),
            transactions.Buy(datetime.date(2008, 1, 4), 'FOO', D('21'),
                             D('1.2345'), D('9.99'), D('35.91'), False),
            transactions.Sell(datetime.date(2008, 1, 5), 'FOO', D('19'),
                              D('2.34'), D('10'), D('34.46')),
            transactions.CapGain(
                datetime.date(2008, 1, 6), 'FOO', D('5.43'), True, False),
            transactions.SecurityTransfer(
                datetime.date(2008, 1, 7), 'FOO', D('3')),
            transactions.SecurityTransfer(
                datetime.date(2008, 1, 7), 'FOO', D('-1')),
        ])

        output = StringIO.StringIO()
        csv_exporter.export_to_file(output, txn_list)

        output.seek(0)
        reader = csv.DictReader(output)

        self.assertDictContainsSubset({
            'type': 'Dividend',
            'date': '2008-01-01',
            'symbol': 'FOO',
            'total': '$0.01',
        }, reader.next())
        self.assertDictContainsSubset({
            'type': 'Dividend',
            'date': '2008-12-31',
            'symbol': 'BAR',
            'total': '$1.2345',
        }, reader.next())

        self.assertDictContainsSubset({
            'type': 'Transfer', 'total': '$400',
            'date': '2008-01-02',
        }, reader.next())
        self.assertDictContainsSubset({
            'type': 'Transfer', 'total': '$-800',
            'date': '2008-01-03',
        }, reader.next())

        self.assertDictContainsSubset({
            'type': 'Interest', 'total': '$0.02',
            'date': '2008-01-03',
        }, reader.next())

        self.assertDictContainsSubset({
            'type': 'Buy',
            'date': '2008-01-04',
            'symbol': 'FOO',
            'quantity': '21',
            'price': '1.2345',
            'fees': '9.99',
            'total': '$35.91',
        }, reader.next())

        self.assertDictContainsSubset({
            'type': 'Sell',
            'date': '2008-01-05',
            'symbol': 'FOO',
            'quantity': '19',
            'price': '2.34',
            'fees': '10',
            'total': '$34.46',
        }, reader.next())

        self.assertDictContainsSubset({
            'type': 'CapGain',
            'date': '2008-01-06',
            'symbol': 'FOO',
            'total': '$5.43',
            'is_long_term': 'True',
        }, reader.next())

        self.assertDictContainsSubset({
            'type': 'SecurityTransfer',
            'date': '2008-01-07',
            'quantity': '3',
        }, reader.next())
        self.assertDictContainsSubset({
            'type': 'SecurityTransfer',
            'date': '2008-01-07',
            'quantity': '-1',
        }, reader.next())

        self.assertRaises(StopIteration, reader.next)
