# -*- coding: utf-8 -*-

from jsonado.core.exceptions import BaseError


class ReDBError(BaseError):

    def message_attr_is_not_string(self, *args):
        return ('The "{0}" attribute needs a string or buffer,'
                ' "{1}" found.').format(*args)

    def message_attr_is_not_connection(self, *args):
        return ('Expected a "Connection" class,'
                ' got "{0}" instead.').format(*args)
