# -*- coding: utf-8 -*-

from jsonado.core.exceptions import CommandError
from jsonado.core.exceptions import LogError
import glob
import os
import pyclbr
import re
import sys


def match(regex, text):
    return bool(re.search(regex, text))


def get_module(module, name):
    return getattr(__import__('{}'.format(
        module), fromlist=[name]), name)


class ClassFinder(object):

    def __init__(self, module, class_name, *args, **kwargs):
        self.superclass = get_module(module, class_name)
        super(ClassFinder, self).__init__(*args, **kwargs)

    def _find_modules(self, path, reset=False):
        if reset:
            self._modules_list = []
        if reset or not hasattr(
                self, '_modules_list') or not self._modules_list:
            self._modules_list = []
            for root, dirnames, filenames in os.walk(path):
                for py_file in glob.glob('{0}/*.py'.format(root)):
                    self._modules_list.append(re.sub(
                        r'.py$', '', py_file).replace('/', '.'))
        return self._modules_list

    def find(self, path, reset=False):
        py_files = self._find_modules(path, reset=reset)
        for module_str in py_files:
            browser = pyclbr.readmodule(module_str)
            for name in browser.keys():
                obj = get_module('{}'.format(module_str), name)
                if issubclass(obj, self.superclass):
                    yield obj


class Commands(object):

    def __init__(self, *args, **kwargs):
        cmd_args = sys.argv if not args else list(args)
        cmd_args.pop(0)
        if len(cmd_args) > 0:
            command = cmd_args.pop(0)
            cmd_def = 'cmd_{0}'.format(command)
            if hasattr(self, cmd_def):
                getattr(self, cmd_def)(*cmd_args)
            else:
                raise CommandError(code='cmd_not_found', args=[command])
        else:
            raise CommandError(code='no_args_provided')
        super(Commands, self).__init__(*args, **kwargs)


class Logger(object):
    enclosure = ['[', ']']

    @classmethod
    def _find_log_def(cls, code, *args):
        log_def = 'log_{0}'.format(code)
        if hasattr(cls, log_def):
            return getattr(cls(), log_def)(*args)
        else:
            raise LogError(code='log_not_found', args=[code])

    @classmethod
    def _get_enclosure(cls, value):

        if isinstance(cls.enclosure, basestring):
            return '{0}{1}'.format(value, cls.enclosure[0])

        if not (isinstance(cls.enclosure, list) or
                isinstance(cls.enclosure, tuple)):
            raise LogError(
                code='invalid_enclosure_type',
                args=[type(cls.enclosure).__name__]
            )

        if len(cls.enclosure) > 2 or not cls.enclosure:
            raise LogError(
                code='invalid_enclosure_len',
                args=[len(cls.enclosure)]
            )

        if len(cls.enclosure) == 1:
            return '{0}{1}'.format(cls.enclosure[0], value)

        return '{0}{1}{2}'.format(cls.enclosure[0], value, cls.enclosure[1])

    @classmethod
    def raw(cls, code, args=[]):
        log_def = cls._find_log_def(code, *args)
        print log_def

    @classmethod
    def info(cls, code, args=[]):
        log_def = cls._find_log_def(code, *args)
        print '{0} {1}'.format(cls._get_enclosure('INFO'), log_def)

    @classmethod
    def warning(cls, code, args=[]):
        log_def = cls._find_log_def(code, *args)
        print '{0} {1}'.format(cls._get_enclosure('WARNING'), log_def)

    @classmethod
    def error(cls, code, args=[]):
        log_def = cls._find_log_def(code, *args)
        print '{0} {1}'.format(cls._get_enclosure('ERROR'), log_def)
