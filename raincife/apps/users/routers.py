# -*- coding: utf-8 -*-


from users.handlers import UserListHandler


routers = [
    ('/api/v1/users/', UserListHandler),
]
