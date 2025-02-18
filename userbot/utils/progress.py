


import math
import time

from telethon.errors.rpcerrorlist import MessageNotModifiedError

from .exceptions import CancelProcess
from .tools import humanbytes, time_formatter


async def progress(
    current, total, gdrive, start, prog_type, file_name=None, is_cancelled=False
):
    now = time.time()
    diff = now - start
    if is_cancelled is True:
        raise CancelProcess

    if round(diff % 15.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff)
        eta = round((total - current) / speed)
        if "upload" in prog_type.lower():
            status = "Uploading"
        elif "download" in prog_type.lower():
            status = "Downloading"
        else:
            status = "Unknown"
        progress_str = "`{0}` | `[{1}{2}] {3}%`".format(
            status,
            "".join("●" for i in range(math.floor(percentage / 10))),
            "".join("○" for i in range(10 - math.floor(percentage / 10))),
            round(percentage, 2),
        )

        tmp = (
            f"{progress_str}\n"
            f"`{humanbytes(current)} of {humanbytes(total)}"
            f" @ {humanbytes(speed)}`\n"
            f"**ETA :**` {time_formatter(eta)}`\n"
            f"**Duration :** `{time_formatter(elapsed_time)}`"
        )
        try:
            if file_name:
                await gdrive.edit(
                    f"**{prog_type}**\n\n"
                    f"**Nama File : **`{file_name}`**\nStatus**\n{tmp}"
                )
            else:
                await gdrive.edit(f"**{prog_type}**\n\n" f"**Status**\n{tmp}")
        except MessageNotModifiedError:
            pass


class CancelProcess(Exception):
    """
    Cancel Process
    """
