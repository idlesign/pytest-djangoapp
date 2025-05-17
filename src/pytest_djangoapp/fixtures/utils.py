from time import time

import pytest

from ..configuration import Configuration


def get_stamp() -> str:
    """Returns current timestamp as a string."""
    return f'{time()}'


@pytest.fixture(scope='session')
def conf_app_name() -> str:
    """Returns your application name (deduced or provided)."""
    return Configuration.get_dict()[Configuration.KEY_APP]
