# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""

import importlib
import inspect

from spil.conf.util import extrapolate, pattern_replacing

# stubs that are replaced by imports
sid_templates = {}
key_types = {}
key_patterns = {}
extension_alias = {}

try:
    module = importlib.import_module('sid_conf')
except ModuleNotFoundError as e:
    problem = """
    -------------------------------------------------------------------------------------------------------------
    CONFIGURATION PROBLEM: 
    
    The configuration module "sid_conf" was not found.
    
    Ensure to either include "demo_conf" in your python path, 
    or create your own "sid_conf" and add its folder to the python path.    
    
    (If you are running a py.test edit the SPIL_CONF_PATH variable in tests/test_00_init.py to match a python path.)
    
    Please see installation and configuration documentation.
    
    -------------------------------------------------------------------------------------------------------------
    """
    print(problem)
    raise Exception(problem)

__all__ = []
for name, value in inspect.getmembers(module):
    if name.startswith('__'):
        continue

    globals()[name] = value
    __all__.append(name)

sid_templates = extrapolate(sid_templates, key_types)
pattern_replacing(sid_templates, key_patterns)

if __name__ == '__main__':

    from pprint import pprint

    pprint(globals())

