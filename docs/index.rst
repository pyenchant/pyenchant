
PyEnchant is a spellchecking library for Python, based on the excellent `Enchant <http://www.abisource.com/enchant/>`_ library. Read more below, or skip straight ahead to the :doc:`download<download>` page.


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



About PyEnchant
---------------

PyEnchant is a set of language bindings and some wrapper classes to make the excellent `Enchant <http://www.abisource.com/enchant/>`_ spellchecker available as a Python module. The bindings are created using `ctypes <http://docs.python.org/lib/module-ctypes.html>`_. It includes all the functionality of Enchant with the flexibility of Python and a nice "Pythonic" object-oriented interface. It also aims to provide some higher-level functionality than is available in the C API.

To get started, check out the comprehensive :doc:`tutorial<tutorial>` or the auto-generated :doc:`API listing<api/enchant>`. If you just want to get up and running in a hurry, here's a quick sample of pyenchant in action::

    >>> import enchant
    >>> d = enchant.Dict("en_US")
    >>> d.check("Hello")
    True
    >>> d.check("Helo")
    False
    >>> d.suggest("Helo")
    ['He lo', 'He-lo', 'Hello', 'Helot', 'Help', 'Halo', 'Hell', 'Held', 'Helm', 'Hero', "He'll"]
    >>>


You can report bugs and view the latest development progress at the `github project page <http://github.com/rfk/pyenchant/tree/master>`_. There are more downloads available at the `python package index <http://pypi.python.org/pypi/pyenchant/>`_, including all the `old versions of pyenchant <http://pypi.python.org/simple/pyenchant/>`_.
    

Documentation
-------------

.. toctree::
   :maxdepth: 2

   download.rst
   tutorial.rst
   faq.rst
   api/index.rst
   shootout.rst

