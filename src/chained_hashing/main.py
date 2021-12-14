# pylint: disable=line-too-long
"""Main module."""
from __future__ import annotations

import logging
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from hashlib import sha256
from os import SEEK_CUR, SEEK_SET
from pathlib import Path
from typing import IO

from chained_hashing.constants import BLOCK_SIZE, SHA_SIZE
from chained_hashing.exceptions import ChainedHashingError

_LOG = logging.getLogger(__name__)


class Transcoder(ABC):  # pylint: disable=too-few-public-methods
    """Base class for transcoders."""

    @abstractmethod
    def run(self, data: bytes) -> bytes:
        """Run transcoder."""


@dataclass
class Decoder(Transcoder):
    """Decoder class."""

    sha: bytes | str
    block_size: int = BLOCK_SIZE

    def __post_init__(self):
        """Initialize dataclass."""
        self.sha = bytes.fromhex(self.sha) if isinstance(self.sha, str) else self.sha

    def run(self, data: bytes) -> bytes:
        """Remove appened hash and validate data.

        >>> decoder = Decoder("c97c29c7a71b392b437ee03fd17f09bb10b75e879466fc0eb757b2c4a78ac938", block_size=4);
        >>> decoder.run("DATA".encode())
        b'DATA'
        >>> decoder.run("DATA".encode())
        Traceback (most recent call last):
           ...
        chained_hashing.exceptions.ChainedHashingError: ValueError - Received SHA = 44415441, Expected SHA = c97c29c7a71b392b437ee03fd17f09bb10b75e879466fc0eb757b2c4a78ac938
        """
        sha_new = sha256(data).digest()
        if self.sha != sha_new:
            msg = f"Received SHA = {self.sha.hex()}, Expected SHA = {sha_new.hex()}"
            _LOG.error(msg)
            raise ChainedHashingError(ValueError(msg))
        self.sha = data[-SHA_SIZE:]
        return data[: self.block_size]


@dataclass
class Encoder(Transcoder):
    """Encoder class."""

    _sha: bytes = b""

    @property
    def sha(self):
        """Get hash value."""
        return self._sha

    def run(self, data: bytes) -> bytes:
        r"""Append hash of previous data to current data.

        Note: Does not verify the data block sizes are consistent.
        >>> encoder = Encoder();
        >>> encoder.run("".encode())
        b''
        >>> encoder.run("DATA".encode())
        b"DATA\xe3\xb0\xc4B\x98\xfc\x1c\x14\x9a\xfb\xf4\xc8\x99o\xb9$'\xaeA\xe4d\x9b\x93L\xa4\x95\x99\x1bxR\xb8U"
        """
        previous_sha = self._sha
        self._sha = sha256(data + self._sha).digest()
        _LOG.debug("Data hash - %s", self._sha.hex())
        return data + previous_sha


def _get_paths(src: Path | str, dest: Path | str) -> tuple[Path, Path]:
    return (
        Path(src) if isinstance(src, str) else src,
        Path(dest) if isinstance(dest, str) else dest,
    )


def decode(
    src: Path | str,
    dest: Path | str = "",
    sha: bytes | str | None = None,
    block_size: int = BLOCK_SIZE,
):
    """Decode file encoded with chained hashing."""
    src, dest = _get_paths(src, dest)
    dest.touch()
    dest = "" if not dest.is_file() else dest
    with src.open("rb") as src_fid, dest.open("wb") if isinstance(
        dest, Path
    ) else sys.stdout as dest_fid:
        sha_h0 = src_fid.read(SHA_SIZE)
        decoder = Decoder(sha=sha or sha_h0, block_size=block_size)
        while data := src_fid.read(block_size + SHA_SIZE):
            data = decoder.run(data)
            dest_fid.write(data if dest else data.decode())

        if dest:
            _LOG.debug("Data validated and written to %s", dest)


def encode(src: Path | str, dest: Path | str, block_size: int = BLOCK_SIZE) -> str:
    """Encode file with chained hashing."""

    def poke(fid: IO[bytes], data: bytes):
        fid.seek(-(len(data)), SEEK_CUR)
        fid.write(data)
        fid.seek(-(len(data)), SEEK_CUR)

    src, dest = _get_paths(src, dest)
    src_size = src.stat().st_size
    hashed_blocks = src_size // block_size - (not src_size % block_size)
    encoder = Encoder()

    with src.open("rb") as src_fid, dest.open("wb") as dest_fid:
        src_fid.seek(hashed_blocks * block_size, SEEK_SET)
        dest_fid.seek((hashed_blocks + 1) * SHA_SIZE + src_size)
        poke(dest_fid, encoder.run(src_fid.peek(block_size)))
        while src_fid.tell():
            _LOG.info(
                "%.2f%% complete at %s",
                (src_size - src_fid.tell()) / src_size * 100,
                src_fid.tell(),
            )
            src_fid.seek(-block_size, SEEK_CUR)
            poke(dest_fid, encoder.run(src_fid.peek(block_size)[:block_size]))
        poke(dest_fid, encoder.sha)

    sha = encoder.sha.hex()
    _LOG.info("h0 is %s", sha)
    return sha


if __name__ == "__main__":
    from runpy import run_module

    run_module("chained_hashing", run_name=__name__)
