"""
This doctest from Sid turned out to not work,
because user configuration (~/.spil) contained a different default path,
after a test set it to "server" instead of "local", the factory default.

"""

from pathlib import Path
from spil import conf, Sid
from spil import log
from resolva import utils as rut

rut.log.setLevel(10)

log.setLevel(10)

path = Path(conf.default_sid_conf_data_path) / "testing/SPIL_PROJECTS/LOCAL/PROJECTS/HAMLET/PROD/ASSETS/char/ophelia/model/v001/char_ophelia_model_WORK_v001.ma"
print(path)
s = Sid(path=path)  # path (default config) # TODO: any config

print(s.uri)
# Sid('asset__file:hamlet/a/char/ophelia/model/v001/w/ma')