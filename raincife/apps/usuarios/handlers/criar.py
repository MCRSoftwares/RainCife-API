# -*- coding: utf-8 -*-

from jsonado.handlers.generic import ReDBHandler
from core.exceptions import ValidationError
from usuarios.db.tables import Usuario
from token.db.tables import Token
from decouple import config
from tornado import gen
import json
import bcrypt


class UsuarioCreateHandler(ReDBHandler):
    """
    Handler responsável pela criação de novos usuários.
    """
    table = Usuario
    post_fields = {
        'usuario': str,
        'senha': str,
        'nome': str,
        'email': str
    }

    @gen.coroutine
    def post(self):
        """
        Método assíncrono responsável pelo tratamento dos dados enviados
        via POST para a aplicação.
        """
        data = json.loads(self.request.body)
        response = (yield self.validate(data))
        self.write(response)

    @gen.coroutine
    def validate(self, data):
        """
        Método assíncrono responsável por validar os campos
        da requisição de criação de um usuário via POST.
        """

        # Checa se os campos e valores desses campos correspondem
        # ao que foi previamente definido em 'self.post_fields'.
        for field, value in data.iteritems():
            if field not in self.post_fields.keys():
                raise ValidationError(
                    code='invalid_field', args=[field, value])
            if not isinstance(value, self.post_fields[field]):
                raise ValidationError(
                    code='invalid_type_for_field', args=[field, value])

        # Criptografa a senha antes de salvá-la no banco.
        data['senha'] = bcrypt.hashpw(
            data['senha'], bcrypt.gensalt(config('HASH_COMPLEXITY')))

        # Executa a inserção do usuário.
        response = (yield self.docs.insert(data).run())

        raise gen.Return(response)
