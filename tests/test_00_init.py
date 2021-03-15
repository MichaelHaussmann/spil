# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""

"""

See INSTALL.md about Testing.

The SPIL library works with a configuration package, containing at least sid_conf, fs_conf.

At delivery, SPIL contains "demo_conf" as a configuration package.

Once you start working with your own data, you will replace the demo_conf folder by a folder of your choice.
For SPIL to work, simply include this folder to your python path.

The pytest uses its own python path.
For the tests to work, you need to specify here the path to this configuration folder.

If this is not configured, it falls back to ""
By default it uses "demo_conf".

"""
import os
import sys

# CHANGE PATH HERE FOR TESTS ON CUSTOM DATA (See comment above)
SPIL_CONF_PATH = ''

if not SPIL_CONF_PATH:
    SPIL_CONF_PATH = os.path.realpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'demo_conf'))
    print('Defaulting to demo_conf for tests')

sys.path.append(SPIL_CONF_PATH)

from pprint import pprint
pprint(sys.path)

import sid_conf
print( sid_conf )
