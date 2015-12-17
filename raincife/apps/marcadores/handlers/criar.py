# -*- coding: utf-8 -*-

from jsonado.handlers import CORSHandler
from core.exceptions import ValidationError
from core.utils import gen_pw
from core.enums import USER_AUTH_COOKIE
from core.enums import TIMEZONE
from marcadores.db.tables import Marcador
from usuarios.db.tables import Usuario
from datetime import datetime
from tornado import gen
import rethinkdb as r
import json


class UsuarioCreateHandler(CORSHandler):
    """
    Handler responsável pela criação de novos usuários.
    """
    table = Marcador
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


        raise gen.Return(response)
