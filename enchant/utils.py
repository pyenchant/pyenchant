# pyenchant
#
# Copyright (C) 2004 Ryan Kelly
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
#
# In addition, as a special exception, you are
# given permission to link the code of this program with
# non-LGPL Spelling Provider libraries (eg: a MSFT Office
# spell checker backend) and distribute linked combinations including
# the two.  You must obey the GNU Lesser General Public License in all
# respects for all of the code used other than said providers.  If you modify
# this file, you may extend this exception to your version of the
# file, but you are not obligated to do so.  If you do not wish to
# do so, delete this exception statement from your version.
#
"""

    enchant.utils:    Misc utilities for the enchant package
    
    This module provies miscellaneous utilities for use with the
    enchant spellchecking package.  Currently available functionality
    includes:
        
        * functions for dealing with locale/language settings
        * ability to list supporting data files (win32 only)
          
"""

import os

# Attempt to access local language information
try:
    import locale
except ImportError:
    locale = None

class _EnchantStr(str):
    """String subclass for interfacing with enchant.

    This class encapsulate the logic for interfacing between python native
    string/unicode objects and the underlying enchant library, which expects
    all strings to tbe UTF-8 character arrays.

    Initialise it with a string or uniode object, and use the encode() method
    to obtain an object suitable for passing to the underlying C library.
    When strings are read back into python, use decode(s) to translate them
    back into the appropriate python-level string type.

    This allows us to following the common Python 2.x idiom of returning
    unicode when unicode is passed in, and strings otherwise.  It also
    lets the interface be upwards-compatible with Python 3, in which string
    objects will be unicode by default.
    """

    def __new__(self,value):
        """_EnchantStr data constructor.

        This method records whether the initial string was unicode, then
        simply passes it along to the default string constructor.
        """
        if type(value) is unicode:
          self._was_unicode = True
          value = value.encode("utf-8")
        else:
          self._was_unicode = False
        return str.__new__(self,value)

    def encode(self):
        """Encode this string into a form usable by the enchant C library."""
        return self

    def decode(self,value):
        """Decode a string returned by the enchant C library."""
        if self._was_unicode:
            return value.decode("utf-8")
        else:
            return value


def get_default_language(default=None):
    """Determine the user's default language, if possible.
    
    This function uses the 'locale' module to try to determine
    the user's prefered language.  The return value is as
    follows:
        
        * if a locale is available for the LC_MESSAGES category,
          that language is used
        * if a default locale is available, that language is used
        * if the keyword argument <default> is given, it is used
        * None
        
    Note that determining the user's language is in general only
    possible if they have set the necessary environment variables
    on their system.
    """
    try:
        import locale
        tag = locale.getlocale()[0]
        if tag is None:
            tag = locale.getdefaultlocale()[0]
            if tag is None:
                raise Error("No default language available")
        return tag
    except:
        pass
    return default


def win32_data_files():
    """Get list of supporting data files, for use with setup.py
    
    This function returns a list of the supporting data files available
    to the running version of PyEnchant.  This is in the format expected
    by the data_files argument of the distutils setup function.  It's
    very useful, for example, for including the data files in an executable
    produced by py2exe.
    
    Only really tested on the win32 platform (it's the only platform for
    which we ship our own supporting data files)
    """
    dataDirs = ("share/enchant/myspell","share/enchant/ispell","lib/enchant")
    mainDir = os.path.abspath(os.path.dirname(__file__))
    dataFiles = []
    for dataDir in dataDirs:
        files = []
        fullDir = os.path.join(mainDir,os.path.normpath(dataDir))
        for fn in os.listdir(fullDir):
            fullFn = os.path.join(fullDir,fn)
            if os.path.isfile(fullFn):
                files.append(fullFn)
        dataFiles.append((dataDir,files))
    return dataFiles

# Make enchant.Error available
# Done at bottom of file to avoid circular imports
from enchant import Error


