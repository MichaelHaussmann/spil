"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations

# import traceback


class SpilException(Exception):
    """
    A SpilException.

    This SpilException should always be raised and handled inside this Spil package.
    """

    def __init__(self, *args, **kwargs):
        self.message = str(args[0])

    def __str__(self):
        return f"[SpilException] {self.message}"


def raiser(exception: str | Exception):
    """
    Utility function to raise errors after an "or".

    Examples:

        ... print(0 or raiser('Null value'))
        ... print(0 or raiser(ValueError('null value')))

    Inspired by https://mail.python.org/pipermail/python-ideas/2014-November/029921.html


    Args:
        exception: in case of a string, raises a SpilException

    Returns:
        raises the given exception or a SpilException
    """
    if isinstance(exception, Exception):
        raise exception
    else:
        raise SpilException(str(exception))


if __name__ == "__main__":

    try:
        try:
            raise Exception("foo")
        except Exception as ex:
            raise SpilException(ex)

    except SpilException as pe:

        print("caught : ", pe)
