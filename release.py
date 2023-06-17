import os
import shutil
import subprocess

from bootstrap import bootstrap_windows


def run(*cmd: str) -> None:
    print(*cmd)
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE)


def ensure_empty(data_path: str) -> None:
    if os.path.exists(data_path):
        print("rm", data_path)
        shutil.rmtree(data_path)
    os.mkdir(data_path)


def make_windows_wheel(bits: int) -> None:
    ensure_empty("build/")
    ensure_empty("enchant/data/")
    bootstrap_windows(bits=bits)
    platform = {32: "win32", 64: "win_amd64"}[bits]
    run("python", "setup.py", "bdist_wheel", "--plat-name", platform)


def make_wheel_any() -> None:
    ensure_empty("build/")
    ensure_empty("enchant/data/")
    run("python", "setup.py", "bdist_wheel")


def make_sdist() -> None:
    ensure_empty("build/")
    ensure_empty("enchant/data/")
    run("python", "setup.py", "sdist")


def main() -> None:
    """Build artifacts that we need to upload to  pypi"""
    ensure_empty("build/")
    ensure_empty("dist/")

    print("Building artifacts for new release ...")
    make_windows_wheel(bits=32)
    make_windows_wheel(bits=64)

    make_wheel_any()
    make_sdist()

    print("Done. Artifacts are in dist/, ready for upload.")


if __name__ == "__main__":
    main()
