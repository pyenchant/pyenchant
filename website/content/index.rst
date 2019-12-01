
PyEnchant
=========

PyEnchant is a spellchecking library for Python, based on the excellent `Enchant <http://www.abisource.com/enchant/>`_ library.

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



Documentation Index
-------------------

.. toctree::
   :maxdepth: 2

   tutorial.rst
   api/index.rst

