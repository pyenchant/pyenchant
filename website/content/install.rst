Installation
=============

PyEnchant is compatible with Python versions **3.5** and above at
the time of writing - `tox.ini <https://github.com/pyenchant/pyenchant/blob/master/tox.ini>`_
being the authoritative source.

The PyEnchant package is available `on pypi <https://pypi.org/project/pyenchant>`_.

You can install it with ``pip`` as usual.

However, PyEnchant needs to find the Enchant C library in order to work properly. The way to
achieve this depends on the platform you are using:

On Linux
--------

The quickest way is to install `libenchant` using the package manager of
your current distribution. PyEnchant tries to be compatible with a large
number of `libenchant` versions. If you find an incompatibility with
your `libenchant` installation, feel free to `open a bug report
<https://github.com/pyenchant/pyenchant/issues>`_.

To detect the `libenchant` binaries, PyEnchant uses
`ctypes.util.find_library() <https://docs.python.org/3/library/ctypes.html#finding-shared-libraries>`_,
which requires `ldconfig`, `gcc`, `objdump` or `ld` to be installed.
This is the case on most major distributions,
however statically linked distributions (like Alpine Linux)
might not bring along `binutils` by default.

On macOS
--------

The quickest way is to install `libenchant` using `Homebrew <https://brew.sh/>`_:

.. code-block:: console

    brew update
    brew install enchant

On Windows
----------

The `enchant` C library depends on `glib2`, which poses some interesting challenges.

There are two ways to use install the PyEnchant library on Windows,
both with their pros and cons.

Using the binary wheel
+++++++++++++++++++++++

The Windows binary wheels on *pypi.org* contain a pre-compiled `enchant` library,
if your Python version is compatible, it will get used by `pip` automatically.

Pros:

 * "Just works" in the majority of cases

Cons:

 * The only provider is ``hunspell``
 * The only installed dictionary is for the English language
 * A copy of the `glib2.dll` and other dependencies are included

Using MinGW
+++++++++++

An other way to use `pyenchant` is to install MinGW (for instance
with `Chocolatey <https://chocolatey.org/>`_), then use  `pacman` to install
the `libenchant` and all its dependencies.

In that case, you can ask pip to **not** use the wheel by running it like this:

.. code-block:: console

   pip install --no-binary pyenchant

Pros:

 * You are using the "official" way to build `enchant` one Windows, thanks
   to the work of the `MinGW` maintainers
 * You can use all the supported providers
 * You can add a new language using `pacman`

Cons:

 * It only works with the ``python3`` binary of the ``MinGW`` distribution,
   so typically *not* the one you've installed from `python.org`.


Troubleshooting
---------------

Despite our best efforts, it is possible that the procedures documented above
do not work.

To have a clue about what is wrong, you can set the `PYENCHANT_VERBOSE_FIND` environment
variable to any non-empty value and run ``python -c 'import enchant'``.

If you can't figure out what is wrong, it's probably a bug in PyEnchant,
so feel free to open an issue on GitHub,  preferably containing the output
of the above command.
