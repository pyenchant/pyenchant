PyEnchant
=========

Introduction
------------

PyEnchant is a spellchecking library for Python, based on the excellent `Enchant <https://abiword.github.io/enchant/>`_ library.

PyEnchant combines all the functionality of the underlying Enchant
library with the flexibility of Python and a nice "Pythonic"
object-oriented interface. It also aims to provide some higher-level
functionality than is available in the C API.

Here's a quick sample of PyEnchant in action::

    >>> import enchant
    >>> d = enchant.Dict("en_US")
    >>> d.check("Hello")
    True
    >>> d.check("Helo")
    False
    >>> d.suggest("Helo")
    ['He lo', 'He-lo', 'Hello', 'Helot', 'Help', 'Halo', 'Hell', 'Held', 'Helm', 'Hero', "He'll"]
    >>>


.. warning::
   In genereal, PyEnchant will **not** work out of the box after having
   been installed with `pip`. See the :ref:`installation` section for
   more details.


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
   contributing.rst
