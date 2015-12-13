# -*- coding: utf-8 -*-


from usuarios.handlers import UsuarioListHandler
from usuarios.handlers import UsuarioCreateHandler
from usuarios.handlers import UsuarioUpdateHandler


base_router = '/api/v1/usuarios{}'

routers = [
    (base_router.format('/'), UsuarioListHandler),
    (base_router.format('/alterar/'), UsuarioUpdateHandler),
    (base_router.format('/criar/'), UsuarioCreateHandler),
]
