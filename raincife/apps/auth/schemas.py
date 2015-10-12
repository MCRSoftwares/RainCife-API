# -*- coding: utf-8 -*-

from raincife.utils.schemas import Schema


class TokenSchema(Schema):
    base_field = 'auth'
    fields = {
        'id': {'type': basestring, 'required': True},
        'user': {'type': basestring, 'required': True},
        'type': {'type': basestring, 'required': True},
    }


class UserSchema(Schema):
    base_field = 'auth'
    fields = {
        'type': {'type': basestring, 'required': True},
        'username': {'type': basestring, 'required': True},
        'password': {'type': basestring, 'required': True},
    }

Token = TokenSchema()
User = UserSchema()
