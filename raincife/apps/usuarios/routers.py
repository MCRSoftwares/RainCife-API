# -*- coding: utf-8 -*-


from users.handlers import UsuarioListHandler


routers = [
    ('/api/v1/usuarios/', UsuarioListHandler),
]
