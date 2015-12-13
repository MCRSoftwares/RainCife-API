# -*- coding: utf-8 -*-

from jsonado.handlers.generic import ReDBHandler
from usuarios.db.tables import Usuario
from tornado import gen
import json


class UsuarioCreateHandler(ReDBHandler):
    table = Usuario

    @gen.coroutine
    def post(self):
        data = json.loads(self.request.body)
        response = (yield self.docs.insert(data).run())
        self.write(response)
