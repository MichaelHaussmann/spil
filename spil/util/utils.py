"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2024 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""

def uniqfy(seq, reverse=False):
    """
    Returns a list with unique items, preserving order.
    
    If optional "reverse", the last duplicated item is kept. 
    (back is not optimized)

    (used by spil_ui)
    
    http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
    http://www.peterbe.com/plog/uniqifiers-benchmark
    
    @author Markus Jarderot
    """
    # return list(dict.fromkeys(seq))  #  This will work in Python >=3.6 and preserve order
    seen = set()
    seen_add = seen.add
    if reverse:
        result = []
        [result.insert(0, x) for x in reversed(seq) if not (x in seen or seen_add(x))]
        return result
    else:
        return [x for x in seq if not (x in seen or seen_add(x))]


def get_key(adict, value, default=None):
    """
    Gets a dict key by the value.

    If a value exists multiple times:
        If the dictionary is ordered, returns the first key.
        Otherwise key is returned "randomly".
    """
    try:
        index = list(adict.values()).index(value)
    except ValueError:
        return default

    result = list(adict.keys())[index]

    return result


if __name__ == '__main__':
    
    # print( is_sequence('toto') )
    #
    # print( uniqfy(['a', 'b', 'c', 'a', 'c', 'd']) )
    #
    # print( is_filename('folder/02_260_0200-animation_export-setDressing.json') )
    # print( is_filename('folder') )
    # print( is_filename('test/toto.json') )

    _dict = {'name': 'Doe',
             'first_name': 'John',
             'middle_name': 'John'}
    print(get_key(_dict, 'John'))


