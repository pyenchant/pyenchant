Provider Shootout
==================

The PyEnchant source distribution contains the script
"tools/shootout.py", which can be used to run a comparative test between
the different providers available in an enchant installation. The idea
is loosely based on the aspell comparison tests run by Kevin Atkinson
(http://aspell.net/test/) and used the test data that he provides, but
the code is pure Python and written from scratch.

The following table summarises results from three spellchecking
providers, all using PyEnchant 3.2.2 and Enchant 2.7.3:

-  *aspell:* Aspell backend, version 0.60.8.1
-  *hunspell:* Hunspell backend, version 1.7.2, with dictionaries from `SCOWL <http://wordlist.aspell.net/>`__
-  *nuspell:* Nuspell backend, version 5.1.4, with the same dictionaries as Hunspell

======== ======= ========= ===== ====== ======= ======== ====
Provider EXISTED SUGGESTED FIRST FIRST5 FIRST10 AVG DIST TIME
======== ======= ========= ===== ====== ======= ======== ====
aspell   97.7    88.9      57.1  81.0   85.3    1.61      0.5
hunspell 97.7    76.5      54.7  75.0   76.3    0.58     11.8
nuspell  97.7    77.3      55.3  74.8   76.5    0.70     17.2
======== ======= ========= ===== ====== ======= ======== ====

The statistics were collected on test data containing over 500 US
English words and
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
-  *TIME:* duration of the test, in seconds, averaged over three runs,
   on an Intel Core i7-860 processor.
