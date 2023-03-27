from spil.util.exception import raiser
from spil import Sid, Getter


class NextGetter(Getter):  # noqa (does not implement all of superclass)
    """
    Receives specific "next." attributes and returns accordingly.

    Currently implemented to calculate and retrieve the "next" version of a Sid.
    """

    def get_attr(self, sid, attribute):
        """
        Acts as a callback for Sid.get_next(), via GetFromAll.

        See Sid.get_next documentation.

            >>> NextGetter().get_attr('hamlet/a/char/ophelia/model/v001/w/ma', 'next.version')
            Sid('asset__file:hamlet/a/char/ophelia/model/v002/w/ma')

            >>> NextGetter().get_attr('hamlet/a/char/ophelia/model/*/w/ma', 'next.version')
            Sid('asset__file:hamlet/a/char/ophelia/model/v003/w/ma')

            >>> NextGetter().get_attr('hamlet/a/char/ophelia/model', 'next.version')
            Sid('asset__version:hamlet/a/char/ophelia/model/v001')

        Args:
            sid:
            attribute:

        Returns:

        """

        spec, key = attribute.split(".")
        (spec == "next" and key == "version") or raiser("This implementation is limited to returning the next version Sid.")

        _sid = Sid(sid)
        current = _sid.get("version")

        # extracts current version
        if current:
            if current in ["*", ">"]:
                version = (_sid.get_last("version").get("version") or "v000").split("v")[-1] or 0
            else:
                # temporary workaround for "v001"
                version = str(current).split("v")[-1]
        # or 0 if no current version
        else:
            version = 0  # starts with v001

        # increments and formats
        version = int(version) + 1
        version = "v" + str("%03d" % version)

        # builds Sid and returns
        result = _sid.get_with(version=version) or Sid()
        return result
