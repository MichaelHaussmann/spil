
from spil import conf


def get_writer_for(sid):  # TODO: implement separate source and destination objects.
    return conf.get_writer_for(sid)


class Setter:
    pass


