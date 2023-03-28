from spil_fs_conf import *  # type: ignore

# for test and demo purposes
from pathlib import Path
project_server_root_path = Path(__file__).parent / "data" / "testing" / "SPIL_PROJECTS" / "SERVER" / "PROJECTS"

path_templates = path_templates.copy()  # type: ignore

# Replace this by your own folder root, eg
# path_templates['project_root'] = r'/home/mh/Desktop/SPIL_PROJECTS/SERVER/PRJ'
path_templates['project_root'] = str(project_server_root_path)


