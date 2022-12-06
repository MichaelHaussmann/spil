# -*- coding: utf-8 -*-
"""
Example File System resolver config.
"""

from sid_conf import shot_tasks, asset_tasks, asset_types
from sid_conf import extensions_scene, extensions_movie, extensions_cache

path_templates = {

       # 'project_root':            '/home/mh/Desktop/SID_DEMO/projects',
    'project_root':            'P:',

    # type asset
    'asset__work_scene':       '{@project_root}/{project}/{type:assets}/{assettype}/{asset}/{tasktype}_{task}/{state:work}/' +
                                '{project}_{assettype}_{asset}_{tasktype}_{task}_{state:work}_{version}.{ext:scenes}',

    'asset__publish_scene':    '{@project_root}/{project}/{type:assets}/{assettype}/{asset}/{tasktype}_{task}/{state:publish}/{version}/{ext:scenes}/{name}/' +
                                '{project}_{assettype}_{asset}_{tasktype}_{task}_{state:publish}_{version}_{name}.{ext:scenes}',

    'asset__publish_cache':    '{@project_root}/{project}/{type:assets}/{assettype}/{asset}/{tasktype}_{task}/{state:publish}/{version}/{ext:caches}/{name}/' +
                                '{project}_{assettype}_{asset}_{tasktype}_{task}_{state:publish}_{version}_{name}.{ext:caches}',
    'asset__publish_movie':    '{@project_root}/{project}/{type:assets}/{assettype}/{asset}/{tasktype}_{task}/{state:publish}/{version}/{ext:movies}/{name}/' +
                                '{project}_{assettype}_{asset}_{tasktype}_{task}_{state:publish}_{version}_{name}.{ext:movies}',

    'asset__state':            '{@project_root}/{project}/{type:assets}/{assettype}/{asset}/{tasktype}_{task}/{state}',
    'asset__task':             '{@project_root}/{project}/{type:assets}/{assettype}/{asset}/{tasktype}_{task}',
    'asset__asset':            '{@project_root}/{project}/{type:assets}/{assettype}/{asset}',
    'asset__assettype':        '{@project_root}/{project}/{type:assets}/{assettype}',

    'asset':                   '{@project_root}/{project}/{type:assets}',

    # type shot
    'shot__work_scene':        '{@project_root}/{project}/{type:shots}/{sequence}/{shot}/{tasktype}_{task}/{state:work}/' +
                                '{project}_{sequence}_{shot}_{tasktype}_{task}_{state:work}_{version}.{ext:scenes}',

    'shot__publish_scene':     '{@project_root}/{project}/{type:shots}/{sequence}/{shot}/{tasktype}_{task}/{state:publish}/{version}/{ext:scenes}/{name}/' +
                                '{project}_{sequence}_{shot}_{tasktype}_{task}_{state:publish}_{version}_{name}.{ext:scenes}',

    'shot__publish_cache':     '{@project_root}/{project}/{type:shots}/{sequence}/{shot}/{tasktype}_{task}/{state:publish}/{version}/{ext:caches}/{name}/' +
                                '{project}_{sequence}_{shot}_{tasktype}_{task}_{state:publish}_{version}_{name}.{ext:caches}',

    'shot__publish_movie':     '{@project_root}/{project}/{type:shots}/{sequence}/{shot}/{tasktype}_{task}/{state:publish}/{version}/{ext:movies}/{name}/' +
                                '{project}_{sequence}_{shot}_{tasktype}_{task}_{state:publish}_{version}_{name}.{ext:movies}',

    'shot__state':             '{@project_root}/{project}/{type:shots}/{sequence}/{shot}/{tasktype}_{task}/{state}',
    'shot__task':              '{@project_root}/{project}/{type:shots}/{sequence}/{shot}/{tasktype}_{task}',
    'shot__shot':              '{@project_root}/{project}/{type:shots}/{sequence}/{shot}',
    'shot__sequence':          '{@project_root}/{project}/{type:shots}/{sequence}',

    'shot':                    '{@project_root}/{project}/{type:shots}',

    # type project
    'project':                 '{@project_root}/{project}',

}

path_templates_reference = 'project_root'

path_defaults = {

    'state': 'work',
    # 'frame': '#'  does not need to be part of the sid, but may be needed for path creation
}

# path_new_keys
sidkeys_to_extrakeys = {
    'project': {
        'project_short': {
            'M:/testpipe': 'testpipe',
            'N:/harvester': 'harvester',
            'O:/train': 'train',
            'P:/clocker': 'clocker',
            'Q:/firemen': 'firemen',
            'R:/kowloon': 'kowloon',
            'S:/rome': 'rome',
            'T:/icepick': 'icepick',
            'U:/noodles': 'noodles',
            'V:/silhouette': 'silhouette',
            'W:/brume': 'brume',
            'X:/kaiju': 'kaiju',
            'Y:/lumi': 'lumi',
            'Z:/heatwave': 'heatwave',
            '*': '*',  # needed for search
        },
    },
}

extrakeys_to_sidkeys = {
    'project_short': {
            'project': {
                'testpipe': 'tp',
                'harvester': 'harvester',
                'train': 'train',
                'clocker': 'clocker',
                'firemen': 'firemen',
                'kowloon': 'kowloon',
                'rome': 'rome',
                'icepick': 'icepick',
                'noodles': 'noodles',
                'silhouette': 'silhouette',
                'brume': 'brume',
                'kaiju': 'kaiju',
                'lumi': 'lumi',
                'heatwave': 'heatwave',
                '*': '*',  # needed for search
            },
        },
}

path_mapping = {  # TODO put into project_conf

    'project': {
        'M:/testpipe': 'tp',
        'N:/harvester': 'harvester',
        'O:/train': 'train',
        'P:/clocker': 'clocker',
        'Q:/firemen': 'firemen',
        'R:/kowloon': 'kowloon',
        'S:/rome': 'rome',
        'T:/icepick': 'icepick',
        'U:/noodles': 'noodles',
        'V:/silhouette': 'silhouette',
        'W:/brume': 'brume',
        'X:/kaiju': 'kaiju',
        'Y:/lumi': 'lumi',
        'Z:/heatwave': 'heatwave',
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

"""
    'testpipe': 'tp',
        'icepick': 'icepick',
        'silhouette': 'silhouette',
        'firemen': 'firemen',
"""

search_path_mapping = {  # FIXME: useful ?
    # '/3d/scenes/': '/*/scenes/',
}

project_path_names = list(path_mapping.get('project').keys())

key_patterns = {

    '__': {
        '{state}':   r'{state:(work|publish|\*|\>)}',       # "work" or "publish" or *
        '{state:work}': r'{state:(work|\*|\>)}',            # "work" or *
        '{state:publish}': r'{state:(publish|\*|\>)}',      # "publish" or *
        '{version}': r'{version:(v\d\d\d|\*|\>)}',          # "V" followed by 3 digits, or *
        '{sequence}':     r'{sequence:(s\d\d|\*|\>)}',      # "s" followed by 2 digits, or *  # !!!: do not use r'{2}', error with lucidity
        '{shot}':    r'{shot:(p\d\d\d|\*|\>)}',             # "p" followed by 3 digits, or *  # !!!: do not use r'{3}', error with lucidity
        #'{frame}':   r'{frame:(\*|\$\w*|#*|@*|[0-9]*)}',  # number, or "$" followed by a word, or "#"s, or "@"s, or *

        '{ext:scenes}': r'{ext:(' + '|'.join(extensions_scene) + r'|\*|\>)}',
        '{ext:caches}': r'{ext:(' + '|'.join(extensions_cache) + r'|\*|\>)}',
        #'{ext:images}': r'{ext:(' + '|'.join(extensions_image) + r'|\*|\>)}',
        '{ext:movies}': r'{ext:(' + '|'.join(extensions_movie) + r'|\*|\>)}',
    },

    'asset__': {
        '{step}': r'{step:(' + '|'.join(asset_steps) + r'|\*|\>)}',
        '{assettype}': r'{assettype:(' + '|'.join(asset_types) + r'|\*|\>)}',
        # '{name}': r'{name:([a-z0-9]+|\*|\?|\>)}',  # lowercase word or number, with at least one character
    },
    'shot__': {
        '{step}': r'{step:(' + '|'.join(shot_steps) + r'|\*|\>)}',
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