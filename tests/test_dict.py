class TestDict(unittest.TestCase):
    """Test cases for the proper functioning of Dict objects.
    These tests assume that there is at least one working provider
    with a dictionary for the "en_US" language.
    """

    def setUp(self):
        self.dict = Dict("en_US")

    def tearDown(self):
        del self.dict

    def test_HasENUS(self):
        """Test that the en_US language is available through default broker."""
        self.assertTrue(dict_exists("en_US"))

    def test_check(self):
        """Test that check() works on some common words."""
        self.assertTrue(self.dict.check("hello"))
        self.assertTrue(self.dict.check("test"))
        self.assertFalse(self.dict.check("helo"))
        self.assertFalse(self.dict.check("testt"))
        self.assertRaises(ValueError, self.dict.check, "")

    def test_broker(self):
        """Test that the dict's broker is set correctly."""
        self.assertTrue(self.dict._broker is enchant._broker)

    def test_tag(self):
        """Test that the dict's tag is set correctly."""
        self.assertEqual(self.dict.tag, "en_US")

    def test_suggest(self):
        """Test that suggest() gets simple suggestions right."""
        self.assertTrue(self.dict.check("hello"))
        self.assertTrue("hello" in self.dict.suggest("helo"))
        self.assertRaises(ValueError, self.dict.suggest, "")

    def test_suggestHang1(self):
        """Test whether suggest() hangs on some inputs (Bug #1404196)"""
        self.assertTrue(len(self.dict.suggest("Thiis")) >= 0)
        self.assertTrue(len(self.dict.suggest("Thiiis")) >= 0)
        self.assertTrue(len(self.dict.suggest("Thiiiis")) >= 0)

    def test_unicode1(self):
        """Test checking/suggesting for unicode strings"""
        # TODO: find something that actually returns suggestions
        us1 = raw_unicode(r"he\u2149lo")
        self.assertTrue(type(us1) is unicode)
        self.assertFalse(self.dict.check(us1))
        for s in self.dict.suggest(us1):
            self.assertTrue(type(s) is unicode)

    def test_session(self):
        """Test that adding words to the session works as required."""
        self.assertFalse(self.dict.check("Lozz"))
        self.assertFalse(self.dict.is_added("Lozz"))
        self.dict.add_to_session("Lozz")
        self.assertTrue(self.dict.is_added("Lozz"))
        self.assertTrue(self.dict.check("Lozz"))
        self.dict.remove_from_session("Lozz")
        self.assertFalse(self.dict.check("Lozz"))
        self.assertFalse(self.dict.is_added("Lozz"))
        self.dict.remove_from_session("hello")
        self.assertFalse(self.dict.check("hello"))
        self.assertTrue(self.dict.is_removed("hello"))
        self.dict.add_to_session("hello")

    def test_AddRemove(self):
        """Test adding/removing from default user dictionary."""
        nonsense = "kxhjsddsi"
        self.assertFalse(self.dict.check(nonsense))
        self.dict.add(nonsense)
        self.assertTrue(self.dict.is_added(nonsense))
        self.assertTrue(self.dict.check(nonsense))
        self.dict.remove(nonsense)
        self.assertFalse(self.dict.is_added(nonsense))
        self.assertFalse(self.dict.check(nonsense))
        self.dict.remove("pineapple")
        self.assertFalse(self.dict.check("pineapple"))
        self.assertTrue(self.dict.is_removed("pineapple"))
        self.assertFalse(self.dict.is_added("pineapple"))
        self.dict.add("pineapple")
        self.assertTrue(self.dict.check("pineapple"))

    def test_DefaultLang(self):
        """Test behaviour of default language selection."""
        defLang = utils.get_default_language()
        if defLang is None:
            # If no default language, shouldn't work
            self.assertRaises(Error, Dict)
        else:
            # If there is a default language, should use it
            # Of course, no need for the dict to actually exist
            try:
                d = Dict()
                self.assertEqual(d.tag, defLang)
            except DictNotFoundError:
                pass

    def test_pickling(self):
        """Test that pickling doesn't corrupt internal state."""
        d1 = Dict("en")
        self.assertTrue(d1.check("hello"))
        d2 = pickle.loads(pickle.dumps(d1))
        self.assertTrue(d1.check("hello"))
        self.assertTrue(d2.check("hello"))
        d1._free()
        self.assertTrue(d2.check("hello"))
