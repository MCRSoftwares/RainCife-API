# -*- coding: utf-8 -*-

from core.mixins import RaincifeTable
from jsonado.db import tables
from raincife.db.connections import MainConnection
from usuarios.db.managers import UsuarioManager


class Usuario(RaincifeTable, tables.Table):
    """
    Classe que referencia a tabela 'usuario' no banco 'raincife'.
    """
    table = 'usuario'
    connection = MainConnection
    documents = UsuarioManager
    indexes = {
        'usuario': lambda row: row['usuario'],
        'email': lambda row: row['email']
    }
