"""
write.Writer

create Sids
update Sids
delete Sids
set attributes

The idea is to register data destinations, objects implementing Writer.
Eg. WriteTo

Note: if a FindInCache Finder is used, FindInCache.create() should also be a registered data destination.

(TBD:
WriteToDestinations
WriteToRegistered
WriteToMultiple... )
"""
from __future__ import annotations

import shutil

from spil import Sid, SpilException
from spil import conf
from spil.util.log import debug
from pathlib import Path


class Writer:

    def create(self, sid: Sid | str, data: dict | None = None) -> bool:
        """
        Creates the given Sid, with given data.

        :param sid: Sid or str
        :param data: dictionary
        :return: True on Success, False on failure
        """
        pass


class WriteToDestinations(Writer):
    """
    Writes to different destinations, depending on the Sids type.
    Can write to multiple destinations, in given order.

    # TODO: implement transactions across destinations
    (a failure (False) in create could trigger previous deletes)
    """

    def create(self, sid: Sid | str, data: dict | None = None) -> bool:
        # FIXME: this is a stub.
        return
        destination = get_data_destination(sid)
        if destination:  # and hasattr(destination, 'create'):
            return destination.create(sid, data=data)


class WriteToPaths(Writer):

    def __init__(self, config: str | None):
        self.config = config or conf.default_path_config

    def _create_parent(self, path: Path) -> bool:

        if not path.parent.exists():
            path.parent.mkdir(parents=True)

        if path.parent.exists():
            return True

    def create(self, sid: Sid | str, data: dict | None = None) -> bool:

        _sid = Sid(sid)
        if not _sid.path(self.config):
            raise SpilException(f"Cannot Create: sid {sid} has no path.")

        path = _sid.path(self.config)
        if path.exists():
            raise SpilException(f"Cannot Create: path already exists for {sid}. Path: {path}.")

        suffix = path.suffix
        if suffix:
            debug(f"Path is a file: {path}")
            template = conf.create_file_using_template.get(suffix[1:])  # we remove the dot of the suffix
            if template:
                debug(f"Will be created by copying template: {template}")
                self._create_parent(path)
                shutil.copy2(template, path)
            elif conf.create_file_using_touch:
                debug(f"Will be created by touch. {path}")
                self._create_parent(path)
                path.touch()
            debug(f"File will not be created: {path}")

        else:
            debug(f"Path is a directory {path}")
            path.mkdir(parents=True)

        return path.exists()









