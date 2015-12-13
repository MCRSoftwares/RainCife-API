# -*- coding: utf-8 -*-

from jsonado.handlers.generic import ReDBHandler
from usuarios.db.tables import Usuario
from tornado import gen
import json


class UsuarioCreateHandler(ReDBHandler):
    """
    Handler responsável pela criação de novos usuários.
    """
    table = Usuario

    @gen.coroutine
    def post(self):
        """
        Método assíncrono responsável pelo tratamento dos dados enviados
        via POST para a aplicação.
        """
        data = json.loads(self.request.body)
        response = (yield self.docs.insert(data).run())
        self.write(response)
