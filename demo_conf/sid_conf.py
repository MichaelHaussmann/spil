# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2022 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
from collections import OrderedDict

"""
Example Sid resolver config

TODO:
- include sub version granularity level (namespace/slot/node)
- implement frames

"""

sip = '/'  # sid separator  # FIXME: not properly used yet
sid_templates = OrderedDict([

    # type asset
    ('asset__work_scene',       '{project}/{type:a}/{assettype}/{asset}/{tasktype}/{task}/{state:w}/{version}/{ext:scenes}'),
    ('asset__publish_scene',    '{project}/{type:a}/{assettype}/{asset}/{tasktype}/{task}/{state:p}/{version}/{name}/{ext:scenes}'),

    # Unnamed ('asset__publish_file',    '{project}/{type:a}/{assettype}/{asset}/{tasktype}/{task}/{state:p}/{version}/{name}/{ext:scenes}'),
    # ('asset__work_cache',        '{project}/{type:a}/{assettype}/{asset}/{tasktype}/{task}/{state:w}/{version}/{ext:scenes}'),
    ('asset__publish_cache',     '{project}/{type:a}/{assettype}/{asset}/{tasktype}/{task}/{state:p}/{version}/{name}/{ext:caches}'),
    ('asset__publish_movie',     '{project}/{type:a}/{assettype}/{asset}/{tasktype}/{task}/{state:p}/{version}/{name}/{ext:movies}'),

    ('asset',                     '{project}/{type:a}'),

    # type shot
    ('shot__work_scene',         '{project}/{type:s}/{sequence}/{shot}/{tasktype}/{task}/{state:w}/{version}/{ext:scenes}'),
    ('shot__publish_scene',      '{project}/{type:s}/{sequence}/{shot}/{tasktype}/{task}/{state:p}/{version}/{name}/{ext:scenes}'),
    ('shot__publish_cache',      '{project}/{type:s}/{sequence}/{shot}/{tasktype}/{task}/{state:p}/{version}/{name}/{ext:caches}'),
    ('shot__publish_movie',      '{project}/{type:s}/{sequence}/{shot}/{tasktype}/{task}/{state:p}/{version}/{name}/{ext:movies}'),

    ('shot',                     '{project}/{type:s}'),

    # type project
    ('project',                 '{project}'),

])

to_extrapolate = ['asset__work_scene', 'shot__work_scene']
extrapolation_leaf_subtype = 'work_scene'

projects = ['tp']  # A project code.
asset_tasks = ['concept', 'modeling', 'surfacing', 'rigging', 'texturing']
shot_tasks = ['storyboard', 'layout', 'animation', 'fx', 'lighting', 'compositing']
asset_types = ['characters', 'environment', 'props', 'fx']

extensions_scene = ['ma', 'mb', 'hip', 'blend', 'hou', 'maya', 'nk']
extensions_cache = ['abc', 'json', 'fur', 'grm', 'vdb', 'cache']
# extensions_image = ['jpg', 'png', 'exr', 'dpx', 'img']
extensions_movie = ['mp4', 'mov', 'avi', 'movie']

extension_alias = {
#     'img': extensions_image,
    'cache': extensions_cache,
    'hou': ['hip', 'hipnc'],
    'maya': ['ma', 'mb'],
    'movie': extensions_movie
}

key_patterns = {

    '__': {
        '{state}':   r'{state:(w|p|\*|\>)}',     # "w" or "p" or *
        '{state:w}':  r'{state:(w|\*|\>)}',     # "w" or "p" or *
        '{state:p}':  r'{state:(p|\*|\>)}',     # "w" or "p" or *
        '{version}': r'{version:(v\d\d\d|\*|\>)}',  # "V" followed by 3 digits, or *
        '{seq}':     r'{seq:(s\d\d|\*|\>)}',      # "s" followed by 2 digits, or *  # !!!: do not use r'{2}', error with lucidity
        '{shot}':    r'{shot:(p\d\d\d|\*|\>)}',      # "p" followed by 3 digits, or *  # !!!: do not use r'{3}', error with lucidity
        #'{frame}':   r'{frame:(\*|\$\w*|#*|@*|[0-9]*)}',  # number, or "$" followed by a word, or "#"s, or "@"s, or *

        '{ext:scenes}': r'{ext:(' + '|'.join(extensions_scene) + r'|\*|\>)}',
        '{ext:caches}': r'{ext:(' + '|'.join(extensions_cache) + r'|\*|\>)}',
        #'{ext:images}': r'{ext:(' + '|'.join(extensions_image) + r'|\*|\>)}',
        '{ext:movies}': r'{ext:(' + '|'.join(extensions_movie) + r'|\*|\>)}',
    },

    'asset__': {
        '{tasktype}': r'{tasktype:(' + '|'.join(asset_tasks) + r'|\*|\>)}',
        '{assettype}': r'{assettype:(' + '|'.join(asset_types) + r'|\*|\>)}',
        #'{name}': r'{name:([a-z0-9]+|\*|\?|\>)}',  # lowercase word or number, with at least one character
    },
    'shot__': {
        '{tasktype}': r'{tasktype:(' + '|'.join(shot_tasks) + r'|\*|\>)}',
    },
    't': {  # everything   containing a "t" (asset, shot, project...) # FIXME
        '{project}': r'{project:(' + '|'.join(projects) + r'|\*|\>)}',
        '{type:a}': r'{type:(a|\*|\>)}',
        '{type:s}': r'{type:(s|\*|\>)}',
    },
}

# These keytypes are used by the resolver to sort the keys
key_types = {
    'asset': ['project', 'type', 'assettype', 'asset', 'tasktype', 'task', 'state', 'version', 'name', 'ext'],
    'shot': ['project', 'type', 'sequence', 'shot', 'tasktype', 'task', 'state', 'version', 'name', 'ext'],
    'project': ['project'],
}
# '{project}/{type:a}/{assettype}/{asset}/{tasktype}/{task}/{state:p}/{version}/{name}/{ext:scenes}'),
# '{project}/{type:s}/{sequence}/{shot}/{tasktype}/{task}/{state:p}/{version}/{name}/{ext:scenes}'),
# I recommand having versioned published (using version mapping between work and publish) and the state after the version.

# These keytypes are used during "extrapolation"
# Extrapolation is filling intermediate types from leave ("file") types
extrapolate_types = {
    'asset': ['project', 'type', 'assettype', 'asset', 'tasktype', 'task', 'state', 'version', 'ext'],
    'shot': ['project', 'type', 'sequence', 'shot', 'tasktype', 'task', 'state', 'version', 'ext'],
    'project': ['project'],
}

if __name__ == '__main__':

    from pprint import pprint

    pprint(globals())
