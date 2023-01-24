# -*- coding: utf-8 -*-
"""
Example File System resolver config_name.
"""
from collections import OrderedDict
from sid_conf import shot_tasks, shot_sub_tasks, asset_tasks, asset_sub_tasks

path_templates = OrderedDict([

    ('project_root',            r'V:'),

    # type asset
    ('asset__file',             r'{@project_root}/{project}/3_PROD/32_3D/{type:321_ASSETS}/{cat_long}/{name}/{state}/{task}/{soft:MAYA}/{cat}_{name}_{task}_{state}_{version}.{ext:scenes}'),
    ('asset__movie_file',       r'{@project_root}/{project}/3_PROD/32_3D/{type:321_ASSETS}/{cat_long}/{name}/{state}/{task}/{soft:MAYA}/OUTPUT/{cat}_{name}_{task}_{state}_{version}.{ext:movies}'),
    ('asset__cache_file',       r'{@project_root}/{project}/3_PROD/32_3D/{type:321_ASSETS}/{cat_long}/{name}/{state}/{task}/{soft:MAYA}/OUTPUT/{cat}_{name}_{task}_{state}_{version}.{ext:caches}'),
    ('asset__spp_file',         r'{@project_root}/{project}/3_PROD/32_3D/{type:321_ASSETS}/{cat_long}/{name}/{state}/{task}/{sppsoft:SUBSTANCE}/{cat}_{name}_{task}_{state}_{version}.{ext:spp}'),
    ('asset__zprj_file',        r'{@project_root}/{project}/3_PROD/32_3D/{type:321_ASSETS}/{cat_long}/{name}/{state}/{task}/{marvsoft:MARVELOUS}/{cat}_{name}_{task}_{state}_{version}.{ext:zprj}'),

    ('asset__task',             r'{@project_root}/{project}/3_PROD/32_3D/{type:321_ASSETS}/{cat_long}/{name}/{state}/{task}'),
    ('asset__state',            r'{@project_root}/{project}/3_PROD/32_3D/{type:321_ASSETS}/{cat_long}/{name}/{state}'),
    ('asset__name',             r'{@project_root}/{project}/3_PROD/32_3D/{type:321_ASSETS}/{cat_long}/{name}'),
    ('asset__cat',              r'{@project_root}/{project}/3_PROD/32_3D/{type:321_ASSETS}/{cat_long}'),

    ('asset',                   r'{@project_root}/{project}/3_PROD/32_3D/{type:321_ASSETS}'),

    # type shot
    ('shot__file',             r'{@project_root}/{project}/3_PROD/32_3D/{type:322_SEQUENCES}/{seq}/{seq}_{shot}/{state}/{task}/{soft:MAYA}/{seq}_{shot}_{task}_{state}_{version}.{ext:scenes}'),
    ('shot__movie_file',       r'{@project_root}/{project}/3_PROD/32_3D/{type:322_SEQUENCES}/{seq}/{seq}_{shot}/{state}/{task}/{soft:MAYA}/EXPORT/{seq}_{shot}_{task}_{state}_{version}.{ext:movies}'),
    ('shot__zprj_file',        r'{@project_root}/{project}/3_PROD/32_3D/{type:322_SEQUENCES}/{seq}/{seq}_{shot}/{state}/{task}/{marvsoft:MARVELOUS}/{seq}_{shot}_{task}_{state}_{version}.{ext:zprj}'),
    ('shot__comp_file',        r'{@project_root}/{project}/4_POSTPROD/{type:43_COMPO}/{seq}/{seq}_{shot}/{task:COMP}/{seq}_{shot}_{task:COMP}_{version}.{ext:nk}'),
    #                             "V:   \FTRACK_ONLINE_TEST\4_POSTPROD\43_COMPO      \SQ0001\SQ0001_SH0002\COMP   \SQ0001_SH0030_COMP_V003.nk"
    ('shot__comp_task',        r'{@project_root}/{project}/4_POSTPROD/{type:43_COMPO}/{seq}/{seq}_{shot}/{task:COMP}'),

    ('shot__data',          r'{@project_root}/{project}/3_PROD/32_3D/{type:322_SEQUENCES}/{seq}/{seq}_{shot}/OK/DATA/{data:datas}/{seq}_{shot}_{data:datas}.json'),
    # V:\FTRACK_ONLINE_TEST\3_PROD\32_3D\322_SEQUENCES\SQ1000\SQ1000_SH0010\OK\DATA\CASTING\SQ1000_SH0010_CASTING.json

    ('shot__cache_file',       r'{@project_root}/{project}/3_PROD/32_3D/{type:322_SEQUENCES}/{seq}/{seq}_{shot}/{state}/{task}/{soft:MAYA}/EXPORT/{seq}_{shot}_{node}_{state}_{version}.{ext:caches}'),
    ('shot__cache_unversioned_file',       r'{@project_root}/{project}/3_PROD/32_3D/{type:322_SEQUENCES}/{seq}/{seq}_{shot}/{state}/{task}/{soft:MAYA}/EXPORT/{subfolder}/{node}.{ext:caches}'),
    # V:\CRASH_BANDICOOT_MOBILE\3_PROD\32_3D\322_SEQUENCES\SQ0001\SQ0001_SH0020\WIP\ANI\MAYA\EXPORT\ALEMBIC\CHR_CRASH_ABC_1.abc         # unversioned shot cache, node : CHR_CRASH_ABC_1
    # V:\CRASH_BANDICOOT_MOBILE\3_PROD\32_3D\322_SEQUENCES\SQ0001\SQ0001_SH0020\WIP\ANI\MAYA\EXPORT\SQ0001_SH0020_CAM_WIP_V019.abc      # versioned shot cache, node : CAM

    ('shot__task',             r'{@project_root}/{project}/3_PROD/32_3D/{type:322_SEQUENCES}/{seq}/{seq}_{shot}/{state}/{task}'),
    ('shot__state',            r'{@project_root}/{project}/3_PROD/32_3D/{type:322_SEQUENCES}/{seq}/{seq}_{shot}/{state}'),
    ('shot__shot',             r'{@project_root}/{project}/3_PROD/32_3D/{type:322_SEQUENCES}/{seq}/{seq}_{shot}'),
    ('shot__seq',              r'{@project_root}/{project}/3_PROD/32_3D/{type:322_SEQUENCES}/{seq}'),
    ('shot',                   r'{@project_root}/{project}/3_PROD/32_3D/{type:322_SEQUENCES}'),

    # type render
    ('render__aov_file',       r'{@project_root}/{project}/4_POSTPROD/{type:42_OUT_3D}/{seq}/{seq}_{shot}/{seq}_{shot}_RND_WIP_{version}/{layer}/{layer}.{aov}.{frame}.{ext:images}'),
    ('render__file',           r'{@project_root}/{project}/4_POSTPROD/{type:42_OUT_3D}/{seq}/{seq}_{shot}/{seq}_{shot}_RND_WIP_{version}/{layer}/{layer}.{frame}.{ext:images}'),
    ('render__layer',          r'{@project_root}/{project}/4_POSTPROD/{type:42_OUT_3D}/{seq}/{seq}_{shot}/{seq}_{shot}_RND_WIP_{version}/{layer}'),
    # ('render__state',        r'{@project_root}/{project}/4_POSTPROD/{type:42_OUT_3D}/{seq}/{seq}_{shot}/{seq}_{shot}_{task}_{state}_{version}'),  # no folder
    ('render__version',        r'{@project_root}/{project}/4_POSTPROD/{type:42_OUT_3D}/{seq}/{seq}_{shot}/{seq}_{shot}_RND_WIP_{version}'),
    # ('render__task',         r'{@project_root}/{project}/4_POSTPROD/{type:42_OUT_3D}/{seq}/{seq}_{shot}/{task}'),  # no folder
    ('render__shot',           r'{@project_root}/{project}/4_POSTPROD/{type:42_OUT_3D}/{seq}/{seq}_{shot}'),
    ('render__seq',            r'{@project_root}/{project}/4_POSTPROD/{type:42_OUT_3D}/{seq}'),
    ('render',                 r'{@project_root}/{project}/4_POSTPROD/{type:42_OUT_3D}'),

    # type project
    ('project',                r'{@project_root}/{project}'),

])

path_templates_reference = 'project_root'

path_defaults = {

    'soft': 'MAYA',
    'sppsoft': 'SUBSTANCE',  # these needed ? Try hardcode in fs paths.
    'marvsoft': 'MARVELOUS',
    'state': 'WIP',
    'subfolder': 'ALEMBIC',
    'aov': 'Beauty'
    # 'frame': '#'  # does not need to be part of the sid, but may be needed for path creation
}
# path_new_keys
sidkeys_to_extrakeys = {
    'cat': {
            'cat_long': {
                'CHR': '3211_CHR',
                'SET': '3212_SET',
                'PRP': '3213_PRP',
                '*': '*',  # needed for search
            },
        },
}

extrakeys_to_sidkeys = {

    'cat_long': {
        'cat': {
            '3211_CHR': 'CHR',
            '3212_SET': 'SET',
            '3213_PRP': 'PRP',
            '*': '*',  # needed for search
        },
    },
}


path_mapping = {  # TODO put into project_conf

    'project': {            # 3 words : initials, otherwise 6 first letters, lowercased
        'FTRACK_ONLINE_TEST': 'FTOT',
        'CBM': 'CBM',
        'FFM': 'FFM',
        'NPC': 'NPC',
        'PIKKO_DEV': 'PIK',
    },
    'type': OrderedDict([        # the resolver gets the key by value - if the value exists multiple times, the first one is returned.
        ('321_ASSETS', 'A'),
        ('322_SEQUENCES', 'S'),
        ('42_OUT_3D', 'R')
    ]),

    # Specific path mapping
    ('type', 'shot__comp_file'): {
        '43_COMPO': 'S',
    },
    ('type', 'shot__comp_task'): {
        '43_COMPO': 'S',
    },
}

search_path_mapping = {
    # '/3d/scenes/': '/*/scenes/',
}

asset_cats = ['CHR', 'SET', 'PRP']

extensions_scene = ['ma', 'mb', 'hip', 'py']  # only real file extensions, not aliases
extensions_compo = ['nk']
extensions_cache = ['abc', 'json', 'fur', 'grm', 'vdb', 'fbx']
extensions_image = ['jpg', 'png', 'exr', 'dpx']
extensions_movie = ['mp4', 'mov', 'avi']

datas = ['CASTING', 'FRAMERANGE']

project_path_names = list(path_mapping.get('project').keys())

key_patterns = {

    '__': {
        '{state}':   r'{state:(WIP|OK|\*|\>)}',     # "w" or "p" or *
        '{version}': r'{version:(V\d\d\d|\*|\>)}',  # "V" followed by 3 digits, or *
        '{seq}':     r'{seq:(SQ\w*|\*|\>)}',      # "sq" followed by a word, or *
        '{shot}':    r'{shot:(SH\w*|\*|\>)}',      # "sh" followed by a word, or *
        '{frame}':   r'{frame:(\*|\$\w*|#*|@*|[0-9]*)}',  # r'{frame:(\*|\$\w*|#*|@*|0101)}',  # number, or "$" followed by a word, or "#"s, or "@"s, or *

        '{ext:scenes}': r'{ext:(' + '|'.join(extensions_scene) + r'|\*|\>)}',
        '{ext:caches}': r'{ext:(' + '|'.join(extensions_cache) + r'|\*|\>)}',
        '{ext:images}': r'{ext:(' + '|'.join(extensions_image) + r'|\*|\>)}',
        '{ext:movies}': r'{ext:(' + '|'.join(extensions_movie) + r'|\*|\>)}',
        '{ext:nk}':     r'{ext:(' + '|'.join(extensions_compo) + r'|\*|\>)}',
        '{ext:spp}':    r'{ext:(' + '|'.join(['spp']) + r'|\*|\>)}',
        '{ext:zprj}':    r'{ext:(' + '|'.join(['zprj']) + r'|\*|\>)}',
        '{data:datas}': r'{data:(' + '|'.join(datas) + r'|\*|\>)}',
    },

    'asset__': {
        '{task}': r'{task:(' + '|'.join(asset_tasks) + '|' + '|'.join(asset_sub_tasks) + r'|\*|\>)}',
    },

    'shot__': {
         '{task}': r'{task:(' + '|'.join(shot_tasks) + '|' + '|'.join(shot_sub_tasks) + r'|\*|\>)}',
    },
    't': {  # everything containing a "t" (asset, shot, project...)
        '{project}': r'{project:(' + '|'.join(project_path_names) + r'|\*\>)}',
        '{type:322_SEQUENCES}': r'{type:(322_SEQUENCES|\*\>)}',
        '{type:321_ASSETS}': r'{type:(321_ASSETS|\*\>)}',
        '{type:43_COMPO}': r'{type:(43_COMPO|\*\>)}',
    },
    'render': {
        '{project}': r'{project:(' + '|'.join(project_path_names) + r'|\*\>)}',
        '{task}': r'{task:(' + '|'.join(shot_tasks) + '|' + '|'.join(shot_sub_tasks) + r'|\*|\>)}',
        '{type:42_OUT_3D}': r'{type:(42_OUT_3D|\*\>)}',
    },
}


if __name__ == '__main__':

    from pprint import pprint

    pprint(globals())

    for key in path_templates:
        print(path_templates.get(key))
