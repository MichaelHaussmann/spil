# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations
from typing import Iterator, List, Set
from pprint import pformat

from spil import Finder, SpilException, Sid
from spil.sid.core.sid_resolver import dict_to_sid
from spil.util.utils import get_key

from spil_plugins.sg.connect_sg import get_sg
from spil_plugins.sg.utils import sid_format
from spil_sg_conf import field_mappings, type_mapping, value_mappings, defaults_by_basetype  # type: ignore

from spil.util.log import DEBUG, get_logger, INFO

log = get_logger("spil_sg")

"""
Notes: 

    # TODO: "search re-grouping"
    Currently, a search Sid is "unfolded" into a list of typed search Sids.
    Examples :

    hamlet/*/** -->
    [Sid("asset__file:hamlet/a/*/*/*/*/*/*"),
     Sid("shot__file:hamlet/s/*/*/*/*/*/*"),
     Sid("shot__cache_node_file:hamlet/s/*/*/*/*/*/*/*")]
    In many cases, like the above, Search Sid types are different,
    which leads naturally to multiple search calls to SG.

    "hamlet/*/**/maya" is unfolded to :
        [Sid("asset__file:hamlet/a/*/*/*/*/*/ma"),
         Sid("asset__file:hamlet/a/*/*/*/*/*/mb"),
         Sid("shot__file:hamlet/s/*/*/*/*/*/ma"),
         Sid("shot__file:hamlet/s/*/*/*/*/*/mb")]
    Sometimes, identical types repeat.
    This makes sense in glob searches, where the "or" operator does not exist.
    But in SG, it would make sense to re-group same type searches,
    and include variations (like the "or") in the search request.

"""


class FindInSG(Finder):
    """
    Finder Implementation for Shotgrid backend.
    Relies on the spil_sg_conf.
    """

    def __init__(self):
        self.sg = get_sg()  # TODO: handle connection pool while freeing resource when un needed.

    # TODO: implement type overrides
    def do_find(self, search_sids: List[Sid], as_sid: bool = True) -> Iterator[Sid] | Iterator[str]:
        """
        Yields Sids (if as_bool is True, the default) or strings (if as_bool is set to False),
        as found in Shotgrid by querying the given search_sids.

        Args:
            search_sids: A list of Typed Search Sids
            as_sid: If True (default) Sid objects are yielded, else Strings.

        Returns:
            Iterator over Sids or strings.
        """

        found: Set = set()

        if not search_sids:
            log.warning("Nothing Searchable. ")

        for search_sid in search_sids:
            for sid in self._sg_request(search_sid):
                if sid not in found:
                    found.add(sid)
                    if as_sid:
                        yield Sid(sid)
                    else:
                        yield sid

    def _sg_request(self, sid: Sid) -> Iterator[str]:
        """
        For a given typed search sid, retrieves the result be querying Shotgrid.

        Implementation steps:
        - Using "type_mapping" and "field_mapping", the Search Sid translates to SG type, filters and fields
        - The query (type, filters and fields) is send to the SG API, and the result is retrieved
        - Using "field_mapping" and "value_mapping" the results are translated back
        - the resulting dictionaries are resolved to Sid objects

        Args:
            sid: types search Sid

        Returns:
            generator over Sid strings
        """

        if not sid:
            raise SpilException(f'Sid "{sid}" is not typed, cannot search.')

        sid_type = sid.type
        sg_type = type_mapping.get(sid_type)
        if not sg_type:
            raise SpilException(
                f'This sid type "{sid_type}" cannot currently not be queried in SG directly. Use another Finder.'
            )

        field_mapping = field_mappings.get(sid_type)
        if not field_mapping:
            raise SpilException(
                f'Fields for sid type "{sid_type}" were not configured. Check the config.'
            )

        # building SG request filters
        filters = []
        for key, value in sid.fields.items():
            # print(f"Field {key} / {value}")
            # for every Sid field, we get the corresponding SG field
            field = get_key(field_mapping, key)
            if field:
                if value == "*":
                    sg_filter = [field, "is_not", None]
                else:
                    value_mapping = value_mappings.get(key, {})
                    # we set the value, or map the value
                    value = get_key(value_mapping, value) or value
                    sg_filter = [field, "is", value]
                filters.append(sg_filter)

        # SG request fields as configured
        fields = list(field_mapping.keys())

        # Memo:
        # fields = list(self.sg.schema_field_read('Shot').keys())  # all fields
        # order = [{'field_name': 'code', 'direction': 'asc'}, {},...]

        log.debug(sg_type)
        log.debug(pformat(filters))
        log.debug(pformat(fields))

        # lauch the find
        results = self.sg.find(sg_type, filters, fields)

        # looping over results, that are SG dicts
        for sg_dict in results:

            log.debug("*" * 20)
            log.debug(pformat(sg_dict))

            # getting a Sid dict with default values (or empty if no defaults configured)
            new_sid = defaults_by_basetype.get(sid.basetype, {})

            # transforming the SG dict in a Sid dict, for each key/value pair
            for key, value in sg_dict.items():

                # Mapping the key from SG to Sid
                key = field_mapping.get(key)
                if not key:
                    continue

                # Mapping or formatting the value from SG to Sid
                value_mapping = value_mappings.get(key, {})
                if value_mapping:
                    value = value_mapping.get(value)
                else:
                    value = sid_format(value)
                if not value:
                    continue

                # setting the key/value
                new_sid[key] = value

            # new Sid dict is done
            log.debug(new_sid)

            # Unless the dict is empty, we resolve to string sid and return.
            # TODO: create a Sid directly, instead of a Sid string. Evaluate what is faster.
            if new_sid:
                sid_string = dict_to_sid(new_sid, sid_type)
                log.debug(sid_string)
                if sid_string:
                    yield sid_string


if __name__ == "__main__":

    log.setLevel(INFO)

    search = "hamlet/a,s/*/*/*"

    finder = FindInSG()

    for f in finder.find(search):
        print(f)

    for f in finder.find(search):
        print(f)
