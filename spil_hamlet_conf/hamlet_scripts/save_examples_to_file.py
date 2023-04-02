"""
This script loads test sids
and writes them into a test file.

This test file will be read in test scripts.

"""
from pathlib import Path
from spil import conf
from hamlet_scripts.generate_example_sids import sids  # type: ignore
from spil.tests.prep.save_sid_list_to_file import write_sids_to_file

sid_file = Path(conf.default_sid_conf_data_path) / "testing" / "hamlet.sids.txt"

if not sid_file.exists():
    print(f"Creating Sid test file: {sid_file}")
    write_sids_to_file(sids, sid_file)
    print(f"Done. {len(sids)} written to file")
else:
    print(f"Sid file exists, nothing written. File: {sid_file}")
