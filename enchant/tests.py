# pyenchant
#
# Copyright (C) 2004-2009, Ryan Kelly
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPsE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
#
# In addition, as a special exception, you are
# given permission to link the code of this program with
# non-LGPL Spelling Provider libraries (eg: a MSFT Office
# spell checker backend) and distribute linked combinations including
# the two.  You must obey the GNU Lesser General Public License in all
# respects for all of the code used other than said providers.  If you modify
# this file, you may extend this exception to your version of the
# file, but you are not obligated to do so.  If you do not wish to
# do so, delete this exception statement from your version.
#
"""

    enchant.tests:  testcases for pyenchant

"""

import os
import sys
import unittest
try:
    import subprocess
except ImportError:
    subprocess is None

import enchant
from enchant import *
from enchant import _enchant as _e
from enchant.utils import unicode, raw_unicode, printf


def runcmd(cmd):
    if subprocess is not None:
        kwds = dict(stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        p = subprocess.Popen(cmd,**kwds)
        (stdout,stderr) = p.communicate()
        if p.returncode:
            sys.stderr.write(stderr.decode())
        return p.returncode
    else:
        return os.system(cmd)


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
        self.assert_(self.broker.dict_exists("en_US"))
    
    def test_LangsAreAvail(self):
        """Test whether all advertised languages are in fact available."""
        for lang in self.broker.list_languages():
            if not self.broker.dict_exists(lang):
                assert False, "language '"+lang+"' advertised but non-existent"
            
    def test_ProvsAreAvail(self):
        """Test whether all advertised providers are in fact available."""
        for (lang,prov) in self.broker.list_dicts():
            self.assert_(self.broker.dict_exists(lang))
            if not self.broker.dict_exists(lang):
                assert False, "language '"+lang+"' advertised but non-existent"
            if prov not in self.broker.describe():
                assert False, "provier '"+str(prov)+"' advertised but non-existent"
    
    def test_ProvOrdering(self):
        """Test that provider ordering works correctly."""
        langs = {}
        provs = []
        # Find the providers for each language, and a list of all providers
        for (tag,prov) in self.broker.list_dicts():
            # Skip hyphenation dictionaries installed by OOo
            if tag.startswith("hyph_") and prov.name == "myspell":
                continue
            # Canonicalize separators
            tag = tag.replace("-","_")
            langs[tag] = []
            # NOTE: we are excluding Zemberek here as it appears to return
            #       a broker for any language, even nonexistent ones
            if prov not in provs and prov.name != "zemberek":
                provs.append(prov)
        for prov in provs:
            for tag in langs:
                b2 = Broker()
                b2.set_ordering(tag,prov.name)
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
                b2.set_ordering(tag,prov.name)
                d = b2.request_dict(tag)
                self.assertEqual((d.provider,tag),(prov,tag))
                del d
                del b2
        # Place providers that dont have the language in the ordering
        for tag in langs:
            for prov in langs[tag]:
                order = prov.name
                for prov2 in provs:
                    if prov2 not in langs[tag]:
                        order = prov2.name + "," + order
                b2 = Broker()
                b2.set_ordering(tag,order)
                d = b2.request_dict(tag)
                self.assertEqual((d.provider,tag,order),(prov,tag,order))
                del d
                del b2

    def test_UnicodeTag(self):
        """Test that unicode language tags are accepted"""
        d1 = self.broker._request_dict_data(raw_unicode("en_US"))
        self.assert_(d1)
        _e.broker_free_dict(self.broker._this,d1)
        d1 = Dict(raw_unicode("en_US"))
        self.assert_(d1)

    def test_GetSetParam(self):
        try:
            self.broker.get_param("pyenchant.unittest")
        except AttributeError:
            return
        self.assertEqual(self.broker.get_param("pyenchant.unittest"),None)
        self.broker.set_param("pyenchant.unittest","testing")
        self.assertEqual(self.broker.get_param("pyenchant.unittest"),"testing")
        self.assertEqual(Broker().get_param("pyenchant.unittest"),None)


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
        self.assert_(dict_exists("en_US"))
    
    def test_check(self):
        """Test that check() works on some common words."""
        self.assert_(self.dict.check("hello"))
        self.assert_(self.dict.check("test"))
        self.failIf(self.dict.check("helo"))
        self.failIf(self.dict.check("testt"))
        
    def test_broker(self):
        """Test that the dict's broker is set correctly."""
        self.assert_(self.dict._broker is enchant._broker)
    
    def test_tag(self):
        """Test that the dict's tag is set correctly."""
        self.assertEqual(self.dict.tag,"en_US")
    
    def test_suggest(self):
        """Test that suggest() gets simple suggestions right."""
        self.assert_(self.dict.check("hello"))
        self.assert_("hello" in self.dict.suggest("helo"))

    def test_suggestHang1(self):
        """Test whether suggest() hangs on some inputs (Bug #1404196)"""
        self.assert_(len(self.dict.suggest("Thiis")) >= 0)
        self.assert_(len(self.dict.suggest("Thiiis")) >= 0)
        self.assert_(len(self.dict.suggest("Thiiiis")) >= 0)

    def test_unicode1(self):
        """Test checking/suggesting for unicode strings"""
        # TODO: find something that actually returns suggestions
        us1 = raw_unicode(r"he\u2149lo")
        self.assert_(type(us1) is unicode)
        self.failIf(self.dict.check(us1))
        for s in self.dict.suggest(us1):
            self.assert_(type(s) is unicode)

    def test_session(self):
        """Test that adding words to the session works as required."""
        self.failIf(self.dict.check("Lozz"))
        self.failIf(self.dict.is_added("Lozz"))
        self.dict.add_to_session("Lozz")
        self.assert_(self.dict.is_added("Lozz"))
        self.assert_(self.dict.check("Lozz"))
        self.dict.remove_from_session("Lozz")
        self.failIf(self.dict.check("Lozz"))
        self.failIf(self.dict.is_added("Lozz"))
        self.dict.remove_from_session("hello")
        self.failIf(self.dict.check("hello"))
        self.assert_(self.dict.is_removed("hello"))
        self.dict.add_to_session("hello")

    def test_AddRemove(self):
        """Test adding/removing from default user dictionary."""
        nonsense = "kxhjsddsi"
        self.failIf(self.dict.check(nonsense))
        self.dict.add(nonsense)
        self.assert_(self.dict.is_added(nonsense))
        self.assert_(self.dict.check(nonsense))
        self.dict.remove(nonsense)
        self.failIf(self.dict.is_added(nonsense))
        self.failIf(self.dict.check(nonsense))
        self.dict.remove("pineapple")
        self.failIf(self.dict.check("pineapple"))
        self.assert_(self.dict.is_removed("pineapple"))
        self.failIf(self.dict.is_added("pineapple"))
        self.dict.add("pineapple")
        self.assert_(self.dict.check("pineapple"))
    
    def test_DefaultLang(self):
        """Test behaviour of default language selection."""
        defLang = utils.get_default_language()
        if defLang is None:
            # If no default language, shouldnt work
            self.assertRaises(Error,Dict)
        else:
            # If there is a default language, should use it
            # Of course, no need for the dict to actually exist
            try:
                d = Dict()
                self.assertEqual(d.tag,defLang)
            except DictNotFoundError:
                pass


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

    def _path(self,nm=None):
        if nm is None:
          nm = self._fileName
        nm = os.path.join(self._tempDir,nm)
        if not os.path.exists(nm):
          open(nm,'w').close()
        return nm

    def setPWLContents(self,contents):
        """Set the contents of the PWL file."""
        pwlFile = open(self._path(),"w")
        for ln in contents:
            pwlFile.write(ln)
            pwlFile.write("\n")
        pwlFile.flush()
        pwlFile.close()
        
    def getPWLContents(self):
        """Retrieve the contents of the PWL file."""
        pwlFile = open(self._path(),"r")
        contents = pwlFile.readlines()
        pwlFile.close()
        return [c.strip() for c in contents]
    
    def test_check(self):
        """Test that basic checking works for PWLs."""
        self.setPWLContents(["Sazz","Lozz"])
        d = request_pwl_dict(self._path())
        self.assert_(d.check("Sazz"))
        self.assert_(d.check("Lozz"))
        self.failIf(d.check("hello"))

    def test_UnicodeFN(self):
        """Test that unicode PWL filenames are accepted."""
        d = request_pwl_dict(unicode(self._path()))
        self.assert_(d)

    def test_add(self):
        """Test that adding words to a PWL works correctly."""
        d = request_pwl_dict(self._path())
        self.failIf(d.check("Flagen"))
        d.add("Esquilax")
        d.add("Esquilam")
        self.assert_(d.check("Esquilax"))
        self.assert_("Esquilax" in self.getPWLContents())
        self.assert_(d.is_added("Esquilax"))
        
    def test_suggestions(self):
        """Test getting suggestions from a PWL."""
        self.setPWLContents(["Sazz","Lozz"])
        d = request_pwl_dict(self._path())
        self.assert_("Sazz" in d.suggest("Saz"))
        self.assert_("Lozz" in d.suggest("laz"))
        self.assert_("Sazz" in d.suggest("laz"))
        d.add("Flagen")
        self.assert_("Flagen" in d.suggest("Flags"))
        self.failIf("sazz" in d.suggest("Flags"))
    
    def test_DWPWL(self):
        """Test functionality of DictWithPWL."""
        self.setPWLContents(["Sazz","Lozz"])
        d = DictWithPWL("en_US",self._path(),self._path("pel.txt"))
        self.assert_(d.check("Sazz"))
        self.assert_(d.check("Lozz"))
        self.assert_(d.check("hello"))
        self.failIf(d.check("helo"))
        self.failIf(d.check("Flagen"))
        d.add("Flagen")
        self.assert_(d.check("Flagen"))
        self.assert_("Flagen" in self.getPWLContents())
        d.remove("Lozz")
        d.remove("hello")
        self.failIf(d.check("Lozz"))
        self.failIf(d.check("hello"))

    def test_DWPEL(self):
        """Test functionality of DictWithPWL using exclude list."""
        self.setPWLContents(["Sazz","Lozz"])
        d = DictWithPWL("en_US",self._path())
        self.assert_(d.check("Sazz"))
        self.assert_(d.check("Lozz"))
        self.assert_(d.check("hello"))
        self.failIf(d.check("helo"))
        self.failIf(d.check("Flagen"))
        d.add("Flagen")
        self.assert_(d.check("Flagen"))
        self.assert_("Flagen" in self.getPWLContents())
        d.remove("Lozz")
        self.failIf(d.check("Lozz"))

    def test_DWPWL_empty(self):
        """Test functionality of DictWithPWL using transient dicts."""
        d = DictWithPWL("en_US",None,None)
        self.assert_(d.check("hello"))
        self.failIf(d.check("helo"))
        self.failIf(d.check("Flagen"))
        d.add("Flagen")
        self.assert_(d.check("Flagen"))
        d.remove("hello")
        self.failIf(d.check("hello"))
        d.add("hello")
        self.assert_(d.check("hello"))

    def test_PyPWL(self):
        """Test our pure-python PWL implementation."""
        d = PyPWL()
        self.assert_(list(d._words) == [])
        d.add("hello")
        d.add("there")
        d.add("duck")
        ws = list(d._words)
        self.assert_(len(ws) == 3)
        self.assert_("hello" in ws)
        self.assert_("there" in ws)
        self.assert_("duck" in ws)
        d.remove("duck")
        d.remove("notinthere")
        ws = list(d._words)
        self.assert_(len(ws) == 2)
        self.assert_("hello" in ws)
        self.assert_("there" in ws)

    def test_UnicodeCharsInPath(self):
        """Test that unicode chars in PWL paths are accepted."""
        self._fileName = raw_unicode(r"test_\xe5\xe4\xf6_ing")
        d = request_pwl_dict(self._path())
        self.assert_(d)


class TestDocStrings(unittest.TestCase):
    """Test the spelling on all docstrings we can find in this module.

    This serves two purposes - to provide a lot of test data for the
    checker routines, and to make sure we don't suffer the embarrassment
    of having spelling errors in a spellchecking package!
    """

    WORDS = ["spellchecking","utf","dict","unicode","bytestring","bytestrings",
             "str","pyenchant","ascii", "utils","setup","distutils","pkg",
             "filename", "tokenization", "tuple", "tuples", "tokenizer",
             "tokenizers","testcase","testcases","whitespace","wxpython",
             "spellchecker","dialog","urls","wikiwords","enchantobject",
             "providerdesc", "spellcheck", "pwl", "aspell", "myspell",
             "docstring", "docstrings", "stopiteration", "pwls","pypwl",
             "dictwithpwl","skippable","dicts","dict's","filenames",
             "trie","api","ctypes","wxspellcheckerdialog","stateful",
             "cmdlinechecker","spellchecks","callback","clunkier","iterator",
             "ispell","cor","backends"]

    def test_docstrings(self):
        """Test that all our docstrings are error-free."""
        import enchant
        import enchant.utils
        import enchant.pypwl
        import enchant.tokenize
        import enchant.tokenize.en
        import enchant.checker
        import enchant.checker.CmdLineChecker
        try:
            import enchant.checker.GtkSpellCheckerDialog
        except ImportError:
            pass
        try:
            import enchant.checker.wxSpellCheckerDialog
        except ImportError:
            pass
        errors = []
        #  Naive recursion here would blow the stack, instead we
        #  simulate it with our own stack
        tocheck = [enchant]
        checked = []
        while tocheck:
            obj = tocheck.pop()
            checked.append(obj)
            newobjs = list(self._check_docstrings(obj,errors))
            tocheck.extend([obj for obj in newobjs if obj not in checked])
        self.assertEqual(len(errors),0)

    def _check_docstrings(self,obj,errors):
        import enchant
        if hasattr(obj,"__doc__"):
            skip_errors = [w for w in getattr(obj,"_DOC_ERRORS",[])]
            chkr = enchant.checker.SpellChecker("en_AU",obj.__doc__,filters=[enchant.tokenize.URLFilter])
            for err in chkr:
                if len(err.word) == 1:
                    continue
                if err.word.lower() in self.WORDS:
                    continue
                if skip_errors and skip_errors[0] == err.word:
                    skip_errors.pop(0)
                    continue
                errors.append((obj,err.word,err.wordpos))
                msg = "\nDOCSTRING SPELLING ERROR: %s %s %d %s\n" % (obj,err.word,err.wordpos,chkr.suggest())
                printf(msg,file=sys.stderr)
        #  Find and yield all child objects that should be checked
        for name in dir(obj):
            if name.startswith("__"):
                continue
            child = getattr(obj,name)
            if hasattr(child,"__file__"):
                if not hasattr(globals(),"__file__"):
                    continue
                if not child.__file__.startswith(os.path.dirname(__file__)):
                    continue
            else:
                cmod = getattr(child,"__module__",None)
                if not cmod:
                    cclass = getattr(child,"__class__",None)
                    cmod = getattr(cclass,"__module__",None)
                if cmod and not cmod.startswith("enchant"):
                    continue
            yield child


class TestInstallEnv(unittest.TestCase):
    """Run all testcases in a variety of install environments."""
   
    def setUp(self):
        self._tempDir = self._mkdtemp()
        self._insDir = "build"
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self._tempDir)

    def _mkdtemp(self):
        import tempfile
        return tempfile.mkdtemp()

    def install(self):
        import os, sys, shutil
        insdir = os.path.join(self._tempDir,self._insDir)
        os.makedirs(insdir)
        shutil.copytree("enchant",os.path.join(insdir,"enchant"))

    def runtests(self):
        import os, sys
        insdir = os.path.join(self._tempDir,self._insDir)
        if str is not unicode and isinstance(insdir,unicode):
            insdir = insdir.encode(sys.getfilesystemencoding())
        os.environ["PYTHONPATH"] = insdir
        script = os.path.join(insdir,"enchant","__init__.py")
        res = runcmd("\"%s\" %s" % (sys.executable,script,))
        self.assertEquals(res,0)

    def test_basic(self):
        """Test proper functioning of TestInstallEnv suite."""
        self.install()
        self.runtests()
    test_basic._DOC_ERRORS = ["TestInstallEnv"]

    def test_UnicodeInstallPath(self):
        """Test installation in a path containing unicode chars."""
        self._insDir = raw_unicode(r'test_\xe5\xe4\xf6_ing')
        self.install()
        self.runtests()


class TestPy2exe(unittest.TestCase):
    """Run all testcases inside a py2exe executable"""
    _DOC_ERRORS = ["py","exe"]
   
    def setUp(self):
        self._tempDir = self._mkdtemp()
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self._tempDir)

    def test_py2exe(self):
        """Test pyenchant running inside a py2exe executable."""
        import os, sys, shutil
        from os import path
        from os.path import dirname
        try:
            import py2exe
        except ImportError:
            return
        os.environ["PYTHONPATH"] = dirname(dirname(__file__))
        setup_py = path.join(dirname(__file__),"..","tools","setup.py2exe.py")
        if not path.exists(setup_py):
            return
        buildCmd = '%s %s -q py2exe --dist-dir="%s"'
        buildCmd = buildCmd % (sys.executable,setup_py,self._tempDir)
        res = runcmd(buildCmd)
        self.assertEqual(res,0)
        testCmd = self._tempDir + "\\test_pyenchant.exe"
        self.assertTrue(os.path.exists(testCmd))
        res = runcmd(testCmd)
        self.assertEqual(res,0)
    test_py2exe._DOC_ERRORS = ["py","exe"]
        
    def _mkdtemp(self):
        import tempfile
        return tempfile.mkdtemp()


def buildtestsuite(recurse=True):
    from enchant.checker.tests import TestChecker
    from enchant.tokenize.tests import TestTokenization, TestFilters
    from enchant.tokenize.tests import TestTokenizeEN
    suite = unittest.TestSuite()
    if recurse:
        suite.addTest(unittest.makeSuite(TestInstallEnv))
        suite.addTest(unittest.makeSuite(TestPy2exe))
    suite.addTest(unittest.makeSuite(TestBroker))
    suite.addTest(unittest.makeSuite(TestDict))
    suite.addTest(unittest.makeSuite(TestPWL))
    suite.addTest(unittest.makeSuite(TestDocStrings))
    suite.addTest(unittest.makeSuite(TestChecker))
    suite.addTest(unittest.makeSuite(TestTokenization))
    suite.addTest(unittest.makeSuite(TestTokenizeEN))
    suite.addTest(unittest.makeSuite(TestFilters))
    return suite


def runtestsuite():
    return unittest.TextTestRunner(verbosity=0).run(buildtestsuite(recurse=False))

