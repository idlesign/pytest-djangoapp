# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from time import time


def get_stamp():
    """Returns curent timestamp as string.

    :rtype: str|unicode
    """
    return '%s' % time()
