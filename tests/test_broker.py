import pytest

from enchant import Broker, Dict, _e
from enchant.utils import raw_unicode


@pytest.fixture
def broker():
    res = Broker()
    yield res
    del res


def test_HasENUS(broker):
    """Test that the en_US language is available."""
    assert broker.dict_exists("en_US")


def test_LangsAreAvail(broker):
    """Test whether all advertised languages are in fact available."""
    for lang in broker.list_languages():
        if not broker.dict_exists(lang):
            assert False, "language '" + lang + "' advertised but non-existent"


def test_ProvsAreAvail(broker):
    """Test whether all advertised providers are in fact available."""
    for (lang, prov) in broker.list_dicts():
        assert broker.dict_exists(lang)
        if not broker.dict_exists(lang):
            assert False, "language '" + lang + "' advertised but non-existent"
        if prov not in broker.describe():
            assert False, "provier '" + str(prov) + "' advertised but non-existent"


def test_ProvOrdering(broker):
    """Test that provider ordering works correctly."""
    langs = {}
    provs = []
    # Find the providers for each language, and a list of all providers
    for (tag, prov) in broker.list_dicts():
        # Skip hyphenation dictionaries installed by OOo
        if tag.startswith("hyph_") and prov.name == "myspell":
            continue
        # Canonicalize separators
        tag = tag.replace("-", "_")
        langs[tag] = []
        # NOTE: we are excluding Zemberek here as it appears to return
        #       a broker for any language, even nonexistent ones
        if prov not in provs and prov.name != "zemberek":
            provs.append(prov)
    for prov in provs:
        for tag in langs:
            b2 = Broker()
            b2.set_ordering(tag, prov.name)
            try:
                d = b2.request_dict(tag)
                if d.provider != prov:
                    raise ValueError()
                langs[tag].append(prov)
            except:
                pass
    # Check availability using a single entry in ordering
    for tag in langs:
        for prov in langs[tag]:
            b2 = Broker()
            b2.set_ordering(tag, prov.name)
            d = b2.request_dict(tag)
            assert (d.provider, tag) == (prov, tag)
            del d
            del b2
    # Place providers that don't have the language in the ordering
    for tag in langs:
        for prov in langs[tag]:
            order = prov.name
            for prov2 in provs:
                if prov2 not in langs[tag]:
                    order = prov2.name + "," + order
            b2 = Broker()
            b2.set_ordering(tag, order)
            d = b2.request_dict(tag)
            assert (d.provider, tag, order) == (prov, tag, order)
            del d
            del b2


def test_UnicodeTag(broker):
    """Test that unicode language tags are accepted"""
    d1 = broker._request_dict_data(raw_unicode("en_US"))
    assert d1
    broker._free_dict_data(d1)
    d1 = Dict(raw_unicode("en_US"))
    assert d1


def test_GetSetParam(broker):
    # Older enchnt versions do not have these functions.
    if not hasattr(_e.broker_get_param, "argtypes"):
        return
    assert broker.get_param("pyenchant.unittest") is None
    broker.set_param("pyenchant.unittest", "testing")
    assert broker.get_param("pyenchant.unittest") == "testing"
    other_broker = Broker()
    assert other_broker.get_param("pyenchant.unittest") is None
