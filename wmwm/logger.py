#!/usr/bin/python

'''
Logging module.

This module defines five logging levels: `DEBUG`, `VERBOSE`, `INFO`, `WARN`,
`ERROR`. It also defines their corresponding single-letter logging methods:
`d()`, `v()`, `i()`, `w()`, `e()`. These methods should be used exclusively
instead of the builtin methods (such as `debug()`).
'''

import logging
import types

# Loglevels.
DEBUG = logging.DEBUG
VERBOSE = logging.INFO - 1
INFO = logging.INFO
WARN = logging.WARN
ERROR = logging.ERROR

# Loglevel code-to-name mapping.
LOGLEVELZ = {
    DEBUG: 'debug',
    VERBOSE: 'verbose',
    INFO: 'info',
    WARN: 'warn',
    ERROR: 'error',
}

def d(self, msg, *args, **kwargs):
    '''Log at debug level.'''
    return self.log(DEBUG, msg, *args, **kwargs)

def v(self, msg, *args, **kwargs):
    '''Log at verbose level.'''
    return self.log(VERBOSE, msg, *args, **kwargs)

def i(self, msg, *args, **kwargs):
    '''Log at info level.'''
    return self.log(INFO, msg, *args, **kwargs)

def w(self, msg, *args, **kwargs):
    '''Log at warn level.'''
    return self.log(WARN, msg, *args, **kwargs)

def e(self, msg, *args, **kwargs):
    '''Log at error level.'''
    return self.log(ERROR, msg, *args, **kwargs)

# The logger object.
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

# Bind logging methods to the logger object.
logger.d = types.MethodType(d, logger)
logger.v = types.MethodType(v, logger)
logger.i = types.MethodType(i, logger)
logger.w = types.MethodType(w, logger)
logger.e = types.MethodType(e, logger)
