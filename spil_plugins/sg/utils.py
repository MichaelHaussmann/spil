# -*- coding: utf-8 -*-
import doctest
import unidecode


def sid_format(input: str) -> str:  # TODO: movie this into a config ?
    """
    Formats data for usage in Sid:
    - replaces " " by "_"
    - removes "/", "*", "\" and quotes
    - lowers case
    - unidecodes

    Example:
    >>> sid_format("hällo Bi'l\l*")
    'hallo_bill'

    TODO: better special character check.

    :param input:
    :return:
    """
    backslash = r'\_'[0]
    return str(
        unidecode.unidecode(
            str(input).replace(" ", "_").replace("'", "").replace('"', "").replace(backslash, "").replace("/", "").replace("*", "").lower()
        )
    )


if __name__ == "__main__":
    doctest.testmod()

