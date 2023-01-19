"""

This code is work in progress.


Gazu / Zou access functions.

Related docs:
Full Rest API: https://kitsu-api.cg-wire.com/#/

TODO:
Many functions need multiple calls to get the complete data hierarchy.
We need to
- log and count the amount of raw api calls
- reduce that amount by grouping and/or caching calls
- explore the GraphQL API to get the hierarchical representation of the data.


"""
from __future__ import annotations

from typing import List
from spil import Sid, SpilException

from spil_plugins.kitsu import conf as zou_conf
from spil.util.caching import lru_kw_cache as kw_cache, lru_cache as cache, hit_cache
from spil_plugins.kitsu import connect_gazu
from spil_plugins.kitsu.util import sid_format
from spil.util.exception import raiser
from spil.util.log import get_logger, logging
logger = get_logger("spil_kitsu", logging.DEBUG)

gazu = connect_gazu.connect()

sid_key = "code"  # shotgun_id or code, currently testing

########################
# Utility
########################


@kw_cache
def get_asset_types(as_gazu: bool = False) -> List[Sid | dict]:

    assettypes_gazu = gazu.asset.all_asset_types()
    if not assettypes_gazu:
        raise SpilException(f'No Asset Types found.')
    # if as_gazu: FIXME
    return assettypes_gazu


@cache
def get_asset_type_ids():  # TODO cache
    """
    Reads all asset types and returns a dictionary with name: id and id: name entries.

    :return:
    """
    result = {}
    for item in get_asset_types():
        name = sid_format(item.get("name"))
        result[item.get("id")] = name
        result[name] = item.get("id")
    return result

@cache
def get_project_ids():  # TODO cache
    result = {}
    for item in gazu.project.all_projects():
        name = item.get("name")
        name = zou_conf.name_mapping.get('project', {}).get(name)
        result[item.get("id")] = name
        result[name] = item.get("id")
    return result


def gazu_to_sid(gazu_dict: dict) -> Sid:
    """
    Sid from gazu resolver.

    Will first attempt to read the Sid that is set in the sid_key field (currently testing "shotgun_id" as the sid field).
    If the sid is not set, will resolve it.

    :param gazu_dict:
    :return:
    """
    if not gazu_dict:
        logger.warning("gazu_dict is empty or none")
        return Sid()

    stored_sid = gazu_dict.get(sid_key)
    if stored_sid:
        sid = Sid(stored_sid)
        if sid:
            logger.debug(f"Sid {sid} resolved from key {sid_key}")
            return sid

    stored_sid = gazu_dict.get("data", {}).get(sid_key)
    if stored_sid:
        sid = Sid(stored_sid)
        if sid:
            logger.debug(f"Sid {sid} resolved from data, with key {sid_key}")
            return sid

    resolver = {
        'Project': f"{project_ids.get(gazu_dict.get('id'))}",
        'Asset': f"{project_ids.get(gazu_dict.get('project_id'))}/a/{asset_type_ids.get(gazu_dict.get('entity_type_id'))}/{gazu_dict.get('name')}",
        'Sequence': f"{project_ids.get(gazu_dict.get('project_id'))}/s/{gazu_dict.get('name')}",
        'Shot': f"{project_ids.get(gazu_dict.get('project_id'))}/s/{gazu_dict.get('sequence_name')}/{gazu_dict.get('name')}",
        # 'Task': f"{project_ids.get(gazu_dict.get('project_id'))}/{gazu_dict.get('sequence_name')}/{gazu_dict.get('entity_name')}/{gazu_dict.get('task_type_name')}//{gazu_dict.get('name')}",
    }
    pattern = resolver.get(gazu_dict.get('type'))
    if not pattern:
        raise Exception(f"No pattern defined for {gazu_dict.get('type')} ({gazu_dict})")
    logger.debug(f"Resolved [{pattern}] from {gazu_dict}")
    sid = Sid(pattern.lower())
    if sid:
        return sid
    else:
        logger.warning(f"Could not resolve {gazu_dict} to valid Sid.")


def get_gazu(sid: Sid | str):  # YAGNI ? untested
    """
    Global Sid to gazu.

    :param sid:
    :return:
    """
    sid = Sid(sid)
    if not sid:
        raise Exception(f'Sid {sid} not valid.')

    getter_by_type = {
        "project": get_project,
        "asset__asset": get_asset,
        # "asset__task": get_task,
        "shot__sequence": get_sequence,
        "shot_shot": get_shot,
        # "shot__task": get_task,
    }

    func = getter_by_type.get(sid.type) or raiser(f"No getter implemented for type {sid.type}, sid: {sid} ")

    return func(as_gazu=True)


project_ids = get_project_ids()
asset_type_ids = get_asset_type_ids()

########################
# Read
########################

@kw_cache  # we cache this because we suppose projects are all created prior to calling this code.
def get_project(project: Sid | str, as_gazu: bool = False) -> Sid | dict:
    project_sid = Sid(project).get_as('project')
    if not project_sid:
        raise SpilException(f'No valid Project Sid for {project}.')
    gazu_project_name = zou_conf.name_mapping.get('project').get(project_sid.get('project'))
    project_gazu = gazu.project.get_project_by_name(gazu_project_name)
    if as_gazu:
        return project_gazu
    else:
        return gazu_to_sid(project_gazu)


@hit_cache
def get_asset(asset: Sid | str, as_gazu: bool = False) -> Sid | dict | None:  #TODO: get sequence and shot in one request.
    asset_sid = Sid(asset).get_as('asset')
    if not asset_sid:
        raise SpilException(f'No valid Asset Sid for {asset}.')
    project_gazu = get_project(asset_sid.get_as('project'), as_gazu=True)
    if not project_gazu:
        raise SpilException(f"For {asset} : Project {asset_sid.get_as('project')} not found")
    asset_gazu = gazu.asset.get_asset_by_name(project_gazu, name=asset_sid.get("asset"))
    if not asset_gazu:
        return None  # TODO return Sid() or {} ?
    if as_gazu:
        return asset_gazu
    else:
        return gazu_to_sid(asset_gazu)  # FIXME


def get_asset_tasks(asset: Sid | str, as_gazu: bool = False) -> List[Sid | dict]:

    asset_sid = Sid(asset).get_as('asset')
    if not asset_sid:
        raise SpilException(f'No valid Asset Sid for {asset}.')
    asset_gazu = get_asset(asset_sid, as_gazu=True)
    if not asset_gazu:
        raise Exception(f"For {asset} : Asset not found")
    tasks_gazu = gazu.task.all_tasks_for_asset(asset_gazu)
    if as_gazu:
        return tasks_gazu
    else:
        result = []
        for task in tasks_gazu:
            task_sid = asset_sid / sid_format(task.get('task_type_name')) / sid_format(task.get('name'))
            if task_sid:
                result.append(task_sid)
            else:
                logger.warning(f"Got invalid Sid {task_sid} from {task}")
        return result


@hit_cache
def get_sequence(sequence: Sid | str, as_gazu=False) -> Sid | None:
    """

    Args:
        sequence:
        as_gazu:

    Returns:

    """
    sequence_sid = Sid(sequence).get_as('sequence')
    if not sequence_sid:
        raise SpilException(f'No valid Sequence Sid for {sequence}.')
    project_gazu = get_project(sequence_sid.get_as('project'), as_gazu=True)
    if not project_gazu:
        raise Exception(f"For {sequence_sid} : Project {sequence_sid.get_as('project')} not found")
    sequence_gazu = gazu.shot.get_sequence_by_name(project_gazu, sequence_sid.get('sequence'))
    #print(f"found {sequence_gazu}")
    if not sequence_gazu:
        return None  # TODO return Sid() or {} ?
    if as_gazu:
        return sequence_gazu
    else:
        return gazu_to_sid(sequence_gazu)


@hit_cache
def get_shot(shot: Sid | str, as_gazu=False) -> Sid | None:  #TODO: get sequence and shot in one go.
    shot_sid = Sid(shot).get_as('shot')
    if not shot_sid:
        raise SpilException(f'No valid Sid for {shot}.')
    sequence_gazu = get_sequence(shot_sid.get_as('sequence'), as_gazu=True)
    if not sequence_gazu:
        logger.info(f"For {shot_sid} : Sequence {shot_sid.get_as('sequence')} not found, no Shot returned")
        return None  #TODO return Sid() or {} ?
    shot_gazu = gazu.shot.get_shot_by_name(sequence_gazu, shot_sid.get('shot'))
    if not shot_gazu:
        return None  # TODO return Sid() or {} ?
    #print(f"found {shot_gazu}")
    if as_gazu:
        return shot_gazu
    else:
        return gazu_to_sid(shot_gazu)  # FIXME


def get_shot_tasks(shot: Sid | str, as_gazu: bool = False) -> List[Sid]:

    shot_sid = Sid(shot).get_as('shot')
    if not shot_sid:
        raise SpilException(f'No valid Sid for {shot}.')
    shot_gazu = get_shot(shot_sid, as_gazu=True)
    if not shot_gazu:
        raise SpilException(f"For {shot_sid} : Shot not found")
    tasks_gazu = gazu.task.all_tasks_for_shot(shot_gazu)
    if as_gazu:
        return tasks_gazu
    else:
        result = []
        for task in tasks_gazu:
            task_sid = shot_sid / sid_format(task.get('task_type_name')) / sid_format(task.get('name'))
            if task_sid:
                result.append(task_sid)
            else:
                logger.warning(f"Got invalid Sid {task_sid} from {task}")
        return result


########################
# Create
########################

def create_asset(asset: Sid | str, as_gazu: bool = False) -> Sid:

    asset_sid = Sid(asset).get_as('asset')
    asset_gazu = get_asset(asset_sid, as_gazu=True)

    if asset_gazu:
        logger.info(f"Asset already exists: {asset_gazu}")
        return asset_gazu if as_gazu else asset_sid

    asset_type = gazu.asset.get_asset_type_by_name(asset_sid.get("assettype").capitalize())  # RULE
    if not asset_type:
        raise SpilException(f'Type: "{asset_sid.get("assettype").capitalize()}" not found for Asset {asset}. Cannot create Asset.')

    project_gazu = get_project(asset_sid.get_as("project"), as_gazu=True)
    if not project_gazu:
        raise SpilException(f"No project found for Asset {asset}. Cannot create Asset.")

    asset_gazu = gazu.asset.new_asset(project=project_gazu, asset_type=asset_type, name=asset_sid.get('asset'))

    asset_gazu[sid_key] = str(asset_sid)
    asset_gazu = gazu.asset.update_asset(asset_gazu)

    logger.info(f"Created {asset_sid} / {asset_gazu}")
    assert(asset_sid == gazu_to_sid(asset_gazu))  # final check for correctness

    if as_gazu:
        return asset_gazu
    else:
        return asset_sid


def create_sequence(sequence: Sid | str, as_gazu: bool = False) -> Sid | dict:

    sequence_sid = Sid(sequence).get_as('sequence')
    sequence_gazu = get_sequence(sequence_sid, as_gazu=True)

    if sequence_gazu:
        logger.warning(f"Sequence already exists: {sequence_sid}")
        return sequence_sid

    project_gazu = get_project(sequence_sid.get_as('project'), as_gazu=True)

    sequence_gazu = gazu.shot.new_sequence(project_gazu, name=sequence_sid.get('sequence'))

    # Adding the sid into the code field. Needs an update call, there is no way to add data during creation (even in raw post)
    sequence_gazu[sid_key] = str(sequence_sid)
    sequence_gazu = gazu.shot.update_sequence(sequence_gazu)

    logger.info(f"Created {sequence_sid} / {sequence_gazu}")
    assert(sequence_sid == gazu_to_sid(sequence_gazu))  # final check for correctness

    if as_gazu:
        return sequence_gazu
    else:
        return sequence_sid


def create_shot(shot: Sid | str, do_create_parent: bool = False, as_gazu: bool = False) -> Sid:

    shot_sid = Sid(shot).get_as('shot')
    shot_gazu = get_shot(shot_sid, as_gazu=True)

    if shot_gazu:
        logger.info(f"Shot already exists: {shot_gazu}")
        return shot_gazu if as_gazu else shot_sid

    sequence_gazu = get_sequence(shot_sid.get_as('sequence'), as_gazu=True)
    if not sequence_gazu:
        if do_create_parent:
            sequence_gazu = create_sequence(shot_sid.get_as('sequence'), as_gazu=True)

    if not sequence_gazu:
        raise SpilException(f"No sequence found or created for shot {shot}. Cannot create Shot.")

    shot_gazu = gazu.shot.new_shot(project=sequence_gazu.get('project_id'), sequence=sequence_gazu, name=shot_sid.get('shot'))

    shot_gazu[sid_key] = str(shot_sid)
    shot_gazu = gazu.shot.update_shot(shot_gazu)

    logger.info(f"Created {shot_sid} / {shot_gazu}")
    assert(shot_sid == gazu_to_sid(shot_gazu))  # final check for correctness

    if as_gazu:
        return shot_gazu
    else:
        return shot_sid


def create_asset_task(task: Sid | str, do_create_parent: bool = False, as_gazu: bool = False) -> Sid | dict:

    task_sid = Sid(task).get_as('task')
    asset_sid = task_sid.get_as('asset')

    asset_gazu = get_asset(asset_sid, as_gazu=True)
    if not asset_gazu:
        if do_create_parent:
            asset_gazu = create_asset(asset_sid, as_gazu=True)
    if not asset_gazu:
        raise SpilException(f"No Asset found or created for task {task}. Cannot create Task.")

    task_sids = get_asset_tasks(asset_sid)
    if task_sid in task_sids:
        logger.info(f"Task already exists: {task}")
        return task_sid  # TODO as_gazu

    task_type = gazu.task.get_task_type_by_name(task_sid.get("step").capitalize())  # RULE
    if not task_type:
        raise SpilException(f"No step found for task {task}. Cannot create Task.")

    task_gazu = gazu.task.new_task(entity=asset_gazu, task_type=task_type, name=task_sid.get("task"))

    task_gazu["data"] = {sid_key: str(task_sid)}
    task_gazu = gazu.task.update_task(task_gazu)

    logger.info(f"Created {task_sid} / {task_gazu}")
    assert(task_sid == gazu_to_sid(task_gazu))  # final check for correctness

    if as_gazu:
        return task_gazu
    else:
        return task_sid


def create_shot_task(task: Sid | str, do_create_parent: bool = False, as_gazu: bool = False) -> Sid | dict:

    task_sid = Sid(task).get_as('task')
    shot_sid = task_sid.get_as('shot')
    task_sids = get_shot_tasks(shot_sid)

    if task_sid in task_sids:
        logger.info(f"Task already exists: {task}")
        return task_sid  # TODO as_gazu

    shot_gazu = get_shot(shot_sid, as_gazu=True)
    if not shot_gazu:
        if do_create_parent:
            shot_gazu = create_shot(shot_sid, do_create_parent=True, as_gazu=True)

    if not shot_gazu:
        raise SpilException(f"No shot found or created for task {task}. Cannot create Task.")

    task_type = gazu.task.get_task_type_by_name(task_sid.get("step").capitalize())  # RULE
    if not task_type:
        raise SpilException(f"No step found for task {task}. Cannot create Task.")

    task_gazu = gazu.task.new_task(entity=shot_gazu, task_type=task_type, name=task_sid.get("task"))

    task_gazu["data"] = {sid_key: str(task_sid)}
    task_gazu = gazu.task.update_task(task_gazu)

    logger.info(f"Created {task_sid} / {task_gazu}")
    assert(task_sid == gazu_to_sid(task_gazu))  # final check for correctness

    if as_gazu:
        return task_gazu
    else:
        return task_sid


########################
# Delete
########################

def delete_asset(asset: Sid | str, force: bool = False) -> bool:

    asset_sid = Sid(asset).get_as('asset')
    asset_gazu = get_asset(asset_sid, as_gazu=True)

    if not asset_gazu:
        logger.warning(f"{asset} does not exists")
        return False

    return gazu.asset.remove_asset(asset_gazu, force=force)  #FIXME: return ?


def delete_sequence(sequence: Sid | str, force: bool = False) -> bool:

    sequence_sid = Sid(sequence).get_as('sequence')
    sequence_gazu = get_sequence(sequence_sid, as_gazu=True)

    if not sequence_gazu:
        logger.warning(f"{sequence} does not exists")
        return False

    return gazu.shot.remove_sequence(sequence_gazu, force=force)  #FIXME: return ?


def delete_shot(shot: Sid | str, force: bool = False) -> bool:

    shot_sid = Sid(shot).get_as('shot')
    shot_gazu = get_shot(shot_sid, as_gazu=True)

    if not shot_gazu:
        logger.warning(f"{shot} does not exists")
        return False

    return gazu.shot.remove_shot(shot_gazu, force=force)  #FIXME: return ?


if __name__ == "__main__":
    from pprint import pprint

    pprint(get_asset("tp/a/character/jadelaide", as_gazu=True))

    # pprint(get_project_ids())
    pprint(get_asset_type_ids())

    print(get_asset_type_ids().get('fx'))

    #gazu.task.new_task_type()



