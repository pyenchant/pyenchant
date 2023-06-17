# Prepare PyEnchant for development
#
# On Windows, we need to populate data/ with the result of an Enchant build
import glob
import os
import platform
import shutil
import sys

import requests

ENCHANT_TAG = "v2.3.4-gh-9"

DOWNLOAD_URL = "https://github.com/pyenchant/enchant/releases/download/"


def get_bits() -> int:
    bits, linkage = platform.architecture()
    if sys.platform == "win32":
        if linkage != "WindowsPE":
            sys.exit("Unsupported platform: " + linkage)
        if bits == "32bit":
            return 32
        elif bits == "64bit":
            return 64
        else:
            sys.exit("Unsupported number of bits: ", bits)
    else:
        # It's 2023 ...
        return 64


def bootstrap_windows(*, bits: int) -> None:
    suffix = {32: "i686", 64: "x86_64"}[bits]
    archive_name = "enchant" + "-" + suffix + ".zip"
    artifact_url = DOWNLOAD_URL + ENCHANT_TAG + "/" + archive_name
    print(":: Retrieving artifact from", artifact_url, "...")
    response = requests.get(artifact_url, stream=True)
    response.raise_for_status()
    with open(archive_name, "wb") as f:
        shutil.copyfileobj(response.raw, f)
    data_path = "enchant/data/"
    print(":: Unpacking artifact to", data_path, "...")
    shutil.unpack_archive(archive_name, data_path)
    cleanup_data(data_path, bits=bits)


def rm(path: str) -> None:
    if os.path.exists(path):
        print("-> rm", path)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def clean_libs(path: str) -> None:
    for static_lib in glob.glob(path + "/*.a"):
        rm(static_lib)
    for la_file in glob.glob(path + "/*.la"):
        rm(la_file)


def clean_bin(path: str) -> None:
    for exe in glob.glob(path + "/*.exe"):
        rm(exe)


def cleanup_data(data_path: str, *, bits: int) -> None:
    """Remove extraneous files from the enchant artifact"""
    print(":: Cleaning up ...")
    mingw_path = os.path.join(data_path, "mingw" + str(bits))
    # Better filter extra files there than in the appveyor script
    for sub_dir in ["share/man", "include", "lib/pkgconfig"]:
        to_rm = os.path.join(mingw_path, sub_dir)
        rm(to_rm)

    clean_libs(os.path.join(mingw_path, "lib"))
    clean_libs(os.path.join(mingw_path, "/lib/enchant-2"))

    clean_bin(os.path.join(mingw_path, "bin"))


def main() -> None:
    bits = get_bits()
    if sys.platform == "win32":
        bootstrap_windows(bits=bits)


if __name__ == "__main__":
    main()
