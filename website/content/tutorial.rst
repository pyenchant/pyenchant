
##################
PyEnchant Tutorial
##################


This page offers a quick tutorial to get up and running with the PyEnchant package. If you are already familiar with the basics of installing and using Python packages, you may prefer to simply browse the PyEnchant API listing.

.. contents::


Installing PyEnchant
====================

Windows Users
-------------

Download the pre-built Windows installer from the download page and run it to install PyEnchant. It will place the 'enchant' module in your Python site-packages directory.

As of PyEnchant 1.5.0 there is a single installer for all versions of Python. It has been successfully testing with Python 2.5 and Python 2.6.


Mac OS X Users
--------------

Download the pre-built OSX installer from the download page and execute it in the finder. It will place the 'enchant' module in your Python site-packages directory.

There are also eggs available for users who prefer them.


Other Platforms
---------------

Your operating system distributor may provide PyEnchant via their own packaging system - please check there first.

If a package is not provided by your operating system distributor, you will need to install from source.

If you have an active internet connection, the following procedure will automatically download any additional files required to complete the installation. If not, you need to ensure that you have the latest version of setuptools installed. The `Easy Install Setup Guide <http://peak.telecommunity.com/DevCenter/EasyInstall#installation-instructions>`_ might help you here.

   1. Install Enchant as described on the `enchant website <http://www.abisource.com/enchant/>`_.
   2. Install PyEnchant using the standard Python setuptools procedure:
         1. :doc:`Download<download>` and untar the source files.
         2. Enter the distribution directory, which contains the file 'setup.py'.
         3. Execute the command::

                python setup.py install

         4. Please refer to the `distutils documentation <http://docs.python.org/inst/inst.html>`_ and the following `notes on setuptools <http://peak.telecommunity.com/DevCenter/setuptools#what-your-users-should-know>`_ for help on installing Python modules in this manner. 


Adding Language Dictionaries
----------------------------

By default, PyEnchant on the Windows platform ships with a limited number of language dictionaries:

    * en_GB: British English
    * en_US: American English
    * de_DE: German
    * fr_FR: French

For users of other platforms, the available dictionaries will depend on your installation of Enchant. If the language you wish to use is not available, you will need to install additional dictionaries.

Windows Users
~~~~~~~~~~~~~

PyEnchant can use dictionaries from the OpenOffice.org project. Locate the appropriate file on their dictionary download page at http://wiki.services.openoffice.org/wiki/Dictionaries.

The download will be a zip file containing the necessary dictionary files. The contents of this zip file must be extracted into the directory "Lib/site-packages/enchant/share/enchant/myspell" inside your Python installation directory. For example, if Python is installed into::

   "C:/Python23"

Then extract the dictionary files into::

   "C:/Python23/Lib/site-packages/enchant/share/enchant/myspell"

Note that despite the legacy name "myspell", the latest version of PyEnchant actually uses Hunspell and should be compatible with the latest Hunspell-specific dictionaries.


Mac OS X Users
~~~~~~~~~~~~~~

PyEnchant can use dictionaries from the OpenOffice.org project. Locate the appropriate file on their dictionary download page at http://wiki.services.openoffice.org/wiki/Dictionaries.

The download will be a zip file containing the necessary dictionary files. The contents of this zip file must be extracted into the directory "site-packages/enchant/share/enchant/myspell" inside your Python installation directory. For example, if Python is installed into::

   "/Library/Frameworks/Python.framework/Versions/2.6"

Then extract the dictionary files into::

    "/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/enchant/share/enchant/myspell"

Note that despite the legacy name "myspell", the latest version of PyEnchant actually uses Hunspell and should be compatible with the latest Hunspell-specific dictionaries.


Other Platforms
~~~~~~~~~~~~~~~

The installation of additional dictionaries is the responsibility of the underlying Enchant library. Please consult your operating system vendor or the Enchant website for more details.


Basic PyEnchant Usage
=====================

Once installed, PyEnchant's functionality is available in the "enchant" module.

Creating and Using Dictionary Objects
-------------------------------------

The most important object in the PyEnchant module is the Dict object, which represents a dictionary. These objects are used to check the spelling of words and to get suggestions for misspelled words. The following shows how to construct a simple Dict and use it to check some words::

    >>> import enchant
    >>> d = enchant.Dict("en_US")
    >>> d.check("Hello")
    True
    >>> d.check("Helo")
    False

Dictionaries are created using a language tag which specifies the language to be checked - in this case, "en_US" signifies American English. If the language tag is not specified, an attempt is made to determine the language currently in use. This is not always possible, in which case an Error is raised.

When the current language can be determined, it operates as follows::

  >>> d = enchant.Dict()
  >>> d.tag
  'en_AU'
  >>> print d.tag
  en_AU

Of course, this may still fail if the appropriate dictionary is not available. If it cannot be determined, the behavior is as follows::

  >>> d = enchant.Dict()
  Traceback (most recent call last):
    File "<stdin>", line 1, in ?
    File "enchant/__init__.py", line 467, in __init__
      raise Error(err)
  enchant.Error: No tag specified and default language could not be determined.


There are several top-level functions in the enchant module which can be used to deal with dictionaries:

    * dict_exists: Check whether a Dict is available for a given language
    * request_dict: Construct and return a new Dict object
    * list_languages: List the languages for which Dicts are available

::

  >>> enchant.dict_exists("fake")
  False
  >>> enchant.dict_exists("en_US")
  True
  >>> d = enchant.request_dict("en_US")
  >>> d
  <enchant.Dict object at 0x2aaaabdffa50>cl
  >>> enchant.list_languages()
  ['en', 'en_CA', 'en_GB', 'en_US', 'eo', 'fr', 'fr_CH', 'fr_FR']

As shown previously, the check method of a Dict object can be used to check whether a word is correctly spelled. To get suggestions for a misspelled word, use the suggest method as shown below::

  >>> d.suggest("Helo")
  ['He lo', 'He-lo', 'Hello', 'Helot', 'Help', 'Halo', 'Hell', 'Held', 'Helm', 'Hero', "He'll"]

The suggestions are returned in a list, ordered from most likely replacement to least likely.

Once a correction is made to a miss-spelled word, it is often useful to store this correction in some way for later use. The Dict object provides several methods to handle this:

    * add: store an unrecognised word in the user's personal dictionary so that it is recognised as correct in the future.
    * remove: store a recognised word in the user's personal exclude list, so that it is identified as an error in the future.
    * add_to_session: store an unrecognised word so that it will be recognised as correct while the Dict object is still in use.
    * store_replacement: note that one word was used to replace another, meaning that it will appear higher in the list of suggestions in the future.


Personal Word Lists
-------------------

Dict objects can also be used to check words against a custom list of correctly-spelled words known as a Personal Word List. This is simply a file listing the words to be considered, one word per line. The following example creates a Dict object for the personal word list stored in "mywords.txt"::

  >>> pwl = enchant.request_pwl_dict("mywords.txt")

The personal word list Dict object can be used in the same way as Dict objects which reference a language dictionary. When the object's add method is called, new entries will be appended to the bottom of the file.

PyEnchant also provides the class DictWithPWL which can be used to combine a language dictionary and a personal word list file::

  >>> d2 = enchant.DictWithPWL("en_US","mywords.txt")
  >>> d2.check("Hello")
  True


Checking entire blocks of text
------------------------------

While the enchant.Dict objects are useful for spellchecking individual words, they cannot be used directly to check, for example, an entire paragraph. The module enchant.checker provides a class SpellChecker which is designed to handle this task.

SpellChecker objects are created in the same way as Dict objects - by passing a language tag to the constructor. The set_text method is used to set the text which is to be checked. Once this is done, the SpellChecker object can be used as an iterator over the spelling mistakes in the text. This is best illustrated by a simple example. The following code will print out the errors encountered in a string::

  >>> from enchant.checker import SpellChecker
  >>> chkr = SpellChecker("en_US")
  >>> chkr.set_text("This is sme sample txt with erors.")
  >>> for err in chkr:
  ...     print "ERROR:", err.word
  ...
  ERROR: sme
  ERROR: txt
  ERROR: erors

The SpellChecker can use filters to ignore certain word forms, by passing a list of filters in as a keyword argument::

  >>> from enchant.checker import SpellChecker
  >>> from enchant.tokenize import EmailFilter, URLFilter
  >>> chkr = SpellChecker("en_US",filters=[EmailFilter,URLFilter])

The iterator paradigm can be used to implement a wide variety of spellchecking functionality. As examples of how this can be done, PyEnchant provides a wxPython-based spellchecking dialog and a command-line spellchecking program. While intended mainly as functionality demos, they are also quite useful in their own right.


wxSpellCheckerDialog
--------------------

The module enchant.checker.wxSpellCheckerDialog provides the class wxSpellCheckerDialog which can be used to interactively check the spelling of some text. The code below shows how to create and use such a dialog from within a wxPython application.

It will pop up a simple spellchecking dialog like the one shown here. Each spelling error is highlighted in turn, with the buttons offering a range of options for how to deal with the error:

    * Ignore: ignore the current occurence of the word
    * Ignore All: ignore the current and all future occurances of the word
    * Replace: replace the current occurence with the corrected word
    * Replace All: replace the current and all future occurences with the corrected word
    * Add: add the word to the user's personal dictionary

::

  >>> import wx
  >>> from enchant.checker import SpellChecker
  >>> from enchant.checker.wxSpellCheckerDialog import wxSpellCheckerDialog
  >>> 
  >>> app = wx.PySimpleApp()
  >>> text = "This is sme text with a fw speling errors in it. Here are a fw more to tst it ut."
  >>> dlg = wxSpellCheckerDialog(None,-1,"")
  >>> chkr = SpellChecker("en_US",text)
  >>> dlg.SetSpellChecker(chkr)
  >>> dlg.Show()
  >>> app.MainLoop()


CmdLineChecker
--------------

The module enchant.checker.CmdLineChecker provides the class CmdLineChecker which can be used to interactively check the spelling of some text. It uses standard input and standard output to interact with the user through a command-line interface. The code below shows how to create and use this class from within a python application, along with a short sample checking session::

  >>> import enchant
  >>> import enchant.checker
  >>> from enchant.checker.CmdLineChecker import CmdLineChecker
  >>> chkr = enchant.checker.SpellChecker("en_US")
  >>> chkr.set_text("this is sme example txt")
  >>> cmdln = CmdLineChecker()
  >>> cmdln.set_checker(chkr)
  >>> cmdln.run()
  ERROR: sme
  HOW ABOUT: ['some', 'same', 'Sm', 'Ame', 'ME', 'Me', 'SE', 'Se', 'me', 'Esme', 'Mme', 'SSE', 'See', 'Sue', 'see', 'sue', 'Ste', "Sm's"]
  >> help
  0..N: replace with the numbered suggestion
  R0..rN: always replace with the numbered suggestion
  i: ignore this word
  I: always ignore this word
  a: add word to personal dictionary
  e: edit the word
  q: quit checking
  h: print this help message
  ----------------------------------------------------
  HOW ABOUT: ['some', 'same', 'Sm', 'Ame', 'ME', 'Me', 'SE', 'Se', 'me', 'Esme', 'Mme', 'SSE', 'See', 'Sue', 'see', 'sue', 'Ste', "Sm's"]
  >> 0
  Replacing 'sme' with 'some'
  ERROR: txt
  HOW ABOUT: ['text', 'TX', 'ext']
  >> i
  DONE
  >>> 
  >>> chkr.get_text()
  'this is some example txt'

As shown by this simple example, the CmdLineChecker prints each error it encounters, along with a list of suggested replacements. The user enters the desired behavior using short alphanumeric commands, as explained by the output of the 'help' command.


Tokenization: splitting text into words
---------------------------------------

An important task in spellchecking is splitting a body of text up into its constituative words, each of which is then passed to a Dict object for checking. PyEnchant provides the enchant.tokenize module to assist with this task. The purpose of this module is to provide an appropriate tokenization function which can be used to split the text. Usually, all that is required is the get_tokenizer function::

  >>> from enchant.tokenize import get_tokenizer
  >>> tknzr = get_tokenizer("en_US")
  >>> tknzr
  <class enchant.tokenize.en.tokenize at 0x2aaaaab531d0>
  >>> [w for w in tknzr("this is some simple text")]
  [('this', 0), ('is', 5), ('some', 8), ('simple', 13), ('text', 20)]

As shown in the example above, the function get_tokenizer takes a language tag as input, and returns a tokenization class that is appropriate for that language. Instantiating this class with some text returns an iterator which will yield the words contained in that text. This is exactly the mechanism that the SpellChecker class uses internally to split text into a series of words.

The items produced by the tokenizer are tuples of the form (WORD,POS) where WORD is the word which was found and POS is the position within the string at which that word begins.


Chunkers
~~~~~~~~

In many applications, checkable text may be intermingled with some sort of markup (e.g. HTML tags) which does not need to be checked. To have the tokenizer return only those words that should be checked, it can be augmented with one or more chunkers.

A chunker is simply a special tokenizer function that breaks text up into large chunks rather than individual tokens. They are typically used by passing a list of chunkers to the get_tokenizer function::

  >>> from enchant.tokenize import get_tokenizer, HTMLChunker
  >>> 
  >>> tknzr = get_tokenizer("en_US"])
  >>> [w for w in tknzr("this is <span class='important'>really important</span> text")]
  [('this', 0), ('is', 5), ('span', 9), ('class', 14), ('important', 21), ('really', 32), ('important', 39), ('span', 50), ('text', 56)]
  >>> 
  >>> 
  >>> tknzr = get_tokenizer("en_US",chunkers=(HTMLChunker,))
  >>> [w for w in tknzr("this is <span class='important'>really important</span> text")]
  [('this', 0), ('is', 5), ('really', 32), ('important', 39), ('text', 56)]


When the HTMLChunker is applied to the tokenizer, the <span> tag and its contents are removed from the list of words.

Currently the only implemented chunker is HTMLChunker. A chunker for LaTeX documents is in the works.


Filters
~~~~~~~

In many applications, it is common for spellchecking to ignore words that have a certain form. For example, when spellchecking an email it is customary to ignore email addresses and URLs. This can be achieved by augmenting the tokenization process with filters.

A filter is simply a wrapper around a tokenizer that can (1) drop certain words from the stream, and (2) further split words into sub-tokens. They are typically used by passing a list of filters to the get_tokenizer function::

  >>> from enchant.tokenize import get_tokenizer, EmailFilter
  >>> 
  >>> tknzr = get_tokenizer("en_US")
  >>> [w for w in tknzr("send an email to fake@example.com please")] [('send', 0), ('an', 5), ('email', 8), ('to', 14), ('fake@example.com', 17), ('please', 34)]
  >>> 
  >>> tknzr = get_tokenizer("en_US",[EmailFilter])
  >>> [w for w in tknzr("send an email to fake@example.com please")]
  [('send', 0), ('an', 5), ('email', 8), ('to', 14), ('please', 34)]

When the EmailFilter is applied to the tokenizer, the email address is removed from the list of words.

Currently implemented filters are EmailFilter, URLFilter and WikiWordFilter.


Advanced PyEnchant Usage
========================

Providers
---------

The underlying programming model provided by the Enchant library is based on the notion of Providers. A provider is a piece of code that provides spell-checking services which Enchant can use to perform its work. Different providers exist for performing spellchecking using different frameworks - for example there is an aspell provider and a MySpell provider.

In this way, enchant forms a "wrapper" around existing spellchecking tools in order to provide a common programming interface.

The provider which is managing a particular Dict object can be determined by accessing its provider attribute. This is a ProviderDesc object with the properties name, desc and file::

  >>> d = enchant.Dict("en_US")
  >>> d.provider <Enchant: Aspell Provider>
  >>> d.provider.name
  u'aspell'
  >>> d.provider.desc
  u'Aspell Provider'
  >>> d.provider.file
  u'/usr/lib64/enchant/libenchant_aspell.so'


Brokers
-------

The details of which provider is used to create a particular dictionary are managed by a Broker object. Such objects have methods for creating dictionaries and checking whether a particular dictionary exists, as shown in the example below::

  >>> b = enchant.Broker()
  >>> b
  <enchant.Broker object at 0x2aaaabdff810>
  >>> b.dict_exists("en_US")
  True
  >>> b.dict_exists("fake")
  False
  >>> b.list_languages()
  ['en', 'en_CA', 'en_GB', 'en_US', 'eo', 'fr', 'fr_CH', 'fr_FR']
  >>> d = b.request_dict("en_US")
  >>> d
  <enchant.Dict object at 0x2aaaabdff8d0>

Brokers also have the method describe which determines which providers are available, and the method list_dicts which lists the dictionaries available through each provider::

  >>> b = enchant.Broker()
  >>> b.describe()
  [<Enchant: Aspell Provider>, <Enchant: Myspell Provider>, <Enchant: Ispell Provider>]
  >>> b.list_dicts()
  [('en', <Enchant: Aspell Provider>), ('en_CA', <Enchant: Aspell Provider>), ('en_GB', <Enchant: Aspell Provider>), ('en_US', <Enchant: Aspell Provider>), ('eo', <Enchant: Aspell Provider>), ('fr', <Enchant: Aspell Provider>), ('fr_CH', <Enchant: Aspell Provider>), ('fr_FR', <Enchant: Aspell Provider>)]


The Default Broker
~~~~~~~~~~~~~~~~~~

In normal use, the functionality provided by brokers is not useful to the programmer. To make the programmer's job easier, PyEnchant creates a default Broker object and uses it whenever one is not explicitly given. For example, the default broker is used when creating dictionary objects directly. This object is available as enchant._broker::

  >>> enchant._broker
  <enchant.Broker object at 0x2aaaabdff590>
  >>> d = enchant.Dict("en_US")
  >>> d._broker
  <enchant.Broker object at 0x2aaaabdff590>

You may have noticed that the top-level functions provided by the enchant module (such as request_dict, dict_exists and list_languages) match the methods provided by the Broker class. These functions are in fact the instance methods of the default Broker object::

  >>> enchant._broker
  <enchant.Broker object at 0x2aaaabdff590>
  >>> enchant.request_dict.im_self
  <enchant.Broker object at 0x2aaaabdff590>
  >>> enchant.dict_exists.im_self
  <enchant.Broker object at 0x2aaaabdff590>


Provider Ordering
~~~~~~~~~~~~~~~~~

Which provider is used for which language is determined by the provider ordering of the Broker. This can be altered using the set_ordering method. This method accepts a language tag and a comma-seperated list of provider names in the order that they should be checked. A language tag of "*" means that the ordering should be the default for all languages where an explicit ordering has not been given.

The following example states that for American English the MySpell provider should be tried first, followed by the aspell provider. For all other languages, the ordering is reversed::

  >>> b = enchant.Broker()
  >>> b.set_ordering("en_US","myspell,aspell")
  >>> b.set_ordering("*","aspell,myspell")
  >>> b.request_dict("en_US").provider
  <Enchant: Myspell Provider>
  >>> b.request_dict("en_GB").provider
  <Enchant: Aspell Provider>

The user can also set their prefered ordering using enchant configuration files. For this reason, application programmers are discouraged from explicitly setting an ordering unless there is a compelling reason to do so.


Extending enchant.tokenize
--------------------------

As explained above, the module enchant.tokenize provides the ability to split text into its component words. The current implementation is based only on the rules for the English language, and so might not be completely suitable for your language of choice. Fortunately, it is straightforward to extend the functionality of this module.

To implement a new tokenization routine for the language TAG, simply create a class/function "tokenize" within the module "enchant.tokenize.TAG". This function will automatically be detected by the module's get_tokenizer function and used when appropriate. The easiest way to accomplish this is to copy the module "enchant.tokenize.en" and modify it to suit your needs.

The author would be very grateful for tokenization routines for languages other than English which can be incorporated back into the main PyEnchant distribution.


PyEnchant and other programs
============================


Packaging PyEnchant with py2exe
-------------------------------


PyEnchant depends on a large number of auxilliary files such as plugin libraries, dictionary files, etc. While py2exe does an excellent job of detecting static file dependencies, it cannot detect these files which are located at runtime.

To successfully package an application that uses PyEnchant, these auxilliary files must be explicitly included in the "data_files" argument to the setup function. The function enchant.utils.win32_data_files returns a list of files which can be used for this purpose.


