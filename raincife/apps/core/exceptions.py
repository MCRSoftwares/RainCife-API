# -*- coding: utf-8 -*-

from jsonado.core.exceptions import BaseError


class AuthError(BaseError):

    def message_token_is_none(self, *args):
        return u'O token de autenticação não foi fornecido.'

    def message_invalid_token(self, *args):
        return u'Token de autenticação inválido.'

    def message_user_is_none(self, *args):
        return u'O ID do usuário não foi fornecido.'
