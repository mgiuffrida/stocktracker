#!/usr/bin/env python2

"""
Exports transactions to a file.
"""

import csv

from stocktracker import dollars, transactions


class Exporter(object):
    """Base class for an exporter."""

    def __init__(self, filename):
        self.filename = filename
        self.transactions = []

    def do_export(self, txn_list):
        """Opens the file and delegates the exporting.

        Overwrites the file if it exists.
        """
        with open(self.filename, 'w+') as dest:
            self.export_to_file(dest, txn_list)

    def export_to_file(self, dest, txn_list):
        """Exports the transactions to the opened file."""
        raise NotImplementedError


csv_cols = (
    'date', 'type',
    # Monetary-related transactions.
    'total',
    # Equity-related transactions.
    'symbol',
    # Trades and equity transfers.
    'quantity',
    # Trades.
    'price', 'fees',
    # Dividends.
    'is_qualified',
    # Capital gains.
    'is_long_term',
)


class CSVExporter(Exporter):
    """Exports to CSV format."""

    def export_to_file(self, dest, txn_list):
        writer = csv.DictWriter(dest, csv_cols)
        writer.writeheader()

        for txn in txn_list:
            data = dict()
            data['date'] = txn.date
            data['type'] = type(txn).__name__
            if isinstance(txn, transactions.Dividend):
                data.update({
                    'symbol': txn.symbol,
                    'total': txn.amount,
                    'is_qualified': txn.qualified,
                })
            if isinstance(txn, transactions.Transfer):
                data['total'] = txn.amount
            if isinstance(txn, transactions.Interest):
                data['total'] = txn.amount
            if isinstance(txn, transactions.Buy):
                data.update({
                    'symbol': txn.symbol,
                    'quantity': txn.num_shares,
                    'price': txn.price,
                    'fees': txn.fees,
                    'total': txn.total,
                })
            if isinstance(txn, transactions.Sell):
                data.update({
                    'symbol': txn.symbol,
                    'quantity': txn.num_shares,
                    'price': txn.price,
                    'fees': txn.fees,
                    'total': txn.total,
                })
            if isinstance(txn, transactions.CapGain):
                data.update({
                    'symbol': txn.symbol,
                    'total': txn.amount,
                    'is_long_term': txn.long_term,
                })
            if isinstance(txn, transactions.SecurityTransfer):
                data.update({
                    'symbol': txn.symbol,
                    'quantity': txn.num_shares,
                })
            if 'total' in data:
                data['total'] = self._dollar_str(data['total'])
            writer.writerow(data)

    def _dollar_str(self, value):
        return dollars.to_str(value,
                              limit_precision=False,
                              accounting_style=False)
