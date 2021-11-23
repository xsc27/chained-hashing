"""Command Line Interface module."""

from __future__ import annotations

import argparse
import importlib.metadata
import logging
import sys
from typing import Any

import chained_hashing
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
        help="Set log level",
    )

    subparsers = parser.add_subparsers(title="actions", dest="cmd", required=False)
    subparsers.add_parser("run", help="Execute command")

    return parser


def run(args: list[Any] | None = None, prog: str | None = None) -> str:
    """Run main CLI workflow."""
    parsed_args = get_argparser(prog).parse_args(args)
    logging.basicConfig(level=getattr(logging, parsed_args.log_level.upper()))
    _LOG.debug("CLI parameters - %s", vars(parsed_args))
    try:
        return str(
            getattr(chained_hashing, parsed_args.cmd)(**vars(parsed_args))
            if parsed_args.cmd
            else chained_hashing.run(**vars(parsed_args))
        )
    except ChainedHashingError as err:
        _LOG.error(err)
        sys.exit(1)


if __name__ == "__main__":
    from runpy import run_module

    run_module("chained_hashing", run_name=__name__)
