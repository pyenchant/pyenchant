"""
Generate the source distribution and 3 wheels

* py3-none-win32.whl, for Windows 32 bits
* py3-none-win64.whl, for Windows 64 bits
* py3-none-any.whl, for everything else

"""

from argparse import ArgumentParser
import os
import shutil
import subprocess
import tomllib
from bootstrap import bootstrap_windows


def run(*cmd: str) -> None:
    print(*cmd)
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE)


def ensure_empty(data_path: str) -> None:
    if os.path.exists(data_path):
        print("rm", data_path)
        shutil.rmtree(data_path)
    os.mkdir(data_path)


def make_windows_wheel(*, version: str, bits: int) -> None:
    # This is done in two steps
    ensure_empty("build/")
    ensure_empty("enchant/data/")
    bootstrap_windows(bits=bits)
    platform = {32: "win32", 64: "win_amd64"}[bits]
    # This builds a wheel with no platform tag
    run("python", "-m", "build", "--wheel")
    # So we need to add it manually:
    run(
        "python",
        "-m",
        "wheel",
        "tags",
        f"--platform-tag={platform}",
        f"dist/pyenchant-{version}-py3-none-any.whl",
    )


def make_wheel_any() -> None:
    ensure_empty("build/")
    ensure_empty("enchant/data/")
    run("python", "-m", "build", "--wheel")


def make_sdist() -> None:
    ensure_empty("build/")
    ensure_empty("enchant/data/")
    run("python", "-m", "build", "--sdist")


def main() -> None:
    """Build artifacts that we need to upload to  pypi"""
    with open("tbump.toml", "rb") as file:
        tbump_config = tomllib.load(file)
        version = tbump_config["version"]["current"]
    ensure_empty("build/")
    ensure_empty("dist/")

    print("Building artifacts for release", version)
    for bits in [32, 64]:
        make_windows_wheel(version=version, bits=32)
        make_windows_wheel(version=version, bits=64)

    make_wheel_any()
    make_sdist()

    print("Done. Artifacts are in dist/, ready for upload.")


if __name__ == "__main__":
    main()
