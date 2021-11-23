"""Main module."""
from __future__ import annotations

from typing import Any

from chained_hashing.exceptions import ChainedHashingError


def run(*args: Any, **kwargs: dict[str, Any]):
    """Execute main logic.

    >>> run()
    Traceback (most recent call last):
       ...
    chained_hashing.exceptions.ChainedHashingError: NotImplementedError - ('run', (), {})
    """
    try:
        raise NotImplementedError("run", args, kwargs)
    except NotImplementedError as err:
        raise ChainedHashingError(err) from err


if __name__ == "__main__":
    from runpy import run_module

    run_module("chained_hashing", run_name=__name__)
