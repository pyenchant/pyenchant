# Prepare PyEnchant for development
#
# On Windows, we need to populate data/ with the result of an Enchant build
import sys
import shutil

import requests

ARTIFACT_URL = "https://github.com/pyenchant/enchant/releases/download/v2.2.7-appveyor-20/enchant-prefix.zip"


def bootstrap_windows():
    print("Retrieving artifact from", ARTIFACT_URL, "...")
    response = requests.get(ARTIFACT_URL, stream=True)
    archive_path = "enchant-prefix.zip"
    with open(archive_path, "wb") as f:
        shutil.copyfileobj(response.raw, f)
    data_path = "enchant/data"
    print("Unpacking artifact to", data_path, "...")
    shutil.unpack_archive(archive_path, data_path)


def main():
    if sys.platform == "win32":
        bootstrap_windows()


if __name__ == "__main__":
    main()
