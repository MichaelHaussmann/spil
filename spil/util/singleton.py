"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

@author: michael.haussmann
"""


class Singleton(object):

    instances = {}

    def __new__(cls, *args, **kwargs):
        if Singleton.instances.get(cls) is None:
            Singleton.instances[cls] = object.__new__(cls, *args, **kwargs)
        return Singleton.instances[cls]


if __name__ == '__main__':

    class Person(Singleton):
        pass

    john = Person()
    jane = Person()

    assert(john is jane)

    print(john)
    print(jane)

