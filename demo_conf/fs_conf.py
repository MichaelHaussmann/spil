# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2022 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
"""
Example File System resolver config.
Maps file paths to Sid components.
The order is important, first match is returned.
#TODO : one root path per project
#IDEA config per project
"""

from collections import OrderedDict
from sid_conf import shot_tasks, asset_tasks, asset_types


###########################################################################################
# PATHS The order is important, first match is returned.
###########################################################################################

path_templates = OrderedDict([

    # ('project_root',            r'/home/mh/Desktop/SID_DEMO/projects'),
    ('project_root',            r'P:'),

    # type asset
    ('asset__work_scene',       r'{@project_root}/{project}/{type:assets}/{assettype}/{asset}/{tasktype}_{task}/{state:work}/' +
                                r'{project}_{assettype}_{asset}_{tasktype}_{task}_{state:work}_{version}.{ext:scenes}'),

    ('asset__publish_scene',    r'{@project_root}/{project}/{type:assets}/{assettype}/{asset}/{tasktype}_{task}/{state:publish}/{version}/{ext:scenes}/{name}/' +
                                r'{project}_{assettype}_{asset}_{tasktype}_{task}_{state:publish}_{version}_{name}.{ext:scenes}'),

    ('asset__publish_cache',    r'{@project_root}/{project}/{type:assets}/{assettype}/{asset}/{tasktype}_{task}/{state:publish}/{version}/{ext:caches}/{name}/' +
                                r'{project}_{assettype}_{asset}_{tasktype}_{task}_{state:publish}_{version}_{name}.{ext:caches}'),
    ('asset__publish_movie',    r'{@project_root}/{project}/{type:assets}/{assettype}/{asset}/{tasktype}_{task}/{state:publish}/{version}/{ext:movies}/{name}/' +
                                r'{project}_{assettype}_{asset}_{tasktype}_{task}_{state:publish}_{version}_{name}.{ext:movies}'),

    ('asset__state',            r'{@project_root}/{project}/{type:assets}/{assettype}/{asset}/{tasktype}_{task}/{state}'),
    ('asset__task',             r'{@project_root}/{project}/{type:assets}/{assettype}/{asset}/{tasktype}_{task}'),
    ('asset__asset',            r'{@project_root}/{project}/{type:assets}/{assettype}/{asset}'),
    ('asset__assettype',        r'{@project_root}/{project}/{type:assets}/{assettype}'),

    ('asset',                   r'{@project_root}/{project}/{type:assets}'),

    # type shot
    ('shot__work_scene',        r'{@project_root}/{project}/{type:shots}/{sequence}/{shot}/{tasktype}_{task}/{state:work}/' +
                                r'{project}_{sequence}_{shot}_{tasktype}_{task}_{state:work}_{version}.{ext:scenes}'),

    ('shot__publish_scene',     r'{@project_root}/{project}/{type:shots}/{sequence}/{shot}/{tasktype}_{task}/{state:publish}/{version}/{ext:scenes}/{name}/' +
                                r'{project}_{sequence}_{shot}_{tasktype}_{task}_{state:publish}_{version}_{name}.{ext:scenes}'),

    ('shot__publish_cache',     r'{@project_root}/{project}/{type:shots}/{sequence}/{shot}/{tasktype}_{task}/{state:publish}/{version}/{ext:caches}/{name}/' +
                                r'{project}_{sequence}_{shot}_{tasktype}_{task}_{state:publish}_{version}_{name}.{ext:caches}'),

    ('shot__publish_movie',     r'{@project_root}/{project}/{type:shots}/{sequence}/{shot}/{tasktype}_{task}/{state:publish}/{version}/{ext:movies}/{name}/' +
                                r'{project}_{sequence}_{shot}_{tasktype}_{task}_{state:publish}_{version}_{name}.{ext:movies}'),

    ('shot__state',             r'{@project_root}/{project}/{type:shots}/{sequence}/{shot}/{tasktype}_{task}/{state}'),
    ('shot__task',              r'{@project_root}/{project}/{type:shots}/{sequence}/{shot}/{tasktype}_{task}'),
    ('shot__shot',              r'{@project_root}/{project}/{type:shots}/{sequence}/{shot}'),
    ('shot__sequence',          r'{@project_root}/{project}/{type:shots}/{sequence}'),

    ('shot',                    r'{@project_root}/{project}/{type:shots}'),

    # type project
    ('project',                r'{@project_root}/{project}'),

])

path_templates_reference = 'project_root'

path_defaults = {

    'state': 'work',
    # 'frame': '#'  does not need to be part of the sid, but may be needed for path creation
}

# not needed here
sidkeys_to_extrakeys = {}

extrakeys_to_sidkeys = {}


path_mapping = {  # TODO put into project_conf

    'project': {
        'test_pipe': 'tp',
    },
    'state': {
        'work': 'w',
        'publish': 'p',
    },
    'type': OrderedDict([        # the resolver gets the key by value - if the value exists multiple times, the first one is returned.
        ('assets', 'a'),
        ('shots', 's'),
    ]),
}

search_path_mapping = {  # FIXME: useful ?
    # '/3d/scenes/': '/*/scenes/',
}

# asset_cats = ['CHR', 'SET', 'PRP']

extensions_scene = ['ma', 'mb', 'hip', 'py']  # only real file extensions, not aliases
extensions_cache = ['abc', 'json', 'fur', 'grm', 'vdb', 'fbx']
#extensions_image = ['jpg', 'png', 'exr', 'dpx']
extensions_movie = ['mp4', 'mov', 'avi']

project_path_names = list(path_mapping.get('project').keys())

key_patterns = {

    '__': {
        '{state}':   r'{state:(work|publish|\*|\>)}',     # "w" or "p" or *
        '{state:work}': r'{state:(work|\*|\>)}',  # "w" or "p" or *
        '{state:publish}': r'{state:(publish|\*|\>)}',  # "w" or "p" or *
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
        # '{name}': r'{name:([a-z0-9]+|\*|\?|\>)}',  # lowercase word or number, with at least one character
    },
    'shot__': {
        '{tasktype}': r'{tasktype:(' + '|'.join(shot_tasks) + r'|\*|\>)}',
    },
    't': {  # everything   containing a "t" (asset, shot, project...) # FIXME
        '{project}': r'{project:(' + '|'.join(project_path_names) + r'|\*|\>)}',
        '{type:assets}': r'{type:(assets|\*|\>)}',
        '{type:shots}': r'{type:(shots|\*|\>)}',
    },
}


if __name__ == '__main__':

    from pprint import pprint

    pprint(globals())

    for key in path_templates:
        print(path_templates.get(key))
