# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.


"""


class SpilException(Exception):
    """
    A SpilException.

    This SpilException should always be raised and handled inside this Spil package.
    """
    pass


if __name__ == '__main__':
    
    try:
        try:
            raise Exception('toto')
        except Exception as ex:
            raise SpilException(ex)
        
    except SpilException as pe:
        
        print('caught : ', pe)
