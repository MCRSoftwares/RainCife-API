# -*- coding: utf-8 -*-

from usuarios.routers import routers as usuario_routers
from marcadores.routers import routers as marcadores_routers

routers = []
routers += usuario_routers
routers += marcadores_routers
