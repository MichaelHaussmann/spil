"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 20119 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.


"""


def is_filename(path):
    """
    if the given string ends with an extension, eg. a dot followed by 2 to 5 signs, we suppose it's a file name.

    :param path: path string
    :return:
    """
    return len(str(path).rsplit('.')) > 1 and 1 < len(str(path).rsplit('.')[-1]) < 6


def is_sequence(arg): 
    """
    Duck-typing-style sequence detection 
    
    @author Alex Martelli
    http://stackoverflow.com/questions/2937114/python-check-if-an-object-is-a-sequence 
    """
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))


def uniqfy(seq, reverse=False):
    """
    Returns a list with unique items, preserving order.
    
    If optional "reverse", the last duplicated item is kept. 
    (back is not optimized)
    
    http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
    http://www.peterbe.com/plog/uniqifiers-benchmark
    
    @author Markus Jarderot
    """
    
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
    (experimental - may misfunction for obvious reasons)

    Note : if a value exists multiple times, key is returned "randomly".
    """
    try:
        index = list(adict.values()).index(value)
    except ValueError:
        return default

    result = list(adict.keys())[index]

    return result


if __name__ == '__main__':
    
    print( is_sequence('toto') )
    
    print( uniqfy(['a', 'b', 'c', 'a', 'd']) )
    print( uniqfy(['a', 'b', 'c', 'a', 'd'], reverse=True) )

    print( is_filename('folder/02_260_0200-animation_export-setDressing.json') )
    print( is_filename('folder') )
    print( is_filename('test/toto.json') )

    _dict = {'name': 'Doe',
             'first_name': 'John',
             'middle_name': 'John'}
    print(get_key(_dict, 'John'))
