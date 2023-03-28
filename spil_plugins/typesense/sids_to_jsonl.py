import os
from pathlib import Path
import json

from spil import Sid
from scripts.example_sids import sids  # type: ignore


def write_to(path):
    """
    http://www.dabeaz.com/coroutines/

    Args:
        path:

    Returns:

    """
    with path.open(mode="w") as f:
        print(f"Opened {path}")
        while True:
            data = yield
            f.write(json.dumps(data) + os.linesep)


# shots_jsonl = Path().resolve(strict=True) / "data" / "tests" / "shots.jsonl"
# assets_jsonl = Path().resolve(strict=True) / "data" / "tests" / "assets.jsonl"
all_jsonl = Path().resolve(strict=True) / "data" / "tests" / "all.jsonl"

# assets_jsonl.parent.mkdir(parents=True, exist_ok=True)
# shots_jsonl.parent.mkdir(parents=True, exist_ok=True)
all_jsonl.parent.mkdir(parents=True, exist_ok=True)

# to_shots = write_to(shots_jsonl)
# to_assets = write_to(assets_jsonl)
to_all = write_to(all_jsonl)

# to_assets.send(None)
# to_shots.send(None)
to_all.send(None)

to_pop = ['type', 'assettype', 'asset', 'sequence', 'shot']
for _sid in sids:
    sid = Sid(_sid)

    if not sid:
        print(f"not a sid: {_sid}")

    data = {}
    data.update(sid.fields)
    for key in to_pop:
        if key in data:
            data.pop(key)
    data.update(
        {
            "id": str(sid).replace("/", "_"),
            "text": str(sid).replace("/", " "),
            "type": sid.type,
            "sid": str(sid),
            "length": len(sid),
        }
    )
    print(data)

    to_all.send(data)

    # if sid.get("type") == "s":
    #     to_shots.send(data)
    # else:
    #     to_assets.send(data)
