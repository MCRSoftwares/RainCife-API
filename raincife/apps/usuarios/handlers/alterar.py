# -*- coding: utf-8 -*-

from core.mixins import CurrentUserMixin
from usuarios.db.tables import Usuario
from tornado import gen
from tornado.web import authenticated
import json


class UsuarioUpdateHandler(CurrentUserMixin):
    """
    Handler responsável pela alteração de usuários existentes no banco.
    """
    table = Usuario

    @authenticated
    @gen.coroutine
    def post(self):
        """
        Método assíncrono responsável pelo tratamento dos dados enviados
        via POST para a aplicação.
        """
        data = json.loads(self.request.body)
        usuario_id = self.get_current_user()
        response = (yield self.docs.get(usuario_id).update(data).run())
        self.write(response)
