# -*- coding: utf-8 -*-

from core.mixins import RaincifeTable
from raincife.db.connections import MainConnection
from tokens.db.managers import TokenManager


class Token(RaincifeTable):
    """
    Classe que referencia a tabela 'token' no banco 'raincife'.
    """
    table = 'token'
    connection = MainConnection
    documents = TokenManager
    indexes = {
        'usuario_id': lambda row: row['usuario_id']
    }
