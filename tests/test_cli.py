#! /usr/bin/env python3
"""Tests for CLI module."""

import runpy
import shlex
from filecmp import cmp

import pytest

from chained_hashing import cli, encode


def test_no_arguments():
    """Test the `run` function with no arguments."""
    # Arrange
    args = []
    # Act
    with pytest.raises(SystemExit) as pytest_err:
        cli.run(args)
    # Assert
    assert pytest_err.type is SystemExit  # noqa: S101
    assert pytest_err.value.code >= 1  # noqa: S101


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


def test_roundtrip(tmp_path):
    """Test round trip encode and decode."""
    # Arrange
    sample_file = "LICENSE"
    tmp_dec = tmp_path.joinpath("decoded")
    tmp_enc = tmp_path.joinpath("encoded")
    # Act
    cli.run(shlex.split(f"-l error encode -i {sample_file} -o {tmp_enc}"))
    cli.run(shlex.split(f"-l debug decode -i {tmp_enc} -o {tmp_dec}"))
    # Assert
    assert cmp(sample_file, tmp_dec)  # noqa: S101


def test_roundtrip_hash(tmp_path):
    """Test round trip encode and decode with hash."""
    # Arrange
    sample_file = "LICENSE"
    tmp_dec = tmp_path.joinpath("decoded")
    tmp_enc = tmp_path.joinpath("encoded")
    # Act
    sha = encode(sample_file, tmp_enc)
    cli.run(shlex.split(f"-l debug decode -i {tmp_enc} -o {tmp_dec} {sha}"))
    # Assert
    assert cmp(sample_file, tmp_dec)  # noqa: S101


def test_invalid_hash(tmp_path):
    """Test the `run` function with no arguments."""
    # Arrange
    sample_file = "LICENSE"
    tmp_dec = tmp_path.joinpath("decoded")
    args = shlex.split(f"decode -i {sample_file} -o {tmp_dec}")
    # Act
    with pytest.raises(SystemExit) as pytest_err:
        cli.run(args)
    # Assert
    assert pytest_err.type is SystemExit  # noqa: S101
    assert pytest_err.value.code >= 1  # noqa: S101


if __name__ == "__main__":
    pytest.main(shlex.split(f"--no-cov {__file__}"))
