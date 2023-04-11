"""
uvicorn main:app --reload
"""
from __future__ import annotations
from typing import Any, Optional, List

from pathlib import Path
from fastapi import FastAPI
from starlette.requests import Request

try:
    import spil
except ImportError:
    root = Path(__file__).resolve().parent.parent.parent.parent
    import sys
    sys.path.append(root.as_posix())

from spil import Sid, Finder, Getter, FindInList
from spil import FindInAll, GetFromAll, FindInPaths, GetFromPaths
# from spil_plugins.sg.get_sg import GetFromSG
# from spil_plugins.sg.find_sg import FindInSG
from spil_hamlet_conf.hamlet_scripts.example_sids import sids

app = FastAPI()

finder_config = {
    # 'sg': FindInSG(),
    'all': FindInAll(),
    'paths': FindInPaths(),
    'ls': FindInList(list(sids))
}

getter_config = {
    # 'sg': GetFromSG(),
    'all': GetFromAll(),
    'paths': GetFromPaths()
}

@app.get("/find/{config}/{search:path}")
def find(config: str, search: str, request: Request):
    finder: Finder | None = finder_config.get(config)
    if not finder:
        print(f"Finder not found for {config}")
        return []

    print(f"Finder: {finder}")
    search = f"{search}{('?' + str(request.query_params)) if request.query_params else ''}"
    print(f"{search}")

    for sid in finder.find(search):
        yield {"sid": sid.uri}

@app.get("/get/{config}/{search:path}")
def get(config: str, search: str, request: Request):
    getter: Getter | None = getter_config.get(config)
    if not getter:
        print(f"Finder not found for {config}")
        return []

    print(f"Getter: {getter}")
    search = f"{search}{('?' + str(request.query_params)) if request.query_params else ''}"
    print(f"{search}")

    for data in getter.get(search):
        yield data
