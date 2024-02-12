# type: ignore
"""
Example File System resolver config_name.
Maps file paths to Sid components.
"""
from spil_sid_conf import key_patterns

# for test and demo purposes
from pathlib import Path
project_root_path = Path(__file__).parent / "data" / "testing" / "SPIL_PROJECTS" / "LOCAL" / "PROJECTS"
# Replace "project_root_path" by your own folder root, eg
# r'/home/mh/Desktop/SPIL_PROJECTS/LOCAL/PROJECTS'

path_templates = {

    # 'project_root':            project_root_path.as_posix(),

    # type asset
    'asset__file':             '{@project_root}/{project}/PROD/{type:ASSETS}/{assettype}/{asset}/{task}/{version}/{assettype}_{asset}_{task}_{state}_{version}.{ext:scenes}',
    'asset__movie_file':       '{@project_root}/{project}/PROD/{type:ASSETS}/{assettype}/{asset}/{task}/{version}/OUTPUT/{assettype}_{asset}_{task}_{state}_{version}.{ext:movies}',
    'asset__cache_file':       '{@project_root}/{project}/PROD/{type:ASSETS}/{assettype}/{asset}/{task}/{version}/OUTPUT/{assettype}_{asset}_{task}_{state}_{version}.{ext:caches}',

    'asset__version':          '{@project_root}/{project}/PROD/{type:ASSETS}/{assettype}/{asset}/{task}/{version}',
    'asset__task':             '{@project_root}/{project}/PROD/{type:ASSETS}/{assettype}/{asset}/{task}',
    'asset__asset':            '{@project_root}/{project}/PROD/{type:ASSETS}/{assettype}/{asset}',
    'asset__assettype':        '{@project_root}/{project}/PROD/{type:ASSETS}/{assettype}',

    'asset':                   '{@project_root}/{project}/PROD/{type:ASSETS}',

    # type shot
    'shot__file':              '{@project_root}/{project}/PROD/{type:SHOTS}/{sequence}/{sequence}_{shot}/{task}/{version}/{sequence}_{shot}_{task}_{state}_{version}.{ext:scenes}',
    'shot__movie_file':        '{@project_root}/{project}/PROD/{type:SHOTS}/{sequence}/{sequence}_{shot}/{task}/{version}/EXPORT/{sequence}_{shot}_{task}_{state}_{version}.{ext:movies}',
    'shot__cache_node_file':   '{@project_root}/{project}/PROD/{type:SHOTS}/{sequence}/{sequence}_{shot}/{task}/{version}/EXPORT/{sequence}_{shot}_{task}_{node}_{state}_{version}.{ext:caches}',
    'shot__cache_file':        '{@project_root}/{project}/PROD/{type:SHOTS}/{sequence}/{sequence}_{shot}/{task}/{version}/EXPORT/{sequence}_{shot}_{state}_{version}.{ext:caches}',

    'shot__version':           '{@project_root}/{project}/PROD/{type:SHOTS}/{sequence}/{sequence}_{shot}/{task}/{version}',
    'shot__task':              '{@project_root}/{project}/PROD/{type:SHOTS}/{sequence}/{sequence}_{shot}/{task}',
    'shot__shot':              '{@project_root}/{project}/PROD/{type:SHOTS}/{sequence}/{sequence}_{shot}',
    'shot__sequence':          '{@project_root}/{project}/PROD/{type:SHOTS}/{sequence}',
    'shot':                    '{@project_root}/{project}/PROD/{type:SHOTS}',

    # type project
    'project':                '{@project_root}/{project}',
}

# quick replace, for resolva compatibility
qr = ('{@project_root}', project_root_path.as_posix())
path_templates = {k: v.replace(qr[0], qr[1]) for k, v in path_templates.items()}

# Specific mappings not needed here
path_defaults = {
    'state': 'WORK',
}
sidkeys_to_extrakeys = {}
extrakeys_to_sidkeys = {}

path_mapping = {  # the resolver might get the keys by values. if the value exists multiple times, the first one is returned.

    'project': {
        'HAMLET': 'hamlet',
    },
    'type': {
        'ASSETS': 'a',
        'SHOTS': 's',
    },
    'state': {
        'WORK': 'w',
        'PUBLISH': 'p',
    },

    # Specific path mapping by type not needed here
}

# not needed here ('/3d/scenes/': '/*/scenes/')
search_path_mapping = {}

project_path_names = list(path_mapping.get('project').keys())

# we override elements already set in sid_conf
key_patterns = key_patterns.copy()

key_patterns['__'].update({
        '{state}':   r'{state:(WORK|PUBLISH|\*|\>)}',
        '{state:p}': r'{state:(PUBLISH|\*|\>)}',
        '{state:w}': r'{state:(WORK|\*|\>)}',
    })

key_patterns['t'].update({
        '{project}':        r'{project:(' + '|'.join(project_path_names) + r'|\*|\>)}',
        '{type:SHOTS}':     r'{type:(SHOTS|\*|\>)}',
        '{type:ASSETS}':    r'{type:(ASSETS|\*|\>)}',
    })

if __name__ == '__main__':

    from pprint import pprint

    pprint(globals())

    for key in path_templates:
        print(path_templates.get(key))
