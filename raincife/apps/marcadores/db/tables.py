# -*- coding: utf-8 -*-

from core.mixins import RaincifeTable
from raincife.db.connections import MainConnection
from marcadores.db.managers import MarcadorManager


class Marcador(RaincifeTable):
    """
    Classe que referencia a tabela 'marcador' no banco 'raincife'.
    """
    table = 'marcador'
    connection = MainConnection
    documents = MarcadorManager
    indexes = {
        'usuario_id': lambda row: row['usuario_id']
    }
