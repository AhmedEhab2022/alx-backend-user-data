#!/usr/bin/env python3
""" Filtered Logger """
import re
from typing import List


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """ Returns the log message obfuscated.

    Args:
        fields (List[str]): list of fields to obfuscate
        redaction (str): the obfuscation string
        message (str): the log message
        separator (str): the separator for the message
    """
    for field in fields:
        pattern = field + "=.*?" + separator
        message = re.sub(pattern, field + "=" + redaction + separator, message)
    return message
