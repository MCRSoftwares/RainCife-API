# -*- coding: utf-8 -*-

"""
Routers definem os caminhos (URLs) da aplicação.
Este módulo define e concatena todos os routers da aplicação.
"""

from usuarios.routers import routers as usuario_routers
from marcadores.routers import routers as marcadores_routers

routers = []
routers += usuario_routers
routers += marcadores_routers
