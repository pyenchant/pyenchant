# Prepare PyEnchant for development
#
# On Windows, we need to populate data/ with the result of an Enchant build
import os
import glob
import sys
import shutil
import platform
import requests

ENCHANT_TAG = "v2.2.7-appveyor-41"

DOWNLOAD_URL = "https://github.com/pyenchant/enchant/releases/download/"


def bootstrap_windows(platform):
    bits = {"win32": "32", "win_amd64": "64"}[platform]
    archive_name = "enchant-prefix" + "-" + bits + ".zip"
    artifact_url = DOWNLOAD_URL + ENCHANT_TAG + "/" + archive_name
    print(":: Retrieving artifact from", artifact_url, "...")
    response = requests.get(artifact_url, stream=True)
    with open(archive_name, "wb") as f:
        shutil.copyfileobj(response.raw, f)
    data_path = "enchant/data/"
    print(":: Unpacking artifact to", data_path, "...")
    shutil.unpack_archive(archive_name, data_path)
    cleanup_data(data_path, bits)


def rm(path):
    if os.path.exists(path):
        print("-> rm", path)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def clean_libs(path):
    for static_lib in glob.glob(path + "/*.a"):
        rm(static_lib)
    for la_file in glob.glob(path + "/*.la"):
        rm(la_file)


def clean_bin(path):
    for exe in glob.glob(path + "/*.exe"):
        rm(exe)


def cleanup_data(data_path, bits):
    """ Remove extraneous files from the enchant artifact """
    print(":: Cleaning up ...")
    mingw_path = os.path.join(data_path, "mingw" + bits)
    # Better filter extra files there that on the appveyor script
    for sub_dir in ["share/man", "include", "lib/pkgconfig"]:
        to_rm = os.path.join(mingw_path, sub_dir)
        rm(to_rm)

    clean_libs(os.path.join(mingw_path, "lib"))
    clean_libs(os.path.join(mingw_path, "/lib/enchant-2"))

    clean_bin(os.path.join(mingw_path, "bin"))


def main():
    bits, linkage = platform.architecture()
    if sys.platform == "win32":
        if linkage != "WindowsPE":
            sys.exit("Unsupported platform: " + linkage)
        if bits == "32bit":
            platform_name = "win32"
        elif bits == "64bit":
            platform_name = "win_amd64"
        else:
            sys.exit("Unsupported number of bits: ", bits)
        bootstrap_windows(platform_name)


if __name__ == "__main__":
    main()
