import enchant
from multiprocessing import Pool


def check_words(words):
    d = enchant.Dict("en-US")
    for word in words:
        d.check(word)
    return True


def test_can_use_multiprocessing():
    words = ["hello" for i in range(1000)]
    input = [words for i in range(1000)]
    print("Starting")
    pool = Pool(10)
    for i, result in enumerate(pool.imap_unordered(check_words, input)):
        print("Done {0}: {1}".format(i, result))
    print("Finished")
