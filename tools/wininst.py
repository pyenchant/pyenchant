#!python
#
#  Written by Ryan Kelly, 2004-2005.
#  This script is placed in the public domain.
#
#  wininst.py:  Windows installer script for PyEnchant
#  
#  This script performs additional installation tasks for the windows
#  installer of PyEnchant.  These include:
#
#     * Create basic registry keys if they dont exist on install
#     * Remove keys on uninstall if they reference to-be-removed dirs
#

import sys
import os
from distutils import sysconfig

try:
    import _winreg as reg
except ImportError:
    print "WARNING: Could not access the registry."
    sys.exit(1)

def EnsureKeyValue(key,value,data):
    """Ensure that the given registry key contains the given value.
    If not, create it using the given data.  Keys are assumed to
    be under HKEY_LOCAL_MACHINE and of type REG_SZ.
    """
    # Make sure the key exists
    hkey = reg.CreateKey(reg.HKEY_LOCAL_MACHINE,key)
    try:
        reg.QueryValueEx(hkey,value)
	print "Registry Key Exists: %s\\%s" % (key,value)
    except:
        # Value doesnt exist, create it
        reg.SetValueEx(hkey,value,0,reg.REG_SZ,data)
	print "Created Registry Key: %s\\%s" % (key,value)

def RemoveKeyMatching(key,value,data):
    """Remove the given registry key value if its contents match the
    given data.
    """
    try:
        hkey = reg.OpenKey(reg.HKEY_LOCAL_MACHINE,key,0,reg.KEY_ALL_ACCESS)
    except:
        # Key doesnt exist
        print "  Key %s doesn't exist" % (key,)
        return
    try:
        (dat,typ) = reg.QueryValueEx(hkey,value)
        if dat != data:
             # Data doesnt match, dont delete
            print "  Key %s\\%s contains unexpected value" % (key,)
            return
    except:
        # Key doesnt have value, just return
        print "  Key %s\\%s doesnt exist" % (key,value)
        return
    # Remove the value
    reg.DeleteValue(hkey,value)
    print "  Deleted Value: %s\\%s" % (key,value)

def RemoveEmptyKey(key):
    """Remove the given key, if it is empty."""
    try:
        hkey = reg.OpenKey(reg.HKEY_LOCAL_MACHINE,key,0,reg.KEY_ALL_ACCESS)
    except:
        # Key doesnt exist
        print "  Key %s doesn't exist" % (key,)
        return
    try:
        reg.EnumValue(hkey,0)
        print "  Key %s still contains values" % (key,)
	return
    except:
        try:
            reg.EnumKey(hkey,0)
            print "  Key %s still contains subkeys" % (key,)
            return
        except:
            # Was empty, we can delete it
            reg.DeleteKey(reg.HKEY_LOCAL_MACHINE,key)
            print "  Deleted Key:  %s" % (key,)


#  Values that will be installed into keys
modulesDir = os.path.join(sysconfig.get_python_lib(),"enchant")
ispellDir = os.path.join(sysconfig.get_python_lib(),"enchant","ispell")
myspellDir = os.path.join(sysconfig.get_python_lib(),"enchant","myspell")

if sys.argv[1] == "-install":
    EnsureKeyValue("Software\\Enchant\\Config","Module_Dir",modulesDir)
    EnsureKeyValue("Software\\Enchant\\Ispell","Data_Dir",ispellDir)
    EnsureKeyValue("Software\\Enchant\\Myspell","Data_Dir",myspellDir)

elif sys.argv[1] == "-remove":
    print "Removing installed Registry Keys:"
    RemoveKeyMatching("Software\\Enchant\\Config","Module_Dir",modulesDir)
    RemoveKeyMatching("Software\\Enchant\\Ispell","Data_Dir",ispellDir)
    RemoveKeyMatching("Software\\Enchant\\Myspell","Data_Dir",myspellDir)
    RemoveEmptyKey("Software\\Enchant\\Config")
    RemoveEmptyKey("Software\\Enchant\\Ispell")
    RemoveEmptyKey("Software\\Enchant\\Myspell")
    RemoveEmptyKey("Software\\Enchant")
    print "  Done"


