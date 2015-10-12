# -*- coding: utf-8 -*-


class Tables(object):
    _tables = []

    def all(self):
        return self._tables

    def get(self, index):
        return self._tables[index]

    def add(self, *values):
        for value in values:
            self._tables.append(value)


manager = Tables()
