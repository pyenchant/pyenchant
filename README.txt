
pyenchant:  Python bindings for the Enchant spellchecker
========================================================

This package provides a set of Python language bindings for the Enchant
spellchecking library.  For more information, visit the project website:

    http://www.rfk.id.au/software/pyenchant/


What is Enchant?
----------------

Enchant is used to check the spelling of words and suggest corrections
for words that are miss-spelled.  It can use many popular spellchecking
packages to perform this task, including ispell, aspell and MySpell.  It
is quite flexible at handling multiple dictionaries and multiple
languages.

More information is available on the Enchant website:

    http://www.abisource.com/enchant/


How do I use it?
----------------

For Windows users, there is an executable installer program which can be
used to install the software with a minimum of effort.  Other users will
need to install from source.

Once the software is installed, python's on-line help facilities can
get you started.  Launch python and issue the following commands:

    >>> import enchant
    >>> help(enchant)


Installing with the Windows Installer
-------------------------------------

Download and run the windows installer program.  It will automatically
detect your python installation and set up pyenchant accordingly.

The windows installer version provides a pre-compiled enchant library
as well as several supporting libraries.  Several commonly-used
dictionaries are installed into:

    <YOUR_PYTHON_ROOT>\Lib\site-packages\enchant\share\enchant\myspell.

Additional language dictionaries are available from the OpenOffice.org
project, and are available at:

    http://wiki.services.openoffice.org/wiki/Dictionaries
    
Download the appropriate zip for for the language of interest, and
unzip its contents into the "myspell" directory mentioned above.


Installing from Source
----------------------

First, you must already have the enchant library installed on our system.
You will also need access to a C compiler.

This package is distributed using the Python 'setuptools' framework.
If you have the necessary prerequisites, all that should be required to
install is to execute the following command in the current directory:

    python setup.py install



Who is responsible for all this?
--------------------------------

The credit for Enchant itself goes to Dom Lachowicz.  Find out more details
on the Enchant website listed above.  Full marks to Dom for producing such
a high-quality library.

The glue to pull Enchant into Python via ctypes was written by me, Ryan Kelly.
I needed a decent spellchecker for another project I am working on, and
all the solutions turned up by Google were either extremely non-portable
(e.g. opening a pipe to ispell) or had completely disappeared from the web
(what happened to SnakeSpell?)  It was also a great excuse to teach myself
about SWIG, ctypes, and even a little bit of the Python/C API.

Bugs can be filed on the project's github page:

    http://github.com/rfk/pyenchant/issues

Comments, suggestions, other feedback can be directed to the pyenchant-users
mailing list:

    pyenchant-users@googlegroups.com


