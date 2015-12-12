# -*- coding: utf-8 -*-

from jsonado.db import tables
from raincife.db.connections import MainConnection
from tokens.db.managers import TokenManager


class Token(tables.Table):
    table = 'token'
    db = 'raincife'
    connection = MainConnection
    documents = TokenManager
