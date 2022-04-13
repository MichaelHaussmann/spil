# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
"""
Data config example for the Spil data framework.

For any given Sid, finds the Data Source that is to be used, and returns an instance or function.

Note: imports are in the function to avoid circular import limitations at boot.
"""


def get_data_source(sid):
    """
    Simplest possible implementation.
    Always returns the FS (FileSystem) as a data source
    """
    from spil import FS
    return FS()


def get_attribute_source(sid, attribute):
    """
    Simplest implementation.
    Returns a function that returns the attribute itself.

    :param attribute:
    :return:
    """

    def get_value(attribute):
        """
        Returns the attribute itself

        :param attribute:
        :return:
        """
        return attribute

    return get_value

