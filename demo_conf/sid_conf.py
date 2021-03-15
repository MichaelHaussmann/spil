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

"""
Example Sid resolver config

TODO:
- include sub version granularity level (namespace/slot/node)
- implement frames

"""

sip = '/'  # sid separator  # FIXME: not properly used yet
sid_templates = OrderedDict([

    # type asset
    ('asset__file',            '{project}/{type:a}/{cat}/{name}/{variant}/{task}/{version}/{state}/{ext:scenes}'),
    ('asset__movie_file',      '{project}/{type:a}/{cat}/{name}/{variant}/{task}/{version}/{state}/{ext:movies}'),

    ('asset',                  '{project}/{type:a}'),

    # type shot
    ('shot__file',             '{project}/{type:s}/{seq}/{shot}/{task}/{subtask}/{version}/{state}/{ext:scenes}'),
    ('shot__movie_file',       '{project}/{type:s}/{seq}/{shot}/{task}/{subtask}/{version}/{state}/{ext:movies}'),

    ('shot',                    '{project}/{type:s}'),

    # type project
    ('project',                 '{project}'),

])

projects = ['raj']  # A project code. Example for a "Romeo And Juliet" project.
asset_tasks = ['design', 'modeling', 'setup', 'surfacing', 'groom']
shot_tasks = ['animatic', 'layout', 'animation', 'render', 'fx']
asset_cats = ['char', 'location', 'prop', 'dmp', 'fx']

extensions_scene = ['ma', 'mb', 'hip', 'py', 'hou', 'maya', 'nk']
extensions_cache = ['abc', 'json', 'fur', 'grm', 'vdb', 'cache']
extensions_image = ['jpg', 'png', 'exr', 'dpx', 'img']
extensions_movie = ['mp4', 'mov', 'avi', 'movie']

extension_alias = {
    'img': extensions_image,
    'cache': extensions_cache,
    'hou': ['hip', 'hipnc'],
    'maya': ['ma', 'mb'],
    'movie': extensions_movie
}


key_patterns = {

    '__': {
        '{state}':   r'{state:(w|p|\*|\^)}',     # "w" or "p" or *
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
        '{cat}': r'{cat:(' + '|'.join(asset_cats) + '|\*|\^)}',
    },

    'shot__': {
        '{task}': r'{task:(' + '|'.join(shot_tasks) + '|\*|\^)}',
    },

    't': {  # everything
        '{project}': r'{project:(' + '|'.join(projects) + '|\*|\^)}',
    }

}


# sid types
key_types = {  # FIXME: this is redundant
    'asset': ['project', 'type', 'cat', 'name', 'variant', 'task', 'version', 'state', 'ext'],
    'shot': ['project', 'type', 'seq', 'shot', 'task', 'subtask', 'version', 'state', 'ext'],
    'project': ['project'],
}


if __name__ == '__main__':

    from pprint import pprint

    pprint(globals())
