class TestPWL(unittest.TestCase):
    """Test cases for the proper functioning of PWLs and DictWithPWL objects.
    These tests assume that there is at least one working provider
    with a dictionary for the "en_US" language.
    """

    def setUp(self):
        self._tempDir = self._mkdtemp()
        self._fileName = "pwl.txt"

    def tearDown(self):
        import shutil

        shutil.rmtree(self._tempDir)

    def _mkdtemp(self):
        import tempfile

        return tempfile.mkdtemp()

    def _path(self, nm=None):
        if nm is None:
            nm = self._fileName
        nm = os.path.join(self._tempDir, nm)
        if not os.path.exists(nm):
            open(nm, "w").close()
        return nm

    def setPWLContents(self, contents):
        """Set the contents of the PWL file."""
        pwlFile = open(self._path(), "w")
        for ln in contents:
            pwlFile.write(ln)
            pwlFile.write("\n")
        pwlFile.flush()
        pwlFile.close()

    def getPWLContents(self):
        """Retrieve the contents of the PWL file."""
        pwlFile = open(self._path(), "r")
        contents = pwlFile.readlines()
        pwlFile.close()
        return [c.strip() for c in contents]

    def test_check(self):
        """Test that basic checking works for PWLs."""
        self.setPWLContents(["Sazz", "Lozz"])
        d = request_pwl_dict(self._path())
        self.assertTrue(d.check("Sazz"))
        self.assertTrue(d.check("Lozz"))
        self.assertFalse(d.check("hello"))

    def test_UnicodeFN(self):
        """Test that unicode PWL filenames are accepted."""
        d = request_pwl_dict(unicode(self._path()))
        self.assertTrue(d)

    def test_add(self):
        """Test that adding words to a PWL works correctly."""
        d = request_pwl_dict(self._path())
        self.assertFalse(d.check("Flagen"))
        d.add("Esquilax")
        d.add("Esquilam")
        self.assertTrue(d.check("Esquilax"))
        self.assertTrue("Esquilax" in self.getPWLContents())
        self.assertTrue(d.is_added("Esquilax"))

    def test_suggestions(self):
        """Test getting suggestions from a PWL."""
        self.setPWLContents(["Sazz", "Lozz"])
        d = request_pwl_dict(self._path())
        self.assertTrue("Sazz" in d.suggest("Saz"))
        self.assertTrue("Lozz" in d.suggest("laz"))
        self.assertTrue("Sazz" in d.suggest("laz"))
        d.add("Flagen")
        self.assertTrue("Flagen" in d.suggest("Flags"))
        self.assertFalse("sazz" in d.suggest("Flags"))

    def test_DWPWL(self):
        """Test functionality of DictWithPWL."""
        self.setPWLContents(["Sazz", "Lozz"])
        d = DictWithPWL("en_US", self._path(), self._path("pel.txt"))
        self.assertTrue(d.check("Sazz"))
        self.assertTrue(d.check("Lozz"))
        self.assertTrue(d.check("hello"))
        self.assertFalse(d.check("helo"))
        self.assertFalse(d.check("Flagen"))
        d.add("Flagen")
        self.assertTrue(d.check("Flagen"))
        self.assertTrue("Flagen" in self.getPWLContents())
        self.assertTrue("Flagen" in d.suggest("Flagn"))
        self.assertTrue("hello" in d.suggest("helo"))
        d.remove("hello")
        self.assertFalse(d.check("hello"))
        self.assertTrue("hello" not in d.suggest("helo"))
        d.remove("Lozz")
        self.assertFalse(d.check("Lozz"))

    def test_DWPWL_empty(self):
        """Test functionality of DictWithPWL using transient dicts."""
        d = DictWithPWL("en_US", None, None)
        self.assertTrue(d.check("hello"))
        self.assertFalse(d.check("helo"))
        self.assertFalse(d.check("Flagen"))
        d.add("Flagen")
        self.assertTrue(d.check("Flagen"))
        d.remove("hello")
        self.assertFalse(d.check("hello"))
        d.add("hello")
        self.assertTrue(d.check("hello"))

    def test_PyPWL(self):
        """Test our pure-python PWL implementation."""
        d = PyPWL()
        self.assertTrue(list(d._words) == [])
        d.add("hello")
        d.add("there")
        d.add("duck")
        ws = list(d._words)
        self.assertTrue(len(ws) == 3)
        self.assertTrue("hello" in ws)
        self.assertTrue("there" in ws)
        self.assertTrue("duck" in ws)
        d.remove("duck")
        d.remove("notinthere")
        ws = list(d._words)
        self.assertTrue(len(ws) == 2)
        self.assertTrue("hello" in ws)
        self.assertTrue("there" in ws)

    def test_UnicodeCharsInPath(self):
        """Test that unicode chars in PWL paths are accepted."""
        self._fileName = raw_unicode(r"test_\xe5\xe4\xf6_ing")
        d = request_pwl_dict(self._path())
        self.assertTrue(d)
