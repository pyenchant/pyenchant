import os
import platform
import shutil
import subprocess
import sys


from bootstrap import bootstrap_windows


def run(*cmd):
    print(*cmd)
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE)


def ensure_empty(data_path):
    if os.path.exists(data_path):
        shutil.rmtree(data_path)
    os.mkdir(data_path)


def make_windows_wheel(platform):
    ensure_empty("build/")
    ensure_empty("enchant/data/")
    bootstrap_windows(platform)
    run("python", "setup.py", "bdist_wheel", "--plat-name", platform)


def make_wheel_any():
    ensure_empty("build/")
    ensure_empty("enchant/data/")
    run("python", "setup.py", "bdist_wheel")


def make_sdist():
    ensure_empty("build/")
    ensure_empty("enchant/data/")
    run("python", "setup.py", "sdist")


def main():
    """ Build artifacts that we need to upload to  pypi """
    ensure_empty("build/")
    ensure_empty("dist/")

    print("Building artifacts for new release ...")
    make_windows_wheel(platform="win_amd64")
    make_windows_wheel(platform="win32")

    make_wheel_any()
    make_sdist()

    print("Done!. Artifacts are in dist/, ready for upload")


if __name__ == "__main__":
    main()
