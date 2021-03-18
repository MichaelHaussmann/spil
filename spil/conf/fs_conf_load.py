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

from spil.conf.util import pattern_replacing

# stubs that are replaced by imports
path_templates = {}
key_types = {}
key_patterns = {}
search_path_mapping = {}
sidkeys_to_extrakeys = {}
extrakeys_to_sidkeys = {}
path_mapping = {}
path_templates_reference = ''
path_defaults = {}

try:
    module = importlib.import_module('fs_conf')
except ModuleNotFoundError as e:
    problem = """
    -------------------------------------------------------------------------------------------------------------
    CONFIGURATION PROBLEM: 

    The configuration module "fs_conf" was not found.
    
    Ensure to either include "demo_conf" in your python path, 
    or create your own "fs_conf" and add its folder to the python path.    

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

pattern_replacing(path_templates, key_patterns)

if __name__ == '__main__':
    from pprint import pprint

    pprint(globals())
