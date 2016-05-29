# -*- coding: utf-8 -*-


class BaseError(Exception):
    def __init__(self, code=None, args=[], message='Unknown error.'):
        if code:
            message_def = 'message_{0}'.format(code)
            if hasattr(self, message_def):
                message = getattr(self, message_def)(*args)
        super(BaseError, self).__init__(message)


class CommandError(BaseError):

    def message_cmd_not_found(self, *args):
        return 'Could not find the command "{}".'.format(*args)

    def message_no_args_provided(self, *args):
        return 'No arguments were provided.'


class LogError(BaseError):

    def message_log_not_found(self, *args):
        return 'Could not find the log with code "{}".'.format(*args)

    def message_invalid_enclosure_type(self, *args):
        return ('Expected a string, tuple or list, '
                'got "{}" instead.').format(*args)

    def message_invalid_enclosure_len(self, *args):
        return ('Expected a list with length in range (1, 2), '
                'got a length of "{}" instead.').format(*args)
