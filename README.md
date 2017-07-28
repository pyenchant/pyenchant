# PyEnchant

Python bindings for the Enchant spellchecker

This package provides a set of Python language bindings for the Enchant
spellchecking library.  For more information, visit the project website:

[http://packages.python.org/pyenchant/](http://packages.python.org/pyenchant/)


## What is Enchant?

Enchant aims to provide a simple but comprehensive abstraction for dealing
with different spell checking libraries in a consistent way. A client, such
as a text editor or word processor, need not know anything about a specific
spell-checker, and since all back-ends are plugins, new spell-checkers can
be added without needing any change to the program using Enchant.

More information is available on the Enchant website:

[https://github.com/AbiWord/enchant](https://github.com/AbiWord/enchant)

*[old] [https://github.com/AbiWord/enchant](http://www.abisource.com/enchant/)*


## How do I use it?

For Windows and OSX users, install the pre-built binary packages using
pip::

    pip install pyenchant


These packages bundle a pre-built copy of the underlying enchant library.
Users on other platforms will need to install "enchant" using their system
package manager.

Once the software is installed, python's on-line help facilities can
get you started.  Launch python and issue the following commands:

```python
import enchant
help(enchant)
```


## Who is responsible for all this?

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

[https://github.com/rfk/pyenchant/issues](https://github.com/rfk/pyenchant/issues)

Comments, suggestions, other feedback can be directed to the pyenchant-users
mailing list:

[pyenchant-users@googlegroups.com](pyenchant-users@googlegroups.com)


