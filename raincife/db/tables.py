# -*- coding: utf-8 -*-


class Tables(object):
    _tables = []
    _indexes = {}

    def all(self):
        return self._tables

    def get(self, index):
        return self._tables[index]

    def get_indexes(self, table):
        return self._indexes[table]

    def get_index(self, table, position):
        return self._indexes[table][position]

    def add(self, *values):
        for value in values:
            self._tables.append(value)

    def set_indexes(self, indexes):
        self._indexes = indexes

manager = Tables()
