# -*- coding: utf-8 -*-
"""
Created in the past.

@author: michael.haussmann

A simple logger shortcut / wrapper.

Uses
https://logzero.readthedocs.io/

"""

import logging

import logzero
from logzero import logger
from spil.libs.util import conf


#__logFormat = '[%(asctime)s] %(levelname)8s| %(message)s (%(filename)s:%(funcName)s:%(lineno)d)'

__logFormat = '[%(asctime)s] %(levelname)-6s| [%(module)s.%(funcName)s] %(message)-80s (%(lineno)d)'

#logging.basicConfig(format=__logFormat, level=conf.loglevel) # ??

# The following is needed to override the Maya logging configuration, the "basicConfig" does not work
#logger = logging.getLogger()
"""
for handler in logger.handlers:
    handler.setFormatter(logging.Formatter(fmt=__logFormat))
"""

logzero.formatter(logging.Formatter(fmt=__logFormat))

logger.setLevel(conf.loglevel)



"""
Code shortcuts
"""
debug = logger.debug
info = logger.info
warn = logger.warn
error = logger.error
critical = logger.critical

setLevel = logger.setLevel
getLevel = logger.getEffectiveLevel

DEBUG = logging.DEBUG
INFO = logging.INFO
WARN = logging.WARN
ERROR = logging.ERROR


if __name__ == '__main__':


    setLevel(INFO)
    debug('titi')

    info('toto')
    warn('toto')
    error('toto')
    critical('toto')

    setLevel(DEBUG)

    debug('titi')