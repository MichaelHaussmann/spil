# type: ignore
"""
Demo configuration for the rest API.

Defines Finder and Getter instances for routes formatted as:
"/find/{config}/{search:path}"
where "config" is the name of the config.

"""
from spil import FindInList
from spil import FindInAll, GetFromAll, FindInPaths, GetFromPaths
# from spil_plugins.sg.get_sg import GetFromSG
# from spil_plugins.sg.find_sg import FindInSG
from spil_hamlet_conf.hamlet_scripts.example_sids import sids


# Example:
# "/find/all/hamlet/*"
# will call FindInAll().find()
finder_config = {
    # 'sg': FindInSG(),
    'all': FindInAll(),
    'paths': FindInPaths(),
    'ls': FindInList(list(sids))
}


# Example:
# "/get/all/hamlet/*"
# will call GetFromAll().get()
getter_config = {
    # 'sg': GetFromSG(),
    'all': GetFromAll(),
    'paths': GetFromPaths()
}
