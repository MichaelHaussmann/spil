# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2022 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
from spil.conf.global_conf import *

# user config
from spil.conf.configio import ConfigIO

try:
    from spil.conf.sid_conf_load import *
    # from spil.conf.fs_conf_load import *
    from spil.conf.data_conf_load import *
except Exception as e:
    raise Exception('Unable to import the spil_conf files (sid_conf, data_conf). \n'
                    'Please check the files compatibility with the latest SPIL version.')


# function to override config into user config
def set(key, value, save=True):
    """
    Sets a variable "key" with given "value" as a config variable.

    If the variable exists in the current config, it's value is overriden.

    If save is True (the default), the variable is saved into the user config, and persisted
    (unless the config file is wiped).

    Example :

    conf.set('prefered_project', self.ui.prod_CBB.currentText() or conf.prefered_project)
    # replaces the variable 'prefered_project' (or keeps the default one)

    See also spil.tests.conf_tests
    """
    globals()[key] = value
    if save:
        user_conf.save(key, value)


def get(key):
    """
    Gets a value from the config, or None if not set.
    """
    return globals().get(key)


user_conf = ConfigIO()
globals().update(user_conf.read())

if __name__ == '__main__':

    # This will create a configuration file and folder in the user path.

    from pprint import pprint

    pprint(globals())

    project = 'test'

    # print(projects)

    # user conf
    print(project)
    set('project', 'bla')
    print(project)

    pprint(globals())
