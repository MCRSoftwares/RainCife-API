# -*- coding: utf-8 -*-

from jsonado.db import tables
from raincife.db.connections import MainConnection
from marcadores.db.managers import MarcadorManager


class Marcador(tables.Table):
    """
    Classe que referencia a tabela 'marcador' no banco 'raincife'.
    """
    table = 'marcador'
    db = 'raincife'
    connection = MainConnection
    documents = MarcadorManager
    indexes = {
        'usuario_id': lambda row: row['usuario_id']
    }
