# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from spil.util.log import debug, info
from spil import Sid, SpilException
from spil.sid.pathops.write_paths import WriteToPaths

"""
Creates all given Sids on the filesystem, as defined in data_conf (template or touch)

Important: uses the actual project paths, as in config_name. Be careful !!

"""


def generate_mock_fs(sids, config='fs_conf', force=False):

    root = Sid(sids[0]).get_as('project').path(config)
    print(root)
    if root.exists() and list(root.iterdir()) and not force:
        raise SpilException(f"Root folder {root} exists and is not empty. "
                            f"This script is about to fill it with mock data. "
                            f"For safety, the script is aborted. "
                            f"Use force=True to force. ")

    writer = WriteToPaths(config)

    for sid in sids:
        try:
            writer.create(sid)
            info(f"Created {sid}")
        except SpilException as e:
            debug(e)


if __name__ == '__main__':

    from spil.util.log import setLevel, INFO

    print('')
    print('Tests start')
    print('')

    # setLevel(WARN)
    setLevel(INFO)
    # setLevel(DEBUG)  # In case of problems, use DEBUG mode

    sids = ['hamlet/s/sq010/sh0010/layout/v001/w/hip',
            'hamlet/s/sq010/sh0010/anim/v001/w/ma',
            'hamlet/s/sq010/sh0010/render/v001/p/mov']

    generate_mock_fs(sids, config='server')

