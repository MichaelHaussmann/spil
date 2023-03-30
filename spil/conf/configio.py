# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
import json
import platform

from pathlib import Path

from spil.util.log import debug, info, error
from spil.util.singleton import Singleton

from spil.conf.global_conf import user_app_folder_name, user_conf_file_name


def get_user_config_path():
    """
    Defines the user configuration path (including the conf.json file.
    Relies on Path.home()

    Note: On windows, different python versions return different paths for Path.home().
    To be able to use this library from many Python versions,
    this was unified to be in Path.home() / Documents
    (given "Documents" exist)

    Returns a Path object.
    """
    home = Path.home()
    if home.name == "Documents" and home.parent.exists():
        home = home.parent  # fix for maya
    user_config_path = home / user_app_folder_name / user_conf_file_name

    return user_config_path


user_config_path = get_user_config_path()


class ConfigIO(Singleton):
    '''
    Writer and Reader for User config_name
    '''

    conf_path = None

    def __init__(self):

        self.conf_path = str(user_config_path)

        # Creating file
        try:
            if not user_config_path.exists():
                user_config_path.parent.mkdir(mode=0o777, parents=True, exist_ok=True)
                with open(self.conf_path, 'w') as conf_file:
                    json.dump({}, conf_file)
        except Exception as e:
            error('Problem creating Conf file : {} -> {}'.format(user_config_path, e))

    def save(self, key, value=None):

        data = self.read() or {}

        if value is None:
            data.pop(key, None)  # remove the key if None
        else:
            data[key] = value

        with open(self.conf_path, 'w') as conf_file:
            json.dump(data, conf_file)

    def read(self, key=None, default=None):

        data = {}
        try:
            with open(self.conf_path) as conf_file:
                data = json.load(conf_file)
        except Exception as e:
            error('Problem reading Conf file : {}'.format(e))

        if key is None:
            return data
        else:
            return data.get(key, default)


if __name__ == '__main__':

    from spil import logging
    logging.setLevel(logging.INFO)
    info('Path is : {}'.format(user_config_path))
    cfio = ConfigIO()
    info(cfio.read())
    cfio.save('test', 'brief test ...')
    info(cfio.read())
    cfio.save('test', None)
    cfio.save('tested', 'OK')
    info(cfio.read())

