
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


You can report bugs and view the latest development progress at the `github project page <http://github.com/rfk/pyenchant/tree/master>`_. There are more downloads available at the `python package index <http://pypi.python.org/pypi/pyenchant/>`_, including all the `old versions of PyEnchant <http://pypi.python.org/simple/pyenchant/>`_.


News
----

2010-12-14:  Version 1.6.5 released
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Version 1.6.5 of PyEnchant has been released, with the following changes:

    * restore compatability with Python 3 (including 3.2 beta1)
    * fix unittest DeprecationWarnings on Python 3
    * statically compile libstdc++ into pre-built windows binaries


2010-12-13:  Version 1.6.4 released
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Version 1.6.4 of PyEnchant has been released, with the following changes:

    * DictWithPWL: use pwl and pel to adjust the words returned by suggest()
    * Fix tokenization of utf8 bytes in a mutable character array
    * get_tokenizer(): pass None as language tag to get default tokenizer
    * prevent build-related files from being included in the source tarball


Documentation Index
-------------------

.. toctree::
   :maxdepth: 2

   download.rst
   tutorial.rst
   faq.rst
   api/index.rst
   shootout.rst

