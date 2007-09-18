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
        
        * 'backported' functionality for python2.2 compatability
        * functions for dealing with locale/language settings
        * ability to list supporting data files (win32 only)
          
"""

# Get generators for python2.2
from __future__ import generators

import os

# Attempt to access local language information
try:
    import locale
except ImportError:
    locale = None

# Define basestring if it's not provided (e.g. python2.2)
try:
    basestring = basestring
except NameError:
    basestring = (str,unicode)
    
# Define enumerate() if it's not provided (e.g. python2.2)
try:
    enumerate = enumerate
except NameError:
    def enumerate(seq):
        """Iterator producing (index,value) pairs for an interable."""
        idx = 0
        for itm in seq:
            yield (idx,itm)
            idx += 1

#  Allow looking up of default language on-demand.

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


