# -*- coding: utf-8 -*-

from jsonado.handlers.generic import ReDBHandler
from core.exceptions import ValidationError
from core.utils import gen_pw
from core.enums import USER_AUTH_COOKIE
from usuarios.db.tables import Usuario
from tokens.db.tables import Token
from tornado import gen
import json


class UsuarioCreateHandler(ReDBHandler):
    """
    Handler responsável pela criação de novos usuários.
    """
    table = Usuario
    post_fields = {
        'usuario': basestring,
        'senha': basestring,
        'email': basestring
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
        if len(self.post_fields.keys()) != len(data.keys()):
            raise ValidationError(code='invalid_fields_len', args=[
                len(self.post_fields.keys()), len(data.keys())])
        for field, value in data.iteritems():
            if field not in self.post_fields.keys():
                raise ValidationError(
                    code='invalid_field', args=[field, value])
            if not isinstance(value, self.post_fields[field]):
                raise ValidationError(code='invalid_type_for_field', args=[
                    self.post_fields[field], field, type(value)])

        # Criptografa a senha antes de salvá-la no banco.
        data['senha'] = gen_pw(data['senha'])

        usuario_exists = (yield self.docs.get_all(
            data['usuario'], index='usuario').coerce_to('array').run())

        email_exists = (yield self.docs.get_all(
            data['email'], index='email').coerce_to('array').run())

        response = {'data': [{}], 'status': 201}
        if usuario_exists:
            response['data'][0].update(
                {
                    'usuario': u'Esse nome de usuário já existe!'
                }
            )
            response['status'] = 409
        if email_exists:
            response['data'][0].update(
                {
                    'email': u'Esse email já está cadastrado!',
                }
            )
            response['status'] = 409

        self.set_status(response['status'])

        if not usuario_exists and not email_exists:
            # Executa a inserção do usuário.
            db_response = (yield self.docs.insert(data).run())
            response = {
                'data': [
                    {
                        'id': (yield self.docs.get_all(
                            data['usuario'],
                            index='usuario').pluck('id').run())[0]['id'],
                        'usuario': data['usuario'],
                        'email': data['email'],
                        'response': db_response
                    }
                ],
                'status': 201
            }
            (yield Token.docs.new_token(
                usuario_id=db_response['generated_keys'][0]).run())
            self.set_secure_cookie(
                USER_AUTH_COOKIE, db_response['generated_keys'][0])
        raise gen.Return(response)
