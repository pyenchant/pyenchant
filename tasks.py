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


@task
def build_artifacts(c):
    """ Build artifacts that we need to upload to  pypi """
    ensure_empty("build/")
    ensure_empty("dist/")

    # Note: poetry honors .gitignore, but we want those files in enchant/data!
    gitignore = "enchant/data/.gitignore"
    if os.path.exists(gitignore):
        os.remove(gitignore)
    print("Building artifacts for new release ...")
    make_windows_wheel(c, platform="win_amd64")
    make_windows_wheel(c, platform="win32")

    make_wheel_any(c)
    make_sdist(c)

    print("Done!. Artifacts are in dist/, Please restore enchant/data/.gitignore")


@task(pre=[build_artifacts])
def release(c, testpypi=False):
    """ Release artifacts to pypi.org """
    c.run("twine upload dist/*")


@task
def website(c, dev=False):
    """ Build website """
    if dev:
        program = "sphinx-autobuild"
    else:
        program = "sphinx-build"
    with c.cd("website"):
        c.run(f"{program} -W -c . -d build/ -b html content/ html/")


@task
def lint(c):
    """ Run all linters """
    c.run("black --check .")
    c.run("flake8 enchant tests")


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


def rename_wheel(platform):
    with open("pyproject.toml") as f:
        cfg = tomlkit.loads(f.read())
    version = cfg["tool"]["poetry"]["version"]
    src = f"dist/pyenchant-{version}-py3-none-any.whl"
    dest = src.replace("any", platform)
    print(src, "->", dest)
    os.rename(src, dest)


def ensure_empty(data_path):
    print(":: Ensuring that", data_path, "is empty")
    if os.path.exists(data_path):
        shutil.rmtree(data_path)
    os.mkdir(data_path)


def make_windows_wheel(c, platform):
    ensure_empty("build/")
    ensure_empty("enchant/data/")
    bootstrap_windows(platform)
    c.run("poetry build -f wheel")
    rename_wheel(platform)


def make_wheel_any(c):
    ensure_empty("build/")
    ensure_empty("enchant/data/")
    c.run("poetry build -f wheel")


def make_sdist(c):
    ensure_empty("build/")
    ensure_empty("enchant/data/")
    c.run("poetry build -f sdist")
