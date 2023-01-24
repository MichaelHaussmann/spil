# -*- coding: utf-8 -*-
"""

This is work in progress.

"""
from __future__ import annotations
from typing import Optional

from spil import Sid, Writer


class WriteToWriters(Writer):
    """
    Writes to different destinations, depending on the Sids type.
    Can write to multiple destinations, in given order.

    # TODO: implement transactions across destinations
    (a failure (False) in create could trigger previous deletes)
    """

    def create(self, sid: Sid | str, data: Optional[dict] = None) -> bool:
        # FIXME: this is a stub.
        return False
        destination = get_data_destination(sid)
        if destination:  # and hasattr(destination, 'create'):
            return destination.create(sid, data=data)


