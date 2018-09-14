# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from sys import version_info
from time import time


PY2 = version_info[0] == 2
PY3 = version_info[0] == 3


if PY3:
    string_types = (str,)
    text_type = str
else:
    string_types = (str, unicode)
    text_type = unicode


def get_stamp():
    """Returns curent timestamp as string.

    :rtype: str|unicode
    """
    return '%s' % time()
