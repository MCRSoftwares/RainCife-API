# -*- coding: utf-8 -*-


class classproperty(object):

    def __init__(self, method):
        self.method = method

    def __get__(self, obj, owner):
        return self.method(owner)
