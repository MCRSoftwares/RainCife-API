# -*- coding: utf-8 -*-

from core.mixins import CurrentUserMixin
from core.exceptions import AuthError
from usuarios.db.tables import Usuario
from tokens.db.tables import Token
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
        # O request deve ser autenticado via token antes de proceder
        response = (yield self.authenticate(data))
        self.write(response)

    @gen.coroutine
    def authenticate(self, data):
        """
        Método assíncrono responsável por autenticar
        a requisição de alteração do usuário via POST.
        """
        token = data.pop('token', None)
        usuario_id = data.pop('usuario_id', None)

        if not token:
            # O token não foi encontrado nos dados recebidos
            raise AuthError(code='token_is_none')
        if not usuario_id:
            # O ID do usuário não foi encontrado nos dados recebidos
            raise AuthError(code='user_is_none')

        # Validação do token, via consulta.
        valid_token = (yield Token.docs.usuario(usuario_id).run())[0]
        if token != valid_token['token']:
            # Se o token fornecido for diferente do token presente no banco
            raise AuthError(code='invalid_token')
        # Senão, a alteração é aceita e executada.
        response = (yield self.docs.get(usuario_id).update(data).run())
        # Retorna a resposta do banco.
        raise gen.Return(response)
