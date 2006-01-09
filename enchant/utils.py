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
        * functions for inserting/removing entries into the Windows
          registry, to point to local version of enchant
        * functions for dealing with locale/language settings
    
    Functionality that is temporarily available and may move or disappear
    in future releases:
        
        * useful string-handling functions (soundex, edit_dist, ...)
        * PyPWL, a pure-python PWL object with enhanced functionality
          
"""

# Get generators for python2.2
from __future__ import generators

import sys
import os
from warnings import warn

try:
    import _winreg as reg
except ImportError:
    reg = None

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

# Make a deprecated SpellChecker available for backwards-compatability
def SpellChecker(*args,**kwds):
    warn("utils.SpellChecker is deprecated, please use checker.SpellChecker",
         DeprecationWarning)
    from checker import SpellChecker
    return SpellChecker(*args,**kwds)



# Useful registry-handling functions

def _reg_get():
    """Get the registry module, or None if not available.
    This function raises an appropriate warning if the registry
    is not available.  Functions requiring registry access should
    use the following code:
        
        reg = _reg_get()
        if reg is None:
            return False

    """
    if reg is not None:
        return reg
    if sys.platform == "win32":
        warn("Could not import the registry-handling module _winreg")
    else:
        warn("Attempt to access the registry on non-Windows platform")
    return None

def _reg_remove_broken_key(key,value,allusers=False):
    """Remove the given registry value if its contents match the given data.
    
    This function looks up the given registry key/value and checks whether its
    contents are a valid, non-empty directory in the filesystem.  If not, the
    key is removed.
    
    By default, the work is done on HKEY_CURRENT_USER. The optional argument
    <allusers> may be set to true to specify that HKEY_LOCAL_MACHINE should
    be used instead.
    """
    reg = _reg_get()
    if reg is None:
        return False
    if allusers:
        hkey = reg.HKEY_LOCAL_MACHINE
    else:
        hkey = reg.HKEY_CURRENT_USER
    try:
        hkey = reg.OpenKey(hkey,key,0,reg.KEY_ALL_ACCESS)
    except:
        # Key doesnt exist
        return True
    try:
        (data,typ) = reg.QueryValueEx(hkey,value)
        if os.path.isdir(data) and len(os.listdir(data))>0:
            # Data is a valid directory, leave it alone
            return True
    except:
        # Key doesnt have value, just return
        return True
    reg.DeleteValue(hkey,value)
    return True    

def _reg_remove_empty_key(key,allusers=False):
    """Remove the named registry key, if it is empty.
    
    By default, the work is done on HKEY_CURRENT_USER. The optional argument
    <allusers> may be set to true to specify that HKEY_LOCAL_MACHINE should
    be used instead.
    """
    reg = _reg_get()
    if reg is None:
        return False
    if allusers:
        hkey = reg.HKEY_LOCAL_MACHINE
    else:
        hkey = reg.HKEY_CURRENT_USER
    try:
        hkey = reg.OpenKey(hkey,key,0,reg.KEY_ALL_ACCESS)
    except:
        # Key doesnt exist
        return True
    try:
        reg.EnumValue(hkey,0)
        # Key still contains values
        return True
    except:
        try:
            reg.EnumKey(hkey,0)
            # Key still contains subkeys
            return True
        except:
            # Was empty, we can delete it
            reg.DeleteKey(reg.HKEY_LOCAL_MACHINE,key)
            return True
    return False


def _reg_config_keys():
    """Itrerator giving registry keys of interest.
    This function is an interator yielding (Path,Value) pairs that name
    keys of interest in the Windows Registry.  Each of these keys should,
    if present, point to a non-empty directory in the filesystem.
    """
    yield ("Software\\Enchant\\Config","Module_Dir")
    yield ("Software\\Enchant\\Ispell","Data_Dir")
    yield ("Software\\Enchant\\Myspell","Data_Dir")


# Top-level registry handling functions

def remove_registry_keys(allusers=False):
    """Remove registry keys from previous versions of PyEnchant.
    
    This function can be used to remove the entries from the Windows
    registry that were created by previous versions of PyEnchant.
    The keys are removed if they point to non-existant or empty
    directories.  Empty keys below "Software\Enchant" are also
    removed.
    
    The optional argument <allusers> can be set to True to indicate
    that entries should be removed for all users on the machine. By
    default, the entries are removed only for the current user profile.
    
    On platforms other than Windows, this function returns immediately
    """
    if sys.platform != "win32":
        return
    for (p,v) in _reg_config_keys():
        _reg_remove_broken_key(p,v,allusers)
    for (p,v) in _reg_config_keys():
        _reg_remove_empty_key(p,allusers)
    _reg_remove_empty_key("Software\\Enchant",allusers)
    


##  Allow looking up of default language on-demand.

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
                raise Exception("No default language available")
        return tag
    except:
        pass
    return default
        


# Useful string-handling functions

def soundex(name, len=4):
    """ soundex module conforming to Knuth's algorithm
        implementation 2000-12-24 by Gregory Jorgensen
        public domain
    """
    # digits holds the soundex values for the alphabet
    digits = '01230120022455012623010202'
    sndx = ''
    fc = ''
    # translate alpha chars in name to soundex digits
    for c in name.upper():
        if c.isalpha():
            if not fc: fc = c   # remember first letter
            d = digits[ord(c)-ord('A')]
            # duplicate consecutive soundex digits are skipped
            if not sndx or (d != sndx[-1]):
                sndx += d
    # replace first digit with first alpha character
    sndx = fc + sndx[1:]
    # remove all 0s from the soundex code
    sndx = sndx.replace('0','')
    # return soundex code padded to len characters
    return (sndx + (len * '0'))[:len]

def edit_dist(a,b):
    """Calculates the Levenshtein distance between a and b.
       From Wikipedia: http://en.wikisource.org/wiki/Levenshtein_distance
    """
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n
    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*m
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
    return current[n]

#  Clone of PWL objects in pure python, with more functionality
#  than is in the C version.  Hopefully we can move the good bits
#  back into enchant eventually.

class PyPWL:
    """Pure-python implementation of Personal Word List dictionary.
    This class emulates the Dict objects provided by enchant using the
    function request_pwl_dict(), but with additional functionality.
    In particular, a simple soundex + edit distance algorithm allows
    suggestions to be returned from the list.
    """
    
    def __init__(self,pwl):
        """PyPWL constructor.
        This method takes as its only argument the name of a file
        containing the personal word list, one word per line.  Entries
        will be read from this file, and new entries will be written to
        it automatically.
        """
        self.pwl = os.path.abspath(pwl)
        self.tag = self.pwl
        self.provider= None
        # Read entries into memory
        # Entries will be a dict of dicts indexed by soundex
        # key then by word, all containing True.
        self._entries = {}
        pwlF = file(pwl)
        for ln in pwlF:
            word = ln.strip()
            self.add_to_session(word)
                
    def check(self,word):
        """Check spelling of a word.
        
        This method takes a word in the dictionary language and returns
        True if it is correctly spelled, and false otherwise.
        """
        key = soundex(word)
        try:
            if self._entries[key][word]:
                return True
        except KeyError:
            pass
        return False
    
    def suggest(self,word):
        """Suggest possible spellings for a word.
        
        This method tries to guess the correct spelling for a given
        word, returning the possibilities in a list.
        """
        key = soundex(word)
        try:
            poss = [w for w in self._entries[key]]
        except KeyError:
            return []
        # Assign edit distances, and sort with lowest first
        for n,w in enumerate(poss):
            poss[n] = (edit_dist(word,w),w)
        poss.sort()
        # Trim those that arent good enough
        # Examples: too high edit distance, too many words
        # For the moment, just restrict to 10 suggestions
        poss = poss[:10]
        # Remove edit distances, and return
        return [w for (n,w) in poss]
    
    def add_to_personal(self,word):
        """Add a word to the user's personal dictionary.
        
        NOTE: this method is being deprecated in favour of
        add_to_pwl.  Please change code using add_to_personal
        to use add_to_pwl instead.  This change mirrors a
        change in the Enchant C API.
        
        """
        warn("add_to_personal is deprecated, please use add_to_pwl",
             DeprecationWarning)
        self.add_to_pwl(word)
        
    def add_to_pwl(self,word):
        """Add a word to the user's personal dictionary.
        For a PWL, this means appending it to the file.
        """
        pwlF = file(self.pwl,"a")
        pwlF.write("%s\n" % (word.strip(),))
        pwlF.close()
        self.add_to_session(word)

    def add_to_session(self,word):
        """Add a word to the session list."""
        key = soundex(word)
        try:
            self._entries[key][word] = True
        except KeyError:
            self._entries[key] = {}
            self._entries[key][word] = True
            
    def is_in_session(self,word):
        """Check whether a word is in the session list."""
        # Consider all words to be in the session list
        return self.check(word)
    
    def store_replacement(self,mis,cor):
        """Store a replacement spelling for a miss-spelled word.
        
        This method makes a suggestion to the spellchecking engine that the 
        miss-spelled word <mis> is in fact correctly spelled as <cor>.  Such
        a suggestion will typically mean that <cor> appears early in the
        list of suggested spellings offered for later instances of <mis>.
        """
        # Cant really do anything with it
        pass

