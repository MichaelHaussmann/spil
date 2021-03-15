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
This is currently not used. Sorting needs re-implementation.

"""


from spil.util.log import info
from spil.util import log

import six
if six.PY3:
    unicode = str

log.setLevel(log.INFO)


def compare_by_template(a, b, template=None):
    """
    Compares a and b as strings, first for equality, than using the template list.
    The one that comes first in the list is smaller.

    If no template list is given, or no match is achieved, string comparision is returned.

    Note that per default string comparision is case sensitive.

    If a == b, returns 0
    If a > b, returns 1
    If a < b, returns -1

    Examples:
    >>> compare_by_template(4, 2, [1, 2, 3, 4, 5])  # 4 is bigger than 2 in the ordered template
    1
    >>> compare_by_template(2, 4, [5, 4, 3, 2, 1])  # 2 is bigger than 4 in the reversed template
    1
    >>> compare_by_template('a', 'a', ['whatever'])  # identical
    0
    >>> compare_by_template('a', 'b', [1, 2, 3])  # not found in template: string comparision
    -1
    >>> compare_by_template('layout', 'animation', ['layout', 'animation', 'export', 'render'])  # 'animation' comes later (is bigger)
    -1
    >>> compare_by_template('layout', 'animation')  # by string comparision 'animation' comes first (is smaller)
    1
    >>> compare_by_template('layout', 'x-nonsense', ['layout', 'animation', 'render'])  # partially incompatible (one is not in list): string comparision
    -1

    :param a: string to compare
    :param b: string to compare
    :param template: list of strings
    :return:
    """
    if not a and b:
        return 0
    # debug('start {} - {}'.format(a, b))
    a = unicode(a)
    b = unicode(b)
    if a == b:
        return 0
    if not (a and b):
        return 1 if a > b else -1
    if template:
        template = [str(i) for i in template]
        if not set([a, b]) <= set(template):
            info('Not all of "{}" and "{}" are included in template "{}". Returning string order.'.format(a, b, str(template)))
            template = []
        for item in template:
            if item == a:
                return -1
            if item == b:
                return 1
        if template:
            info('Unable to order "{}" vs "{}" (using "{}"). Returning string order.'.format(a, b, template))
    return 1 if a > b else -1


if __name__ == '__main__':
    """
    Test block.
    Launches doc test (test in the doc).
    """
    from spil.util.log import setLevel, INFO

    setLevel(INFO)

    info('Tests start')

    import doctest
    # info(doctest)

    doctest.testmod()

    info('Tests done.')