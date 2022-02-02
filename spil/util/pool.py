"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2022 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

@author: michael.haussmann
"""

from spil.util.log import debug


class Pooled(object):  #TODO Test Py2
    """
    A Singleton guarantees one single instance of a same class.
    Pooled guarantees one single instance of a same class if they have the same init arguments.

    Example:
        SidCache class extends Pooled.
        a = SidCache('cache/file/A')
        a2 = SidCache('cache/file/A')
        b = SidCache('cache/file/B')
        a and a2 share the same argument, they get the same instance.
        b is a different instance.
    """

    instances = {}

    def __new__(cls, *args, **kwargs):

        key = tuple([cls]) + tuple(args)
        if Pooled.instances.get(key) is None:
            # Singleton.instances[cls] = object.__new__(cls, *args, **kwargs)
            Pooled.instances[key] = object.__new__(cls)
            debug('New Pooled instance of {}, total: {}'.format(cls, len(Pooled.instances.keys())))
            # debug('Pooled instances keys: {}'.format(Pooled.instances.keys()))

        return Pooled.instances[key]


if __name__ == '__main__':

    from spil.util.log import setLevel, DEBUG

    setLevel(DEBUG)

    class Person(Pooled):

        def __init__(self, name):
            self.name = name

        def __str__(self):
            return '[Person] : {} - {}'.format(self.name, id(self))

    class Woman(Pooled):

        def __init__(self, name):
            self.name = name

        def __str__(self):
            return '[Woman] : {} - {}'.format(self.name, id(self))

    john = Person('john')
    print(john)

    john2 = Person('john')
    print(john2)

    jane = Person('jane')
    print(jane)

    jane2 = Woman('jane')
    print(jane2)

    assert(john is john2)
    assert(john is not jane)
    assert(jane is not jane2)

