# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
import sys

import logging
import logzero
from logzero import logger

"""
A simple logger shortcut / wrapper.

Uses
https://logzero.readthedocs.io/

TODO: complete code clean.
"""

#__logFormat = '[%(asctime)s] %(levelname)8s| %(message)s (%(filename)s:%(funcName)s:%(lineno)d)'

__logFormat = '[%(asctime)s] %(levelname)-6s| [%(module)s.%(funcName)s] %(message)-80s (%(lineno)d)'
__logFormat_colored = '%(color)s[%(asctime)s] %(levelname)-6s| [%(module)s.%(funcName)s] %(message)-80s (%(lineno)d)%(end_color)s'
#logging.basicConfig(format=__logFormat, level=conf.loglevel) # ??

# The following is needed to override the Maya logging configuration, the "basicConfig" does not work
#logger = logging.getLogger()
"""
for handler in logger.handlers:
    handler.setFormatter(logging.Formatter(fmt=__logFormat))
"""

# we set a new handler

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logzero.LogFormatter(fmt=__logFormat, color=True))
logger.handlers = []
logger.addHandler(handler)

logzero.formatter(logging.Formatter(fmt=__logFormat))

logger.setLevel(logging.INFO)  # FIXME: config_name (depending on deploy dir)


def get_logger(name, color=True):
    new_logger = logzero.setup_logger(name=name)
    if color:
        new_logger.handlers[0].setFormatter(logzero.LogFormatter(fmt=__logFormat_colored, color=True))
    else:
        new_logger.handlers = []  # if we keep the handler, all logs are red.
        new_logger.addHandler(handler)
    return new_logger

"""
Code shortcuts
"""
debug = logger.debug
info = logger.info
warn = logger.warning  # warn is deprecated
warning = logger.warning
error = logger.error
critical = logger.critical

setLevel = logger.setLevel
getLevel = logger.getEffectiveLevel

DEBUG = logging.DEBUG
INFO = logging.INFO
WARN = logging.WARN
ERROR = logging.ERROR


if __name__ == '__main__':

    # specific logger (recommended)
    log_one = get_logger('one')
    # log_one = get_logger('one', color=False)
    log_one.debug('debug one')
    log_one.info('info one')
    log_one.setLevel(ERROR)
    log_one.debug('debug one')
    log_one.error('error one')

    # default logger
    setLevel(INFO)
    debug('titi')

    info('toto')
    warn('toto')
    error('toto')
    critical('toto')

    setLevel(DEBUG)

    debug('titi')