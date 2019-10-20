# -*- coding: utf-8 -*-
"""
Example Sid resolver config

Some parts of the sid contain hard coded elements :
project, version, state, ext

This config uses the attr library.
(We should add the these later using a global config, using converter/validator functions

TODO : a simpler config that does not need attr
"""
import six
import attr

from spil.conf.project_conf import projects


###########################################################################################
# SID BASE CONFIG / PARTS CONFIG
###########################################################################################

sip = '|'  # sid separator
sid_templates = {
    'asset': '{project}|a|{cat}|{name}|{task}|{subtask}|{version}|{state}|{ext}',
    'shot':  '{project}|s|{seq}|{shot}|{task}|{subtask}|{version}|{state}|{ext}',
    'project': '{project}',
}


###########################################################################################
# SID CLASS ATTRIBUTES CONFIG - using attr library
###########################################################################################

project_keys = ['project']
project_config = {}
for name in project_keys:
    project_config[name] = attr.ib(default=None)
project_config['_keys'] = attr.ib(default=project_keys, init=False, repr=False)

asset_keys = ['project', 'cat', 'name', 'task', 'subtask', 'version', 'state', 'ext']
asset_config = {}
for name in asset_keys:
    asset_config[name] = attr.ib(default=None)
asset_config['_keys'] = attr.ib(default=asset_keys, init=False, repr=False)

shot_keys = ['project', 'seq', 'shot', 'task', 'subtask', 'version', 'state', 'ext']
shot_config = {}
for name in shot_keys:
    shot_config[name] = attr.ib(default=None)
shot_config['_keys'] = attr.ib(default=shot_keys, init=False, repr=False)


# note : tasks are not filtered by a task list
sid_filters = {

    'asset': {
        'project': lambda x: x in list(projects),
        # 'cat': lambda x: x in allowed_categories,
        # 'task': lambda x: not six.text_type(x).isnumeric(),
        'state': lambda x: x in allowed_states,
        # 'ext': lambda x: x in allowed_extensions,
    },

    'shot': {
        'project': lambda x: x in list(projects),
        'state': lambda x: x in allowed_states,
        # 'ext': lambda x: x in allowed_extensions,

    },
    'project': {
        'project': lambda x: x in list(projects),
    }

}

###########################################################################################
# SID CONFIG
###########################################################################################

# SORTING ##################################################

basetype_order = ['project', 'asset', 'shot']

values_sorted = {
    'asset': {
        'task': ['modeling', 'modeling_lo', 'uvs', 'setup', 'gpu', 'surfacing', 'ass'],
        'state': ['w', 'p'],
        'ext': ['ma', 'mb']
    },
    'shot': {
        'task': ['layout', 'blocking', 'animation', 'fx', 'render', 'comp'],
    }
}

optional_keys = ['subtask']

values_defaults = {
    'asset': {
        'state': 'w',
    },
    'shot': {
        'subtask': 'main',
        'state': 'w',
    }
}

# Validation / Type detection ##################################################

cache_extensions = ['abc', 'json', 'fur', 'grm']
image_extensions = ['jpg', 'png', 'exr']
# allowed_extensions = ['ma', 'mb', 'hip', 'hda'] + image_extensions + cache_extensions

allowed_states = ['w', 'p']
multipass_tasks = ['render']

meta_items = ['*', '.', '^', '$', '?', '**']  # allowed items in search sids (# CBB this is part of the sid+fs conf)


###########################################################################################
# SID TYPE DEFINITION
###########################################################################################

def get_sidtype(data):
    """
    rules defining the sidtype, based on the data dict of the sid.
    The keys are always given.
    The values can be empty.

    :param data:
    :return:
    """
    # print 'in da get', data

    if data.get('cat'):
        subtype = 'asset_cat'

        if data.get('name'):
            subtype = 'asset_name'

        if data.get('task'):
            subtype = 'asset_task'

        if data.get('subtask'):
            subtype = 'asset_subtask'

        if data.get('version'):
            subtype = 'asset_version'

        if data.get('state'):
            subtype = 'asset_state'

        if data.get('ext'):
            subtype = 'asset_file'

    elif data.get('seq'):

        subtype = 'shot_seq'

        if data.get('shot'):
            subtype = 'shot_shot'

        if data.get('task'):
            subtype = 'shot_task'

        if data.get('subtask'):
            subtype = 'shot_subtask'

        if data.get('version'):
            subtype = 'shot_version'

        if data.get('state'):
            subtype = 'shot_state'

        if data.get('ext'):
            subtype = 'shot_file'

    else:

        return 'project'

    # print 'the ext ?', data.get('ext')

    if data.get('ext') in cache_extensions:
        if data.get('version'):
            subtype = subtype.replace('_file', '_versioned_cache_file')
        else:
            subtype = subtype.replace('_file', '_cache_file')

    elif data.get('ext') in image_extensions:
        subtype = subtype.replace('_file', '_image_file')

        if data.get('task') in multipass_tasks:
            subtype = subtype.replace('_image_file', '_pass_image_file')

    # print 'out da get', subtype

    return subtype


###########################################################################################
# TEST DATA - TODO : add types for auto tests
###########################################################################################

test_sids = [

    'demo|s|s010|master|01_layout|main|valid|p|ma',
    'demo|a|characters|crab|modeling|maya|valid|p|ma',
    'demo',

    'demo|a|vehicles|race_car',
    'demo|a|props|barrel',
    'demo|a|sets|desert',
    'demo|a|sets|cyberpunk_roof_top',

    'demo|a|fx|smoke|setup|houdini|valid|p|hip',
    'demo|a|fx|fire|setup|houdini|valid|p|hip',
    'demo|a|props|barrel',

    'demo|a|characters|dragon|setup|houdini|valid|p|ma',
    'demo|a|characters|dragon|setup|houdini|v001|p|ma',
    'demo|a|characters|dragon|setup|houdini|v001|w|ma',
    'demo|a|characters|dragon|setup|houdini|v001',
    'demo|a|characters|dragon|setup|houdini',
    'demo|a|characters|dragon|setup',
    'demo|a|characters|dragon',

    'demo|a|characters|crab|modeling_lo',
    'demo|a|characters|crab|modeling|zbrush|v001|w',
    'demo|a|characters|crab|modeling|maya|valid|p|ma',
    'demo|a|characters|crab|modeling|maya|v001|p|ma',
    'demo|a|characters|crab|modeling|maya|v001|w|ma',
    'demo|a|characters|crab|modeling|maya|v001',
    'demo|a|characters|crab|modeling|maya',
    'demo|a|characters|crab|modeling',
    'demo|a|characters|crab',

    'demo|a|characters',
    
    'demo|s|s010|p040',

    'demo|s|s010|p030|03_anim|main|valid|p|ma',
    'demo|s|s010|p030|03_anim|main|v001|p|ma',
    'demo|s|s010|p030|03_anim|main|v001|w|ma',

    'demo|s|s010|p020|03_anim|main|v001|w|ma',

    'demo|s|s010|p010|04_fx|water|v001|w|hip',
    'demo|s|s010|p010|04_fx|pyro|v002|w|hip',
    'demo|s|s010|p010|04_fx|pyro|v001|w|hip',
    'demo|s|s010|p010|03_anim|main|v001|w|ma',

    'demo|s|s010|p010|02_blocking|main|v001|w|ma',
    'demo|s|s010|p010|02_blocking|main|v001|w',
    'demo|s|s010|p010|02_blocking|main|v001',
    'demo|s|s010|p010|02_blocking|main',
    'demo|s|s010|p010|02_blocking',
    'demo|s|s010|p010',

    'demo|s|s010|master|01_layout|main|valid|p|ma',
    'demo|s|s010|master|01_layout|main|v002|p|ma',
    'demo|s|s010|master|01_layout|main|v002|w|ma',
    'demo|s|s010|master|01_layout|main|v001|w|ma',
    'demo|s|s010|master|01_layout',
    'demo|s|s010|master',
    'demo|s|s020',
    'demo|s|s010',
    'demo',

]


if __name__ == '__main__':

    from pprint import pprint

    pprint(globals())