# -*- coding: utf-8 -*-
# type: ignore
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
import importlib
import inspect

from spil.conf.util import extrapolate_templates, pattern_replacing

# stubs that are replaced by imports
sid_templates = {}
to_extrapolate = []
key_types = {}
extrapolate_types = {}
extrapolation_leaf_subtype = None
basetyped_search_narrowing = {}
key_patterns = {}
extension_alias = {}
projects = []
leaf_keys = {}

try:
    module = importlib.import_module('spil_sid_conf')
except ModuleNotFoundError as e:
    problem = sid_conf_import_error_message.format(module='spil_sid_conf')
    print(problem)
    raise Exception(problem)

__all__ = []
for name, value in inspect.getmembers(module):
    if name.startswith('__'):
        continue

    globals()[name] = value
    __all__.append(name)

sid_templates = extrapolate_templates(sid_templates, extrapolate_types, to_extrapolate, extrapolation_leaf_subtype)
pattern_replacing(sid_templates, key_patterns)

if __name__ == '__main__':

    from pprint import pprint

    pprint(globals())
