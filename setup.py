#
#  This is the pyenchant setuptools script.
#  Originally developed by Ryan Kelly, 2004.
#
#  This script is placed in the public domain.
#

try:
    from setuptools import setup, find_packages, Extension
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages, Extension

import sys
import os
import shutil
import errno

setup_kwds = {}
if sys.version_info > (3,):
    setup_kwds["use_2to3"] = True


# Location of the prebuilt binaries, if available
if sys.platform == "win32":
    BINDEPS = ".\\tools\\pyenchant-bdist-win32-sources\\build"
    DYLIB_EXT = ".dll"
elif sys.platform == "darwin":
    BINDEPS = "./tools/pyenchant-bdist-osx-sources/build"
    DYLIB_EXT = ".dylib"

# Package MetaData
NAME = "pyenchant"
DESCRIPTION = "Python bindings for the Enchant spellchecking system"
AUTHOR = "Ryan Kelly"
AUTHOR_EMAIL = "ryan@rfk.id.au"
URL = "https://pythonhosted.org/pyenchant/"
LICENSE = "LGPL"
KEYWORDS = "spelling spellcheck enchant"
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development :: Libraries",
    "Topic :: Text Processing :: Linguistic",
]

#  Module Lists
PACKAGES = find_packages()
EXT_MODULES = []
PKG_DATA = {}
EAGER_RES = []


#
# Helper functions for packaging dynamic libs on OSX.
#

def osx_make_lib_relocatable(libpath,bundle_dir=None):
    """Make an OSX dynamic lib re-locatable by changing dep paths.

    This function adjusts the path information stored in the given dynamic
    library, so that is can be bundled into a directory and redistributed.
    It returns a list of any dependencies that must also be included in the
    bundle directory.
    """
    if sys.platform != "darwin":
        raise RuntimeError("only works on osx")
    import subprocess
    import shutil
    def do(*cmd):
        cmd = [c.encode("utf8") for c in cmd]
        subprocess.Popen(cmd).wait()
    def bt(*cmd):
        cmd = [c.encode("utf8") for c in cmd]
        return subprocess.Popen(cmd,stdout=subprocess.PIPE).stdout.read().decode("utf8")
    (dirnm,nm) = os.path.split(libpath)
    if bundle_dir is None:
        bundle_dir = dirnm
    #  Fix the installed name of the lib to be relative to rpath.
    if libpath.endswith(".dylib"):
        do("install_name_tool","-id","@loader_path/"+nm,libpath)
    #  Fix references to any non-core dependencies, and add them to the list
    #  so they will be copied and fixed-up in turn.
    deps = []
    deplines = bt("otool","-L",libpath).split("\n")
    if libpath.endswith(".dylib"):
        deplines = deplines[2:]
    else:
        deplines = deplines[1:]
    for dep in deplines:
        dep = dep.strip()
        if not dep:
            continue
        dep = dep.split()[0]
        if dep.startswith("/System/"):
            continue
        if dep.startswith("/usr/") and not dep.startswith("/usr/local"):
            continue
        depnm = os.path.basename(dep)
        numdirs = len(dirnm[len(bundle_dir):].split("/")) - 1
        loadpath = "@loader_path/" + ("../"*numdirs) + depnm
        do("install_name_tool","-change",dep,loadpath,libpath)
        deps.append(dep)
    return deps


def osx_bundle_lib(libpath):
    """Bundle dependencies into the same directory as the given library."""
    if sys.platform != "darwin":
        raise RuntimeError("only works on osx")
    bundle_dir = os.path.dirname(libpath)
    # Remove any old libraries from  previous build.
    for nm in os.listdir(bundle_dir):
        oldpath = os.path.join(bundle_dir,nm)
        if oldpath != libpath and os.path.isfile(oldpath):
            os.unlink(oldpath)
    # Copy in and relocate all its dependencies, and theirs, and so-on.
    todo = osx_make_lib_relocatable(libpath,bundle_dir)
    for deppath in todo:
        print("MAKING RELOCATABLE: " + deppath)
        depnm = os.path.basename(deppath)
        bdeppath = os.path.join(bundle_dir,depnm)
        if not os.path.exists(bdeppath):
            shutil.copyfile(deppath,bdeppath)
            todo.extend(osx_make_lib_relocatable(bdeppath,bundle_dir))

#
# Build and distribution information is different on Windows and OSX.
#
# There's the possibility of including pre-built support DLLs
# for the Windows installer.  They will be included if the directory
# <WINDEPS> exists when this script is run.  They are copied into
# the package directory so setuptools can locate them.
#
if sys.platform in ("win32","darwin",):
  try:
    PKG_DATA["enchant"] = ["*"+DYLIB_EXT,"lib/*"+DYLIB_EXT,
                           "lib/enchant/*"+DYLIB_EXT,
                           "lib/enchant/*.so",
                           "lib/enchant/*.txt",
                           "share/enchant/myspell/*.*",
                           "share/enchant/ispell/*.*"]
    EAGER_RES = ["enchant/lib", "enchant/share"]
    # Copy local DLLs across if available
    if os.path.exists(BINDEPS):
      # Main enchant DLL
      libDir = os.path.join(BINDEPS,"lib")
      for fName in os.listdir(libDir):
        if "enchant" in fName and fName.endswith(DYLIB_EXT):
          print("COPYING: " + fName)
          if sys.platform == "win32":
              libroot = os.path.join(".","enchant")
              EAGER_RES.append("enchant/" + fName)
          else:
              libroot = os.path.join(".","enchant","lib")
              EAGER_RES.append("enchant/lib/" + fName)
          shutil.copy(os.path.join(libDir,fName),libroot)
          break
      # Dependencies.  On win32 we just bundle everything, on OSX we call
      # a helper function that tracks (and re-writes) dependencies
      if sys.platform == "darwin":
          osx_bundle_lib(os.path.join(libroot,fName))
          for fName in os.listdir(libroot):
              EAGER_RES.append("enchant/lib/" + fName)
      else:
        for fName in os.listdir(libDir):
          if fName.endswith(DYLIB_EXT):
              print("COPYING: " + fName)
              libroot = os.path.join(".","enchant")
              EAGER_RES.append("enchant/" + fName)
              shutil.copy(os.path.join(libDir,fName),libroot)
      # Enchant plugins
      plugDir = os.path.join(BINDEPS,"lib","enchant")
      for fName in os.listdir(plugDir):
        if fName.endswith(DYLIB_EXT) or fName.endswith(".so"):
          print("COPYING: " + fName)
          EAGER_RES.append("enchant/lib/enchant/" + fName)
          fDest = os.path.join(".","enchant","lib","enchant",fName)
          shutil.copy(os.path.join(plugDir,fName),fDest)
          if sys.platform == "darwin":
              osx_make_lib_relocatable(fDest,libroot)
      # Local Dictionaries
      dictPath = os.path.join(BINDEPS,"share","enchant","myspell")
      if os.path.isdir(dictPath):
        for dictName in os.listdir(dictPath):
          if dictName[-3:] in ["txt","dic","aff"]:
            print("COPYING: " + dictName)
            shutil.copy(os.path.join(dictPath,dictName),
                        os.path.join(".","enchant","share","enchant","myspell"))
      dictPath = os.path.join(BINDEPS,"share","enchant","ispell")
      if os.path.isdir(dictPath):
        for dictName in os.listdir(dictPath):
          if dictName.endswith("hash") or dictName == "README.txt":
            print("COPYING: " + dictName)
            shutil.copy(os.path.join(dictPath,dictName),
                        os.path.join(".","enchant","share","enchant","ispell"))
  except EnvironmentError:
    (_,e,_) = sys.exc_info()
    if e.errno not in (errno.ENOENT,):
        raise
    import traceback
    traceback.print_exc()
    sys.stderr.write("COULD NOT COPY PRE-BUILT DEPENDENCIES\n")

##  Now we can import enchant to get at version info

import enchant
VERSION = enchant.__version__

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
      classifiers=CLASSIFIERS,
      packages=PACKAGES,
      package_data=PKG_DATA,
      eager_resources=EAGER_RES,
      include_package_data=True,
      test_suite="enchant.tests.buildtestsuite",
     )
