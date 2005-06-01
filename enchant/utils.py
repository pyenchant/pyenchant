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
          
"""

# Get generators for python2.2
from __future__ import generators

import sys
import os
from warnings import warn
from distutils import sysconfig

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

def _reg_ensure_key_value(key,value,data,allusers=False):
    """Ensure that the given registry key contains the given value and is valid.
  
    This function is designed to ensure that an appropriate registry key
    exists.  It deals only with keys containing string values that represent
    filenames.  If the named key does not contain the named value, it is
    created using the given data.  If it does contain the named value,
    its current data is checked for validity.  If the current data does
    not point to an existing file location, it is replaced with the
    given data.
  
    Intuitively, it ensures that the named key/value contains a valid
    filename.  If it does not, it is replaced by the given data.
    
    By default, the work is done on HKEY_CURRENT_USER. The optional argument
    <allusers> may be set to true to specify that HKEY_LOCAL_MACHINE should
    be used instead.
    """
    reg = _reg_get()
    if reg is None:
        return False
    if allusers:
        hkey = reg.CreateKey(reg.HKEY_LOCAL_MACHINE,key)
    else:
        hkey = reg.CreateKey(reg.HKEY_CURRENT_USER,key)    
    try:
        (eData,_) = reg.QueryValueEx(hkey,value)
    except:
        # Value doesnt exist, create it
        reg.SetValueEx(hkey,value,0,reg.REG_SZ,data)
        return True
    # Value already exists, check validity
    if not os.path.exists(eData):
        reg.SetValueEx(hkey,value,0,reg.REG_SZ,data)
        return True
    return True
        

def _reg_remove_key_matching(key,value,data,allusers=False):
    """Remove the given registry value if its contents match the given data.
    
    This function looks up the given registry key/value and compares its
    contents to the given data.  If they are an exact match, the value is
    removed from the key.
    
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
        (dat,typ) = reg.QueryValueEx(hkey,value)
        if dat != data:
            # Data doesnt match, dont delete
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
    """Retuns a list of registry keys of interest.
    All keys point to locations in the filesystem and are returned
    as a tuple containing:
        
        * Key Path
        * Key Value
        * Key Data
        
    """
    modulesDir = os.path.join(sysconfig.get_python_lib(),"enchant")
    ispellDir = os.path.join(sysconfig.get_python_lib(),"enchant","ispell")
    myspellDir = os.path.join(sysconfig.get_python_lib(),"enchant","myspell")
    keys = []
    keys.append(("Software\\Enchant\\Config","Module_Dir",modulesDir))
    keys.append(("Software\\Enchant\\Ispell","Data_Dir",ispellDir))
    keys.append(("Software\\Enchant\\Myspell","Data_Dir",myspellDir))
    return keys


# Top-level registry handling functions

def create_registry_keys(allusers=False):
    """Create registry keys to point to local version of enchant.
    
    This function can be used to insert entries into the Windows
    registry which point to a local version of enchant that was shipped
    with the PyEnchant distribution.  Each key is only installed if
    no existing value is found in the registry.
    
    The optional argument <allusers> can be set to True to indicate
    that entries should be created for all users on the machine. By
    default, the entries are created only for the current user.
    """
    for (p,v,d) in _reg_config_keys():
        if os.path.exists(d):
            _reg_ensure_key_value(p,v,d,allusers)

def remove_registry_keys(allusers=False):
    """Remove registry keys pointing to local version of enchant.
    
    This function can be used to remove the entries from the Windows
    registry that were created by create_registry_keys.  The entries
    are only removed if they exactly match those create by that
    function.  Empty keys below "Software\Enchant" are also removed.
    
    The optional argumetn <allusers> can be set to True to indicate
    that entries should be removed for all users on the machine. By
    default, the entries are removed only for the current user profile.
    """
    for (p,v,d) in _reg_config_keys():
        _reg_remove_key_matching(p,v,d,allusers)
    _reg_remove_empty_key("Software\\Enchant\\Config",allusers)
    _reg_remove_empty_key("Software\\Enchant\\Ispell",allusers)
    _reg_remove_empty_key("Software\\Enchant\\Myspell",allusers)
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
        

    