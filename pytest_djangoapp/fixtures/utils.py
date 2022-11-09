from time import time


def get_stamp() -> str:
    """Returns current timestamp as a string."""
    return f'{time()}'
