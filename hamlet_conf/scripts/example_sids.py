# -*- coding: utf-8 -*-
"""
This script generates example Sids, to test the configuration and the SPIL features towards the data.

"""
import random
from math import ceil
from time import sleep

from sid_conf import projects, asset_types, asset_tasks
from sid_conf import extensions_scene, extensions_movie, shot_tasks, extensions_cache
from logging import debug


do_intermediates = True  # If this is False, only leave paths will be generated. See: LS extrapolate.
repeat_times = 1  # 3
num_sequences = 6  # 12
num_shots = 12  # 24
num_versions = 4  # 12

sid_types = ['a', 's']

asset_names = {
                'char': ['hamlet', 'claudius', 'ghost', 'ophelia', 'gertrude', 'horatio', 'polonius'],
                'location': ['elsinore', 'ramparts', 'queens_chamber', 'garden', 'lakeside'],
                'prop': ['sword', 'throne', 'dagger', 'skull', 'crown', 'tapestry'],
                'fx': ['mist', 'blood', 'thunder', 'rain', 'water'],
}

all_assets = sum(asset_names.values(), [])

task_extensions = {
    'art': ['psd', 'mov', 'mp4'],
    'model': ['ma', 'hip', 'blend', 'mp4'],
    'surface': ['ma', 'hip', 'blend', 'mp4'],
    'rig': ['ma', 'hip', 'blend', 'mp4'],
    'board': ['psd', 'mov'],
    'layout': ['ma', 'mb', 'hip', 'blend', 'mp4'],
    'anim': ['mb', 'hip', 'abc', 'mp4'],
    'fx': ['hip', 'abc', 'vdb', 'mp4', 'mov'],
    'render': ['ma', 'mb', 'hip', 'blend', 'mp4', 'mov', 'avi'],
    'comp': ['nk', 'mp4', 'mov'],
}

states = ['w', 'p']

extensions = extensions_scene + extensions_movie + extensions_cache

sequences = ['sq{}'.format(str(x*10). zfill(3)) for x in range(1, num_sequences)]
shots = ['sh{}'.format(str(x*10). zfill(4)) for x in range(1, num_shots)]
versions = ['v{}'.format(str(x). zfill(3)) for x in range(1, num_versions)]


def append(sids, data):
    sid = '/'.join(data)
    sids.append(sid)


sids = []
for i in range(repeat_times):
    for project in projects:
        debug('Generating project: {}'.format(project))
        for sid_type in sid_types:
            debug('Generating type: {}'.format(sid_type))
            data = [project, sid_type]
            if do_intermediates: append(sids, data)

            if sid_type in ['a']:

                for assettype in asset_types:
                    data = [project, sid_type, assettype]
                    if do_intermediates: append(sids, data)

                    for name in asset_names.get(assettype):
                        data = [project, sid_type, assettype, name]
                        if do_intermediates: append(sids, data)

                        for task in asset_tasks:
                            data = [project, sid_type, assettype, name, task]
                            if do_intermediates: append(sids, data)

                            for version in versions:
                                data = [project, sid_type, assettype, name, task, version]
                                if do_intermediates: append(sids, data)

                                for state in states:
                                    data = [project, sid_type, assettype, name, task, version, state]
                                    if do_intermediates: append(sids, data)

                                    k = ceil(len(task_extensions.get(task)) / 2)
                                    for ext in random.sample(task_extensions.get(task), k=k):  # random.choices >py 3.6
                                        data = [project, sid_type, assettype, name, task, version, state, ext]
                                        append(sids, data)

            if sid_type in ['s']:

                for seq in sequences:
                    data = [project, sid_type, seq]
                    if do_intermediates: append(sids, data)

                    for shot in shots:
                        data = [project, sid_type, seq, shot]
                        if do_intermediates: append(sids, data)

                        for task in shot_tasks:
                            data = [project, sid_type, seq, shot, task]
                            if do_intermediates: append(sids, data)

                            for version in versions:
                                data = [project, sid_type, seq, shot, task, version]
                                if do_intermediates: append(sids, data)

                                for state in states:
                                    data = [project, sid_type, seq, shot, task, version, state]
                                    if do_intermediates: append(sids, data)

                                    k = ceil(len(task_extensions.get(task)) / 2)
                                    for ext in random.sample(task_extensions.get(task), k=k):
                                        if ext in extensions_cache and state == 'p':
                                            node = random.choice(all_assets)
                                            data = [project, sid_type, seq, shot, task, version, state, node, ext]
                                        else:
                                            data = [project, sid_type, seq, shot, task, version, state, ext]
                                        append(sids, data)

sids = sorted(list(set(sids)))


if __name__ == '__main__':

    import sys
    # from spil_tests import Timer

    from spil.util.log import DEBUG, ERROR, get_logger

    log = get_logger("spil_tests")
    log.setLevel(DEBUG)

    from spil import Sid
    from pprint import pprint
    print('Start')
    #pprint(sids)

    #global_timer = Timer(name="global", logger=log.debug)
    #global_timer.start()

    print(len(sids))

    y = input("print out detail ?")

    if y != 'y':
        sys.exit()

    for i, s in enumerate(sids):
        sid = Sid(s)
        if not sid:
            print(f"---------------------------------> {sid}")
            sleep(1)
        if i % 20 == 0:
            print(f"{i} -- {repr(sid)}",)

    # global_timer.stop()
    print('Done')

    print(len(sids))

