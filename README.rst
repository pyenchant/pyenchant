pyenchant:  Python bindings for the Enchant spellchecker
========================================================

.. image:: https://img.shields.io/pypi/v/pyenchant.svg
    :target: https://pypi.org/project/pyenchant

.. image:: https://img.shields.io/pypi/pyversions/pyenchant.svg
    :target: https://pypi.org/project/pyenchant

.. image:: https://github.com/pyenchant/pyenchant/workflows/tests/badge.svg
    :target: https://github.com/pyenchant/pyenchant/actions

.. image:: https://builds.sr.ht/~dmerej/pyenchant.svg
    :target: https://builds.sr.ht/~dmerej/pyenchant

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

This package provides a set of Python language bindings for the Enchant
spellchecking library.  For more information, visit the project website:

    http://pyenchant.github.io/pyenchant/

What is Enchant?
----------------

Enchant is used to check the spelling of words and suggest corrections
for words that are miss-spelled.  It can use many popular spellchecking
packages to perform this task, including ispell, aspell and MySpell.  It
is quite flexible at handling multiple dictionaries and multiple
languages.

More information is available on the Enchant website:

    https://rrthomas.github.io/enchant/


How do I use PyEnchant ?
-------------------------

*Warning*: in general, PyEnchant will **not** work out of the box after
having been installed with `pip` (or any other installation method) -
see `the documentation <https://pyenchant.github.io/pyenchant/>`_ for more details.


Who is responsible for all this?
--------------------------------

The credit for Enchant itself goes to Dom Lachowicz.  Find out more details
on the Enchant website listed above.  Full marks to Dom for producing such
a high-quality library.

The glue to pull Enchant into Python via ctypes was written by Ryan Kelly.
He needed a decent spellchecker for another project he was working on, and
all the solutions turned up by Google were either extremely non-portable
(e.g. opening a pipe to ispell) or had completely disappeared from the web
(what happened to SnakeSpell?)  It was also a great excuse to teach himself
about SWIG, ctypes, and even a little bit of the Python/C API.

Finally, after Ryan stepped down from the project, Dimitri Merejkowsky
became the new maintainer.

