"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from spil.sid.core.utils import expand


def execute(sids):
    """
    Expands multi-search characters like /** into a series of /*.
    The ** must exist only once.
    If values are present after the ** they are supposed to be the end of the sids.

    :param sids:
    :return:
    """
    result = []
    for sid in sids:
        result.extend(expand(sid, do_extrapolate=False))

    return result


if __name__ == "__main__":

    from pprint import pprint
    from spil.util.log import setLevel, info, INFO, debug, DEBUG

    info("Tests start")

    setLevel(INFO)

    expandables = [
        "hamlet/s/*/**/ma",
        "hamlet/a/**/v002/*/ma",
        "hamlet",
        "hamlet/a/**",
        "hamlet/s/sq010/sh0010/anim/**/abc",
        "hamlet/s/**/mov",
        "hamlet/s/sq010/sh0010/**/ma",
        "hamlet/s/sq001/sh0020/**",
    ]

    expandables_with_query = [
        "hamlet/s/*/**/ma?version=2",
        "hamlet/s/*/**/ma?version=v002",
        "hamlet/a/**/v002/*/ma?whatever",
        "hamlet/s/sq010/sh0010/**/ma?yes?yes",
        "hamlet/s/sq001/sh0020/**?state=w&version=>",
    ]

    for sid in expandables + expandables_with_query:
        print(" ")
        print(sid + " -->")
        results = expand(sid, do_extrapolate=False)
        # print('Expanded to -->' + str(results))
        for result in results:
            print(result.type)
            print(result.string)
            # print(sid_to_dict(result, result.type))

        pprint(results)

        print("*" * 10)
