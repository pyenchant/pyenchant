
import enchant

# Arrange a short checker shootout to determine
# the best spellchecker of them all!!

# List of providers to test
providers = ("myspell","aspell" )

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
dists = []

# Create each dictionary object
for prov in providers:
    b = enchant.Broker()
    b.set_ordering(lang,prov)
    d = b.request_dict(lang)
    if not d.provider.name == prov:
      raise RuntimeError("Provider '%s' has no dictionary for '%s'"%(prov,lang))
    dicts.append(d)
    missed.append([])
    incorrect.append([])
    dists.append([])
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
            missed[dictnum].append(cor)
        # Check on the suggestions provided
        suggs = dict.suggest(mis)
	if cor not in suggs:
            incorrect[dictnum].append((mis,cor))
            dists[dictnum].append(-1)
        else:
            dists[dictnum].append(suggs.index(cor))
numtests = testnum + 1

# Print a report for each provider
for pnum,prov in enumerate(providers):
    print "======================================="
    exdists = [d for d in dists[pnum] if d >= 0]
    print "PROVIDER:", prov
    print "  EXISTED: %.1f"%(((numtests - len(missed[pnum]))*100.0)/numtests,)
    print "  FOUND: %.1f"%((len(exdists)*100.0)/numtests,)
    print "  FIRST: %.1f"%((len([d for d in exdists if d == 0])*100.0)/numtests,)
    print "  1-5: %.1f"%((len([d for d in exdists if d < 5])*100.0)/numtests,)
    print "  1-10: %.1f"%((len([d for d in exdists if d < 10])*100.0)/numtests,)
    print "  AVERAGE DIST TO CORRECTION: %.2f" % (float(sum(exdists))/len(exdists),)


