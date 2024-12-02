"""Async read/write file lock."""

from __future__ import annotations

from typing import TYPE_CHECKING

from filelock._unix import has_fcntl
from filelock.asyncio import AsyncNonExclusiveUnixFileLock, AsyncUnixFileLock
from filelock.read_write.asyncio._api import BaseAsyncReadWriteFileLock, _DisabledAsyncReadWriteFileLock
from filelock.read_write.asyncio._wrapper import (
    BaseAsyncReadWriteFileLockWrapper,
    _DisabledAsyncReadWriteFileLockWrapper,
)

if TYPE_CHECKING:
    from filelock.asyncio import BaseAsyncFileLock


AsyncReadWriteFileLock: type[BaseAsyncReadWriteFileLock]
AsyncReadWriteFileLockWrapper: type[BaseAsyncReadWriteFileLockWrapper]

if has_fcntl:

    class UnixAsyncReadWriteFileLock(BaseAsyncReadWriteFileLock):
        """Unix implementation of an async read/write FileLock."""

        _shared_file_lock_cls: type[BaseAsyncFileLock] = AsyncNonExclusiveUnixFileLock
        _exclusive_file_lock_cls: type[BaseAsyncFileLock] = AsyncUnixFileLock

    class UnixAsyncReadWriteFileLockWrapper(BaseAsyncReadWriteFileLockWrapper):
        """Wrapper for a Unix implementation of an async read/write FileLock."""

        _read_write_file_lock_cls = UnixAsyncReadWriteFileLock

    AsyncReadWriteFileLock = UnixAsyncReadWriteFileLock
    AsyncReadWriteFileLockWrapper = UnixAsyncReadWriteFileLockWrapper
else:

    class UnixAsyncReadWriteFileLock(BaseAsyncReadWriteFileLock):
        """Unix implementation of an async read/write FileLock."""

    class UnixAsyncReadWriteFileLockWrapper(BaseAsyncReadWriteFileLockWrapper):
        """Wrapper for a Unix implementation of an async read/write FileLock."""

    AsyncReadWriteFileLock = _DisabledAsyncReadWriteFileLock
    AsyncReadWriteFileLockWrapper = _DisabledAsyncReadWriteFileLockWrapper


__all__ = [
    "AsyncReadWriteFileLock",
    "AsyncReadWriteFileLockWrapper",
    "BaseAsyncReadWriteFileLock",
    "BaseAsyncReadWriteFileLockWrapper",
    "UnixAsyncReadWriteFileLock",
    "UnixAsyncReadWriteFileLockWrapper",
]