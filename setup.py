#
#  This is the pyenchant setuptools script.
#  Originally developed by Ryan Kelly, 2004.
#
#  This script is placed in the public domain.
#

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages, Extension

import sys
import os
import shutil

# Location of the windows binaries, if available
WINDEPS = ".\\tools\\pyenchant-bdist-win32-sources\\build"

#  Cant seem to obtain version information from module, must hardcode
VERSION = "1.4.2"

# Package MetaData
NAME = "pyenchant"
DESCRIPTION = "Python bindings for the Enchant spellchecking system"
AUTHOR = "Ryan Kelly"
AUTHOR_EMAIL = "ryan@rfk.id.au"
URL = "http://pyenchant.sourceforge.net/"
LICENSE = "LGPL"
KEYWORDS = "spelling spellcheck enchant"


#  Module Lists
PACKAGES = find_packages()
EXT_MODULES = []
PKG_DATA = {}
EAGER_RES = []


#  The distutils/swig integration doesnt seem to cut it for this module.
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
# Build and distribution information is different on Windows.
#
# There's the possibility of including pre-built support DLLs
# for the Windows installer.  They will be included if the directory
# <WINDEPS> exists when this script is run.  They are copied into
# the package directory so setuptools can locate them.
#
if sys.platform == "win32":
    # Copy local DLLs across if available
    if os.path.exists(WINDEPS):
      # Main DLLs
      libDir = os.path.join(WINDEPS,"lib")
      for fName in os.listdir(libDir):
        if fName[-3:] == "dll":
          shutil.copy(os.path.join(libDir,fName),".\\enchant\\")
      # Enchant plugins
      plugDir = os.path.join(WINDEPS,"lib\\enchant")
      for fName in os.listdir(plugDir):
        if fName[-3:] == "dll":
          shutil.copy(os.path.join(plugDir,fName),".\\enchant\\lib\\enchant\\")
      # Local Dictionaries
      dictPath = os.path.join(WINDEPS,"myspell")
      if os.path.isdir(dictPath):
        for dictName in os.listdir(dictPath):
          if dictName[-3:] in ["txt","dic","aff"]:
            shutil.copy(os.path.join(dictPath,dictName),
			".\\enchant\\share\\enchant\\myspell\\")
      dictPath = os.path.join(WINDEPS,"ispell")
      if os.path.isdir(dictPath):
        for dictName in os.listdir(dictPath):
          if dictName.endswith("hash") or dictName == "README.txt":
            shutil.copy(os.path.join(dictPath,dictName),
			".\\enchant\\share\\enchant\\ispell\\")
    # Set up additional compile info for C extension
    ext1.libraries.append("libenchant")
    ext1.library_dirs.append("enchant")
    PKG_DATA["enchant"] = ["*.dll", "lib/enchant/*.dll",
                           "share/enchant/myspell/*.*",
                           "share/enchant/ispell/*.*"]
    EAGER_RES = ["enchant/lib", "enchant/share"]
else:
    ext1.libraries.append("enchant")

EXT_MODULES.append(ext1)

##
##  Main call to setup() function
##

setup(name=NAME,
      version=VERSION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      description=DESCRIPTION,
      license=LICENSE,
      keywords=KEYWORDS,
      packages=PACKAGES,
      ext_modules=EXT_MODULES,
      package_data=PKG_DATA,
      eager_resources=EAGER_RES,
      test_suite="enchant.testsuite",
     )

