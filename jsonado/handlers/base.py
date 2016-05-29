# -*- coding: utf-8 -*-

from jsonado.handlers.exceptions import HandlerError
from jsonado.db.tables import Table


class ReDBHandlerBase(object):
    table = None

    def __init__(self, *args, **kwargs):
        if not self.table or not issubclass(self.table, Table):
            raise HandlerError(code='attr_is_not_table',
                               args=[type(self.table).__name__])
        self.table = self.table()
        self.docs = self.table.docs
        super(ReDBHandlerBase, self).__init__(*args, **kwargs)
