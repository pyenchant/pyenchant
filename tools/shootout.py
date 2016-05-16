#!python
#
#  Written by Ryan Kelly, 2005.  This script is placed in the public domain.
#
# Arrange a short shootout to determine the best spellchecker of them all!!
#
# This script runs a batch of tests against each enchant spellchecker
# provider, collecting statistics as it goes.  The tests are read from
# a text file, one per line, of the format "<mis> <cor>" where <mis>
# is the misspelled word and <cor> the correct spelling.  Each must be
# a single word.
#
# The statistics printed at the end of the run are:
#
#    EXISTED:    percentage of correct words which the provider
#                reported as being correct
#
#    SUGGESTED:  percentage of misspelled words for which the correct
#                spelling was suggested
#
#    SUGGP:      percentage of misspelled words whose correct spelling
#                existed, for which the correct spelling was suggested
#                (this is simply 100*SUGGESTED/EXISTED)
#
#    FIRST:      percentage of misspelled words for which the correct
#                spelling was the first suggested correction.
#
#    FIRST5:     percentage of misspelled words for which the correct
#                spelling was in the first five suggested corrections
# 
#    FIRST10:    percentage of misspelled words for which the correct
#                spelling was in the first ten suggested corrections
#
#    AVERAGE DIST TO CORRECTION:  the average location of the correct
#                                 spelling within the suggestions list,
#                                 over those words for which the correct
#                                 spelling was found
# 

import enchant
import enchant.utils

# List of providers to test
# Providers can also be named "pypwl:<encode>" where <encode> is
# the encoding function to use for PyPWL.  All PyPWL instances
# will use <wordsfile> as their word list
providers = ("aspell","pypwl",)

# File containing test cases, and the language they are in
# A suitable file can be found at http://aspell.net/test/batch0.tab
datafile = "batch0.tab"
lang = "en_US"
#wordsfile = "/usr/share/dict/words"
wordsfile = "words"

# Corrections to make the 'correct' words in the tests
# This is so we can use unmodified tests published by third parties
corrections = (("caesar","Caesar"),("confucianism","Confucianism"),("february","February"),("gandhi","Gandhi"),("muslims","Muslims"),("israel","Israel"))

# List of dictionary objects to test
dicts = []
# Number of correct words missed by each dictionary
missed = []
# Number of corrections not suggested by each dictionary
incorrect = []
# Number of places to find correct suggestion, or -1 if not found
dists = []

# Create each dictionary object
for prov in providers:
    if prov == "pypwl":
        d = enchant.request_pwl_dict(wordsfile)
    else:
        b = enchant.Broker()
        b.set_ordering(lang,prov)
        d = b.request_dict(lang)
        if not d.provider.name == prov:
          raise RuntimeError("Provider '%s' has no dictionary for '%s'"%(prov,lang))
        del b
    dicts.append(d)
    missed.append([])
    incorrect.append([])
    dists.append([])
    
# Actually run the tests
testcases = file(datafile,"r")
testnum = 0
for testcase in testcases:
    # Skip lines starting with "#"
    if testcase[0] == "#":
        continue
    # Split into words
    words = testcase.split()
    # Skip tests that have multi-word corrections
    if len(words) > 2:
        continue
    cor = words[1].strip(); mis = words[0].strip()
    # Make any custom corrections
    for (old,new) in corrections:
        if old == cor:
            cor = new
            break
    # Actually do the test
    testnum += 1 
    print "TEST", testnum, ":", mis, "->", cor
    for dictnum,dict in enumerate(dicts):
        # Check whether it contains the correct word
        if not dict.check(cor):
            missed[dictnum].append(cor)
        # Check on the suggestions provided
        suggs = dict.suggest(mis)
        if cor not in suggs:
            incorrect[dictnum].append((mis,cor))
            dists[dictnum].append(-1)
        else:
            dists[dictnum].append(suggs.index(cor))
numtests = testnum

# Print a report for each provider
for pnum,prov in enumerate(providers):
    print "======================================="
    exdists = [d for d in dists[pnum] if d >= 0]
    print "PROVIDER:", prov
    print "  EXISTED: %.1f"%(((numtests - len(missed[pnum]))*100.0)/numtests,)
    print "  SUGGESTED: %.1f"%((len(exdists)*100.0)/numtests,)
    print "  SUGGP: %.1f"%((len(exdists)*100.0)/(numtests - len(missed[pnum])),)
    print "  FIRST: %.1f"%((len([d for d in exdists if d == 0])*100.0)/numtests,)
    print "  FIRST5: %.1f"%((len([d for d in exdists if d < 5])*100.0)/numtests,)
    print "  FIRST10: %.1f"%((len([d for d in exdists if d < 10])*100.0)/numtests,)
    print "  AVERAGE DIST TO CORRECTION: %.2f" % (float(sum(exdists))/len(exdists),)
print "======================================="


