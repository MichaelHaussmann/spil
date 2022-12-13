from __future__ import annotations
import importlib
import inspect
from spil import conf
from spil.util.log import debug
from spil.conf.util import pattern_replacing
from spil.util.caching import lru_cache as cache


@cache
def get_path_config(name: str | None = None) -> PathConfig:

    if not name:  # either name, or configured default, or first config_name entry
        name = conf.default_path_config or list(conf.path_configs.keys())[0]

    config_module_name = conf.path_configs.get(name)

    config = PathConfig(name, config_module_name)

    debug(f'Getting: {config}')

    return config


class PathConfig:

    def __init__(self, name: str = 'fs_conf', config_module_name: str = None):

        self.name = name
        config_module_name = config_module_name or name

        try:
            self.module = importlib.import_module(config_module_name)
        except ModuleNotFoundError as e:
            problem = conf.sid_conf_import_error_message.format(module=config_module_name)
            print(problem)
            raise Exception(problem)

        for name, value in inspect.getmembers(self.module):
            if name.startswith('__'):
                continue

            setattr(self, name, value)

        pattern_replacing(self.path_templates, self.key_patterns)

    def __str__(self):
        return f"PathConfig: {self.name} / {self.module}"


if __name__ == '__main__':

    from pprint import pprint
    from spil.util.log import setLevel, INFO, info, DEBUG

    info('Tests start')

    setLevel(INFO)

    conf.set('default_path_config', None)
    get_path_config.cache_clear()

    pc = get_path_config()
    pprint(pc.path_templates.get('project_root'))

    conf.set('default_path_config', 'server')
    get_path_config.cache_clear()

    pc = get_path_config()
    pprint(pc.path_templates.get('project_root'))

    pc = get_path_config('local')
    pprint(pc.path_templates.get('project_root'))

    pc = get_path_config('server')
    pprint(pc.path_templates.get('project_root'))