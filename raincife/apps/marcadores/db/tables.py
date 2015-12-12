# -*- coding: utf-8 -*-

from jsonado.db import tables
from raincife.db.connections import MainConnection
from marcadores.db.managers import MarcadorManager


class Marcador(tables.Table):
    table = 'marcador'
    db = 'raincife'
    connection = MainConnection
    documents = MarcadorManager
