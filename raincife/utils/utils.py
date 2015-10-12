# -*- coding: utf-8 -*-

from re import findall


def str_bool(value):
    return {"True": True}.get(value, False)


def simplify(value):
    return '_'.join(findall('[A-Z]+[a-z]+|[a-z]+', value)).lower()
