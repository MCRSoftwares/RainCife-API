# -*- coding: utf-8 -*-

from core.mixins import URLQueryMixin
from core.mixins import CurrentUserMixin
from jsonado.handlers.generic import ReDBHandler
from usuarios.db.tables import Usuario
from tokens.db.tables import Token
from tornado import gen
from tornado.web import authenticated
from core.utils import is_email
from core.utils import check_pw
from core.enums import USER_AUTH_COOKIE
from core.enums import TIMEZONE
from datetime import datetime
import rethinkdb as r
import json


class UsuarioListHandler(URLQueryMixin):
    """
    Handler responsável pela listagem de usuários existentes no banco.
    """
    table = Usuario

    @authenticated
    @gen.coroutine
    def get(self):
        """
        Método assíncrono responsável por retornar
        os dados recuperados do banco via GET.
        """
        self.set_secure_cookie(USER_AUTH_COOKIE, 'teste')
        self.write({'data': (yield self.url_query)})


class UsuarioLoginHandler(ReDBHandler):
    table = Usuario

    @gen.coroutine
    def post(self):
        try:
            data = json.loads(self.request.body)
        except ValueError:
            data = None
        response = (yield self.authenticate(data))
        self.write(response)

    @gen.coroutine
    def authenticate(self, data=None):
        if not self.get_secure_cookie(USER_AUTH_COOKIE):
            if not data:
                login = self.get_argument('login', None)
                senha = self.get_argument('senha', None)
            else:
                login = data.pop('login', None)
                senha = data.pop('senha', None)
            table_index = 'email' if is_email(login) else 'usuario'
            usuario_query = self.docs.get_all(login, index=table_index)
            usuario = (yield usuario_query.pluck('id', 'senha').run())
            response = {
                'data': [
                    {
                        'login': 'Usuário/Email ou Senha inválidos!'
                    }
                ],
                'status': 401
            }

            if not usuario:
                self.set_status(401)
                raise gen.Return(response)
            usuario = usuario.pop(0)
            if check_pw(senha, usuario['senha']):
                token_id = (yield Token.docs.new_token(
                    usuario_id=usuario['id']).run())['generated_keys'][0]
                self.set_secure_cookie(USER_AUTH_COOKIE, usuario['id'])
                response = {
                    'data': [
                        {
                            'login': usuario['id'],
                            'token': (yield Token.docs.get(
                                token_id).pluck('token').run())['token'],
                            'response': (yield self.docs.get(
                                usuario['id']).update({'ultimo_login': r.expr(
                                    datetime.now(TIMEZONE))}).run())
                        }
                    ],
                    'status': 201
                }
                raise gen.Return(response)

            self.set_status(401)
            raise gen.Return(response)

        response = {
            'data': [
                {
                    'login': 'Você já está logado!'
                }
            ],
            'status': 401
        }
        self.set_status(401)
        raise gen.Return(response)


class UsuarioLogoutHandler(CurrentUserMixin):
    table = Usuario

    @authenticated
    @gen.coroutine
    def get(self):
        self.set_secure_cookie(USER_AUTH_COOKIE, '')
        self.write({
            'data': [
                {
                    'logout': 'Você foi deslogado!'
                }
            ],
            'status': 200
        })
