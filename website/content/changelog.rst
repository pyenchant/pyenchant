Changelog
=========

3.2.2 (2021-10-05)
------------------

* Add support for Python 3.10

3.2.1 (2021-06-24)
--------------------

* Fix ``Dict.__del__`` sometimes raising `TypeError` upon exit (#98). Patch by @rr-
* Default development branch is now called ``main``
* Bump ``black`` to 21.6b0

3.2.0 (2020-12-08)
-------------------

* Add support for Python 3.9
* Add trove classifiers for all supported Python versions
* Run ``pyupgrade`` across the code base
* Update documentation about MacPorts

3.1.1 (2020-05-31)
------------------

* On Windows, set PATH instead of calling ``SetDllDirectory`` before loading the
  Enchant C library. This allows PyEnchant to co-exist with other libraries
  in the same program. Fix #207.

3.1.0 (2020-05-20)
-------------------

* Add ``enchant.get_user_config_dir()``
* Fix: ``enchant.get_enchant_version()`` now returns a ``str``, not some ``bytes``

3.0.1 (2020-03-01)
------------------

* Add missing LICENSE.txt in source distribution


3.0.0 (2020-03-01)
------------------

Highlights
++++++++++

* Uncouple PyEnchant version from the Enchant version. This release should be compatible with
  Enchant 1.6 to 2.2
* Fix using PyEnchant with Enchant >= 2.0
* Add support for pypy3, Python 3.7 and Python 3.8
* New website, hosted on https://pyenchant.github.io/pyenchant/
* Add `enchant.set_prefix_dir()`

Breaking changes
++++++++++++++++

* Drop support for Python2

* **macOS**: The C enchant library is no longer embedded inside the wheel -
  you should install the C enchant library with ``brew`` or ``ports``.


Clean ups
+++++++++

* Port test suite to ``pytest``.
* Add ``tbump`` configuration to simplify the release process
* Format code with ``black``.
* Remove compatibility layers with Python2 from ``enchant.utils``
* Use ``flake8`` to catch some errors during CI
* Fix some PEP8 naming violations
* Switch to GitHub Actions for CI


2.0.0 (2017-12-10)
------------------

* Removed deprecated `is_in_session` method, for compatibility
  with enchant 2.

1.6.6 (2014-06-16)
------------------

* New website and documentation, generated with Hyde and Sphinx.
* Fix ``SpellChecker.replace()`` when the replacement is shorter than
  the erroneous word; previously this would corrupt the internal
  state of the tokenizer.  Thanks Steckelfisch.
* Make Dict class pickle-safe.  Among other things, this should help
  with strange deadlocks when used with the multiprocessing module.
* Ability to import the module even when the enchant C library isn't
  installed, by setting PYENCHANT_IGNORE_MISSING_LIB env var.
* New utility function "trim_suggestions", useful for trimming the
  list of suggestions to a fixed maximum length.
* Change the way DeprecationWarnings are issued, to point to the line
  line in user code rather than inside pyenchant.  Thanks eriolv.
* Add GetSpellChecker() method to wxSpellCheckerDialog.  Thanks bjosey.


1.6.5 (2010-12-14)
------------------

* restore compatibility with Python 3 (including 3.2 beta1).
* fix unittest DeprecationWarnings on Python 3.
* statically compile libstdc++ into pre-built windows binaries.

1.6.4 (2010-12-13)
------------------

* DictWithPWL:  use pwl and pel to adjust the words returned by suggest().
* Fix tokenization of utf8 bytes in a mutable character array.
* get_tokenizer():  pass None as language tag to get default tokenizer.
* prevent build-related files from being included in the source tarball.

1.6.3 (2010-08-17)
------------------

* Bundle pre-compiled libraries for Mac OSX 10.4 and later.
* Improved handling of unicode paths on win32.
* Changed DLL loading logic for win32, to ensure that we don't accidentally
  load older versions of e.g. glib that may be on the DLL search path.
* Added function get_enchant_version() to retrieve the version string for
  the underlying enchant library.

1.6.2 (2010-05-29)
------------------

* Upgraded bundled enchant to v1.6.0.
* Fixed bug in printf() utility function; all input args are now converted
  to strings before printing.

1.6.1 (2010-03-06)
------------------

* Fixed loading of enchant DLL on win32 without pkg_resources installed.
* Fixed HTMLChunker to handle unescaped < and > characters that are
  clearly not part of a tag.

1.6.0 (2010-02-23)
------------------

* Upgraded to enchant v1.5.0:

    * new Broker methods get_param() and set_param() allow
      runtime customisation of provider data

* Added the concept of 'chunkers' to enchant.tokenize.get_tokenizer().
  These serve split split the text into large chunks of checkable tokens.
* implemented a simple HTMLChunker class
* Moved error classes into 'enchant.errors' for easier importing
* Moved testcases into separate files so they're not loaded by default
* Allowed SpellChecker to use default language if none is specified
* Improved compatibility with Python 3

1.5.3 (2009-05-02)
------------------

* Fixed termination conditions in English tokenization loop.
* Improved unicode detection in English tokenizer.
* Made enchant spellcheck all of its docstrings as part of the
  unittest suite.

1.5.2 (2009-04-27)
------------------

* Modify utils.get_resource_filename and utils.win32_data_files for
  compatibility with py2exe (which was broken in the move to ctypes).
  Thanks to Stephen George for the fix.

1.5.1 (2009-01-08)
------------------

* SpellChecker.add_to_personal renamed to SpellChecker.add and fixed
  to use the corresponding Dict method.

1.5.0 (2008-11-25)
------------------

* Migrated from SWIG to ctypes

    * now runs under PyPy!
    * also opens possibilities for Jython, IronPython, ...

* Compatibility updates for Python 3.0, mostly around unicode strings
* Dropped compatibility with Python 2.2

1.4.2 (2008-06-18)
------------------

* upgrade to enchant v1.4.2
* windows version can now be installed at a path containing
  unicode characters

1.4.0 (2008-04-18)
------------------

* upgrade to enchant v1.4.0, with new functionality and APIs:

    * All dictionary providers now use a shared default personal word file
      (largely obsoleting the DictWithPWL class)
    * Ability to exclude words using Dict.remove, remove_from_session
    * Dict.add_to_personal renamed to Dict.add
    * Dict.is_added/Dict.is_removed for checking membership of word lists
    * unicode PWL filenames now handled correctly on Windows
* upgrade bundled glib DLLs in Windows version

1.3.1 (2007-12-19)
------------------

* treat combining unicode marks as letters during tokenization
* cleanup of wxSpellCheckerDialog, thanks to Phil Mayes
* upgrades of bundled components in Windows version

    * upgraded glib DLLs
    * latest dictionaries from OpenOffice.org
    * latest version of Hunspell

1.3.0 (2006-12-29)
------------------

* Re-worked the tokenization API to allow filters but still
  remove non-alpha-numeric characters from words by default.
  This introduces some minor backward-incompatibilities to the
  API, hence the full minor version bump.

    * 'fallback' argument to get_tokenizer() was removed, just
      catch the Error and re-try with whatever is appropriate for
      your application.
    * filters should be passed into get_tokenizer() as the second
      argument, rather than applied as separate functions.
    * Basic whitespace-and-punctuation tokenization separated from
      the language-specific parts.
    * Internal details of Filter classes expanded and generalized
    * English tokenization rules reverted to 1.1.5 version


1.2.0 (2006-11-05)
------------------

* Implemented "filters" that allow tokenization to skip common word
  forms such as URLs, WikiWords, email addresses etc.
* Now ships with enchant-1.3.0, meaning:

  * PWLs can return a useful list of suggestions rather than
    the empty list
  * Hunspell replaces MySpell as the default Windows backend

* Tokenization doesn't split words at non-alpha characters by default
* GtkSpellCheckerDialog contributed by Fredrik Corneliusson
* Removed deprecated functionality:

  * Dict.add_to_personal
  * All registry handling functionality from enchant.utils
  * enchant.utils.SpellChecker (use enchant.checker.SpellChecker)

* Removed PyPWL, as native enchant PWLs can now suggest corrections

1.1.5 (2006-01-19)
------------------

* Fix hang in included MySpell (Windows distribution)
* Workaround for some MySpell/unicode problems
* Update to latest setuptools ez_setup.py

1.1.4 (2006-01-09)
------------------

* No longer need to use the registry under Windows
* Moved to setuptools for managing distribution
* Implemented unittest TestCases, works with `python setup.py test`
* Plugins on Windows moved to "enchant" subdirectory
* SpellChecker now coerces to/from unicode automatically
* Use python default encoding rather than UTF-8 where appropriate
* Various documentation cleanups
* bug fixes:

     * (1230151): count of live instances done by normalized key
     * Accept unicode strings as broker orderings


1.1.3 (2005-06-15)
------------------

* support for Python 2.2
* use 'locale' module to look up default language if none specified
* more and better regression tests
* mark deprecated interfaces with warnings
* removed <data> parameter to Dict constructor, with lots of
  reshuffling behind the scenes
* add DictNotFoundError as a subclass of Error
* Remove de_AT from languages in the Windows version, it was
  causing errors
* bug fixes:

     * memory leak in DictWithPWL._free()
     * incorrect cache handling for PWLs
