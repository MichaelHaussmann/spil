"""


The syntax is fieldname.EntityType.fieldname.
In this example, PlaylistVersionConnection has a field named version.
That field contains a Version entity. The field we are interested on the Version is code.
Put those together with our friend the dot and we have version.Version.code.

"""
type_mapping = {
    'project': 'Project',
    # 'asset__assettype': '',
    'asset__asset': 'Asset',
    "asset__task": 'Task',
    "asset__version": 'Version',
    'shot__sequence': 'Sequence',
    'shot__shot': 'Shot',
    "shot__task": 'Task',
    "shot__version": 'Version',
}


value_mappings = {
    'project': {
        'TestProject_TDLab': 'hamlet',
    },
    'assettype': {
        "Character": "char",
        "Prop": "prop",
        "FX": "fx",
        "Environment": "location"
    },
    'task': {
        'Layout': 'layout',
        'Animation': 'anim',
        'FX': 'fx',
        'Lighting': 'render',
        'Compositing': 'comp',
        'Art': 'art',
        'Modeling': 'model',
        'Surfacing': 'surface',
        'Rigging': 'rig',
    }
}


field_mappings = {
    'project': {
        "name": 'project'
    },
    'asset__assettype': {
        "project.Project.name": 'project',
        "sg_asset_type": "assettype",
    },
    'asset__asset': {
        "project.Project.name": 'project',
        "sg_asset_type": "assettype",
        "code": "asset"
    },
    "asset__task": {
        "project.Project.name": 'project',
        'entity.Asset.sg_asset_type': "assettype",
        "entity.Asset.code": 'asset',
        "content": "task",
    },
    "asset__version": {
        "project.Project.name": 'project',
        'entity.Asset.sg_asset_type': "assettype",
        "entity.Asset.code": 'asset',
        'sg_task.Task.content': 'task',
        "code": "version",
    },
    'shot__sequence': {
        "project.Project.name": 'project',
        "code": "sequence",
    },
    'shot__shot': {
        "project.Project.name": 'project',
        "sg_sequence.Sequence.code": 'sequence',
        "code": "shot",
    },
    "shot__task": {
        "project.Project.name": 'project',
        "entity.Shot.sg_sequence.Sequence.code": 'sequence',
        "entity.Shot.code": 'shot',
        # 'step.Step.code' : 'step' (untested)
        "content": "task",
    },
    "shot__version": {
        "project.Project.name": 'project',
        "entity.Shot.sg_sequence.Sequence.code": 'sequence',
        "entity.Shot.code": 'shot',
        # 'sg_task.Task.step.Step.code': 'step'
        'sg_task.Task.content': 'task',
        "code": "version",
    }
}


defaults_by_basetype = {
    'shot': {
        'type': 's'
    },
    'asset': {
        'type': 'a'
    }
}



