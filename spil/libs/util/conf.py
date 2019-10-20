# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.


@author: michael.haussmann

Application conf for the spil lib.

The user conf (sid, file system templates, productions) is in spil.conf

Should be used as:
from spil.libs.util import conf
print conf.application_name

"""


import os
import logging

pysep = '/'  # python path separator

__version__ = '0.0.1'
application_codename = 'Artichoke'  # because my tools have vegetable names...
application_repo = 'PROD' if os.path.realpath(__file__).count('prod') else 'BETA' if os.path.realpath(__file__).count('beta') else 'ALPHA'
application_name = 'SPIL Simple Pipeline Lib - v{0} ("{1}") - {2}'.format(__version__, application_codename, application_repo)

application_repo_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))).replace(os.sep, pysep)

# automatic replacement to INFO and WARN in BETA and PROD
loglevel = logging.DEBUG


# Put here extra config for ALPHA code
if application_repo == 'ALPHA':
    # print 'ALPHA CONFIG OVERRIDES'
    pass
