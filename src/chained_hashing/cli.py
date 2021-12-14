"""Command Line Interface module."""

from __future__ import annotations

import argparse
import importlib.metadata
import logging
import sys
from typing import Any

import chained_hashing
from chained_hashing.constants import BLOCK_SIZE
from chained_hashing.exceptions import ChainedHashingError

_LOG = logging.getLogger(__name__)


class _CaseInsensitveList(list[str]):
    def __contains__(self, other: str):
        return super().__contains__(other.casefold())


def get_argparser(prog: str | None = None) -> argparse.ArgumentParser:
    """Get parsed argparse agruments."""
    parser = argparse.ArgumentParser(
        prog=prog,
        description="Encode and decode files with chained hashing.",
        allow_abbrev=False,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {importlib.metadata.version(__name__.split('.', maxsplit=1)[0])}",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        choices=_CaseInsensitveList(
            [logging.getLevelName(i_).lower() for i_ in range(0, 51, 10)]
        ),
        default="info",
        help="set log level",
    )

    subparsers = parser.add_subparsers(title="actions", dest="cmd", required=True)

    decode = subparsers.add_parser("decode", help="decode data")
    decode.add_argument("-i", "--input", dest="src", required=True, help="input file")
    decode.add_argument("-o", "--output", dest="dest", default="", help="output file")
    decode.add_argument("-b", "--block_size", default=BLOCK_SIZE, help="block size", type=int)
    decode.add_argument("sha", nargs="?", metavar="hash", help="h0 hash")

    encode = subparsers.add_parser("encode", help="encode data")
    encode.add_argument("-i", "--input", dest="src", required=True, help="input file")
    encode.add_argument("-o", "--output", dest="dest", required=True, help="output file")
    encode.add_argument("-b", "--block_size", default=BLOCK_SIZE, help="block size", type=int)

    return parser


def run(args: list[Any] | None = None, prog: str | None = None) -> str:
    """Run main CLI workflow."""
    parsed_args = get_argparser(prog).parse_args(args)
    logging.basicConfig(level=getattr(logging, parsed_args.log_level.upper()))
    _LOG.debug("CLI parameters - %s", vars(parsed_args))
    # Remove global and empty parameters.
    params = {k: v for k, v in vars(parsed_args).items() if k not in ["cmd", "log_level"] and v}
    try:
        getattr(chained_hashing, parsed_args.cmd)(**params)
    except ChainedHashingError as err:
        _LOG.error(err)
        sys.exit(1)


if __name__ == "__main__":
    from runpy import run_module

    run_module("chained_hashing", run_name=__name__)
