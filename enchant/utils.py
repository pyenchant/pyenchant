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
        
        * functions for inserting/removing entries into the Windows
          registry, to point to local version of enchant
          
"""

import sys
import os
from warnings import warn
from distutils import sysconfig

try:
    import _winreg as reg
except ImportError:
    reg = None


# Make SpellChecker available for backwards compatability
from enchant.checker import SpellChecker


# Useful registry-handling functions

def _reg_get():
    """Get the registry module, or None if not available.
    This function raises an appropriate warning if the registry
    is not available.
    """
    if reg is not None:
        return reg
    if sys.platform == "win32":
        warn("Could not import the registry-handling module _winreg")
    else:
        warn("Attempt to access the registry on non-Windows platform")
    return None

def _reg_ensure_key_value(key,value,data):
    """Ensure that the given registry key contains the given value.
    If not, create it using the given data.  Keys are assumed to
    be under HKEY_LOCAL_MACHINE and of type REG_SZ.
    """
    reg = _reg_get()
    if reg is None:
        return
    # Make sure the key exists
    hkey = reg.CreateKey(reg.HKEY_LOCAL_MACHINE,key)
    try:
        reg.QueryValueEx(hkey,value)
        #print "Registry Key Exists: %s\\%s" % (key,value)
    except:
        # Value doesnt exist, create it
        reg.SetValueEx(hkey,value,0,reg.REG_SZ,data)
        #print "Created Registry Key: %s\\%s" % (key,value)


def _reg_remove_key_matching(key,value,data):
    """Remove the given registry key value if its contents match the
    given data.
    """
    reg = _reg_get()
    if reg is None:
        return
    try:
        hkey = reg.OpenKey(reg.HKEY_LOCAL_MACHINE,key,0,reg.KEY_ALL_ACCESS)
    except:
        # Key doesnt exist
        #print "  Key %s doesn't exist" % (key,)
        return
    try:
        (dat,typ) = reg.QueryValueEx(hkey,value)
        if dat != data:
            # Data doesnt match, dont delete
            #print "  Key %s\\%s contains unexpected value" % (key,)
            return
    except:
        # Key doesnt have value, just return
        #print "  Key %s\\%s doesnt exist" % (key,value)
        return
    # Remove the value
    reg.DeleteValue(hkey,value)
    #print "  Deleted Value: %s\\%s" % (key,value)

def _reg_remove_empty_key(key):
    """Remove the given key, if it is empty."""
    reg = _reg_get()
    if reg is None:
        return
    try:
        hkey = reg.OpenKey(reg.HKEY_LOCAL_MACHINE,key,0,reg.KEY_ALL_ACCESS)
    except:
        # Key doesnt exist
        #print "  Key %s doesn't exist" % (key,)
        return
    try:
        reg.EnumValue(hkey,0)
        #print "  Key %s still contains values" % (key,)
        return
    except:
        try:
            reg.EnumKey(hkey,0)
            #print "  Key %s still contains subkeys" % (key,)
            return
        except:
            # Was empty, we can delete it
            reg.DeleteKey(reg.HKEY_LOCAL_MACHINE,key)
            #print "  Deleted Key:  %s" % (key,)
            
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

def create_registry_keys():
    """Create registry keys to point to local version of enchant.
    This function can be used to insert entries into the Windows
    registry which point to a local version of enchant that was shipped
    with the PyEnchant distribution.  Each key is only installed if
    no existing value is found in the registry.
    """
    for (p,v,d) in _reg_config_keys():
        if os.path.exists(d):
            _reg_ensure_key_value(p,v,d)

def remove_registry_keys():
    """Remove registry keys pointing to local version of enchant.
    This function can be used to remove the entries from the Windows
    registry that were created by create_registry_keys.  The entries
    are only removed if they exactly match those create by that
    function.  Empty keys below "Software\Enchant" are also removed.
    """
    for (p,v,d) in _reg_config_keys():
        _reg_remove_key_matching(p,v,d)
    _reg_remove_empty_key("Software\\Enchant\\Config")
    _reg_remove_empty_key("Software\\Enchant\\Ispell")
    _reg_remove_empty_key("Software\\Enchant\\Myspell")
    _reg_remove_empty_key("Software\\Enchant")

    