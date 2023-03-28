"""
This script loads test sids
and writes them into a test file.

This test file will be read in test scripts.

"""
from pathlib import Path

import spil  # default config path bootstrap
from scripts.generate_example_sids import sids  # type: ignore
from spil_tests.prep.save_sid_list_to_file import write_sids_to_file

sid_file = Path(__file__).parent.parent / "data" / "testing" / "hamlet.sids.txt"

if not sid_file.exists():
    print(f"Creating Sid test file: {sid_file}")
    write_sids_to_file(sids, sid_file)
    print(f"Done. {len(sids)} written to file")
else:
    print(f"Sid file exists, nothing written. File: {sid_file}")
