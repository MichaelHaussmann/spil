"""
This script writes random data to test WriteToPaths.
(and prepares test of GetFromPaths)

WriteToPaths writes data as hidden "sidecar" json files close to the sid path.
"""
import random
from pprint import pprint

from spil import Sid, WriteToPaths
from scripts.example_sids import sids  # type: ignore
from spil.util.log import setLevel, INFO, get_logger

from faker import Faker

fake = Faker()
Faker.seed(26)

log = get_logger("spil_tests")

if __name__ == "__main__":

    setLevel(INFO)

    writer = WriteToPaths(config="local")

    random.seed(26)
    random.shuffle(sids)

    for _sid in sids[:50]:
        sid = Sid(_sid)
        print(sid)

        if not sid.path():
            log.info(f"{sid} has no path, skipped.")
            continue

        data = {
            "author": fake.name(),
            "created": sid.path().stat().st_mtime,
            "updated": fake.date_time(),
            "path": sid.path().stem,
            "comment": fake.sentence(),
            "status": fake.color(),
            "code": fake.isbn13(),
        }

        # writer.delete(sid)

        done = writer.update(sid, data)
        print(Sid(sid).path())
        pprint(data)
        print(f"Update: {done}")

        done = writer.set(sid, status=fake.color(), random_attribute="random value")
        print(f"Set: {done}")

        done = writer.set(sid, attribute="updated", value=fake.date_time())
        print(f"Set: {done}")
