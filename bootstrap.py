# Prepare PyEnchant for development
#
# On Windows, we need to populate data/ with the result of an Enchant build
import sys
import shutil
import platform
import requests

ENCHANT_TAG = "v2.2.7-appveyor-35"

DOWNLOAD_URL = "https://github.com/pyenchant/enchant/releases/download/"


def bootstrap_windows():
    bits, linkage = platform.architecture()
    if linkage != "WindowsPE":
        sys.exit("Unsupported platform: " + linkage)
    if bits == "32bit":
        bits = "32"
    elif bits == "64bit":
        bits = "64"
    else:
        sys.exit("Unsupported number of bits: ", bits)
    artifact_url = DOWNLOAD_URL + ENCHANT_TAG + "/enchant-prefix" + "-" + bits + ".zip"
    print("Retrieving artifact from", artifact_url, "...")
    response = requests.get(artifact_url, stream=True)
    archive_path = "enchant-prefix.zip"
    with open(archive_path, "wb") as f:
        shutil.copyfileobj(response.raw, f)
    data_path = "enchant/data/"
    print("Unpacking artifact to", data_path, "...")
    shutil.unpack_archive(archive_path, data_path)


def main():
    if sys.platform == "win32":
        bootstrap_windows()


if __name__ == "__main__":
    main()
