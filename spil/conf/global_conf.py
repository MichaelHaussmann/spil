# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2022 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
import os

pysep = "/"  # python path separator

__version__ = "0.1.0"
application_codename = "Artichoke"
application_name = 'SPIL The Simple Pipeline Lib - v{0} ("{1}")'.format(
    __version__, application_codename
)

application_repo_path = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
).replace(os.sep, pysep)

# automatic replacement to INFO and WARN in BETA and PROD
loglevel = 80

user_app_folder_name = "spil/conf"
user_conf_file_name = "user_conf.json"

# TODO: move these into sid_conf
sip = "/"  # sid separator - changing this is untested.
ors = ","  # "or" separator
qms = "#"  # question mark read sign (previously '?', thus it's name)
sidtype_keytype_sep = "__"
search_symbols = ["*", ",", ">", "<", "**"]

sid_conf_import_error_message = """
    -------------------------------------------------------------------------------------------------------------
    CONFIGURATION PROBLEM: 

    The configuration module "{module}" was not found.

    Ensure to either include "demo_conf" in your python path, 
    or create your own "{module}" and add its folder to the python path.    

    (If you are running a py.test edit the SPIL_CONF_PATH variable in tests/test_00_init.py to match a python path.)

    Please see installation and configuration documentation.

    -------------------------------------------------------------------------------------------------------------
    """
