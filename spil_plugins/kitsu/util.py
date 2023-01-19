# -*- coding: utf-8 -*-
import doctest
import unidecode


def sid_format(input: str) -> str:
    """
    Formats data for usage in Sid:
    - replaces " " by "_"
    - lowers case
    - unidecodes

    Example:

        >>> sid_format("hällo Bi'l\l*")
        'hallo_bill'

    TODO: better special character check.

    Args:
        input:

    Returns:

    """
    backslash = r'\_'[0]
    return str(
        unidecode.unidecode(
            str(input).replace(" ", "_").replace("'", "").replace('"', "").replace(backslash, "").replace("/", "").replace("*", "").lower()
        )
    )


if __name__ == "__main__":
    doctest.testmod()

