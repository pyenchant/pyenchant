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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
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

import array

import pytest

import enchant
import enchant.tokenize
from enchant.checker import SpellChecker
from enchant.errors import DefaultLanguageNotFoundError
from enchant.utils import get_default_language


def test_basic():
    """Test a basic run of the SpellChecker class."""
    text = """This is sme text with a few speling erors in it. Its gret
    for checking wheather things are working proprly with the SpellChecker
    class. Not gret for much elss though."""
    chkr = SpellChecker("en_US", text=text)
    for n, err in enumerate(chkr):
        if n == 0:
            # Fix up "sme" -> "some" properly
            assert err.word == "sme"
            assert err.wordpos == 8
            assert "some" in err.suggest()
            err.replace("some")
        if n == 1:
            # Ignore "speling"
            assert err.word == "speling"
        if n == 2:
            # Check context around "erors", and replace
            assert err.word == "erors"
            assert err.leading_context(5) == "ling "
            assert err.trailing_context(5) == " in i"
            err.replace("errors")
        if n == 3:
            # Replace-all on gret as it appears twice
            assert err.word == "gret"
            err.replace_always("great")
        if n == 4:
            # First encounter with "wheather", move offset back
            assert err.word == "wheather"
            err.set_offset(-1 * len(err.word))
        if n == 5:
            # Second encounter, fix up "wheather'
            assert err.word == "wheather"
            err.replace("whether")
        if n == 6:
            # Just replace "proprly", but also add an ignore
            # for "SpellChecker"
            assert err.word == "proprly"
            err.replace("properly")
            err.ignore_always("SpellChecker")
        if n == 7:
            # The second "gret" should have been replaced
            # So it's now on "elss"
            assert err.word == "elss"
            err.replace("else")
        if n > 7:
            pytest.fail("Extraneous spelling errors were found")
    text2 = """This is some text with a few speling errors in it. Its great
    for checking whether things are working properly with the SpellChecker
    class. Not great for much else though."""
    assert chkr.get_text() == text2


def test_filters():
    """Test SpellChecker with the 'filters' argument."""
    text = """I contain WikiWords that ShouldBe skipped by the filters"""
    chkr = SpellChecker("en_US", text=text, filters=[enchant.tokenize.WikiWordFilter])
    for err in chkr:
        # There are no errors once the WikiWords are skipped
        pytest.fail("Extraneous spelling errors were found")
    assert chkr.get_text() == text


def test_chunkers():
    """Test SpellChecker with the 'chunkers' argument."""
    text = """I contain <html a=xjvf>tags</html> that should be skipped"""
    chkr = SpellChecker("en_US", text=text, chunkers=[enchant.tokenize.HTMLChunker])
    for err in chkr:
        # There are no errors when the <html> tag is skipped
        pytest.fail("Extraneous spelling errors were found")
    assert chkr.get_text() == text


class TestChunkersAndFilters:
    """Test SpellChecker with the 'chunkers' and 'filters' arguments."""

    text = """I contain <xjvf a=xjvf>tags</xjvf> that should be skipped
              along with a <a href='http://example.com/">link to
              http://example.com/</a> that should also be skipped"""

    def test_chunkers_and_filters(self) -> None:
        # There are no errors when things are correctly skipped
        chkr = SpellChecker(
            "en_US",
            text=self.text,
            filters=[enchant.tokenize.URLFilter],
            chunkers=[enchant.tokenize.HTMLChunker],
        )
        for err in chkr:
            pytest.fail("Extraneous spelling errors were found")
        assert chkr.get_text() == self.text

    def test_filter_only(self) -> None:
        # The "html" is an error when not using HTMLChunker
        chkr = SpellChecker(
            "en_US",
            text=self.text,
            filters=[enchant.tokenize.URLFilter],
        )
        for err in chkr:
            assert err.word == "xjvf"
            break
        assert chkr.get_text() == self.text

    def test_chunkter_only(self) -> None:
        # The "http" from the URL is an error when not using URLFilter
        chkr = SpellChecker(
            "en_US",
            text=self.text,
            chunkers=[enchant.tokenize.HTMLChunker],
        )
        for err in chkr:
            assert err.word == "http"
            break
        assert chkr.get_text() == self.text


def test_unicode():
    """Test SpellChecker with a unicode string."""
    text = """I am a unicode strng with unicode erors."""
    chkr = SpellChecker("en_US", text)
    for n, err in enumerate(chkr):
        if n == 0:
            assert err.word == "unicode"
            assert err.wordpos == 7
            chkr.ignore_always()
        if n == 1:
            assert err.word == "strng"
            chkr.replace_always("string")
            assert chkr._replace_words["strng"] == "string"
        if n == 2:
            assert err.word == "erors"
            chkr.replace("erros")
            chkr.set_offset(-6)
        if n == 3:
            assert err.word == "erros"
            chkr.replace("errors")
    assert n == 3
    assert chkr.get_text() == "I am a unicode string with unicode errors."


def test_chararray():
    """Test SpellChecker with a character array as input."""
    atype = "u"
    text = "I wll be stord in an aray"
    txtarr = array.array(atype, text)
    chkr = SpellChecker("en_US", txtarr)
    for (n, err) in enumerate(chkr):
        if n == 0:
            assert err.word == "wll"
            assert err.word.__class__ == str
        if n == 1:
            assert err.word == "stord"
            txtarr[err.wordpos : err.wordpos + len(err.word)] = array.array(
                atype, "stored"
            )
            chkr.set_offset(-1 * len(err.word))
        if n == 2:
            assert err.word == "aray"
            chkr.replace("array")
    assert n == 2
    assert txtarr.tounicode() == "I wll be stored in an array"


def test_pwl():
    """Test checker loop with PWL."""
    from enchant import DictWithPWL

    d = DictWithPWL("en_US", None, None)
    txt = "I am sme text to be cheked with personal list of cheked words"
    chkr = SpellChecker(d, txt)
    for n, err in enumerate(chkr):
        if n == 0:
            assert err.word == "sme"
        if n == 1:
            assert err.word == "cheked"
            chkr.add()
    assert n == 1


def test_bug2785373():
    """Testcases for bug #2785373."""
    c = SpellChecker(enchant.Dict("en_US"), "")
    c.set_text("So, one dey when I wes 17, I left.")
    for err in c:
        pass
    c = SpellChecker(enchant.Dict("en_US"), "")
    c.set_text("So, one dey when I wes 17, I left.")
    for err in c:
        pass


def test_default_language():
    # Two cases: either SpellChecker() without argument works
    # and its lang is the default language, or
    # it does not and we get a DefaultLanguageNotFoundError
    try:
        checker = SpellChecker()
    except DefaultLanguageNotFoundError:
        # At this point, caught_err must be DefaultLanguageNotFoundError, so
        # we're done testing
        return

    assert checker.lang == get_default_language()


def test_replace_with_shorter_string():
    """Testcase for replacing with a shorter string (bug #10)"""
    text = ". I Bezwaar tegen verguning."
    chkr = SpellChecker("en_US", text)
    for i, err in enumerate(chkr):
        err.replace("SPAM")
        assert i < 3
    assert chkr.get_text() == ". I SPAM SPAM SPAM."


def test_replace_with_empty_string():
    """Testcase for replacing with an empty string (bug #10)"""
    text = ". I Bezwaar tegen verguning."
    chkr = SpellChecker("en_US", text)
    for i, err in enumerate(chkr):
        err.replace("")
        assert i < 3
    assert chkr.get_text() == ". I   ."
