# -*- coding: utf-8 -*-


from usuarios.handlers import UsuarioListHandler
from usuarios.handlers import UsuarioCreateHandler
from usuarios.handlers import UsuarioUpdateHandler


routers = [
    ('/api/v1/usuarios/', UsuarioListHandler),
    ('/api/v1/usuarios/alterar/', UsuarioUpdateHandler),
    ('/api/v1/usuarios/criar/', UsuarioCreateHandler),
]
