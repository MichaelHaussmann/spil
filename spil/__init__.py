"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from spil.conf.global_conf import __version__

try:
    from spil import conf  # default config bootstrap
    from spil.sid.sid import Sid

    from spil.sid.read.finder import Finder
    from spil.sid.pathops.find_paths import FindInPaths
    from spil.sid.read.finders.find_list import FindInList
    from spil.sid.read.finders.find_constants import FindInConstants
    from spil.sid.read.finders.find_all import FindInAll
    from spil.sid.read.getters.getter_all import GetFromAll
#     from spil.sid.read.finders.find_cache import FindInCache

    from spil.sid.read.getter import Getter
    from spil.sid.pathops.getter_paths import GetFromPaths

    from spil.sid.write.writer import Writer
    from spil.sid.write.write_all import WriteToAll
    from spil.sid.pathops.write_paths import WriteToPaths

    # FIXME: keep util level import
    from spil.util.exception import SpilException
    from spil.util import log
    from spil.util import log as logging  # to use as standard logging and create custom loggers
    from spil.util.log import setLevel, ERROR

    setLevel(ERROR)
except Exception as e:
    import traceback  # fmt: skip
    traceback.print_exc()
    raise Exception(
        "Spil is imported, but impossible to import spil packages. \n Please check compatibility of your sid_conf and fs_conf files."
    )
