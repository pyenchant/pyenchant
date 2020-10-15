PyEnchant
=========

Introduction
------------

PyEnchant is a spellchecking library for Python, based on the excellent `Enchant <https://abiword.github.io/enchant/>`_ library.

PyEnchant combines all the functionality of the underlying Enchant
library with the flexibility of Python and a nice "Pythonic"
object-oriented interface. It also aims to provide some higher-level
functionality than is available in the C API.

To get started, check out the comprehensive :doc:`tutorial<tutorial>` or the auto-generated :doc:`API listing<api/enchant>`. If you just want to get up and running in a hurry, here's a quick sample of PyEnchant in action::

    >>> import enchant
    >>> d = enchant.Dict("en_US")
    >>> d.check("Hello")
    True
    >>> d.check("Helo")
    False
    >>> d.suggest("Helo")
    ['He lo', 'He-lo', 'Hello', 'Helot', 'Help', 'Halo', 'Hell', 'Held', 'Helm', 'Hero', "He'll"]
    >>>


Otherwise, take a look at the documentation index:

Documentation Index
-------------------

.. toctree::
   :maxdepth: 1

   install.rst
   tutorial.rst
   api/index.rst
   faq.rst
   shootout.rst
   changelog.rst
