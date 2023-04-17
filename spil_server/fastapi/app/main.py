"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations
from pathlib import Path
from fastapi import FastAPI
from starlette.requests import Request

"""


* This is work in progress *
* Not production ready *


https://fastapi.tiangolo.com/deployment/docker/ (includes a nice intro to dockers)
https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker

Mount volume in Windows:
https://medium.com/@kale.miller96/how-to-mount-your-current-working-directory-to-your-docker-container-in-windows-74e47fa104d7

uvicorn main:app --reload
"""
try:
    import spil
except ImportError:
    root = Path(__file__).resolve().parent.parent.parent.parent
    import sys  # fmt: skip
    sys.path.append(root.as_posix())

from spil import Finder, Getter

try:
    import spil_rest_conf as rest_conf  # type: ignore
except ImportError:
    from spil.conf import sid_conf_import_error_message  # fmt: skip
    problem = sid_conf_import_error_message.format(module="spil_rest_conf")
    print(problem)
    rest_conf = None


app = FastAPI()


@app.get("/find/{config}/{search:path}")
def find(config: str, search: str, request: Request):
    """
    Returns Sids for named "config" and given "search" sid.

    Args:
        config: name of a config
        search: search sid
        request: optional request (is automatically handled)

    Returns:
        the retrieved sids, as json list.

    """
    finder: Finder | None = rest_conf.finder_config.get(config)
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
    """
    Returns Sids and data for named "config" and given "search" sid.

    Args:
        config: name of a config
        search: search sid
        request: optional request (is automatically handled)

    Returns:
        the retrieved data, as json list.
    """
    getter: Getter | None = rest_conf.getter_config.get(config)
    if not getter:
        print(f"Finder not found for {config}")
        return []

    print(f"Getter: {getter}")
    search = f"{search}{('?' + str(request.query_params)) if request.query_params else ''}"
    print(f"{search}")

    for data in getter.get(search):
        yield data
