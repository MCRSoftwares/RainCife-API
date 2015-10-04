# -*- coding: utf-8 -*-

from sys import modules
from types import FunctionType
from re import findall


def _simplify(value):
    return '_'.join(findall('[A-Z]+[a-z]+|[a-z]+', value)).lower()


def include_view(name=None):

    def add_view_to_list(obj):

        module = modules[obj.__module__]

        if not hasattr(module, '__all__'):
            setattr(module, '__all__', [])

        if not name or not isinstance(name, basestring):
            view_name = _simplify(obj.__name__)
        else:
            view_name = name

        if view_name in module.__all__:
            raise Exception('Duplicated View name given: '
                            '\'{0}\''.format(view_name))

        module.__all__.append(view_name)

        if not isinstance(obj, FunctionType):
            try:
                setattr(module, view_name, obj.as_view())

            except AttributeError:
                raise AttributeError('Given class \'{0}\' is not a '
                                     'Class-based View'.format(obj.__name__))
        else:
            return obj

    if name and not isinstance(name, basestring):
        return add_view_to_list(name)

    return add_view_to_list