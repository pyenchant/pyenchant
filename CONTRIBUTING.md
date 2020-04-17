# Contributing to PyEnchant

## Opening bugs

Please use the [GitHub template](./.github/ISSUE_TEMPLATE/bug_report.md) for bug reports

## Submitting Pull Requests

If you want to submit a pull request, it's advised to run the CI checks locally:

* Install Python3
* Install `tox`
* Run `tox` with the proper list of environments:

```console
tox -e website -e linters -e pyXY
```

(Replace `pyXY` by your current Python installation)

Note: you will need an `en_US` dictionary installed for the tests to run. See website
for more details.

## Updating the website

The PyEnchant website is hosted on GitHub pages and there's a GitHub workflow
to automatically update it every time a commit is pushed on the master branch.

You can also run `tox -e website-dev` locally to spawn a process that will watch
the changes in the `website/` directory and auto-refresh connected browsers.

## Making a new release

### Re-building the Enchant C library

Say a new Enchant version is out, and you want to make a new PyEnchant
release containing the pre-compiled Enchant C library.

Here are the steps:

1. Clone [our Enchant fork](https://github.com/pyenchant/enchant)
1. Checkout the `packaging` branch
1. Rebase the branch on top of the appropriate upstream tag
1. Push it and wait the for appveyor builds to kick in. _Note: you do not need to create a pull request!_.
1. Once the appveyor jobs are complete, download the artifacts
1. Push a tag looking like `v<upstream version>-appveyor-<appveyor build number>` in the `pyenchant/enchant` repository
1. Create a release on the tag and and attach the appveyor artifacts to it - that way they won't get lost in 6 months!
1. Adapt the `./bootstrap.py` file with the tag you just pushed

### Publishing to pypi.org

Then you need to bump the version number in `setup.cfg` and publish a new release on Pypi. You can do it
with [tbump](https://github.com/TankerHQ/tbump).
