import pytest

from enchant import request_pwl_dict, DictWithPWL, PyPWL
from enchant.utils import unicode, raw_unicode


@pytest.fixture
def pwl_path(tmpdir):
    res = tmpdir.join("pwl.txt")
    res.ensure(file=True)
    return res


def setPWLContents(path, contents):
    """Set the contents of the PWL file."""
    pwlFile = open(path, "w")
    for ln in contents:
        pwlFile.write(ln)
        pwlFile.write("\n")
    pwlFile.flush()
    pwlFile.close()


def getPWLContents(path):
    """Retrieve the contents of the PWL file."""
    pwlFile = open(path, "r")
    contents = pwlFile.readlines()
    pwlFile.close()
    return [c.strip() for c in contents]


def test_check(pwl_path):
    """Test that basic checking works for PWLs."""
    setPWLContents(pwl_path, ["Sazz", "Lozz"])
    d = request_pwl_dict(str(pwl_path))
    assert d.check("Sazz")
    assert d.check("Lozz")
    assert not d.check("hello")


def test_UnicodeFN(pwl_path):
    """Test that unicode PWL filenames are accepted."""
    d = request_pwl_dict(unicode(pwl_path))
    assert d


def test_add(pwl_path):
    """Test that adding words to a PWL works correctly."""
    d = request_pwl_dict(str(pwl_path))
    assert not d.check("Flagen")
    d.add("Esquilax")
    d.add("Esquilam")
    assert d.check("Esquilax")
    assert "Esquilax" in getPWLContents(pwl_path)
    assert d.is_added("Esquilax")


def test_suggestions(pwl_path):
    """Test getting suggestions from a PWL."""
    setPWLContents(pwl_path, ["Sazz", "Lozz"])
    d = request_pwl_dict(str(pwl_path))
    assert "Sazz" in d.suggest("Saz")
    assert "Lozz" in d.suggest("laz")
    assert "Sazz" in d.suggest("laz")
    d.add("Flagen")
    assert "Flagen" in d.suggest("Flags")
    assert not "sazz" in d.suggest("Flags")


def test_DWPWL(tmpdir, pwl_path):
    """Test functionality of DictWithPWL."""
    setPWLContents(pwl_path, ["Sazz", "Lozz"])
    other_path = tmpdir.join("pel.txt")
    d = DictWithPWL("en_US", str(pwl_path), str(other_path))
    assert d.check("Sazz")
    assert d.check("Lozz")
    assert d.check("hello")
    assert not d.check("helo")
    assert not d.check("Flagen")
    d.add("Flagen")
    assert d.check("Flagen")
    assert "Flagen" in getPWLContents(pwl_path)
    assert "Flagen" in d.suggest("Flagn")
    assert "hello" in d.suggest("helo")
    d.remove("hello")
    assert not d.check("hello")
    assert "hello" not in d.suggest("helo")
    d.remove("Lozz")
    assert not d.check("Lozz")


def test_DWPWL_empty(tmpdir):
    """Test functionality of DictWithPWL using transient dicts."""
    d = DictWithPWL("en_US", None, None)
    assert d.check("hello")
    assert not d.check("helo")
    assert not d.check("Flagen")
    d.add("Flagen")
    assert d.check("Flagen")
    d.remove("hello")
    assert not d.check("hello")
    d.add("hello")
    assert d.check("hello")


def test_PyPWL(tmp_path):
    """Test our pure-python PWL implementation."""
    d = PyPWL()
    assert list(d._words) == []
    d.add("hello")
    d.add("there")
    d.add("duck")
    ws = list(d._words)
    assert len(ws) == 3
    assert "hello" in ws
    assert "there" in ws
    assert "duck" in ws
    d.remove("duck")
    d.remove("notinthere")
    ws = list(d._words)
    assert len(ws) == 2
    assert "hello" in ws
    assert "there" in ws


def test_UnicodeCharsInPath(tmpdir):
    """Test that unicode chars in PWL paths are accepted."""
    _fileName = raw_unicode(r"test_\xe5\xe4\xf6_ing")
    path = tmpdir.join(_fileName)
    d = request_pwl_dict(str(path))
    assert d
