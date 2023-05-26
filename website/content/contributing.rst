Contributing to PyEnchant
=========================

Opening bugs
------------

Please use the `GitHub Template <https://github.com/pyenchant/pyenchant/blob/main/.github/ISSUE_TEMPLATE/bug_report.md>`_ for bug reports

Submitting Pull Requests
-------------------------

If you want to submit a pull request, it's advised to run the CI checks locally:

* Install Python3
* Install `tox`
* Run `tox` with the proper list of environments:

.. code-block:: console

  tox -e website -e linters -e pyXY

(Replace `pyXY` by your current Python installation)

Note: you will need an `en_US` dictionary installed for the tests to run. See :ref:`installation` for more details.
for more details.

Updating the website
---------------------

The PyEnchant website is hosted on GitHub pages and there's a GitHub workflow
to automatically update it every time a commit is pushed on the `main` branch.

You can also run `tox -e website-dev` locally to spawn a process that will watch
the changes in the `website/` directory and auto-refresh connected browsers.

Making a new release
---------------------

Re-building the Enchant C library for Windows
+++++++++++++++++++++++++++++++++++++++++++++

In order to publish the Windows wheels to pypi, you must first compile
the code in the `Enchant repository <https://github.com/AbiWord/enchant/>`_
so that the Windows wheels are usable out of the box.

To do that, we have a fork at ``https://github.com/pyenchant/enchant`` where we publish
DLLs for the Enchant library as GitHub releases, and a ``bootstrap.py`` file that downloads them.

Unfortunately, `AbiWord` switched from AppVeyor to GitHub Actions and our fork is still using AppVeyor, which means
we are stuck with Enchant v2.2.7 for now ...


Publishing to pypi.org
+++++++++++++++++++++++

Then you need to bump the version number in ``setup.cfg`` and publish a new release on Pypi. You can do it
with `tbump <https://github.com/TankerHQ/tbump>`_, which will automate the process:

.. code-block:: console

    pipx install tbump
    tbump <new-version>
