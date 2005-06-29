#
#  This is the pyenchant distutils setup script.
#  Originally developed by Ryan Kelly, 2004.
#
#  This script is placed in the public domain.
#

from distutils.core import setup, Extension
import distutils
import sys
import os

# Location of the windows binaries, if available
WINDEPS = ".\\tools\\pyenchant-bdist-win32-sources\\build"

#  Cant obtain version information from module, must hardcode
VERSION = "1.1.3"

# Package MetaData
NAME = "pyenchant"
DESCRIPTION = "Python bindings for the Enchant spellchecking system"
AUTHOR = "Ryan Kelly"
AUTHOR_EMAIL = "rynklly@users.sourceforge.net"
URL = "http://pyenchant.sourceforge.net/"


#  Module Lists
PY_MODULES = []
PACKAGES = ["enchant","enchant.tokenize","enchant.checker"]
EXT_MODULES = []
PKG_DATA = {}
DATA_FILES = []
SCRIPTS = []


#  The distutils/swig integration doesnt seem to cut it for this module
#  For now, enchant_wrap.c will need to be distributed as well.  At least
#  then people wont *have* to have swig installed.
#  Generate it using `swig -python -noproxy enchant.i` to ensure that
#  proxy class stubs are not generated.
swig_infile = os.path.join('enchant','enchant.i')
swig_outfile = os.path.join('enchant','enchant_wrap.c')
if not os.path.exists(swig_outfile) or \
       os.stat(swig_outfile).st_mtime < os.stat(swig_infile).st_mtime:
    print "Generating '%s'..." % (swig_outfile,)
    os.system('swig -python -noproxy -o %s %s' % (swig_outfile,swig_infile))


# Extension Objects
ext1 = Extension('enchant._enchant',['enchant/enchant_wrap.c'],
                 libraries=[],
                 library_dirs=[],
                )
 
#
# Build and distribution information is different on Windows
# The enchant library builds as 'enchant-1' instead of 'enchant'
#
# Also, there's the possibility of including pre-built support DLLs
# for the Windows installer.  They will be included if the directory
# 'windeps' exists when this script is run.
#
if sys.platform == "win32":
    ext1.libraries.append("libenchant-1")
    # Use local dlls if available
    if os.path.exists(WINDEPS):
        ext1.library_dirs.append(os.path.join(WINDEPS,"lib"))
        LOCAL_DLLS = ["libenchant-1","libglib-2.0-0","iconv","intl",
                      "libgmodule-2.0-0",]
        PKG_DATA["enchant"] = []
        for dllName in LOCAL_DLLS:
            PKG_DATA["enchant"].append(os.path.join(WINDEPS,"lib","%s.dll") \
			                                          % (dllName,))
        # Plugin DLLs are in a seperate directory
        LOCAL_DLLS = ["enchant\\libenchant_myspell-1",
                      "enchant\\libenchant_ispell-1",]
        PKG_DATA["enchant/enchant"] = []
        for dllName in LOCAL_DLLS:
            PKG_DATA["enchant/enchant"].append(os.path.join(WINDEPS,"lib",
		                                          "%s.dll"%(dllName,)))
    # Also include local dictionaries
    PKG_DATA["enchant/myspell"] = []
    dictPath = os.path.join(WINDEPS,"myspell")
    if os.path.isdir(dictPath):
      for dictName in os.listdir(dictPath):
        if dictName[-3:] in ["txt","dic","aff"]:
          PKG_DATA["enchant/myspell"].append(os.path.join(dictPath,dictName))
    PKG_DATA["enchant/ispell"] = []
    dictPath = os.path.join(WINDEPS,"ispell")
    if os.path.isdir(dictPath):
      for dictName in os.listdir(dictPath):
        if dictName.endswith("hash") or dictName == "README.txt":
          PKG_DATA["enchant/ispell"].append(os.path.join(dictPath,dictName))
else:
    ext1.libraries.append("enchant")

EXT_MODULES.append(ext1)

# Try to simulate package_data for older distutils
# Since PKG_DATA is only populated on Windows, we know the path
# to site-packages will be Lib/site-packages
distutils_ver = map(int,distutils.__version__.split("."))
if distutils_ver[2] < 4:
    for k in PKG_DATA:
        DATA_FILES.append(("Lib/site-packages/%s"%(k,),PKG_DATA[k]))
    

setup(name=NAME,
      version=VERSION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      packages=PACKAGES,
      py_modules=PY_MODULES,
      ext_modules=EXT_MODULES,
      package_data=PKG_DATA,
      data_files=DATA_FILES,
      scripts=SCRIPTS,
     )

