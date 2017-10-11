#!/usr/bin/env python2

"""Importers should subclass importers.Importer."""


class Importer(object):
    """Base class for an importer."""

    def __init__(self, filename):
        self.filename = filename
        self.transactions = []

    def do_import(self):
        """Opens the file and delegates the importing."""
        with open(self.filename, 'r') as source:
            self.import_from_file(source)

    def import_from_file(self, source):
        """Imports transactions from the opened file."""
        raise NotImplementedError
