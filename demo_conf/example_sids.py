# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
import random
from sid_conf import projects, asset_cats, asset_tasks, extensions_scene, extensions_movie, shot_tasks
from spil.util.log import debug, setLevel, INFO, DEBUG, info

"""
Example Sid generator, to play and test the config.

"""

setLevel(INFO)

sid_types = ['a', 's']
asset_names = {
                'char': ['romeo', 'juliet', 'mercurio'],
                'location': ['house_juliet', 'street_verona', 'crypt', 'piazza'],
                'prop': ['balcony', 'tree', 'dagger', 'potion'],
                'fx': ['potion', 'blood'],
                'dmp': ['sunset', 'verona'],
}

states = ['w', 'p']

variants = ['main', 'low']
subtasks = ['main']

extensions_movie = ['mp4', 'mov', 'avi']
extensions_scene = ['ma', 'mb', 'hip', 'nk']
extensions = extensions_scene + extensions_movie

sequences = ['sq{}'.format(str(x). zfill(3)) for x in range(1, 10)]
shots = ['sh{}'.format(str(x*10). zfill(4)) for x in range(1, 20)]
versions = ['v{}'.format(str(x). zfill(3)) for x in range(1, 8)] + ['valid']
# frames = ['$F4', '###', '@', '123' ]  # TODO : implement + find a solution to avoid searching on all frames separately


def append(sids, data):
    sid = '/'.join(data)
    sids.append(sid)


do_intermediates = True  # If this is False, only leave paths will be generated. See: LS extrapolate.
repeat_times = 1


sids = []
for i in range(repeat_times):
    for project in projects:
        debug('Generating project: {}'.format(project))
        for sid_type in sid_types:
            debug('Generating type: {}'.format(sid_type))
            data = [project, sid_type]
            if do_intermediates: append(sids, data)

            if sid_type in ['a']:

                for cat in asset_cats:
                    data = [project, sid_type, cat]
                    if do_intermediates: append(sids, data)

                    for name in asset_names.get(cat):
                        data = [project, sid_type, cat, name]
                        if do_intermediates: append(sids, data)

                        for variant in variants:
                            data = [project, sid_type, cat, name, variant]
                            if do_intermediates: append(sids, data)

                            for task in asset_tasks:
                                data = [project, sid_type, cat, name, variant, task]
                                if do_intermediates: append(sids, data)

                                for version in versions:
                                    data = [project, sid_type, cat, name, variant, task, version]
                                    if do_intermediates: append(sids, data)

                                    for state in states:
                                        data = [project, sid_type, cat, name, variant, task, version, state]
                                        if do_intermediates: append(sids, data)

                                        for ext in random.sample(extensions, k=3):  # random.choices >py 3.6
                                            data = [project, sid_type, cat, name, variant, task, version, state, ext]
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

                            for subtask in subtasks:
                                data = [project, sid_type, seq, shot, task, subtask]
                                if do_intermediates: append(sids, data)

                                for version in versions:
                                    data = [project, sid_type, seq, shot, task, subtask, version]
                                    if do_intermediates: append(sids, data)

                                    for state in states:
                                        data = [project, sid_type, seq, shot, task, subtask, version, state]
                                        if do_intermediates: append(sids, data)

                                        for ext in random.sample(extensions, k=3):  # random.choices >py 3.6
                                            data = [project, sid_type, seq, shot, task, subtask, version, state, ext]
                                            append(sids, data)

sids = sorted(list(set(sids)))


if __name__ == '__main__':

    from pprint import pprint
    print('Start')
    pprint(sids)

    print('Done')

    print(len(sids))

