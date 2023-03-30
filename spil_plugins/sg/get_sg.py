"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations
from typing import Iterator, Mapping, Any, List, overload, Optional, Callable, Set, Tuple
from typing_extensions import Literal
from pprint import pformat

from spil import Sid, SpilException
from spil import Getter
from spil.sid.core.sid_resolver import dict_to_sid
from spil.util.utils import get_key

from spil_plugins.sg.connect_sg import get_sg
from spil_plugins.sg.utils import sid_format
from spil_sg_conf import field_mappings, type_mapping, value_mappings, defaults_by_basetype  # type: ignore
from spil_sg_conf import data_mappings  # type: ignore

from spil.util.log import DEBUG, get_logger, INFO, WARN

log = get_logger("spil_sg")
log.setLevel(WARN)


class GetFromSG(Getter):
    """
    Getter from Shotgrid

    """

    def __init__(self):
        self.sg = get_sg()  # TODO: handle connection pool while freeing resource when un needed.

    def do_get(
        self,
        search_sids: List[Sid],
        attributes: Optional[List[str]] = None,
        sid_encode: Callable = str,
    ) -> Iterator[Mapping[str, Any]]:
        """
        For a given list of typed Search Sids, returns an Iterator over Mappings containing the retrieved data.
        One special field named "sid" contains the Sid.
        The Sid can be encoded by providing a callable to "sid_encode". Default is str.

        By default, attributes is None, retrieved data contains all configured data for the Sid type.
        If "attributes" is given, data contains only the key:value for the given attributes.

        The Sids returned by Getter.get() should be identical to those returned by Finder.find().
        Getter retrieves data related to these Sids, whereas the Finder finds only the existing Sids themselves.


        Args:
            search_sids: List of typed Sids for search
            attributes: Optional list of attributes to be retrieved
            sid_encode: Callable to format the returned Sid, as a value of key "sid".

        Returns:
            Iterator over Mappings containing the retrieved data.
            One special field named "sid" contains the Sid

        """
        found: Set = set()

        if not search_sids:
            log.warning("Nothing Searchable. ")

        for search_sid in search_sids:
            for sid, data in self._sg_request(search_sid, attributes=attributes):
                if sid not in found:
                    found.add(sid)
                    _sid = sid_encode(Sid(sid))
                    if _sid:
                        data["sid"] = _sid
                    yield data

    def _sg_request(
        self, sid: Sid, attributes: Optional[List[str]] = None
    ) -> Iterator[Tuple[str, dict]]:

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

        data_mapping = data_mappings.get(sid_type)
        if not data_mapping:
            log.warning(f'No Data Fields for sid type "{sid_type}" were configured.')

        # building SG request filters
        filters = []
        for key, value in sid.fields.items():
            # print(f"Field {key} / {value}")
            field = get_key(
                field_mapping, key
            )  # for every Sid field, we get the corresponding SG field
            if field:
                if value == "*":
                    sg_filter = [field, "is_not", None]
                else:
                    value_mapping = value_mappings.get(key, {})
                    value = (
                        get_key(value_mapping, value) or value
                    )  # we set the value, or map the value
                    sg_filter = [field, "is", value]
                filters.append(sg_filter)

        # SG request fields as configured
        # fields for the Sid
        fields = list(field_mapping.keys())

        # Fields for the data
        if attributes:
            data_fields = list(key for key, value in data_mapping.items() if value in attributes)
        else:
            data_fields = list(data_mapping.keys())

        # Memo:
        # fields = list(self.sg.schema_field_read('Shot').keys())  # all fields
        # order = [{'field_name': 'code', 'direction': 'asc'}, {},...]

        log.debug(f"sg_type: {sg_type}")
        log.debug(f"filters: {pformat(filters)}")
        log.debug(f"fields: {pformat(fields + data_fields)}")
        log.debug(f"data_fields: {data_fields}")

        # lauch the find
        results = self.sg.find(sg_type, filters, fields + data_fields)

        # looping over results, that are SG dicts
        for sg_dict in results:

            log.debug("*" * 20)
            log.debug(pformat(sg_dict))

            # getting a Sid dict with default values (or empty if no defaults configured)
            new_sid = defaults_by_basetype.get(sid.basetype, {})
            new_data = {}

            # transforming the SG dict in a Sid dict, for each key/value pair
            for key, value in sg_dict.items():

                # Getting data fields
                if key in data_fields:
                    sid_data_key = data_mapping.get(key)
                    new_data[sid_data_key] = value

                # Mapping the key from SG to Sid
                sid_key = field_mapping.get(key)
                if not sid_key:
                    continue

                # Mapping or formatting the value from SG to Sid
                value_mapping = value_mappings.get(sid_key, {})
                if value_mapping:
                    value = value_mapping.get(value)
                else:
                    value = sid_format(value)
                if not value:
                    continue

                # setting the key/value
                new_sid[sid_key] = value

            # new Sid dict is done
            log.debug(new_sid)

            # Unless the dict is empty, we resolve to string sid and return.
            # TODO: create a Sid directly.
            if new_sid:
                sid_string = dict_to_sid(new_sid, sid_type)
                # log.info(f"sid_string: {sid_string} ({new_sid})")
                if sid_string:
                    yield sid_string, new_data


if __name__ == "__main__":

    from pprint import pprint

    log.setLevel(INFO)

    getter = GetFromSG()

    print("Assets + shots")
    for f in getter.get("hamlet/a,s/*/*", sid_encode=lambda x: x.uri):
        pprint(f)

    print("Tasks")
    for f in getter.get("hamlet/a/char/ophelia/*"):
        pprint(f)

    print("Chars: status, note only")
    for f in getter.get("hamlet/a/char/*", attributes=["status", "note"]):
        pprint(f)

    print(getter.get_attr("hamlet/a/char/ophelia", "status"))
    print(getter.get_attr("hamlet/a/char/ophelia", "nada"))
    print(getter.get_attr("hamlet/a/char/jim", "status"))
