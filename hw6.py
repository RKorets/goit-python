import sys
import shutil
import re

import asyncio
from aiopath import AsyncPath

DOCUMENTS = []
IMAGES = []
VIDEOS = []
MUSICS = []
OTHER = []
ARCH = []
FOLDERS = []
UNKNOWN = set()
EXTENSION = set()

REGISTERED_EXTENSIONS = {
    'JPEG': IMAGES, 'JPG': IMAGES, 'PNG': IMAGES, 'SVG': IMAGES,
    'AVI': VIDEOS, 'MP4': VIDEOS, 'MOV': VIDEOS, 'MKV': VIDEOS,
    'DOC': DOCUMENTS, 'DOCX': DOCUMENTS, 'TXT': DOCUMENTS, 'PDF': DOCUMENTS, 'XLSX': DOCUMENTS, 'PPTX': DOCUMENTS,
    'MP3': MUSICS, 'OGG': MUSICS, 'WAV': MUSICS, 'AMR': MUSICS,
    'ZIP': ARCH
}

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "e", "u", "ja")

TRANS = {}

for cs, trl in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cs)] = trl
    TRANS[ord(cs.upper())] = trl.upper()


def normalize(name: str) -> str:
    trl_name = name.translate(TRANS)
    trl_name = re.sub(r"\W", "_", trl_name)
    return trl_name


def get_extension(file_name) -> str:
    return AsyncPath(file_name).suffix[1:].upper()


async def scan(folder: AsyncPath):
    folder = AsyncPath(folder)
    async for item in folder.iterdir():
        is_folder = await item.is_dir()
        if is_folder:
            if item.name not in REGISTERED_EXTENSIONS.keys():
                FOLDERS.append(item)
                await scan(item)
            continue

        extension = get_extension(item.name)
        new_name = folder / item.name
        if not extension:
            OTHER.append(new_name)
        else:
            try:
                current_container = REGISTERED_EXTENSIONS[extension]
                EXTENSION.add(extension)
                current_container.append(new_name)

            except KeyError:
                UNKNOWN.add(extension)
                OTHER.append(new_name)


async def handle_file(file: AsyncPath, root_folder: AsyncPath, dist):
    target_folder = root_folder / dist
    await target_folder.mkdir(exist_ok=True)
    ext = AsyncPath(file).suffix
    if dist == "ARCH":
        folder_for_arch = normalize(file.name.replace(ext, ""))
        archive_folder = target_folder / folder_for_arch
        await archive_folder.mkdir(exist_ok=True)
        try:
            shutil.unpack_archive(file, archive_folder)
            await file.unlink(missing_ok=True)
        except shutil.ReadError:
            await archive_folder.rmdir()
            return

    else:
        new_name = normalize(file.name.replace(ext, "")) + ext
        await file.replace(target_folder / new_name)


async def handle_folder(folder: AsyncPath):
    try:
        await folder.rmdir()
    except OSError:
        print(f"Не удалось удалить папку {folder}")


async def main(folder):
    await scan(folder)

    for file in ARCH:
        await handle_file(file, folder, "ARCH")

    for file in OTHER:
        await handle_file(file, folder, "OTHER")

    for items in REGISTERED_EXTENSIONS.values():
        for file in items:
            folder_new = list(REGISTERED_EXTENSIONS.keys())[list(REGISTERED_EXTENSIONS.values()).index(items)]
            await handle_file(file, folder, folder_new)

    for f in FOLDERS:
        await handle_folder(f)


if __name__ == "__main__":
    scan_path = sys.argv[1]
    print(f"Start in folder {scan_path}")
    sort_folder = AsyncPath(scan_path)
    asyncio.run(main(sort_folder))
