# -*- coding: utf-8 -*-

from jsonado.handlers.generic import ReDBHandler
from core.exceptions import AuthError
from usuarios.db.tables import Usuario
from tokens.db.tables import Token
from tornado import gen
import json


class UsuarioUpdateHandler(ReDBHandler):
    table = Usuario

    @gen.coroutine
    def post(self):
        data = json.loads(self.request.body)
        response = (yield self.authenticate(data))
        self.write(response)

    @gen.coroutine
    def authenticate(self, data):
        token = data.pop('token', None)
        usuario_id = data.pop('usuario_id', None)

        if not token:
            raise AuthError(code='token_is_none')
        if not usuario_id:
            raise AuthError(code='user_is_none')

        valid_token = (yield Token.docs.usuario(usuario_id).run())[0]
        if token != valid_token['token']:
            raise AuthError(code='invalid_token')
        update = (yield self.docs.get(usuario_id).update(data).run())
        raise gen.Return(update)
