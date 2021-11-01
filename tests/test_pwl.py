import sys

import pytest

from enchant import DictWithPWL, PyPWL, request_pwl_dict


@pytest.fixture
def pwl_path(tmp_path):
    res = tmp_path / ("pwl.txt")
    res.write_text("")
    return res


def set_pwl_contents(path, contents):
    """Set the contents of the PWL file."""
    path.write_text("\n".join(contents))


def get_pwl_contents(path):
    """Retrieve the contents of the PWL file."""
    contents = path.read_text()
    return [c.strip() for c in contents.splitlines()]


def test_check(pwl_path):
    """Test that basic checking works for PWLs."""
    set_pwl_contents(pwl_path, ["Sazz", "Lozz"])
    d = request_pwl_dict(str(pwl_path))
    assert d.check("Sazz")
    assert d.check("Lozz")
    assert not d.check("hello")


@pytest.mark.skipif(
    sys.implementation.name == "pypy" and sys.platform == "win32",
    reason="failing for an unknown reason",
)
# This test only fails on mypy3 and Windows. Not sure if it's
# a bug in PyEnchant, Enchant or pypy3
def test_unicodefn(tmp_path):
    """Test that unicode PWL filenames are accepted."""
    unicode_path = tmp_path / "테스트"
    set_pwl_contents(unicode_path, ["Lozz"])
    d = request_pwl_dict(str(unicode_path))
    assert d.check("Lozz")
    assert d


def test_add(pwl_path):
    """Test that adding words to a PWL works correctly."""
    d = request_pwl_dict(str(pwl_path))
    assert not d.check("Flagen")
    d.add("Esquilax")
    d.add("Esquilam")
    assert d.check("Esquilax")
    assert "Esquilax" in get_pwl_contents(pwl_path)
    assert d.is_added("Esquilax")


def test_suggestions(pwl_path):
    """Test getting suggestions from a PWL."""
    set_pwl_contents(pwl_path, ["Sazz", "Lozz"])
    d = request_pwl_dict(str(pwl_path))
    assert "Sazz" in d.suggest("Saz")
    assert "Lozz" in d.suggest("laz")
    assert "Sazz" in d.suggest("laz")
    d.add("Flagen")
    assert "Flagen" in d.suggest("Flags")
    assert "sazz" not in d.suggest("Flags")


def test_dwpwl(tmp_path, pwl_path):
    """Test functionality of DictWithPWL."""
    set_pwl_contents(pwl_path, ["Sazz", "Lozz"])
    other_path = tmp_path / "pel.txt"
    d = DictWithPWL("en_US", str(pwl_path), str(other_path))
    assert d.check("Sazz")
    assert d.check("Lozz")
    assert d.check("hello")
    assert not d.check("helo")
    assert not d.check("Flagen")
    d.add("Flagen")
    assert d.check("Flagen")
    assert "Flagen" in get_pwl_contents(pwl_path)
    assert "Flagen" in d.suggest("Flagn")
    assert "hello" in d.suggest("helo")
    d.remove("hello")
    assert not d.check("hello")
    assert "hello" not in d.suggest("helo")
    d.remove("Lozz")
    assert not d.check("Lozz")


def test_dwpwl_empty(tmp_path):
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


def test_pypwl(tmp_path):
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
