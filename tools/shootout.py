
import enchant

# Arrange a short checker shootout to determine
# the best spellchecker of them all!!

# List of providers to test
providers = ("ispell","myspell")

# File containing test cases, and the language they are in
datafile = "batch0.tab"
lang = "en_US"

# List of dictionary objects to test
dicts = []
# Number of correct words missed by each dictionary
missed = []
# Number of corrections not suggested by each dictionary
incorrect = []
# Running average number of places to find correct suggestion
avgdist = []

# Create each dictionary object
for prov in providers:
    b = enchant.Broker()
    b.set_ordering(lang,prov)
    d = b.request_dict(lang)
    dicts.append(d)
    missed.append(0)
    incorrect.append(0)
    avgdist.append(0.0)
    del b

# Actually run the tests
testcases = file(datafile,"r")
for testnum,testcase in enumerate(testcases):
    (mis,cor) = testcase.split("\t")
    cor = cor.strip(); mis = mis.strip()
    print "TEST", testnum, ":", mis, "->", cor
    for dictnum,dict in enumerate(dicts):
        # Check whether it contains the correct word
        if not dict.check(cor):
            missed[dictnum] += 1
            print "MISSED (%s) : %s" % (dict.provider.name,cor)
        # Check on the suggestions provided
        suggs = dict.suggest(mis)
	if cor not in suggs:
            incorrect[dictnum] += 1
            print "INCORRECT (%s) : %s -> %s" % (dict.provider.name,mis,cor)
        else:
            totdist = avgdist[dictnum] * (testnum - incorrect[dictnum])
            totdist += suggs.index(cor)
            avgdist[dictnum] = totdist / (testnum - incorrect[dictnum] + 1)

# Print a report for each provider
for provnum,prov in enumerate(providers):
    print "======================================="
    print "PROVIDER:", prov
    print "  CORRECT WORDS MISSED:", missed[provnum]
    print "  CORRECTIONS NOT SUGGESTED:", incorrect[provnum]
    print "  AVERAGE DIST TO CORRECTION:", avgdist[provnum]


