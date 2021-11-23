#! /usr/bin/env python3
"""Tests for CLI module."""

import runpy
import shlex

import pytest

from chained_hashing import cli


def test_run():
    """Test the `run` function with no arguments."""
    # Arrange
    args = []
    # Act
    with pytest.raises(SystemExit) as pytest_err:
        cli.run(args)
    # Assert
    assert pytest_err.type is SystemExit  # noqa: S101
    assert pytest_err.value.code == 1  # noqa: S101


def test_run_subcommand():
    """Test the `run` function with `run` subcommand."""
    # Arrange
    args = shlex.split("run")
    # Act
    with pytest.raises(SystemExit) as pytest_err:
        cli.run(args)
    # Assert
    assert pytest_err.type is SystemExit  # noqa: S101
    assert pytest_err.value.code == 1  # noqa: S101


def test_logging_debug(caplog):
    """Test the `run` function with parameter to set loglevel."""
    # Arrange
    args = shlex.split("-l debug")
    # Act
    with pytest.raises(SystemExit) as _:
        cli.run(args)
    # Assert
    assert caplog.records[0].message.startswith("CLI parameters")  # noqa: S101
    assert "'log_level': 'debug'" in caplog.records[0].message  # noqa: S101


@pytest.mark.filterwarnings(
    "ignore: 'chained_hashing.*' found in sys.modules after import of package"
)
@pytest.mark.parametrize("module", ["__main__", "cli", "main"])
def test_file(module):
    """Test the `run` function with no arguments."""
    # Act
    with pytest.raises(SystemExit) as pytest_err:
        runpy.run_path(
            runpy.run_module(f"chained_hashing.{module}")["__file__"], run_name="__main__"
        )
    # Assert
    assert pytest_err.value.code >= 1  # noqa: S101


if __name__ == "__main__":
    pytest.main(shlex.split(f"--no-cov {__file__}"))
