import gazu
from spil_plugins.kitsu import conf


def connect():
    """
    Returns a connected SG.
    If a connection already exists, returns it.

    :return:
    """
    gazu.client.set_host(conf.gazu_host)
    gazu.log_in(*conf.gazu_log_in)
    print(f"Gazu connected to {conf.gazu_host}")
    return gazu


if __name__ == "__main__":

    print(connect())
    try:
        #gazu.user.all_open_projects()
        print('logged in')
    except gazu.exception.NotAuthenticatedException:
        print("Not logged in")
    except Exception as e:
        print(f"Exception: {e}")
