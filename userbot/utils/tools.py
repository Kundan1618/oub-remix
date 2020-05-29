# Copyright (C) 2019 Adek Maulana
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import re
import hashlib
import asyncio
import datetime
import logging
import os
import os.path
import sys
import time
from typing import Tuple, Union


from telethon import errors
from telethon.tl import types
from telethon.utils import get_display_name


async def md5(fname: str) -> str:
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def humanbytes(size: int) -> str:
    if size is None or isinstance(size, str):
        return ""

    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def time_formatter(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " day(s), ") if days else "") +
        ((str(hours) + " hour(s), ") if hours else "") +
        ((str(minutes) + " minute(s), ") if minutes else "") +
        ((str(seconds) + " second(s), ") if seconds else "")
    )
    return tmp[:-2]


def human_to_bytes(size: str) -> int:
    units = {
        "M": 2**20, "MB": 2**20,
        "G": 2**30, "GB": 2**30,
        "T": 2**40, "TB": 2**40
    }

    size = size.upper()
    if not re.match(r' ', size):
        size = re.sub(r'([KMGT])', r' \1', size)
    number, unit = [string.strip() for string in size.split()]
    return int(float(number)*units[unit])

async def is_ffmpeg_there():
    cmd = await asyncio.create_subprocess_shell('ffmpeg -version',
                                                stdout=asyncio.subprocess.PIPE,
                                                stderr=asyncio.subprocess.PIPE)
    await cmd.communicate()
    return True if cmd.returncode == 0 else False


class ProgressCallback():
    """Custom class to handle upload and download progress."""
    def __init__(self, event, start=None, filen='unamed', update=5):
        self.event = event
        self.start = start or time.time()
        self.last_upload_edit = None
        self.last_download_edit = None
        self.filen = filen
        self.upload_finished = False
        self.download_finished = False
        self._uploaded = 0
        self._downloaded = 0
        self.update = update    