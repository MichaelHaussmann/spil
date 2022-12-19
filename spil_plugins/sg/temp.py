"""
SG read functions.

See doc

Filter syntax:
https://developer.shotgridsoftware.com/python-api/reference.html#operators-and-arguments

“field hopping”
https://developer.shotgridsoftware.com/python-api/usage_tips.html
['project.Project.name', 'is', project_name]

TODO: implement “field hopping” and global sid mapping.

"""

from __future__ import annotations  # py37 compatibility

from pprint import pformat
import logging
from typing import Iterator

import sid_conf
from spil import Sid, LS

from silexsg.core.util import sid_format
from silexsg.core.util.log import get_logger
from silexsg.core.util.caching import lru_cache as cache
from silexsg.conf import sg_project_ids as project_ids, sg_conf
from silexsg.core.sg.connect_sg import get_sg
from silexsg.core.util.exception import raiser, SilexSGException


sg = get_sg()
logger = get_logger("silex_sg", logging.DEBUG)

# sid_key = "sg_sid"  # shotgun_id or code, currently testing


@cache
def get_project_id(project: Sid | str) -> int:
    """
    For a given project Sid or string, returns the project SG identifier.

    :param project:
    :return:
    """
    id = 0
    try:
        project_sid = Sid(project)
        id = project_ids.get(project_sid.get('project'))
    except Exception as e:
        logger.warn(f'Problem getting ID for given project: "{project}". Exception: {e}')
    if id:
        return id
    else:
        raise SilexSGException(f'No project ID found for given project: "{project}"')


def get_assets(project: Sid | str) -> Iterator[Sid]:
    """
    For a given project Sid or string,
    Returns an Iterator on all assets as Sids.

    :param project:
    :return:
    """

    project_sid = Sid(project).get_as('project')
    if not project_sid:
        raise SilexSGException(f'No valid Project Sid for {project}.')

    found = set()
    project_id = get_project_id(project_sid)
    filters = [
        ['id', 'is_not', None],
        ['project', 'is', {'type': 'Project', 'id': project_id}]
    ]
    fields = ["code", "sg_asset_type"]
    # fields = list(sg.schema_field_read('Asset').keys())  # all fields
    order = [{'field_name': 'sg_asset_type', 'direction': 'asc'},
             {'field_name': 'code', 'direction': 'asc'}]
    assets = sg.find("Asset", filters, fields, order)
    for a in assets:
        result = {k: v for k, v in a.items() if v}
        logger.debug(f"Found : {a.get('code')} ({pformat(result)})")
        name = sid_format(a.get('code'))
        asset_type = sid_format(a.get('sg_asset_type'))
        asset_sid = project_sid / 'a' / asset_type / name
        if not asset_sid.type:
            logger.warning(f'WARN: this asset is not conform, ignored: "{asset_sid}" ({a})')
            continue
        if asset_sid not in found:
            found.add(asset_sid)
            yield asset_sid


def get_shots(project: Sid | str) -> Iterator[Sid]:
    """
    For a given project Sid or string,
    Returns an Iterator on all shots as Sids.

    :param project:
    :return:
    """

    project_sid = Sid(project).get_as('project')
    if not project_sid:
        raise SilexSGException(f'No valid Project Sid for {project}.')

    found = set()
    project_id = get_project_id(project_sid)
    filters = [
        ['id', 'is_not', None],
        ['project', 'is', {'type': 'Project', 'id': project_id}]
    ]
    fields = ['code', 'tasks', 'sg_sid']
    order = [{'field_name': 'code', 'direction': 'asc'}]
    shots = sg.find("Shot", filters, fields, order)
    for s in shots:
        logger.debug(f"Found shot: {s.get('code')} ({s})")
        try:
            sq, sh = s.get('code').split('_')
            shot_sid = project_sid / 's' / sq / sh
            if not shot_sid.type:
                logger.warning(f'WARN: this shot is not conform, ignored: "{shot_sid}" ({s})')
                continue
            if shot_sid not in found:
                found.add(shot_sid)
                yield shot_sid

        except Exception as ex:
            logger.warning(f"Something went wrong with shot {s}, skipped. Error: {ex}")


def get_asset_tasks(project: Sid | str, asset: Sid | str = None, include_na: bool = False) -> Iterator[Sid]:  # IDEA: allow "tp/a/character", "tp/a/character/*", "tp/a/*/michael",
    """
    For a given project Sid or string,
    Returns an Iterator on all Tasks as Sids.

    If an asset Sid or string is given, only Tasks for the given asset are yielded.

    The Task Sid contains:
    project / a / assettype / name / step / task

    By default NA tasks are skipped.
    If include_na is set to True, NA tasks will be included.

    If a Shotgrid Task is malformed or doesn't compy with the naming convention, it is ignored.
    Only valid Sids are returned.

    Additionally to the Sid validation, the Tasks go through a sg_conf.special_task_check function.

    :param asset:
    :param project:
    :param include_na:
    :return:
    """
    project_sid = Sid(project).get_as('project')
    if not project_sid:
        raise SilexSGException(f'No valid Project Sid for {project}.')

    project_id = get_project_id(project_sid)
    filters = [
        ["project", "is", {'type': 'Project', 'id': project_id}],
        ["entity", "type_is", "Asset"],
        #["entity.Asset.sg_sid", "is", "tp/a/character/michael"],  # unable to query a custom field
    ]
    if asset:
        asset = Sid(asset) or raiser(f'Given asset "{asset}" is not valid')
        filters.append(["entity.Asset.sg_asset_type", "is", asset.get('assettype')])
        filters.append(["entity.Asset.code", "is", asset.get('asset')])
    if not include_na:
        filters.append(["sg_status_list", "is_not", "na"])

    fields = ["content", "step", "entity.Asset.code", "entity.Asset.sg_asset_type", "sg_sid"]
    order = [{'field_name': 'sg_asset_type', 'direction': 'asc'},
             {'field_name': 'code', 'direction': 'asc'},
             {'field_name': 'step', 'direction': 'asc'},
             {'field_name': 'content', 'direction': 'asc'}]
    tasks = sg.find("Task", filters, fields, order)
    found = set()
    for t in tasks:
        logger.debug(f"Found task: {t.get('content')} ({t})")
        try:
            #print(f"Digesting: {t}")
            assettype = sid_format(t.get("entity.Asset.sg_asset_type"))
            name = sid_format(t.get("entity.Asset.code"))
            step = sid_format(t.get('step').get('name'))
            task = sid_format(t.get('content') or '')
            if step.startswith(task):  # RULE : "compositing" starts with "comp" --> main.
                task = "main"  # RULE
            task_sid = project_sid / 'a' / assettype / name / step / task
            if not task_sid.type:
                logger.warning(f'WARN: this task is not conform, ignored: "{task_sid}" ({t})')
                continue
            if not sg_conf.special_task_check('a', step, task):
                logger.warning(f'WARN: this task is not conform, skipped: "{task_sid}" ({t})')
                continue
            if task_sid not in found:
                found.add(task_sid)
                yield task_sid

        except Exception as ex:
            logger.warning(f"Something went wrong with task {t}, skipped. Error: {ex}")


def get_shot_tasks(project: Sid, shot: Sid | str = None, include_na: bool = False) -> Iterator[Sid]:
    """
    For a given project Sid or string,
    Returns an Iterator on all Tasks as Sids.

    If a shot Sid or string is given, only Tasks for the given shot are yielded.

    The Task Sid contains:
    project / s / sequene / shot / step / task

    By default NA tasks are skipped.
    If include_na is set to True, NA tasks will be included.

    If a Shotgrid Task is malformed or doesn't compy with the naming convention, it is ignored.
    Only valid Sids are returned.

    Additionally to the Sid validation, the Tasks go through a sg_conf.special_task_check function.

    :param shot:
    :param asset:
    :param project:
    :param include_na:
    :return:
    """
    project_sid = Sid(project).get_as('project')
    if not project_sid:
        raise SilexSGException(f'No valid Project Sid for {project}.')

    project_id = get_project_id(project_sid)
    filters = [
        ["project", "is", {'type': 'Project', 'id': project_id}],
        ["entity", "type_is", "Shot"],
    ]
    if shot:
        shot = Sid(shot) or raiser(f'Given shot "{shot}" is not valid')
        shot_code = f"{shot.get('sequence')}_{shot.get('shot')}"  #IDEA use 'starts_with' / 'ends_with' to implement sequence and/or shot search with *
        filters.append(["entity.Shot.code", "is", shot_code])
    if not include_na:
        filters.append(["sg_status_list", "is_not", "na"])

    fields = ["content", "step", "entity.Shot.code", "sg_sid"]
    order = [{'field_name': 'code', 'direction': 'asc'},
             {'field_name': 'step', 'direction': 'asc'},
             {'field_name': 'content', 'direction': 'asc'}]
    tasks = sg.find("Task", filters, fields, order)
    found = set()
    for t in tasks:
        logger.debug(f"Found task: {t.get('content')} ({t})")
        try:
            #print(f"Digesting: {t}")
            sq, sh = t.get('entity.Shot.code').split('_')
            step = sid_format(t.get('step').get('name'))
            task = sid_format(t.get('content') or '')
            if step.startswith(task):  # RULE : "compositing" starts with "comp" --> main.
                task = "main"  # RULE
            task_sid = project_sid / 's' / sq / sh / step / task
            if not task_sid.type:
                logger.warning(f'WARN: this task is not conform, ignored: "{task_sid}" ({t})')
                continue
            if not sg_conf.special_task_check('s', step, task):
                logger.warning(f'WARN: this task is not conform, skipped: "{task_sid}" ({t})')
                continue
            if task_sid not in found:
                found.add(task_sid)
                yield task_sid

        except Exception as ex:
            logger.warning(f"Something went wrong with task {t}, skipped. Error: {ex}")


def get_sorted_asset_tasks(project: Sid | str, asset: Sid | str = None, include_na: bool = False) -> Iterator[Sid]:
    """
    For a given project Sid or string,
    Returns an Iterator on all Tasks as Sids.

    Tasks arrive sorted by assettype (alphabetic) / asset (alphabetic) / step (configuration order) / task (configuration order).

    If an asset Sid or string is given, only Tasks for the given asset are yielded.

    The Task Sid contains:
    project / a / assettype / name / step / task

    By default NA tasks are skipped.
    If include_na is set to True, NA tasks will be included.

    If a Shotgrid Task is malformed or doesn't compy with the naming convention, it is ignored.
    Only valid Sids are returned.

    Additionally to the Sid validation, the Tasks go through a sg_conf.special_task_check function.

    :param project:
    :param asset:
    :param include_na:
    :return:
    """

    all_tasks = [str(t) for t in get_asset_tasks(project=project, asset=asset, include_na=include_na)]
    list_search = LS(all_tasks)

    for asset in get_assets(project):
        for step in sid_conf.asset_steps:
            for task in sid_conf.asset_tasks:
                to_find = asset / step / task
                if to_find:  # if it is a valid Sid
                    founds = list_search.get(to_find)
                    for s in founds:
                        yield s


def get_sorted_shot_tasks(project: Sid, shot: Sid | str = None, include_na: bool = False) -> Iterator[Sid]:
    """
    For a given project Sid or string,
    Returns an Iterator on all Tasks as Sids.

    Tasks arrive sorted by shot (alphabetic) / step (configuration order) / task (configuration order).

    If a shot Sid or string is given, only Tasks for the given shot are yielded.

    The Task Sid contains:
    project / s / sequence / shot / step / task

    By default NA tasks are skipped.
    If include_na is set to True, NA tasks will be included.

    If a Shotgrid Task is malformed or doesn't compy with the naming convention, it is ignored.
    Only valid Sids are returned.

    Additionally to the Sid validation, the Tasks go through a sg_conf.special_task_check function.

    :param project:
    :param shot:
    :param include_na:
    :return:
    """

    all_tasks = [str(t) for t in get_shot_tasks(project=project, shot=shot, include_na=include_na)]
    list_search = LS(all_tasks)

    for shot in get_shots(project):
        for step in sid_conf.shot_steps:
            for task in sid_conf.shot_tasks:
                to_find = shot / step / task
                if to_find:  # if it is a valid Sid
                    founds = list_search.get(to_find)
                    for s in founds:
                        yield s


def get_event_log_entry(id: int) -> dict:

    filters = [
        ['id', 'is', id],
    ]
    fields = ['entity.ActionMenuItem.sg_action', 'entity.ActionMenuItem.url', 'entity', 'event_type', 'meta', 'project']
    # fields = list(sg.schema_field_read('EventLogEntry').keys())  # all fields

    result = sg.find_one("EventLogEntry", filters, fields)

    return result


if __name__ == "__main__":
    from pprint import pprint
    import sys

    pprint(get_event_log_entry(1765763))

    sys.exit()

    project = Sid("tp")

    for s in get_shots(project):
        pprint(s)
        pass

    for t in get_shot_tasks(project, shot="tp/s/s01/p010"):
        pprint(t)

    for t in get_asset_tasks(project, asset="tp/a/character/michael"):
        pprint(t)
        pass

    for a in get_assets(project):
        print(a)
        pass

    pprint(list(get_sorted_asset_tasks(project)))
    pprint(list(get_sorted_shot_tasks(project)))
