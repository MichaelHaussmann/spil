# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2024 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations
from typing import Optional

import importlib
import inspect

from resolva import Resolver

from spil import conf
from spil.util.log import debug
from spil.conf.util import pattern_replacing
from spil.util.caching import lru_cache as cache


@cache
def get_path_config(name: Optional[str] = None) -> PathConfig:

    if not name:  # either name, or configured default, or first config_name entry
        name = conf.default_path_config or list(conf.path_configs.keys())[0]  # type: ignore

    config_module_name = conf.path_configs.get(name)  # type: ignore

    config = PathConfig(name, config_module_name)  # type: ignore

    debug(f'Getting: {config}')

    return config


class PathConfig:

    def __init__(self, name: Optional[str] = 'spil_fs_conf', config_module_name: Optional[str] = None):

        self.name = name
        config_module_name = config_module_name or name

        try:
            self.module = importlib.import_module(config_module_name)  # type: ignore
        except ModuleNotFoundError as e:
            problem = conf.sid_conf_import_error_message.format(module=config_module_name)
            print(problem)
            raise Exception(problem)

        for name, value in inspect.getmembers(self.module):
            if name.startswith('__'):
                continue
            setattr(self, name, value)

        pattern_replacing(self.path_templates, self.key_patterns)  # type: ignore

        # instantiates a resolver if not already in instance cache
        Resolver.get(self.name) or Resolver(self.name, self.path_templates)  # type: ignore

    def __str__(self):
        return f"PathConfig: {self.name} / {self.module}"


if __name__ == '__main__':

    from spil.util.log import setLevel, INFO, info

    info('Tests start')

    setLevel(INFO)

    conf.set('default_path_config', None)
    get_path_config.cache_clear()

    pc = get_path_config()
    info(pc.path_templates.get('project'))

    conf.set('default_path_config', 'server')
    get_path_config.cache_clear()

    pc = get_path_config()
    info(pc.path_templates.get('project'))

    pc = get_path_config('local')
    info(pc.path_templates.get('project'))

    pc = get_path_config('server')
    info(pc.path_templates.get('project'))

    # clear at the end, because this is written to the user prefs.
    conf.set('default_path_config', None)