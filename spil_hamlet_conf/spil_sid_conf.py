
sip = '/'  # sid separator

projects = ['hamlet']

sid_templates = {

    # type asset
    'asset__file':            '{project}/{type:a}/{assettype}/{asset}/{task}/{version}/{state}/{ext:scenes}',
    'asset__movie_file':      '{project}/{type:a}/{assettype}/{asset}/{task}/{version}/{state}/{ext:movies}',
    'asset__cache_file':      '{project}/{type:a}/{assettype}/{asset}/{task}/{version}/{state}/{ext:caches}',

    'asset__state':           '{project}/{type:a}/{assettype}/{asset}/{task}/{version}/{state}',  # extrapolated

    'asset':                  '{project}/{type:a}',

    # type shot
    'shot__file':             '{project}/{type:s}/{sequence}/{shot}/{task}/{version}/{state}/{ext:scenes}',
    'shot__movie_file':       '{project}/{type:s}/{sequence}/{shot}/{task}/{version}/{state}/{ext:movies}',
    'shot__cache_file':       '{project}/{type:s}/{sequence}/{shot}/{task}/{version}/{state}/{ext:caches}',
    'shot__cache_node_file':  '{project}/{type:s}/{sequence}/{shot}/{task}/{version}/{state}/{node}/{ext:caches}',
    'shot__cache_node':       '{project}/{type:s}/{sequence}/{shot}/{task}/{version}/{state}/{node}',

    'shot__state':            '{project}/{type:s}/{sequence}/{shot}/{task}/{version}/{state}',  # extrapolated

    'shot':                   '{project}/{type:s}',

    # type project
    'project':                '{project}',

}

to_extrapolate = ['asset__state', 'shot__state']

asset_tasks = ['art', 'model', 'surface', 'rig']
shot_tasks = ['board', 'layout', 'anim', 'fx', 'render', 'comp']
asset_types = ['char', 'location', 'prop', 'fx']

# alias as last value
extensions_scene = ['ma', 'mb', 'hip', 'blend', 'hou', 'psd', 'nk', 'maya']
extensions_cache = ['abc', 'json', 'fur', 'grm', 'vdb', 'cache']
extensions_movie = ['mp4', 'mov', 'avi', 'movie']

extension_alias = {
    'cache': extensions_cache[:-1],  # we remove the last value, which is the alias itself
    'hou': ['hip', 'hipnc'],
    'maya': ['ma', 'mb'],
    'movie': extensions_movie[:-1]
}

key_patterns = {

    '__': {
        '{state}':      r'{state:(w|p|\*|\>)}',         # "w" or "p" or *
        '{state:w}':    r'{state:(w|\*|\>)}',           # "w" or "p" or *
        '{state:p}':    r'{state:(p|\*|\>)}',           # "w" or "p" or *
        '{version}':    r'{version:(v\d\d\d|\*|\>)}',   # "V" followed by 3 digits, or *
        '{sequence}':   r'{sequence:(sq\d\d\d|\*|\>)}',   # "sq" followed by 3 digits, or *  # !!!: do not use r'{2}', error with lucidity
        '{shot}':       r'{shot:(sh\d\d\d\d|\*|\>)}',     # "sh" followed by 4 digits, or *  # !!!: do not use r'{3}', error with lucidity

        '{ext:scenes}': r'{ext:(' + '|'.join(extensions_scene) + r'|\*|\>)}',
        '{ext:caches}': r'{ext:(' + '|'.join(extensions_cache) + r'|\*|\>)}',
        '{ext:movies}': r'{ext:(' + '|'.join(extensions_movie) + r'|\*|\>)}',
    },

    'asset__': {
        '{task}': r'{task:(' + '|'.join(asset_tasks) + r'|\*|\>)}',
        '{assettype}': r'{assettype:(' + '|'.join(asset_types) + r'|\*|\>)}',
    },
    'shot__': {
        '{task}': r'{task:(' + '|'.join(shot_tasks) + r'|\*|\>)}',
    },
    't': {  # everything   containing a "t" (asset, shot, project...) # FIXME
        '{project}': r'{project:(' + '|'.join(projects) + r'|\*|\>)}',
        '{type:a}': r'{type:(a|\*|\>)}',
        '{type:s}': r'{type:(s|\*|\>)}',
    },
}

# These keytypes are used by the resolver to sort the keys
key_types = {
    'asset': ['project', 'type', 'assettype', 'asset', 'task', 'version', 'state', 'ext'],
    'shot': ['project', 'type', 'sequence', 'shot', 'task', 'version', 'state', 'node', 'ext'],
    'project': ['project'],
}

# "leaf": last key of a Sid, per basetype. Typically "ext".
leaf_keys = {'asset': 'ext',
             'shot': 'ext',
             'project': 'ext',  # used for expand
             None: 'ext'}  # if the Sid has None basetype

"""
Once a search Sid is typed, we may need to narrow down the values, to make sure the right type is hit in the search.
For example: 
"asset__assettype:hamlet/*/*" and "shot__sequence:hamlet/*/*" should be narrowed down to 
"asset__assettype:hamlet/a/*" and "shot__sequence:hamlet/s/*"
The patterns cannot yet be properly automated. The goal for this config_name is to explicitly configure this.
"""
basetyped_search_narrowing = {

    'asset': 'type=~a',
    'shot': 'type=~s',

}

typed_search_narrowing = {  # type: ignore
    # not implemented yet.

    # this does not work because the Sid is typed (signle values only)
    # 'asset__movie_file': 'ext=~' + ','.join(extension_alias.get('movie'))  # type: ignore
}


if __name__ == '__main__':

    from pprint import pprint

    pprint(globals())
