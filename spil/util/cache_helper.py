# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2022 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""


# FIXME: this is work in progress
def reload_lru_caches():
    """
    Reloads all current lru caches.


    """
    from spil.data.find_in_cache import get_sidcache
    from spil.data.data import get_cached_attribute, get_data_source
    from spil.sid.read.tools import unfold_search
    from spil.sid.core.sid_resolver import sid_to_dict, sid_to_dicts
    from spil.sid.core.fs_resolver import path_to_dict

    cached_functions = [get_cached_attribute, sid_to_dict, path_to_dict, get_data_source, unfold_search, get_sidcache, sid_to_dicts]
    for f in cached_functions:
        f.cache_clear()


if __name__ == '__main__':

    reload_lru_caches()
