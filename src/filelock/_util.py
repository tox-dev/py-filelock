from __future__ import annotations

import os
import stat
import sys
from errno import EACCES, EISDIR


def raise_unwritable_file(filename: str) -> None:
    """
    Raise an exception if attempting to open the file for writing would fail.
    This is done so files that will never be writable can be separated from
    files that are writable but currently locked
    :param filename: file to check
    :raises OSError: as if the file was opened for writing
    """
    try:
        file_stat = os.stat(filename)  # use stat to do exists + can write to check without race condition
    except OSError:
        return None  # swallow does not exist or other errors

    if file_stat.st_mtime != 0:  # if os.stat returns but modification is zero that's an invalid os.stat - ignore it
        if not (file_stat.st_mode & stat.S_IWUSR):
            raise PermissionError(EACCES, "Permission denied", filename)

        if stat.S_ISDIR(file_stat.st_mode):
            if sys.platform == "win32":
                # On Windows, this is PermissionError
                raise PermissionError(EACCES, "Permission denied", filename)
            else:
                # On linux / macOS, this is IsADirectoryError
                raise IsADirectoryError(EISDIR, "Is a directory", filename)


__all__ = [
    "raise_unwritable_file",
]
