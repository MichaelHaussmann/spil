from __future__ import annotations
from typing import List, Mapping
from spil import Sid, SpilException


def from_sid_build_searches(sid: Sid | str) -> Mapping[Sid, str]:
    """
    Given a Sid, generates search sids by filling fields with * and **
    These searches can then be used for tests.

    The given sid is included in the search sids.

    :param sid:
    :return:
    """
    _sid: Sid = Sid(sid)
    if not _sid:
        raise SpilException(f'Given sid "{sid}" does not resolve to a valid Sid.')

    searches = {}
    searches[_sid] = f"Plain {_sid.type} Sid"

    for key in reversed(list(_sid.fields.keys())):

        search = _sid.get_as(key).get_with(key=key, value='**')
        searches[search] = f"Find all under {key} (**)"

        ext = _sid.get('ext') or '*'
        search = _sid.get_as(key).get_with(key=key, value='**') / ext
        searches[search] = f'Find all under {key} with "{ext}" extension'

        search = _sid.get_as(key).get_with(key=key, value='*')
        searches[search] = f"Find all {key}s"

        search = _sid.get_with(key=key, value='*')
        searches[search] = f"{_sid.type} with all {key}"

        for subkey in list(_sid.fields.keys()):
            if subkey == key:
                continue
            subsearch = search.get_with(key=subkey, value='*')
            searches[subsearch] = f"{search.type} with all {key} and {subkey}"
            for subsubkey in list(_sid.fields.keys()):
                if (subsubkey == key) or (subsubkey == subkey):
                    continue
                subsubsearch = subsearch.get_with(key=subsubkey, value='*')
                searches[subsubsearch] = f"{subsearch.type} with all {key}, {subkey} and {subsubkey}"

    return dict(reversed(sorted(searches.items())))


if __name__ == '__main__':

    from pprint import pformat
    from spil import Sid, FindInPaths, setLevel
    from spil.util.log import DEBUG, INFO, WARN, ERROR

    setLevel(ERROR)

    show_max = 10
    config = ''
    sid = Sid('hamlet/a/char/claudius/model/v001/p/ma')

    print("Starting !")

    searches = from_sid_build_searches(sid)
    for search, label in searches.items():
        print(f"search: {search} <=> \t\t\t{label}")

    print(" ")

    input("start ?")
    finder = FindInPaths(config)

    for search, label in searches.items():

        print(f"search: {search} / {label}")
        i = -1
        path_proof = ''

        for i, found in enumerate(finder.find(search)):
            bingo = ' ------> Bingo' if found == sid else ""
            if bingo or (i <= show_max):
                if config:
                    path_proof = f" ({str(found.path(config))[0:50]}...) "
                print(f"\t{found}{path_proof} {bingo}")
            if i == show_max + 1:
                print('...')

        print(f'Total found: {i+1}')
        print(' ')
        print('-' * 20)
