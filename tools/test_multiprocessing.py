
import os
import enchant
from multiprocessing import Pool


def do_something(words):
    d = enchant.Dict('en-US')
    for word in words:
        d.check(word)
    return True


def will_block():
    words = ["hello" for i in range(1000)]
    input = [words for i in range(1000)]
    print('Starting')
    pool = Pool(10)
    for i, result in enumerate(pool.imap_unordered(do_something, input)):
        print ('Done {0}: {1}'.format(i, result))
    print('Finished')


if __name__ == '__main__':
    will_block()

