# -*- coding: utf-8 -*-

from jsonado.db import tables
from raincife.db.connections import MainConnection
from users.db.managers import UsuarioManager


class Usuario(tables.Table):
    table = 'usuario'
    db = 'raincife'
    connection = MainConnection
    documents = UsuarioManager
