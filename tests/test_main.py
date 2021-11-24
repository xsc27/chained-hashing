#! /usr/bin/env python3
"""Tests for CLI module."""

import shlex
from filecmp import cmp

import pytest

from chained_hashing import decode, encode


def test_roundtrip(tmp_path):
    """Test round trip encode and decode with hash."""
    # Arrange
    sample_file = "LICENSE"
    tmp_dec = tmp_path.joinpath("decoded")
    tmp_enc = tmp_path.joinpath("encoded")
    # Act
    encode(sample_file, tmp_enc)
    decode(src=tmp_enc, dest=tmp_dec)
    # Assert
    assert cmp(sample_file, tmp_dec)  # noqa: S101


def test_roundtrip_hash(tmp_path):
    """Test round trip encode and decode with hash."""
    # Arrange
    sample_file = "LICENSE"
    tmp_dec = tmp_path.joinpath("decoded")
    tmp_enc = tmp_path.joinpath("encoded")
    # Act
    decode(src=tmp_enc, dest=tmp_dec, sha=encode(sample_file, tmp_enc))
    # Assert
    assert cmp(sample_file, tmp_dec)  # noqa: S101


if __name__ == "__main__":
    pytest.main(shlex.split(f"--no-cov {__file__}"))
