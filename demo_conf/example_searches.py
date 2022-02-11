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

searches = {}
searches['tp/s/*'] = 'sequences'
searches['tp/s/s01/*'] = 'shots'
searches['tp/s/s01/p020/*/*'] = 'tasks'
searches['tp/s/s01/p020/**/ma'] = ''
searches['tp/s/s01/p020/*/*/*/*/*/ma'] = 'shot__publish_scene'
searches['tp/s/s01/p020/*/*/*/*/ma'] = 'shot__work_scene'
searches['tp/s/s01/p020/fx/**/ma'] = 'fx tasktype'
searches['tp/s/**/maya'] = 'all maya'
searches['tp/s/**/cache'] = 'all caches'
# searches['tp/s/**/maya?state=p'] = 'all published maya'
# searches['tp/a/**/maya'] = 'all maya'

#searches = {}
searches['tp/a/*'] = 'asset types'
searches['tp/a/characters/*'] = 'chars'
searches['tp/a/characters/baobab/*/*'] = 'baobab tasks'
searches['tp/a/characters/baobab/*/*/*'] = 'baobab states'
searches['tp/a/characters/baobab/*/*/*/*/maya'] = 'baobab maya work scenes'
searches['tp/a/characters/baobab/**/maya'] = 'baobab all maya'
searches['tp/a/characters/baobab/**/cache'] = 'baobab all caches'
searches['tp/a/**/maya'] = 'all asset maya files'
searches['tp/a/**/vdb'] = 'all asset vdbs'
searches['tp/a/**/cache'] = 'all asset caches'
searches['tp/a/**/*'] = 'all asset files'
