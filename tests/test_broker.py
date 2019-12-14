class TestBroker(unittest.TestCase):
    """Test cases for the proper functioning of Broker objects.

    These tests assume that there is at least one working provider
    with a dictionary for the "en_US" language.
    """

    def setUp(self):
        self.broker = Broker()

    def tearDown(self):
        del self.broker

    def test_HasENUS(self):
        """Test that the en_US language is available."""
        self.assertTrue(self.broker.dict_exists("en_US"))

    def test_LangsAreAvail(self):
        """Test whether all advertised languages are in fact available."""
        for lang in self.broker.list_languages():
            if not self.broker.dict_exists(lang):
                assert False, "language '" + lang + "' advertised but non-existent"

    def test_ProvsAreAvail(self):
        """Test whether all advertised providers are in fact available."""
        for (lang, prov) in self.broker.list_dicts():
            self.assertTrue(self.broker.dict_exists(lang))
            if not self.broker.dict_exists(lang):
                assert False, "language '" + lang + "' advertised but non-existent"
            if prov not in self.broker.describe():
                assert False, "provier '" + str(prov) + "' advertised but non-existent"

    def test_ProvOrdering(self):
        """Test that provider ordering works correctly."""
        langs = {}
        provs = []
        # Find the providers for each language, and a list of all providers
        for (tag, prov) in self.broker.list_dicts():
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
                self.assertEqual((d.provider, tag), (prov, tag))
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
                self.assertEqual((d.provider, tag, order), (prov, tag, order))
                del d
                del b2

    def test_UnicodeTag(self):
        """Test that unicode language tags are accepted"""
        d1 = self.broker._request_dict_data(raw_unicode("en_US"))
        self.assertTrue(d1)
        self.broker._free_dict_data(d1)
        d1 = Dict(raw_unicode("en_US"))
        self.assertTrue(d1)

    def test_GetSetParam(self):
        # Older enchnt versions do not have these functions.
        if not hasattr(_e.broker_get_param, "argtypes"):
            return
        self.assertEqual(self.broker.get_param("pyenchant.unittest"), None)
        self.broker.set_param("pyenchant.unittest", "testing")
        self.assertEqual(self.broker.get_param("pyenchant.unittest"), "testing")
        self.assertEqual(Broker().get_param("pyenchant.unittest"), None)
