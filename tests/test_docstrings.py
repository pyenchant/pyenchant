"""Test the spelling on all docstrings we can find in this module.

This serves two purposes - to provide a lot of test data for the
checker routines, and to make sure we don't suffer the embarrassment
of having spelling errors in a spellchecking package!
"""

from typing import Any, Iterator, List, Set, Tuple

import pytest

import enchant
import enchant.checker  # noqa: F401
import enchant.checker.CmdLineChecker  # noqa: F401
import enchant.errors  # noqa: F401
import enchant.pypwl  # noqa: F401
import enchant.tokenize  # noqa: F401
import enchant.tokenize.en  # noqa: F401
import enchant.utils  # noqa: F401

try:
    import enchant.checker.GtkSpellCheckerDialog  # noqa: F401
except ImportError:
    pass

try:
    import enchant.checker.wxSpellCheckerDialog  # noqa: F401
except ImportError:
    pass

WORDS = {
    "spellchecking",
    "utf",
    "dict",
    "unicode",
    "bytestring",
    "bytestrings",
    "str",
    "pyenchant",
    "ascii",
    "utils",
    "setup",
    "distutils",
    "pkg",
    "filename",
    "tokenization",
    "tuple",
    "tuples",
    "tokenizer",
    "tokenizers",
    "testcase",
    "testcases",
    "whitespace",
    "wxpython",
    "spellchecker",
    "dialog",
    "urls",
    "wikiwords",
    "enchantobject",
    "providerdesc",
    "spellcheck",
    "pwl",
    "aspell",
    "myspell",
    "docstring",
    "docstrings",
    "stopiteration",
    "pwls",
    "pypwl",
    "dictwithpwl",
    "skippable",
    "dicts",
    "dict's",
    "filenames",
    "fr",
    "trie",
    "api",
    "ctypes",
    "wxspellcheckerdialog",
    "stateful",
    "cmdlinechecker",
    "spellchecks",
    "callback",
    "clunkier",
    "iterator",
    "ispell",
    "cor",
    "backends",
    "subclasses",
    "initialise",
    "runtime",
    "py",
    "meth",
    "attr",
    "func",
    "exc",
    "enchant",
}


def pytest_generate_tests(metafunc: Any) -> None:
    """Test that all our docstrings are error-free."""
    #  Naive recursion here would blow the stack, instead we
    #  simulate it with our own stack
    checked: Set[Any] = set()
    objs: Set[Any] = set()

    tocheck = [enchant]
    while tocheck:
        obj = tocheck.pop()

        if obj in checked:
            continue
        checked.add(obj)

        if getattr(obj, "__doc__", ""):
            objs.add(obj)

        tocheck.extend(_crawl_docstrings(obj))

    metafunc.parametrize("obj", objs, ids=_id)


@pytest.fixture(scope="session")
def chkr() -> enchant.checker.SpellChecker:
    return enchant.checker.SpellChecker(
        "en_US",
        filters=[enchant.tokenize.URLFilter],
    )


def test_docstring(obj: Any, chkr: enchant.checker.SpellChecker) -> None:
    errors: List[Tuple[str, int]] = []
    skip_errors = list(getattr(obj, "_DOC_ERRORS", []))
    chkr.set_text(obj.__doc__)
    for err in chkr:
        if len(err.word) == 1:
            continue
        if err.word.lower() in WORDS:
            continue
        if skip_errors and skip_errors[0] == err.word:
            skip_errors.pop(0)
            continue
        errors.append((err.word, err.wordpos))

    assert not errors


def _crawl_docstrings(obj: Any) -> Iterator[Any]:
    """
    Recursively yield all child objects
    """
    for name in dir(obj):
        if name.startswith("_"):
            continue
        child = getattr(obj, name)
        cmod = getattr(child, "__module__", None)
        if not cmod:
            cclass = getattr(child, "__class__", None)
            cmod = getattr(cclass, "__module__", None)
        if cmod and not cmod.startswith("enchant"):
            continue
        yield child


def _id(obj: Any) -> str:
    return ".".join(
        label
        for label in (
            getattr(obj, "__module__", "") or "",
            getattr(obj, "__qualname__", "") or getattr(obj, "__name__", "") or "",
        )
        if label
    )
