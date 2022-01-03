import sys
from multiprocessing import Pool

import pytest

import enchant


def check_words(words):
    d = enchant.Dict("en-US")
    for word in words:
        d.check(word)
    return True


@pytest.mark.skipif(
    sys.implementation.name == "pypy" and sys.platform == "win32",
    reason="hangs for an unknown reason",
)
def test_can_use_multiprocessing():
    words = ["hello" for i in range(1000)]
    input = [words for i in range(1000)]
    pool = Pool(10)
    assert all(pool.imap_unordered(check_words, input))
