Status: maintenance transfer
-----------------------------

Maintenance of this project is getting transferred from
Ryan Kelly to me, Dimitri Merejkowsky. Expect a few bumps
down the road while issues are sorted out.

A new release is being worked on, see the `"next release" milestone <https://github.com/pyenchant/pyenchant/milestone/1>`_
for more details.

pyenchant:  Python bindings for the Enchant spellchecker
========================================================

This package provides a set of Python language bindings for the Enchant
spellchecking library.  For more information, visit the project website:

    http://pyenchant.github.io/pyenchant/

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

For Windows and OSX users, install the pre-built binary packages using
pip::

    pip install pyenchant


These packages bundle a pre-built copy of the underlying enchant library.
Users on other platforms will need to install "enchant" using their system
package manager.

Once the software is installed, python's on-line help facilities can
get you started.  Launch python and issue the following commands:

    >>> import enchant
    >>> help(enchant)



Who is responsible for all this?
--------------------------------

The credit for Enchant itself goes to Dom Lachowicz.  Find out more details
on the Enchant website listed above.  Full marks to Dom for producing such
a high-quality library.

The glue to pull Enchant into Python via ctypes was written by Ryan Kelly.
He needed a decent spellchecker for another project he was working on, and
all the solutions turned up by Google were either extremely non-portable
(e.g. opening a pipe to ispell) or had completely disappeared from the web
(what happened to SnakeSpell?)  It was also a great excuse to teach himself
about SWIG, ctypes, and even a little bit of the Python/C API.

Finally, after Ryan stepped down from the project, Dimitri Merejkowsky
became the new maintainer.

