# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""

from collections import OrderedDict

searches = OrderedDict()

# star search
searches['raj/s/sq001/*'] = 'All shots of Sequence sq001'

# double star search
searches['raj/s/sq001/sh0020/**/avi'] = 'All avi files of shot sq001/sh0020'
searches['raj/s/sq001/sh0020/**/p/avi'] = 'All p avi files of shot sq001/sh0020'
searches['raj/s/**/p/ma'] = 'All published (p) maya files in shots'

# sorted search
searches['raj/s/sq001/^'] = 'Last shot of Sequence sq001'
searches['raj/s/sq001/*/^'] = 'Last task for all shots of Sequence sq001'
searches['raj/s/sq001/sh0010/layout/*/^/w/ma'] = 'Maya file for last work version of layout'
searches['raj/s/sq001/sh0010/animation/*/^/*/mov'] = 'Mov file for last version of Animation'
searches['raj/s/sq001/sh0020/**/^/p/avi'] = 'All last published (p) avi files of shot sq001/sh0020'
searches['raj/s/sq001/**/^/^/p/avi'] = 'Last published (p) avi files from last task, for all shots of sq001'

searches['raj/a/*'] = 'All asset categories'
searches['raj/a/prop/*'] = 'All props'
searches['raj/a/prop/*/*/^'] = 'Last task of all props'
searches['raj/a/prop/*/*/*'] = 'All tasks of all props'
searches['raj/a/char/romeo/low/**'] = 'Everything under romeo low'

# "or" (comma separated values) in search
searches['raj/a/char,prop/*'] = 'All characters and props'

# extension alias in search ("movie" is an alias for avi, mp4, mov)
searches['raj/a/char/romeo/main/surfacing/**/movie'] = 'All romeo main surfacing movie files ("movie" alias)'

# mixed features
searches['raj/s/sq001,sq002/sh0050/animation/**/maya'] = 'All H.....'
searches['raj/s/sq001,sq002/sh0050/animation/*/*/*/maya'] = 'All H.....'
searches['raj/s/sq001,sq002/sh0050/animation/*/^/p/maya'] = 'Last published (p) maya file for animation of shot 10 in sq 1 and 2'

searches['raj/a/location/?/**/maya'] = 'All sets that have maya files'
searches['raj/a/prop/?/**/hip'] = 'All props that have hip files'

# currently not working - looks like sorted and double star do not work
searches['raj/s/sq001/sh0020/**/^/p/avi'] = 'All last published (p) avi files of shot sq001/sh0020'
searches['raj/s/sq001,sq002/sh0010/^/**/maya'] = 'Last task for ...'