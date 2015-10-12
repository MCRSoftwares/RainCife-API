# -*- coding: utf-8 -*-

JSON = {
    'invalid_format': {
        'error': {
            'code': 'JSON001',
            'message': u'JSON com formatação inválida'
        }
    },
    'not_implemented': {
        'error': {
            'code': 'JSON002',
            'message': u'Métodos \'json_invalid\' e \'json_valid\' '
                       u'devem ser implementados na subclasse'
        }
    }
}

AUTH = {
    'invalid_token': {
        'error': {
            'code': 'AUTH001',
            'message': u'Token de autenticação inválido'
        }
    },
}

SCHEMA = {
    'none_fields': {
        'error': {
            'code': 'SCHEMA001',
            'message': u'O campo \'fields\' não pode ser nulo'
        }
    }
}
