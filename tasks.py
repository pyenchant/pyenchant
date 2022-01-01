from invoke import call, task

from bootstrap import main as main_bootstrap


@task
def bootstrap(c):
    main_bootstrap()


@task
def black(c, check=False):
    print("Running black")
    cmd = f"black ."
    if check:
        cmd += " --check"
    c.run(cmd)


@task
def isort(c, check=False):
    print("Running isort")
    cmd = f"isort ."
    if check:
        cmd += " --check"
    c.run(cmd)


@task
def flake8(c):
    print("Running flake8")
    c.run(f"flake8 enchant tests")


@task
def sphinx(c, autobuild=False, builder="html"):
    build_dir = "website/build"
    source_dir = "website/content"
    conf_dir = "website"
    out_dir = f"website/out/{builder}"
    if autobuild:
        script = "sphinx-autobuild"
    else:
        script = "sphinx-build"
    cmd = f"{script} -build -W -b {builder} -c {conf_dir} {source_dir} {out_dir}"
    c.run(cmd, echo=True)


@task(
    pre=[
        call(black, check=True),
        call(isort, check=True),
        call(flake8),
    ]
)
def lint(c):
    pass


@task
def test(c):
    c.run("pytest")
