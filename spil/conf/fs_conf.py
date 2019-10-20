# -*- coding: utf-8 -*-
"""
Example File System resolver config.

Maps file paths to Sid components.
The order is important, first match is returned.

#TODO : one root path per project
#IDEA config per project

"""
from collections import OrderedDict

###########################################################################################
# SOFT CONFIG
###########################################################################################


"""
SID TEMPLATES AS MEMO
sid_templates = {
    'asset': '{project}|a|{cat}|{name}|{task}|{subtask}|{version}|{state}|{ext}',
    'shot':  '{project}|s|{seq}|{shot}|{task}|{subtask}|{version}|{state}|{ext}',
    'project': '{project}',
}

"""

###########################################################################################
# PATHS The order is important, first match is returned.
###########################################################################################
path_templates = OrderedDict([

    ('project_root', r'/home/mh/spil/projects/{project}/work'),
    # ('project_root', r'/home/mh/Bureau/PROJECT_PATHS/TEST/prod_data'),

    ('asset_file', r'{@project_root}/01_assets/{cat}/{name}/3d/scenes/{task}/{subtask}/{state}_{version}/{name}.{ext}'),
    ('asset_image_file', r'{@project_root}/01_assets/{cat}/{name}/3d/images/{task}/{subtask}/{state}_{version}/{name}.{frame}.{ext}'),
    ('asset_cache_file', r'{@project_root}/01_assets/{cat}/{name}/3d/caches/{task}/{subtask}/{state}_{version}/{name}.{ext}'),
    ('asset_state', r'{@project_root}/01_assets/{cat}/{name}/3d/scenes/{task}/{subtask}/{state}_{version}'),
    #('asset_version', r'{@project_root}/01_assets/{cat}/{name}/3d/scenes/{task}/{subtask}/{state}_{version}'),
    ('asset_subtask', r'{@project_root}/01_assets/{cat}/{name}/3d/scenes/{task}/{subtask}'),
    ('asset_task', r'{@project_root}/01_assets/{cat}/{name}/3d/scenes/{task}'),
    ('asset_name', r'{@project_root}/01_assets/{cat}/{name}'),
    ('asset_cat', r'{@project_root}/01_assets/{cat}'),

    ('shot_file', r'{@project_root}/02_shots/3d/scenes/{seq}/{shot}/{task}/{subtask}/{state}_{version}/{seq}_{shot}.{ext}'),
    ('shot_image_file', r'{@project_root}/02_shots/3d/images/{seq}/{shot}/{task}/{subtask}/{state}_{version}/{seq}_{shot}.{frame}.{ext}'),
    ('shot_image_pass_file', r'{@project_root}/02_shots/3d/images/{seq}/{shot}/{task}/{subtask}/{state}_{version}/{pass}/{seq}_{shot}.{frame}.{ext}'),
    ('shot_cache_file', r'{@project_root}/02_shots/3d/caches/{seq}/{shot}/{task}/{subtask}/{state}_{version}/{seq}_{shot}.{frame}.{ext}'),
    # TODO no frame caches, non versioned caches
    ('shot_state', r'{@project_root}/02_shots/3d/scenes/{seq}/{shot}/{task}/{subtask}/{state}_{version}'),
    # ('shot_version', r'{@project_root}/02_shots/3d/scenes/{seq}/{shot}/{task}/{subtask}/{state}_{version}'),
    ('shot_subtask', r'{@project_root}/02_shots/3d/scenes/{seq}/{shot}/{task}/{subtask}'),
    ('shot_task', r'{@project_root}/02_shots/3d/scenes/{seq}/{shot}/{task}'),
    ('shot_shot', r'{@project_root}/02_shots/3d/scenes/{seq}/{shot}'),
    ('shot_seq', r'{@project_root}/02_shots/3d/scenes/{seq}'),

    ('project', r'{@project_root}'),

])

path_templates_reference = 'project_root'

path_defaults = {

#    'state': 'w',
    'frame': '#'  # does not need to be part of the sid, but may be needed for path creation
}


path_mapping = {  # TODO put into project_conf

    'project': {
        'demo': 'demo',
    },
    'state': {
        'work': 'w',
        'publish': 'p',
        '*': '*',  # FIXME : needed for search
    },
}



###########################################################################################
# TEST DATA - # TODO add types to test types
###########################################################################################

test_paths = [
    '/home/mh/spil/projects/demo/work/02_shots/3d/scenes/s010/master/01_layout/main/publish_valid/s010_master.ma',
    '/home/mh/spil/projects/demo/work/01_assets/characters/crab/3d/scenes/modeling/maya/publish_valid/crab.ma',
    '/home/mh/spil/projects/demo/work',
    '/home/mh/spil/projects/demo/work/01_assets/vehicles/race_car',
    '/home/mh/spil/projects/demo/work/01_assets/props/barrel',
    '/home/mh/spil/projects/demo/work/01_assets/sets/desert',
    '/home/mh/spil/projects/demo/work/01_assets/sets/cyberpunk_roof_top',
    '/home/mh/spil/projects/demo/work/01_assets/fx/smoke/3d/scenes/setup/houdini/publish_valid/smoke.ma',
    '/home/mh/spil/projects/demo/work/01_assets/fx/fire/3d/scenes/setup/houdini/publish_valid/fire.ma',
    '/home/mh/spil/projects/demo/work/01_assets/props/barrel',
    '/home/mh/spil/projects/demo/work/01_assets/characters/dragon/3d/scenes/setup/houdini/publish_valid/dragon.ma',
    '/home/mh/spil/projects/demo/work/01_assets/characters/dragon/3d/scenes/setup/houdini/publish_v001/dragon.ma',
    '/home/mh/spil/projects/demo/work/01_assets/characters/dragon/3d/scenes/setup/houdini/work_v001/dragon.ma',
    '/home/mh/spil/projects/demo/work/01_assets/characters/dragon/3d/scenes/setup/houdini',
    '/home/mh/spil/projects/demo/work/01_assets/characters/dragon/3d/scenes/setup',
    '/home/mh/spil/projects/demo/work/01_assets/characters/dragon',
    '/home/mh/spil/projects/demo/work/01_assets/characters/crab/3d/scenes/modeling_lo',
    '/home/mh/spil/projects/demo/work/01_assets/characters/crab/3d/scenes/modeling/zbrush/work_v001',
    '/home/mh/spil/projects/demo/work/01_assets/characters/crab/3d/scenes/modeling/maya/publish_valid/crab.ma',
    '/home/mh/spil/projects/demo/work/01_assets/characters/crab/3d/scenes/modeling/maya/publish_v001/crab.ma',
    '/home/mh/spil/projects/demo/work/01_assets/characters/crab/3d/scenes/modeling/maya/work_v001/crab.ma',
    '/home/mh/spil/projects/demo/work/01_assets/characters/crab/3d/scenes/modeling/maya',
    '/home/mh/spil/projects/demo/work/01_assets/characters/crab/3d/scenes/modeling',
    '/home/mh/spil/projects/demo/work/01_assets/characters/crab',
    '/home/mh/spil/projects/demo/work/01_assets/characters',
    '/home/mh/spil/projects/demo/work/02_shots/3d/scenes/s010/p040',
    '/home/mh/spil/projects/demo/work/02_shots/3d/scenes/s010/p030/03_anim/main/publish_valid/s010_p030.ma',
    '/home/mh/spil/projects/demo/work/02_shots/3d/scenes/s010/p030/03_anim/main/publish_v001/s010_p030.ma',
    '/home/mh/spil/projects/demo/work/02_shots/3d/scenes/s010/p030/03_anim/main/work_v001/s010_p030.ma',
    '/home/mh/spil/projects/demo/work/02_shots/3d/scenes/s010/p020/03_anim/main/work_v001/s010_p020.ma',
    '/home/mh/spil/projects/demo/work/02_shots/3d/scenes/s010/p010/04_fx/water/work_v001/s010_p010.hip',
    '/home/mh/spil/projects/demo/work/02_shots/3d/scenes/s010/p010/04_fx/pyro/work_v002/s010_p010.hip',
    '/home/mh/spil/projects/demo/work/02_shots/3d/scenes/s010/p010/04_fx/pyro/work_v001/s010_p010.hip',
    '/home/mh/spil/projects/demo/work/02_shots/3d/scenes/s010/p010/03_anim/main/work_v001/s010_p010.ma',
    '/home/mh/spil/projects/demo/work/02_shots/3d/scenes/s010/p010/02_blocking/main/work_v001/s010_p010.ma',
    '/home/mh/spil/projects/demo/work/02_shots/3d/scenes/s010/p010/02_blocking/main/work_v001',
    '/home/mh/spil/projects/demo/work/02_shots/3d/scenes/s010/p010/02_blocking/main',
    '/home/mh/spil/projects/demo/work/02_shots/3d/scenes/s010/p010/02_blocking',
    '/home/mh/spil/projects/demo/work/02_shots/3d/scenes/s010/p010',
    '/home/mh/spil/projects/demo/work/02_shots/3d/scenes/s010/master/01_layout/main/publish_valid/s010_master.ma',
    '/home/mh/spil/projects/demo/work/02_shots/3d/scenes/s010/master/01_layout/main/publish_v002/s010_master.ma',
    '/home/mh/spil/projects/demo/work/02_shots/3d/scenes/s010/master/01_layout/main/work_v002/s010_master.ma',
    '/home/mh/spil/projects/demo/work/02_shots/3d/scenes/s010/master/01_layout/main/work_v001/s010_master.ma',
    '/home/mh/spil/projects/demo/work/02_shots/3d/scenes/s010/master/01_layout',
    '/home/mh/spil/projects/demo/work/02_shots/3d/scenes/s010/master',
    '/home/mh/spil/projects/demo/work/02_shots/3d/scenes/s020',
    '/home/mh/spil/projects/demo/work/02_shots/3d/scenes/s010',
    '/home/mh/spil/projects/demo/work'
]

not_covered = [
]


search_sids = [
    'demo|*',       # ?
    'demo|a|*',     # cats
    'demo|a|characters|*',     #
    'demo|a|characters|crab|*',     #
    'demo|a|characters|crab|01_modeling|*',     #
    'demo|a|characters|crab|01_modeling|maya|*',     #
    'demo|a|characters|crab|01_modeling|maya|work_v001|*',     #
    'demo|a|characters|crab|01_modeling|maya|work_v001|ma',     #
]


if __name__ == '__main__':

    from pprint import pprint

    pprint(globals())