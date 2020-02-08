import os
import platform
import shutil
import subprocess
import sys

import requests
import tomlkit
from invoke import task

ENCHANT_TAG = "v2.2.7-appveyor-35"

DOWNLOAD_URL = "https://github.com/pyenchant/enchant/releases/download/"


@task
def bootstrap(c):
    """ Bootstrap PyEnchant for developement """
    if sys.platform == "win32":
        bits, linkage = platform.architecture()
        if linkage != "WindowsPE":
            sys.exit("Unsupported platform: " + linkage)
        if bits == "32bit":
            bootstrap_windows("win32")
        elif bits == "64bit":
            bootstrap_windows("win_amd64")
        else:
            sys.exit("Unsupported number of bits: ", bits)


def bootstrap_windows(platform):
    print(":: Bootstraping for", platform)
    bits = {"win32": "32", "win_amd64": "64"}[platform]
    archive_name = "enchant-prefix" + "-" + bits + ".zip"
    artifact_url = DOWNLOAD_URL + ENCHANT_TAG + "/" + archive_name
    print("-> Retrieving artifact from", artifact_url, "...")
    response = requests.get(artifact_url, stream=True)
    response.raise_for_status()
    with open(archive_name, "wb") as f:
        shutil.copyfileobj(response.raw, f)
    data_path = "enchant/data/"
    print("-> Unpacking artifact to", data_path, "...")
    shutil.unpack_archive(archive_name, data_path)
