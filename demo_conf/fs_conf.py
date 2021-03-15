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

from sid_conf import projects, asset_tasks, shot_tasks, asset_cats, extensions_scene, extensions_cache, extensions_image, extensions_movie

"""
Example File System resolver config.

Maps file paths to Sid components.


"""

###########################################################################################
# PATHS The order is important, first match is returned.
###########################################################################################

path_templates = OrderedDict([

    # ('project',                 r'/home/mh/Desktop/SID_DEMO/projects/{project}'),
    ('project_root',            r'/home/mh/Desktop/SID_DEMO/projects/{project}'),

    # type asset
    ('asset__file',             r'{@project_root}/{type:01_assets}/{cat_long}/{name}/{variant}/{task}/{state}_{version}/{name}.{ext:scenes}'),
    ('asset__movie_file',       r'{@project_root}/{type:01_assets}/{cat_long}/{name}/{variant}/{task}/{state}_{version}/{name}.{ext:movies}'),

    ('asset__state',          r'{@project_root}/{type:01_assets}/{cat_long}/{name}/{variant}/{task}/{state}_{version}'),
    # ('asset__version',            r'{@project_root}/{type:01_assets}/{cat_long}/{name}/{variant}/{task}/{}'),  # FIXME: should not exist as a folder

    ('asset__task',             r'{@project_root}/{type:01_assets}/{cat_long}/{name}/{variant}/{task}'),
    ('asset__variant',          r'{@project_root}/{type:01_assets}/{cat_long}/{name}/{variant}'),
    ('asset__name',             r'{@project_root}/{type:01_assets}/{cat_long}/{name}'),
    ('asset__cat',              r'{@project_root}/{type:01_assets}/{cat_long}'),

    ('asset',                   r'{@project_root}/{type:01_assets}'),

    # type shot
    ('shot__file',             r'{@project_root}/{type:02_shots}/{seq}/{seq}_{shot}/{task}/{subtask}/{state}_{version}/{seq}_{shot}.{ext:scenes}'),
    ('shot__movie_file',       r'{@project_root}/{type:02_shots}/{seq}/{seq}_{shot}/{task}/{subtask}/{state}_{version}/{seq}_{shot}.{ext:movies}'),

    ('shot__state',          r'{@project_root}/{type:02_shots}/{seq}/{seq}_{shot}/{task}/{subtask}/{state}_{version}'),
    #  ('shot__version',             r'{@project_root}/{type:02_shots}/{seq}/{seq}_{shot}/{task}/{subtask}/{}'),
    ('shot__subtask',          r'{@project_root}/{type:02_shots}/{seq}/{seq}_{shot}/{task}/{subtask}'),
    ('shot__task',             r'{@project_root}/{type:02_shots}/{seq}/{seq}_{shot}/{task}'),
    ('shot__shot',             r'{@project_root}/{type:02_shots}/{seq}/{seq}_{shot}'),
    ('shot__seq',              r'{@project_root}/{type:02_shots}/{seq}'),
    ('shot',                   r'{@project_root}/{type:02_shots}'),

    # type project
    ('project',                r'{@project_root}'),

])

path_templates_reference = 'project_root'

path_defaults = {

    'state': 'work',
    # 'frame': '#'  #  does not need to be part of the sid, but may be needed for path creation
}

# path_new_keys
sidkeys_to_extrakeys = {
    'cat': {
            'cat_long': {
                'char': '01_char',
                'location': '02_location',
                'prop': '03_prop',
                'fx': '04_fx',
                'dmp': '05_dmp',
                '*': '*',  # FIXME : needed for search ?
            },
        },
}

extrakeys_to_sidkeys = {  # FIXME: generate from above (redundant)

    'cat_long': {
        'cat': {
            '01_char': 'char',
            '02_location': 'location',
            '03_prop': 'prop',
            '04_fx': 'fx',
            '05_dmp': 'dmp',
            '*': '*',  # FIXME : needed for search ?
        },
    },
}


path_mapping = {  # TODO put into project_conf

    'project': {
        'ROMEO_AND_JULIET': 'raj',
    },
    'state': {
        'work': 'w',
        'publish': 'p',
        '*': '*',  # FIXME : needed for search
    },
    'type': {
        '01_assets': 'a',
        '02_shots': 's',
        '*': '*',  # FIXME : needed for search
    },
}

search_path_mapping = {
    # '/3d/scenes/': '/*/scenes/',
}

key_patterns = {

    '__': {
        '{state}':   r'{state:(work|publish|\*|\^)}',     # "work" or "publish" or *
        '{version}': r'{version:(v\w*|\*|\^)}',  # "v" followed by a word, or *
        '{seq}':     r'{seq:(sq\w*|\*|\^)}',      # "sq" followed by a word, or *
        '{shot}':    r'{shot:(sh\w*|\*|\^)}',      # "sh" followed by a word, or *
        # '{frame}':   r'{frame:(\*|\$\w*|#*|@*|[0-9]*)}',  # number, or "$" followed by a word, or "#"s, or "@"s, or *

        '{ext:scenes}': r'{ext:(' + '|'.join(extensions_scene) + '|\*|\^)}',
        '{ext:caches}': r'{ext:(' + '|'.join(extensions_cache) + '|\*|\^)}',
        '{ext:images}': r'{ext:(' + '|'.join(extensions_image) + '|\*|\^)}',
        '{ext:movies}': r'{ext:(' + '|'.join(extensions_movie) + '|\*|\^)}',
    },

    'asset__': {
        '{task}': r'{task:(' + '|'.join(asset_tasks) + '|\*|\^)}',
    },

    'shot__': {
        '{task}': r'{task:(' + '|'.join(shot_tasks) + '|\*|\^)}',
    }

}


if __name__ == '__main__':

    from pprint import pprint

    pprint(globals())

    for key in path_templates:
        print(path_templates.get(key))
