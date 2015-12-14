# -*- coding: utf-8 -*-

from jsonado.handlers.generic import ReDBHandler
from core.exceptions import ValidationError
from usuarios.db.tables import Usuario
from tokens.db.tables import Token
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
        'usuario': basestring,
        'senha': basestring,
        'nome': basestring,
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
        data['senha'] = bcrypt.hashpw(
            data['senha'].encode('utf-8'), bcrypt.gensalt(
                config('HASH_COMPLEXITY', default=10, cast=int)))

        usuario_exists = (yield self.docs.get_all(
            data['usuario'], index='usuario').coerce_to('array').run())

        email_exists = (yield self.docs.get_all(
            data['email'], index='email').coerce_to('array').run())

        if usuario_exists:
            response = {
                'data': [
                    {
                        'usuario': u'Esse nome de usuário já existe!',
                    }
                ]
            }
            self.set_status(400)
        elif email_exists:
            response = {
                'data': [
                    {
                        'email': u'Esse email já está cadastrado!',
                    }
                ]
            }
            self.set_status(400)
        else:
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
                        'nome': data['nome'],
                        'response': db_response
                    }
                ]
            }
            Token.docs.new_token(usuario=data['usuario'])
        raise gen.Return(response)
