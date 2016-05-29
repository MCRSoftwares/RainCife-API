# -*- coding: utf-8 -*-

from jsonado.core.exceptions import BaseError


class HandlerError(BaseError):

    def message_attr_is_not_table(self, *args):
        return ('Expected a "Table" class, got "{0}" instead.').format(*args)
