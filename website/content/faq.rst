FAQ
===

This page contains some frequently asked questions about PyEnchant,
along with some questions which haven't technically been asked but which
are probably of interest to many readers.

-  `How do I report bugs, give feedback etc? <#faq_feedback>`__
-  `How is PyEnchant licensed? <#faq_license>`__
-  `Are there similar projects available? <#faq_similar_projects>`__
-  `What are the advantages/disadvantages of PyEnchant over other
   solutions? <#faq_advantages>`__
-  `How does PyEnchant handle Unicode/non-ASCII text? <#faq_unicode>`__
-  `Which Enchant provider should I use? (Aspell, Ispell,
   MySpell...?) <#faq_shootout>`__

.. _faq_feedback:

How do I report bugs, give feedback etc?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use the issue reporting tools on the `github project
page <https://github.com/rfk/pyenchant/issues>`__ or send the author an
email at ryan@rfk.com.au. For general questions, please use the
`PyEnchant mailing
list <http://groups.google.com/group/pyenchant-users>`__.

.. _faq_license:

How is PyEnchant licensed?
~~~~~~~~~~~~~~~~~~~~~~~~~~

Like the underlying Enchant library, PyEnchant is made available under
the `GNU LGPL <http://www.gnu.org/copyleft/lesser.html>`__ with a
special exemption allowing linking with proprietary spellchecking
plugins.

.. _faq_similar_projects:

Are there similar projects available?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are several projects to produce Python bindings for the
`aspell <http://aspell.sourceforge.net/>`__ spellchecking library,
including
`aspell-python <http://www.republika.pl/wmula/proj/aspell-python/index.html>`__
and `pyaspell <http://savannah.nongnu.org/projects/pyaspell/>`__. The
`myspell-python <http://developer.berlios.de/projects/myspell-python/>`__
package offers a Python wrapper for the MySpell engine. It is also
possible to invoke a command-line program such as ispell, as shown in
this `ASPN Python
Recipie <http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/117221>`__.

.. _faq_advantages:

What are the advantages/disadvantages of PyEnchant over other solutions?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Most of the solutions listed above are tied to a single spellchecking
platform, such as aspell or MySpell. By contrast, Enchant supports
multiple spellchecking platforms. A good discussion of why this is an
advantage can be found on the `Enchant
website <http://www.abisource.com/enchant/>`__ under the heading
"Enchant and Multiple Backends".

-  Different backends can be used for different languages, depending on
   which does a better job
-  Integration with the user's "native" spellchecker, whatever that may
   be
-  This flexibility is transparent to the application programmer

As explained above, PyEnchant is available under the GNU LGPL. This may
mean it can be used in some projects where other libraries (such as
GPL-licensed libraries) cannot.

The Enchant API is also generally simpler than that provided by other
spellchecking solutions. This can be an advantage or disadvantage
depending on the needs of your program.

.. _faq_unicode:

How does PyEnchant handle Unicode/non-ASCII text?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As of version 1.1, PyEnchant supports input of both standard Python
strings and unicode strings. It follows the standard Python practice of
returning unicode strings when unicode strings are given, and standard
strings when standard strings are given.

As of version 1.5, PyEnchant is compatible with the new string
infrastructure of Python 3, and uses it unicode strings consistently
throughout. It does not accept bytestrings in Python 3.

Unfortunately, the author (a native English speaker) does not have a
great deal of experience with the use of unicode. Any help with testing
the support for unicode input/output would be greatly appreciated.

.. _faq_shootout:

Which Enchant provider should I use? (Aspell, Ispell, MySpell...?)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The simple answer is: whichever works best for your language of choice.
The source distribution contains a tool to conduct a `Provider
Shootout <shootout.html>`__ given an appropriate set of test data, which
can be used to determine which provider performs the best for your
language.

Ideally, this choice should be made by the system administrator when
enchant is installed. One of the premises of the Enchant library is to
relieve the user from making such low-level choices.
