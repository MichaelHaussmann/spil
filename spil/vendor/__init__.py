# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.


"""

import os
import sys

"""
This package can be imported to force the vendor versions to be used. 

The lucidity lib has some minor incompatibilities with Python 3. These were fixed in the vendor version. 

"""

vendor_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../vendor'))

if vendor_path not in sys.path:
    # print('inserting {}'.format(vendor_path))
    sys.path.insert(0, vendor_path)


if __name__ == '__main__':

    print(vendor_path)

    from pprint import pprint
    pprint(sys.path)

    import lucidity
    print(lucidity)
