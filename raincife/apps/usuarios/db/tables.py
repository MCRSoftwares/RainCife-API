# -*- coding: utf-8 -*-

from jsonado.db import tables
from raincife.db.connections import MainConnection
from usuarios.db.managers import UsuarioManager


class Usuario(tables.Table):
    """
    Classe que referencia a tabela 'usuario' no banco 'raincife'.
    """
    table = 'usuario'
    db = 'raincife'
    connection = MainConnection
    documents = UsuarioManager
    indexes = {
        'usuario': lambda row: row['usuario']
    }
