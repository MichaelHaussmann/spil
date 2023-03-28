
from pathlib import Path

from spil_plugins.typesense.connect_ts import get_ts

# shots_jsonl = Path().resolve(strict=True) / "data" / "tests" / "shots.jsonl"
# assets_jsonl = Path().resolve(strict=True) / "data" / "tests" / "assets.jsonl"
all_jsonl = Path().resolve(strict=True) / "data" / "tests" / "all.jsonl"

client = get_ts()

with all_jsonl.open() as jsonl_file:
  client.collections['all'].documents.import_(jsonl_file.read().encode('utf-8'))
