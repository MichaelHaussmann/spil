from data_conf import implementations, data_sources


class Data(object):
    """
    Data abstraction Layer.

    On top of the built-in FS, and delegating data access to other custom Data sources.
    """

    def get_data_implementation(self, sid, attribute):
        return implementations.get(attribute, {}).get(sid.type)

    def get_data_source(self, sid):
        return data_sources.get(sid.type, {}) or data_sources.get('default', {})

    def get_data(self, sid, attribute):

        func = self.get_data_implementation(sid, attribute)
        if func:
            return func(sid)
        else:
            print('Data Source implementation not found for Sid "{}" ({}) and attribute "{}"'.format(sid, sid.type, attribute))
            return None

    def get(self, sid, as_sid=True):

        source = self.get_data_source(sid)
        if source:
            print('Using source: {}'.format(source))
            return source().get(sid, as_sid=as_sid)
        else:
            print('Data Source not found for Sid "{}" ({})'.format(sid, sid.type))
            return None


if __name__ == '__main__':

    from spil import Sid
    sid = 'raj/a/char/juliet/low/design/v002/w/mp4'
    sid = Sid(sid)
    got = Data().get_data(sid, 'comment')
    print(got)

    sid = 'raj/a/char/juliet/low/design/**'
    sid = Sid(sid)
    print(sid)
    got = Data().get(sid)
    for i in got:
        print(i)

    sid = 'raj/*'
    sid = Sid(sid)
    print(sid)
    got = Data().get(sid)
    for i in got:
        print(i)