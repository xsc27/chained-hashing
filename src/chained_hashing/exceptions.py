"""Exceptions for package."""
from __future__ import annotations


class ChainedHashingError(Exception):
    """Chained Hashing exception.

    Attributes:
        fmt (str): Format of error message
    """

    fmt = "{}"

    def __init__(self, msg: str | Exception, *args, **kwargs):
        """Initialize exception.

        Args:
            msg (str): Exception message
        """
        err_msg = self.fmt.format(self.get_msg(msg), *args, **kwargs)
        super().__init__(err_msg)

    @staticmethod
    def get_msg(value) -> str:
        """Return name of raised from exception or string of value."""
        return f"{type(value).__name__} - {value}" if isinstance(value, Exception) else str(value)
