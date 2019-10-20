# -*- coding: utf-8 -*-
"""
A simple logger shortcut / wrapper.

Uses
https://logzero.readthedocs.io/

Coloring Code borrowed from https://stackoverflow.com/questions/20333674/pycharm-logging-output-colours
@author https://stackoverflow.com/users/1329248/dablak

Modified to add formatter & None color.

# NOTE : The Handler streams to stdout per default (instead of stderr)

# FIXME : colors are hardcoded
"""

import sys
import logging
from logging import DEBUG, INFO, WARN, ERROR, CRITICAL
import logzero
from logzero import logger

from spil.libs.util import conf

msg_colors = {
        DEBUG: 'green',
        INFO: None,
        WARN: 'magenta',
        ERROR: 'red',
        CRITICAL: 'red'
    }


class _AnsiColorizer(object):
    """
    A colorizer is an object that loosely wraps around a stream, allowing
    callers to write text to the stream in a particular color.

    Colorizer classes must implement C{supported()} and C{write(text, color)}.
    """
    _colors = dict(black=30, red=31, green=32, yellow=33,
                   blue=34, magenta=35, cyan=36, white=37)

    def __init__(self, stream):
        self.stream = stream

    @classmethod
    def supported(cls, stream=sys.stdout):
        """
        A class method that returns True if the current platform supports
        coloring terminal output using this method. Returns False otherwise.
        """
        if not stream.isatty():
            return False  # auto color only on TTYs
        try:
            import curses
        except ImportError:
            return False
        else:
            try:
                try:
                    return curses.tigetnum("colors") > 2
                except curses.error:
                    curses.setupterm()
                    return curses.tigetnum("colors") > 2
            except:
                raise
                # guess false in case of error
                return False

    def write(self, text, color=None):
        """
        Write the given text to the stream in the given color.

        @param text: Text to be written to the stream.

        @param color: A string label for a color. e.g. 'red', 'white'.
        """
        if color:
            color = self._colors[color]
            self.stream.write('\x1b[%s;1m%s\x1b[0m' % (color, text))
        else:
            self.stream.write(text)


class ColorHandler(logging.StreamHandler):

    def __init__(self, stream=sys.stdout):
        super(ColorHandler, self).__init__(_AnsiColorizer(stream))

    def emit(self, record):

        color = msg_colors.get(record.levelno, "blue")
        self.stream.write(self.format(record) + "\n", color)


#__logFormat = '[%(asctime)s] %(levelname)8s| %(message)s (%(filename)s:%(funcName)s:%(lineno)d)'
# __logFormat = '%(color)s [%(asctime)s] %(levelname)-6s| [%(module)s.%(funcName)s] %(message)-80s (%(lineno)d) %(end_color)s'

__logFormat = '[%(asctime)s] %(levelname)-6s| [%(module)s.%(funcName)s] %(message)-80s (%(lineno)d)'

#logging.basicConfig(format=__logFormat, level=conf.loglevel) # ??
# The following is needed to override the Maya logging configuration, the "basicConfig" does not work
#logger = logging.getLogger()

# logzero.formatter(logging.Formatter(fmt=__logFormat))
#formatter = logzero.formatter(Formatter(fmt=__logFormat))
# logger = logzero.setup_logger(name='sid', formatter=formatter)

"""
for handler in logger.handlers:
    print handler
"""

# we set a new handler
# handler = StreamHandler(sys.stdout)
handler = ColorHandler(sys.stdout)
handler.setFormatter(logzero.LogFormatter(fmt=__logFormat, color=True))
logger.handlers = []
logger.addHandler(handler)

logger.setLevel(conf.loglevel)

'''
Code shortcuts
'''
debug = logger.debug
info = logger.info
warn = logger.warn
error = logger.error
critical = logger.critical

setLevel = logger.setLevel
getLevel = logger.getEffectiveLevel

'''
def debug_var(*args, **kwargs): # not used
    caller = '({0}:{1}:{2})'.format(os.path.basename(inspect.stack()[1][1]),inspect.stack()[1][2], inspect.stack()[1][3] )
    if len(args) == 2:
        if isinstance(args[0], basestring):
            ret = '{0}: {1}'.format(args[0], args[1]) + caller
            print(ret)
'''

if __name__ == '__main__':

    setLevel(INFO)
    debug('titi')

    info('toto')
    warn('toto')
    error('toto')
    critical('toto')

    setLevel(DEBUG)

    debug('titi')
