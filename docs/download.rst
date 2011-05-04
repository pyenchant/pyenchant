
Downloading PyEnchant
=====================

The current release of PyEnchant is version 1.6.5. See the python package index for a full list of available downloads.

Prerequisites
-------------

To get PyEnchant up and running, you will need the following software installed:

    * Python 2.3 or later, with the `ctypes <http://docs.python.org/library/ctypes.html>`_ module installed.
        * Python 2.5 and higher include ctypes by default.
        * For older versions, it can be downloaded `here <http://sourceforge.net/projects/ctypes/>`_.
    * The `enchant <http://www.abisource.com/enchant/>`_ library, version 1.5.0 or later.
        * For Windows users, the binary installers below include a pre-built copy of enchant.
        * For Mac OSX users, the experimental binary installers below include a pre-built copy of enchant.


Source Distribution
-------------------

PyEnchant is distributed using the Python "setuptools" framework. In most cases this works just like the standard "distutils" framework, but you may be interested in these `notes on installing with setuptools <http://peak.telecommunity.com/DevCenter/setuptools#what-your-users-should-know>`_. Basic instructions for building from source can also be found in the :doc:`tutorial<tutorial>`. The source is available for download in the following file:

    * `pyenchant-1.6.5.tar.gz <http://pypi.python.org/packages/source/p/pyenchant/pyenchant-1.6.5.tar.gz>`_


Windows Users
-------------

For convenience, Windows users are provided with a pre-built installation program which can be used to install PyEnchant.

    * `pyenchant-1.6.5.win32.exe <http://pypi.python.org/packages/any/p/pyenchant/pyenchant-1.6.5.win32.exe>`_

There are also `Python Eggs <http://peak.telecommunity.com/DevCenter/PythonEggs>`_ available for users who prefer them:

    * Python 2.5: `pyenchant-1.6.5-py2.5-win32.egg <http://pypi.python.org/packages/2.5/p/pyenchant/pyenchant-1.6.5-py2.5-win32.egg>`_
    * Python 2.6: `pyenchant-1.6.5-py2.6-win32.egg <http://pypi.python.org/packages/2.6/p/pyenchant/pyenchant-1.6.5-py2.6-win32.egg>`_
    * Python 2.7: `pyenchant-1.6.5-py2.7-win32.egg <http://pypi.python.org/packages/2.7/p/pyenchant/pyenchant-1.6.5-py2.7-win32.egg>`_

These pre-built distributions contain a compiled Enchant binary as well as several DLLs produced by `Tor Lillqvist <http://www.gimp.org/~tml/gimp/win32>`_. In order to ensure compliance with the license for these supporting libraries, the sourcecode and supporting build environment is available for download in the following file:

    * `pyenchant-bdist-win32-sources-1.6.5.tar.gz <https://github.com/downloads/rfk/pyenchant/pyenchant-bdist-win32-sources-1.6.5.tar.gz>`_

Windows users can also follow the instructions above to build from source.


Mac OS X Users
--------------

For convenience, Mac OS X users are provided with a pre-built installer program which can be used to install PyEnchant. Please note that these distributions are currently **experimental** but seem to work well.

    * Python 2.5: `pyenchant-1.6.5-py2.5-macosx-10.4-universal.dmg <http://pypi.python.org/packages/2.5/p/pyenchant/pyenchant-1.6.5-py2.5-macosx-10.4-universal.dmg>`_
    * Python 2.6: `pyenchant-1.6.5-py2.6-macosx-10.4-universal.dmg <http://pypi.python.org/packages/2.6/p/pyenchant/pyenchant-1.6.5-py2.6-macosx-10.4-universal.dmg>`_
    * Python 2.7: `pyenchant-1.6.5-py2.7-macosx-10.4-universal.dmg <http://pypi.python.org/packages/2.7/p/pyenchant/pyenchant-1.6.5-py2.7-macosx-10.4-universal.dmg>`_

There are also Python Eggs available for users who prefer them:

    * Python 2.5: `pyenchant-1.6.5-py2.5-macosx-10.4-universal.egg <http://pypi.python.org/packages/2.5/p/pyenchant/pyenchant-1.6.5-py2.5-macosx-10.4-universal.egg>`_
    * Python 2.6: `pyenchant-1.6.5-py2.6-macosx-10.4-universal.egg <http://pypi.python.org/packages/2.6/p/pyenchant/pyenchant-1.6.5-py2.6-macosx-10.4-universal.egg>`_
    * Python 2.7: `pyenchant-1.6.5-py2.7-macosx-10.4-universal.egg <http://pypi.python.org/packages/2.7/p/pyenchant/pyenchant-1.6.5-py2.7-macosx-10.4-universal.egg>`_

These pre-built distributions contain a compiled Enchant binary as well as several supporting libraries. In order to ensure compliance with the license for these supporting libraries, the sourcecode and supporting build environment is available for download in the following file:

    * `pyenchant-bdist-osx-sources-1.6.5.tar.gz <https://github.com/downloads/rfk/pyenchant/pyenchant-bdist-osx-sources-1.6.5.tar.gz>`_

Mac OSX users can also follow the instructions above to build from source. 


