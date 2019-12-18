Provider Shootout
==================

The PyEnchant source distribution contains the script
"tools/shootout.py", which can be used to run a comparative test between
the different providers available in an enchant installation. The idea
is loosely based on the aspell comparison tests run by Kevin Atkinson
(http://aspell.net/test/) and used the test data that he provides, but
the code is pure Python and written from scratch.

The following table summarises results from three spellchecking
providers, all using PyEnchant 1.1.0 and Enchant 1.1.5:

-  *aspell:* Aspell backend, version 0.60.2
-  *ispell:* Ispell backend, with dictionaries from AbiWord's `AbiSpell
   component <http://sourceforge.net/project/showfiles.php?group_id=15518&package_id=25690>`__
-  *myspell:* MySpell backend, with dictionaries from
   `OpenOffice.org <http://lingucomponent.openoffice.org/spell_dic.html>`__

======== ======= ========= ===== ====== ======= ========
Provider EXISTED SUGGESTED FIRST FIRST5 FIRST10 AVG DIST
======== ======= ========= ===== ====== ======= ========
aspell   97.9    87.2      50.0  77.6   84.4    1.77
ispell   99.8    53.4      34.0  50.6   51.7    1.10
myspell  99.2    69.5      45.9  64.1   68.8    1.06
======== ======= ========= ===== ====== ======= ========

The statistics were collected on test data containing over 500 words and
express the following quantities:

-  *EXISTED:* percentage of correctly-spelled test words that were
   marked correct by the spellchecker. This tests the provider's
   coverage of the language.
-  *SUGGESTED:* percentage of misspelled test words for which the
   correct spelling was suggested by the spellchecker. This tests the
   ability of the provider to guess the correct spelling of a word.
-  *FIRST:* percentage of misspelled test words for which the correct
   spelling was the first suggestion made by the spellchecker.
-  *FIRST5:* percentage of misspelled test words for which the correct
   spelling was in the first five suggestions made by the spellchecker.
-  *FIRST10:* percentage of misspelled test words for which the correct
   spelling was in the first ten suggestions made by the spellchecker.
-  *AVG DIST:* average position of the correct spelling of a word within
   the list of suggestions returned by the spellchecker, with zero
   meaning the word was at the front of the list.

On the basis of this data, the default provider for the stand-alone
Windows distribution was changed from ispell to myspell for version
1.1.0. The two have similar language coverage and quality of suggestions
(EXISTED and AVG DIST respectively) but myspell has a significantly
better ability to guess the intended spelling of a word (SUGGESTED).
