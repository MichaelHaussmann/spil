"""

--------- WORK IN PROGRESS --------


Data layer will also be useable to access attributes of Sids and other data.



"""


class Data():
    """
    Data abstraction Layer.

    On top of the built-in FS, and delegating data access to other custom Data sources.
    """

    """
    def get_data_implementation(self, sid, attribute):
        return implementations.get(attribute, {}).get(sid.type)

    def get_data(self, sid, attribute):

        func = self.get_data_implementation(sid, attribute)
        if func:
            return func(sid)
        else:
            print('Data Source implementation not found for Sid "{}" ({}) and attribute "{}"'.format(sid, sid.type, attribute))
            return None
    """
    pass


if __name__ == '__main__':

    from spil.util.log import setLevel, DEBUG, ERROR

    setLevel(ERROR)

    sid = 'raj/a/char/juliet/low/design/v002/w/mp4'
    sid = Sid(sid)
    got = Data().get_data(sid, 'comment')
    print(got)
