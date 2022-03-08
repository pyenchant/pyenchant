.. _installation:

Installation
=============

PyEnchant is compatible with Python versions **3.7** and above at
the time of writing - `tox.ini <https://github.com/pyenchant/pyenchant/blob/main/tox.ini>`_
being the authoritative source.

The PyEnchant package is available `on pypi <https://pypi.org/project/pyenchant>`_.

You can install it with ``pip`` as usual.

However, to work properly, PyEnchant needs to:

* find the Enchant C library
* find the dictionaries for your particular language

The way to achieve this depends on the platform you are using:

Installing the Enchant C library
--------------------------------

On FreeBSD
+++++++++++

The quickest way is to install `libenchant` using `pkg(8) <man.freebsd.org/pkg/8>`_:

.. code-block:: console

    pkg install enchant2

On Linux
++++++++

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
++++++++

The quickest way is to install `libenchant` using `Homebrew <https://brew.sh/>`_:

.. code-block:: console

    brew update
    brew install enchant

Apple Silicon related errors
~~~~~~~~~~~

If you get this error:
``The 'enchant' C library was not found and maybe needs to be installed.``,
as a workaround, you may need to install an ``x86_64`` (Intel) version of ``enchant``.
In order to do so, you need to install the ``x86_64`` version of Homebrew in
``/usr/local/`` and then use this version to install the corresponding
version of ``enchant``.

.. code-block:: bash

    arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    arch -x86_64 /usr/local/bin/brew install enchant
    
If you get this error:
``[...] (mach-o file, but is an incompatible architecture (have 'x86_64', need 'arm64e')), [...]``
This means that you are mixing architectures (the ``arm64`` native one with architecture and the ``x86_64`` architecture emulated by Rosetta2) between the ``libenchant`` (installed with Homebrew) and your python interpreter that ``import enchant``. This can happen if you keep parallel python environments for different architecures.

If you are using ``conda`` environments , please note that the ``pyenchant`` cannot yet be installed via ``conda`` on MacOS (see `this comment <https://github.com/pyenchant/pyenchant/issues/279#issuecomment-1047079747>`_). You'll have to install it via ``pip``, and it causes some troubles if you are in a ``arm64`` ``conda`` environment.
If you installed Python using ``conda``, it won't find the ``enchant`` C library because it won't look under the native library homebrew installation folder (``/opt/homebrew/lib/``) where it was installed via ``brew install enchant``.
There are 3 workarounds to this problem:

* set the environment variable ``PYENCHANT_LIBRARY_PATH=/opt/homebrew/lib/libenchant-2.2.dylib`` or
* set the environment variable ``DYLD_LIBRARY_PATH=/opt/homebrew/lib/`` or
* use the python installed with ``homebrew`` (``/opt/homebrew/Cellar/python@<version>``) instead of the one installed by ``conda``, but you lose the benefit of using different python versions in different environments.

Refer to the comments in `this issue <https://github.com/pyenchant/pyenchant/issues/265>`_ for a more detailled description of some of the issues related to Apple Silicon.

MacPorts
~~~~~~~~~~~

If you are using `MacPorts <https://www.macports.org/>`_ you can also
install the `enchant2 <https://github.com/macports/macports-
ports/tree/master/textproc/enchant2>`_ package. Please make sure to add
the port variants for the spellers you’d like to use. For example, to
build the enchant library for aspell and hunspell, use:

.. code:: bash

   sudo port install enchant2 +aspell +hunspell +applespell

On Windows
+++++++++++

The `enchant` C library depends on `glib2`, which poses some interesting challenges.

There are two ways to use install the PyEnchant library on Windows,
both with their pros and cons.

Using the binary wheel
~~~~~~~~~~~~~~~~~~~~~~~

The Windows binary wheels on *pypi.org* contain a pre-compiled `enchant` library,
if your Python version is compatible, it will get used by `pip` automatically.

Pros:

 * "Just works" in the majority of cases

Cons:

 * The only provider is ``hunspell``
 * The only installed dictionary is for the English language
 * A copy of the `glib2.dll` and other dependencies are included

Using MinGW
~~~~~~~~~~~

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

On an other platfrom
++++++++++++++++++++++

Unfortunately, if your platfrom is not listed here, there's a good chanche that
PyEnchant will not work. Feel free to open an issue on PyEnchant bug tracker if
this is the case.

Installing a dictionary
------------------------

Let's assume you want to use PyEnchant on a text written in German.

First, use the Enchant Python API to list known languages and providers::

    import enchant
    broker = enchant.Broker()
    broker.describe()
    broker.list_languages()


If ``enchant.list_languages()`` shows ``de_DE``, you're done and can move on to the
tutorial section.

If not, you should install the dictionary for one of the listed providers.

So for instance, if the ``hunspell`` is listed as a Enchant provider, you
should install the German dictionary for the ``hunspell`` provider.

On **FreeBSD**, **Linux**, and **macOS**,this can be done
by installing the ``hunspell-de`` or the ``de-hunspell`` package.

On **Windows**, if you have installed PyEnchant from a
wheel, you can download the hunspell dictionary files you need
(both the `.dic` and `.aff` extensions) and put them inside
``/path/to/enchant/data/mingw<bits>/enchant/share/hunspell``. You
can find many dictionaries in `LibreOffice sources
<https://cgit.freedesktop.org/libreoffice/dictionaries/tree/>`_.


Troubleshooting
---------------

Despite our best efforts, it is possible that the procedures documented above
do not work.

To have a clue about what is wrong, you can set the `PYENCHANT_VERBOSE_FIND` environment
variable to any non-empty value and run ``python -c 'import enchant'``.

If you can't figure out what is wrong, it's probably a bug in PyEnchant,
so feel free to open an issue on GitHub,  preferably containing the output
of the above command.
