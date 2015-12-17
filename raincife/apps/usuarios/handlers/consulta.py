# -*- coding: utf-8 -*-

from core.mixins import CurrentUserMixin
from jsonado.handlers import CORSHandler
from usuarios.db.tables import Usuario
from tornado import gen
from tornado.web import authenticated
from core.utils import is_email
from core.utils import check_pw
from core.enums import USER_AUTH_COOKIE
from core.enums import TIMEZONE
from datetime import datetime
import rethinkdb as r
import json


class UsuarioListHandler(CurrentUserMixin):
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
        self.write({'data': (yield self.get_url_query())})

    @gen.coroutine
    def get_url_query(self):
        raise gen.Return((yield self.docs.all().without(
            'ultimo_login', 'criado_em', 'senha').run()))


class UsuarioLogadoHandler(CurrentUserMixin):
    table = Usuario

    @authenticated
    @gen.coroutine
    def get(self):
        try:
            usuario = self.docs.get(self.get_current_user())
            response = {
                'data': [
                    (yield usuario.without(
                     'senha', 'id', 'criado_em', 'ultimo_login').run())
                ],
                'status': 200
            }
        except r.ReqlNonExistenceError:
            response = {
                'data': [
                    {
                        'usuario': u'Usuário não encontrado.'
                    }
                ],
                'status': 404
            }
            self.set_status(404)
        self.write(response)


class UsuarioInfoHandler(CurrentUserMixin):
    table = Usuario

    @authenticated
    @gen.coroutine
    def get(self, usuario):
        try:
            usuario = self.docs.get_all(usuario, index='usuario').without(
                'senha', 'id', 'criado_em', 'ultimo_login')
            response = {
                'data': [
                    (yield (yield usuario.run(cursor=True)).next())
                ],
                'status': 200
            }
        except r.ReqlCursorEmpty:
            response = {
                'data': [
                    {
                        'usuario': u'Usuário não encontrado.'
                    }
                ],
                'status': 404
            }
            self.set_status(404)
        self.write(response)


class UsuarioLoginHandler(CORSHandler):
    table = Usuario

    @gen.coroutine
    def post(self):
        data = json.loads(self.request.body)
        response = (yield self.authenticate(data))
        self.write(response)

    @gen.coroutine
    def authenticate(self, data=None):
        if not self.get_secure_cookie(USER_AUTH_COOKIE):
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
                self.set_secure_cookie(USER_AUTH_COOKIE, usuario['id'])
                response = {
                    'data': [
                        {
                            'id': usuario['id'],
                            'response': (yield self.docs.get(
                                usuario['id']).update({'ultimo_login': r.expr(
                                    datetime.now(TIMEZONE))}).run())
                        }
                    ],
                    'status': 200
                }
                self.set_status(200)
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
