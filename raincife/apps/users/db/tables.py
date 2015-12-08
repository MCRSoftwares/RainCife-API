# -*- coding: utf-8 -*-

from jsonado.db import tables
from raincife.db.connections import MainConnection
from users.db.managers import UserManager


class User(tables.Table):
    table = 'user'
    db = 'raincife'
    connection = MainConnection
    documents = UserManager
