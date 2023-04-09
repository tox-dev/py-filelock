from __future__ import annotations

import os
import sys
from errno import EACCES
from typing import cast

from ._api import BaseFileLock
from ._util import raise_unwritable_file

if sys.platform == "win32":  # pragma: win32 cover
    import msvcrt

    class WindowsFileLock(BaseFileLock):
        """Uses the :func:`msvcrt.locking` function to hard lock the lock file on windows systems."""

        def _acquire(self) -> None:
            raise_unwritable_file(self._lock_file)
            flags = (
                os.O_RDWR  # open for read and write
                | os.O_CREAT  # create file if not exists
                | os.O_TRUNC  # truncate file if not empty
            )
            try:
                fd = os.open(self._lock_file, flags, self._mode)
            except OSError as exception:
                if exception.errno != EACCES:  # has no access to this lock
                    raise
            else:
                try:
                    msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
                except OSError as exception:
                    os.close(fd)  # close file first
                    if exception.errno != EACCES:  # file is already locked
                        raise
                else:
                    self._lock_file_fd = fd

        def _release(self) -> None:
            fd = cast(int, self._lock_file_fd)
            self._lock_file_fd = None
            msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
            os.close(fd)

            try:
                os.remove(self._lock_file)
            # Probably another instance of the application hat acquired the file lock.
            except OSError:
                pass

else:  # pragma: win32 no cover

    class WindowsFileLock(BaseFileLock):
        """Uses the :func:`msvcrt.locking` function to hard lock the lock file on windows systems."""

        def _acquire(self) -> None:
            raise NotImplementedError

        def _release(self) -> None:
            raise NotImplementedError


__all__ = [
    "WindowsFileLock",
]
