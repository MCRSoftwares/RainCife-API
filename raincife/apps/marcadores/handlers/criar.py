# -*- coding: utf-8 -*-

from core.mixins import CurrentUserMixin
from core.exceptions import ValidationError
from marcadores.db.tables import Marcador
from tornado import gen
from tornado.web import authenticated
import json


class MarcadorCreateHandler(CurrentUserMixin):
    """
    Handler responsável pela criação de novos usuários.
    """
    table = Marcador
    post_fields = {
        'usuario': basestring,
        'latitude': basestring,
        'longitude': basestring,
        'intensidade': basestring
    }

    @authenticated
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

        usuario_id = self.get_current_user()
        db_response = (yield self.docs.new_marcador(usuario_id, data).run())
        response = {
            'data': [
                {
                    'id': db_response['generated_keys'][0],
                    'usuario_id': data['usuario_id'],
                    'latitude': data['latitude'],
                    'longitude': data['longitude'],
                    'response': db_response
                }
            ],
            'status': 201
        }

        raise gen.Return(response)
