# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
from spil.conf.global_conf import __version__
try:
    from spil.sid.sid import Sid
    from spil.sid.search.fs import FS
    from spil.sid.search.ls import LS
    from spil.data.data import Data
    from spil.util.exception import SpilException
    from spil.util import log
    from spil.util.log import setLevel, ERROR
    setLevel(ERROR)
except Exception as e:
    raise Exception('Spil is imported, but impossible to import spil packages. \n Please check compatibility of your sid_conf and fs_conf files.')