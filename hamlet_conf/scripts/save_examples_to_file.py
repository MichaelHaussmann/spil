from pathlib import Path

from scripts.example_sids import sids  # type: ignore
from spil_tests.prep.save_sid_list_to_file import write_sids_to_file

sid_file = Path(__file__).parent.parent / "data" / "hamlet.sids.txt"

print(sid_file)

write_sids_to_file(sids, sid_file)

