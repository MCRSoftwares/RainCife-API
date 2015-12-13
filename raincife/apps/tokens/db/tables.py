# -*- coding: utf-8 -*-

from jsonado.db import tables
from raincife.db.connections import MainConnection
from tokens.db.managers import TokenManager


class Token(tables.Table):
    """
    Classe que referencia a tabela 'token' no banco 'raincife'.
    """
    table = 'token'
    db = 'raincife'
    connection = MainConnection
    documents = TokenManager
    indexes = {
        'usuario_id': lambda row: row['usuario_id']
    }
