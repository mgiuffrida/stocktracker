#!/usr/bin/env python2

"""Importer for stocktracker CSV files from CSVExporter."""

from decimal import Decimal
import ast
import csv

from stocktracker import dollars, exporter, transactions, utility
from .importer import Importer


class CSVImporter(Importer):
    """Imports from CSV files created by CSVExporter."""

    def import_from_file(self, source):
        reader = csv.DictReader(source)
        assert tuple(reader.fieldnames) == exporter.csv_cols

        for row in reader:
            txn = self._parse_transaction(row)
            assert txn
            self.transactions.append(txn)

    def _parse_transaction(self, data):
        date = utility.from_js_date(data['date'])
        total = dollars.parse(data['total']) if data['total'] else None

        if data['type'] == 'Dividend':
            return transactions.Dividend(
                date,
                data['symbol'],
                total,
                ast.literal_eval(data['is_qualified']),
                False)
        if data['type'] == 'Transfer':
            return transactions.Transfer(date, total)
        if data['type'] == 'SecurityTransfer':
            return transactions.SecurityTransfer(
                date, data['symbol'], Decimal(data['quantity']))
        if data['type'] == 'Interest':
            return transactions.Interest(date, total)
        if data['type'] == 'CapGain':
            return transactions.CapGain(
                date, data['symbol'], total,
                ast.literal_eval(data['is_long_term']), False)
        assert data['type'] in ('Buy', 'Sell')
        return self._parse_trade(data, date, total)

    def _parse_trade(self, data, date, total):
        quantity = Decimal(data['quantity'])
        price = dollars.parse(data['price'])
        fees = dollars.parse(data['fees'])
        symbol = data['symbol']
        if data['type'] == 'Buy':
            return transactions.Buy(
                date, symbol, quantity, price, fees, total, False)
        return transactions.Sell(
            date, symbol, quantity, price, fees, total)
