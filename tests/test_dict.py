"""Test cases for the proper functioning of Dict objects.
These tests assume that there is at least one working provider
with a dictionary for the "en_US" language.
"""
import pickle

import pytest

import enchant
from enchant import Dict, DictNotFoundError, Error, dict_exists
from enchant.utils import get_default_language


@pytest.fixture
def en_us_dict():
    res = Dict("en_US")
    yield res
    del res


def test_has_en_us():
    """Test that the en_US language is available through default broker."""
    assert dict_exists("en_US")


def test_check(en_us_dict):
    """Test that check() works on some common words."""
    assert en_us_dict.check("hello")
    assert en_us_dict.check("test")
    assert not en_us_dict.check("helo")
    assert not en_us_dict.check("testt")
    with pytest.raises(ValueError):
        en_us_dict.check("")


def test_broker(en_us_dict):
    """Test that the dict's broker is set correctly."""
    assert en_us_dict._broker is enchant._broker


def test_tag(en_us_dict):
    """Test that the dict's tag is set correctly."""
    assert en_us_dict.tag == "en_US"


def test_suggest(en_us_dict):
    """Test that suggest() gets simple suggestions right."""
    assert en_us_dict.check("hello")
    assert "hello" in en_us_dict.suggest("helo")
    with pytest.raises(ValueError):
        en_us_dict.suggest("")


def test_suggest_hang_1(en_us_dict):
    """Test whether suggest() hangs on some inputs (Bug #1404196)"""
    assert en_us_dict.suggest("Thiis")
    assert len(en_us_dict.suggest("Thiiis")) >= 0
    assert len(en_us_dict.suggest("Thiiiis")) >= 0


def test_unicode1(en_us_dict):
    """Test checking/suggesting for unicode strings"""
    # TODO: find something that actually returns suggestions
    us1 = r"he\u2149lo"
    assert type(us1) is str
    assert not en_us_dict.check(us1)
    for s in en_us_dict.suggest(us1):
        assert type(s) is str


def test_session(en_us_dict):
    """Test that adding words to the session works as required."""
    assert not en_us_dict.check("Lozz")
    assert not en_us_dict.is_added("Lozz")

    en_us_dict.add_to_session("Lozz")
    assert en_us_dict.is_added("Lozz")
    assert en_us_dict.check("Lozz")

    en_us_dict.remove_from_session("Lozz")
    assert not en_us_dict.check("Lozz")
    assert not en_us_dict.is_added("Lozz")

    en_us_dict.remove_from_session("hello")
    assert not en_us_dict.check("hello")
    assert en_us_dict.is_removed("hello")

    # TODO: fixture please
    en_us_dict.add_to_session("hello")


def test_add_remove(en_us_dict):
    """Test adding/removing from default user dictionary."""
    nonsense = "kxhjsddsi"
    assert not en_us_dict.check(nonsense)
    en_us_dict.add(nonsense)
    assert en_us_dict.is_added(nonsense)
    assert en_us_dict.check(nonsense)

    en_us_dict.remove(nonsense)
    assert not en_us_dict.is_added(nonsense)
    assert not en_us_dict.check(nonsense)
    en_us_dict.remove("pineapple")

    assert not en_us_dict.check("pineapple")
    assert en_us_dict.is_removed("pineapple")
    assert not en_us_dict.is_added("pineapple")
    en_us_dict.add("pineapple")
    assert en_us_dict.check("pineapple")


def test_default_lang(en_us_dict):
    """Test behaviour of default language selection."""
    def_lang = get_default_language()
    if def_lang is None:
        # If no default language, shouldn't work
        with pytest.raises(Error):
            Dict()
    else:
        # If there is a default language, should use it
        # Of course, no need for the dict to actually exist
        try:
            d = Dict()
            assert d.tag == def_lang
        except DictNotFoundError:
            pass


def test_pickling(en_us_dict):
    """Test that pickling doesn't corrupt internal state."""
    d1 = Dict("en_US")
    assert d1.check("hello")
    d2 = pickle.loads(pickle.dumps(d1))
    assert d1.check("hello")
    assert d2.check("hello")
    d1._free()
    assert d2.check("hello")
