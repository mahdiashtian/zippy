import aiofiles
from fastapi import UploadFile

from config import settings
import os
import random
import string

from typing import Tuple


def get_file_name(file_name: str) -> Tuple[str, str]:
    base_name = os.path.basename(file_name)
    name, ext = os.path.splitext(base_name)
    return name, ext


async def save_file(file: UploadFile) -> str:
    file_path = os.path.join(
        settings.MEDIA.MEDIA_DIR,
        file.filename
    )
    if os.path.exists(file_path):
        name, ext = get_file_name(file.filename)
        ascii_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        file_path = os.path.join(
            settings.MEDIA.MEDIA_DIR,
            name + ascii_text + ext
        )

    async with aiofiles.open(file_path, "wb") as f:
        while chunk := await file.read(settings.DEFAULT_CHUNK_SIZE):
            await f.write(chunk)
    return file_path
