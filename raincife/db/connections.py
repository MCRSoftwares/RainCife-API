# -*- coding: utf-8 -*-


from jsonado.db import tables
from decouple import config


class MainConnection(tables.Connection):
    db_host = config('DB_HOST', default='localhost')
    db_port = config('DB_PORT', default='28015')
