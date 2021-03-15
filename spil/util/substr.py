"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.


"""


class SubStr(str):
    """
    A string that knows substraction ... 
    """
    
    def __sub__(self, other):
        """
        "Substracts" - meaning removes from the right outer part - other from self. 
        """
        try:
            if other:
                return SubStr( ''.join(self.rsplit(str(other),1)) )
            else:
                return self
        except Exception as ex:
            print('so you really believed string substraction could work ? ',)
            print(ex)
            return self
        
        
if __name__ == '__main__':

    # definitions
    a = 'anything'
    x = 'any other string'
    y = 'not the end of a'
    assert(SubStr(a + x) - x == a)      # a + x - x == a
    assert(SubStr(a) - a == '')         # a - a = ''
    if not a.endswith(y):
        assert(SubStr(a) - y == a)

    s = SubStr('hello you')
    print( s - 'me' )
    print( s - 'you' )
    print( s - '' )
    print( s - None )
    print( 's - s : ', s - s )
    print( 's-s-"you" : ', s - s - 'you' )