# -*- coding: utf-8 -*-


from jsonado.db import tables
from decouple import config


class MainConnection(tables.Connection):
    """
    Conexão principal com o servidor do banco de dados.
    """
    db_host = config('DB_HOST', default='localhost')
    db_port = config('DB_PORT', default='28015')
