"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from pathlib import Path


def write_sids_to_file(sids, sid_file):
    """
    This function writes given Sids to the given Sid file
    (EOL separated file = one Sid string per line).

    To obtain Example Sids by parsing the existing files, use parse_sid_files.py.
    """
    sid_file = Path(sid_file)

    if sid_file.exists():
        raise Exception('The test file "{}" already exists. Skipped'.format(sid_file))

    with open(str(sid_file), 'w') as f:
        for sid in sids:
            f.write(str(sid) + '\n')

    print('Written {} Sids to {}'.format(len(sids), sid_file))


if __name__ == '__main__':

    print('Generating Example Sids.')

    sids = ['hamlet/s/sq010/sh0010/layout/v001/w/hip',
            'hamlet/s/sq010/sh0010/anim/v001/w/ma',
            'hamlet/s/sq010/sh0010/render/v001/p/mov']

    # sid_file = ""  # define path
    # write_sids_to_file(sids, sid_file)

    print('Done.')
