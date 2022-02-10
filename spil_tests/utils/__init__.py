import six

# to be imported from here
if six.PY3:  #TODO: add Timer in package for PY3 (they have a great package setup) - Also add tox.
    from codetiming import Timer
else:
    from spil_tests.mock_timer import Timer


def stop():
    """
    Simple script stop function.
    """
    import sys
    sys.exit(0)
