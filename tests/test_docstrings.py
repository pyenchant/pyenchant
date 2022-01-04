"""Test the spelling on all docstrings we can find in this module.

This serves two purposes - to provide a lot of test data for the
checker routines, and to make sure we don't suffer the embarrassment
of having spelling errors in a spellchecking package!
"""

import os

WORDS = [
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
]


def test_docstrings():
    """Test that all our docstrings are error-free."""
    import enchant
    import enchant.checker
    import enchant.checker.CmdLineChecker
    import enchant.pypwl
    import enchant.tokenize
    import enchant.tokenize.en
    import enchant.utils

    try:
        import enchant.checker.GtkSpellCheckerDialog
    except ImportError:
        pass
    try:
        import enchant.checker.WxSpellCheckerDialog
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
        newobjs = list(_check_docstrings(obj, errors))
        tocheck.extend([obj for obj in newobjs if obj not in checked])
    assert not errors


def _check_docstrings(obj, errors):
    import enchant

    if hasattr(obj, "__doc__"):
        skip_errors = [w for w in getattr(obj, "_DOC_ERRORS", [])]
        chkr = enchant.checker.SpellChecker(
            "en_US", obj.__doc__, filters=[enchant.tokenize.URLFilter]
        )
        for err in chkr:
            if len(err.word) == 1:
                continue
            if err.word.lower() in WORDS:
                continue
            if skip_errors and skip_errors[0] == err.word:
                skip_errors.pop(0)
                continue
            errors.append((obj, err.word, err.wordpos))
    #  Find and yield all child objects that should be checked
    for name in dir(obj):
        if name.startswith("__"):
            continue
        child = getattr(obj, name)
        if hasattr(child, "__file__"):
            if not hasattr(globals(), "__file__"):
                continue
            if not child.__file__.startswith(os.path.dirname(__file__)):
                continue
        else:
            cmod = getattr(child, "__module__", None)
            if not cmod:
                cclass = getattr(child, "__class__", None)
                cmod = getattr(cclass, "__module__", None)
            if cmod and not cmod.startswith("enchant"):
                continue
        yield child
