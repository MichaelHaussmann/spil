import six

if six.PY2:
    from urllib import urlencode
    import urlparse as urlparse
else:
    from urllib.parse import urlencode
    from urllib import parse as urlparse


def to_dict(uri_string):
    """
    Converts a uri string into a dictionary.

    All ? can be used as &.
    Optionally leading or rtailing ? or & are ignored.

    Examples:
    >>> to_dict('keyA=valueA&keyB=valueB, XX')
    {'keyA': 'valueA', 'keyB': 'valueB, XX'}

    >>> to_dict('?keyA=valueA&keyB=valueB')
    {'keyA': 'valueA', 'keyB': 'valueB'}

    >>> to_dict('?keyA=valueA?keyB=valueB')
    {'keyA': 'valueA', 'keyB': 'valueB'}

    """
    uri_string = uri_string.replace('?', '&')  # we allow a=b?x=y but change it to a proper uri: a=b&x=y

    # cleaning start / end signs
    if uri_string.startswith('&'):
        uri_string = str(uri_string[1:])

    if uri_string.endswith('&'):
        uri_string = str(uri_string[:-1])

    uri_pairs = dict(urlparse.parse_qsl(urlparse.urlsplit('?' + uri_string).query))
    return uri_pairs


def to_string(uri_dict):
    """
    Converts a uri dict into a string.
    Does not do urlencoding, just strips whitespaces.

    Examples:
    >>> to_string({'keyA': 'valueA', 'keyB': 'valueB, BB'})
    'keyA=valueA&keyB=valueB,BB'
    """
    def encode(x, *args, **kwargs):
        return x.replace(' ', '')

    if six.PY2:
        l = []
        for k, v in six.iteritems(uri_dict):
            l.append(encode(k) + '=' + encode(v))
        return '&'.join(sorted(l))

    return urlencode(uri_dict, quote_via=encode)


if __name__ == '__main__':
    """
    Test block.
    Launches doc test (test in the doc).
    
    In PY2 the test does not pass, because the dict is not sorted by default.
    """
    from spil.util.log import info, setLevel, INFO

    setLevel(INFO)

    info('Tests start')

    import doctest
    # info(doctest)

    doctest.testmod()

    r = to_dict('&keyA=valueA&keyB=valueB&')
    print(r)

    info('Tests done.')
