#
#  A simple example of how to use pyenchant with py2exe.
#  This script is also used in unittests to test py2exe integration.
#

from distutils.core import setup
import py2exe

from enchant.utils import win32_data_files

setup(
    name="PyEnchant py2exe demo",
    version="0.0.1",
    # Include the necessary supporting data files
    data_files = win32_data_files(),
    # Make a "test_pyenchant.exe" that runs the unittest suite
    console=[dict(script="enchant\\__init__.py",dest_base="test_pyenchant")],
)
