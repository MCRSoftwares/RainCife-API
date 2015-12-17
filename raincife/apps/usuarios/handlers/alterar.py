# -*- coding: utf-8 -*-

from core.mixins import CORSMixin
from usuarios.db.tables import Usuario
from tornado import gen
import json


class UsuarioUpdateHandler(CORSMixin):
    """
    Handler responsável pela alteração de usuários existentes no banco.
    """
    table = Usuario

    @gen.coroutine
    def post(self):
        """
        Método assíncrono responsável pelo tratamento dos dados enviados
        via POST para a aplicação.
        """
        data = json.loads(self.request.body)
        usuario_id = data['usuario_id']
        response = (yield self.docs.get(usuario_id).update(data).run())
        self.write(response)
