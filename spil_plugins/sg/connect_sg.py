from shotgun_api3 import shotgun
from spil_plugins.sg import conf  # FIXME: make parent package indepentent

sg = None

def get_sg():
    """
    Returns a connected SG.
    If a connection already exists, returns it.
    TODO: closing mechanism (for long running scripts)
    :return:
    """
    global sg
    if not sg:
        sg = shotgun.Shotgun(conf.sg_host, conf.sg_log_in[0], conf.sg_log_in[1])
    return sg


if __name__ == "__main__":
    print(get_sg())
    print(get_sg())
    from pprint import pprint


