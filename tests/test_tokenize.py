# pyenchant
#
# Copyright (C) 2004-2008, Ryan Kelly
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
#
import textwrap

import pytest

from enchant.tokenize import (
    EmailFilter,
    HTMLChunker,
    URLFilter,
    WikiWordFilter,
    basic_tokenize,
    empty_tokenize,
    get_tokenizer,
    wrap_tokenizer,
)
from enchant.tokenize.en import tokenize as tokenize_en


def test_basic_tokenize():
    """Simple regression test for basic white-space tokenization."""
    input = """This is a paragraph.  It's not very special, but it's designed
2 show how the splitter works with many-different combos
of words. Also need to "test" the (handling) of 'quoted' words."""
    assert list(basic_tokenize(input)) == [
        ("This", 0),
        ("is", 5),
        ("a", 8),
        ("paragraph", 10),
        ("It's", 22),
        ("not", 27),
        ("very", 31),
        ("special", 36),
        ("but", 45),
        ("it's", 49),
        ("designed", 54),
        ("2", 63),
        ("show", 65),
        ("how", 70),
        ("the", 74),
        ("splitter", 78),
        ("works", 87),
        ("with", 93),
        ("many-different", 98),
        ("combos", 113),
        ("of", 120),
        ("words", 123),
        ("Also", 130),
        ("need", 135),
        ("to", 140),
        ("test", 144),
        ("the", 150),
        ("handling", 155),
        ("of", 165),
        ("quoted", 169),
        ("words", 177),
    ]


def test_tokenize_strip():
    """Test special-char-stripping edge-cases in basic_tokenize."""
    input = "((' <this> \"\" 'text' has (lots) of (special chars} >>]"
    assert list(basic_tokenize(input)) == [
        ("<this>", 4),
        ("text", 15),
        ("has", 21),
        ("lots", 26),
        ("of", 32),
        ("special", 36),
        ("chars}", 44),
        (">>", 51),
    ]


def test_wrap_tokenizer():
    """Test wrapping of one tokenizer with another."""
    input = "this-string will be split@according to diff'rnt rules"
    from enchant.tokenize import en

    tknzr = wrap_tokenizer(basic_tokenize, en.tokenize)
    tknzr = tknzr(input)
    assert tknzr._tokenizer.__class__ == basic_tokenize
    assert tknzr._tokenizer.offset == 0
    for (n, (word, pos)) in enumerate(tknzr):
        if n == 0:
            assert pos == 0
            assert word == "this"
        if n == 1:
            assert pos == 5
            assert word == "string"
        if n == 2:
            assert pos == 12
            assert word == "will"
            # Test setting offset to a previous token
            tknzr.set_offset(5)
            assert tknzr.offset == 5
            assert tknzr._tokenizer.offset == 5
            assert tknzr._curtok.__class__ == empty_tokenize
        if n == 3:
            assert word == "string"
            assert pos == 5
        if n == 4:
            assert pos == 12
            assert word == "will"
        if n == 5:
            assert pos == 17
            assert word == "be"
            # Test setting offset past the current token
            tknzr.set_offset(20)
            assert tknzr.offset == 20
            assert tknzr._tokenizer.offset == 20
            assert tknzr._curtok.__class__ == empty_tokenize
        if n == 6:
            assert pos == 20
            assert word == "split"
        if n == 7:
            assert pos == 26
            assert word == "according"
            # Test setting offset to middle of current token
            tknzr.set_offset(23)
            assert tknzr.offset == 23
            assert tknzr._tokenizer.offset == 23
        if n == 8:
            assert pos == 23
            assert word == "it"
        # OK, I'm pretty happy with the behaviour, no need to
        # continue testing the rest of the string


@pytest.fixture
def test_text():
    text = """this text with http://url.com and SomeLinksLike
              ftp://my.site.com.au/some/file AndOthers not:/quite.a.url
              with-an@aemail.address as well"""
    return text


def test_url_filter(test_text):
    """Test filtering of URLs"""
    tknzr = get_tokenizer("en_US", filters=(URLFilter,))
    assert list(tknzr(test_text)) == [
        ("this", 0),
        ("text", 5),
        ("with", 10),
        ("and", 30),
        ("SomeLinksLike", 34),
        ("AndOthers", 93),
        ("not", 103),
        ("quite", 108),
        ("a", 114),
        ("url", 116),
        ("with", 134),
        ("an", 139),
        ("aemail", 142),
        ("address", 149),
        ("as", 157),
        ("well", 160),
    ]


def test_wiki_word_filter(test_text):
    """Test filtering of WikiWords"""
    tknzr = get_tokenizer("en_US", filters=(WikiWordFilter,))
    assert list(tknzr(test_text)) == [
        ("this", 0),
        ("text", 5),
        ("with", 10),
        ("http", 15),
        ("url", 22),
        ("com", 26),
        ("and", 30),
        ("ftp", 62),
        ("my", 68),
        ("site", 71),
        ("com", 76),
        ("au", 80),
        ("some", 83),
        ("file", 88),
        ("not", 103),
        ("quite", 108),
        ("a", 114),
        ("url", 116),
        ("with", 134),
        ("an", 139),
        ("aemail", 142),
        ("address", 149),
        ("as", 157),
        ("well", 160),
    ]


def test_email_filter(test_text):
    """Test filtering of email addresses"""
    tknzr = get_tokenizer("en_US", filters=(EmailFilter,))
    assert list(tknzr(test_text)) == [
        ("this", 0),
        ("text", 5),
        ("with", 10),
        ("http", 15),
        ("url", 22),
        ("com", 26),
        ("and", 30),
        ("SomeLinksLike", 34),
        ("ftp", 62),
        ("my", 68),
        ("site", 71),
        ("com", 76),
        ("au", 80),
        ("some", 83),
        ("file", 88),
        ("AndOthers", 93),
        ("not", 103),
        ("quite", 108),
        ("a", 114),
        ("url", 116),
        ("as", 157),
        ("well", 160),
    ]


def test_combined_filter(test_text):
    """Test several filters combined"""
    tknzr = get_tokenizer("en_US", filters=(URLFilter, WikiWordFilter, EmailFilter))
    assert list(tknzr(test_text)) == [
        ("this", 0),
        ("text", 5),
        ("with", 10),
        ("and", 30),
        ("not", 103),
        ("quite", 108),
        ("a", 114),
        ("url", 116),
        ("as", 157),
        ("well", 160),
    ]


def test_html_chunker():
    """Test filtering of URLs"""
    text = """hello<html><head><title>my title</title></head><body>this is a
              <b>simple</b> HTML document for <p> test<i>ing</i> purposes</p>.
            It < contains > various <-- special characters.
            """
    tknzr = get_tokenizer("en_US", chunkers=(HTMLChunker,))
    assert list(tknzr(text)) == [
        ("hello", 0),
        ("my", 24),
        ("title", 27),
        ("this", 53),
        ("is", 58),
        ("a", 61),
        ("simple", 80),
        ("HTML", 91),
        ("document", 96),
        ("for", 105),
        ("test", 113),
        ("ing", 120),
        ("purposes", 128),
        ("It", 154),
        ("contains", 159),
        ("various", 170),
        ("special", 182),
        ("characters", 190),
    ]


def test_tokenize_en():
    """Simple regression test for English tokenization."""
    input = """This is a paragraph.  It's not very special, but it's designed
2 show how the splitter works with many-different combos
of words. Also need to "test" the handling of 'quoted' words."""
    assert list(tokenize_en(input)) == [
        ("This", 0),
        ("is", 5),
        ("a", 8),
        ("paragraph", 10),
        ("It's", 22),
        ("not", 27),
        ("very", 31),
        ("special", 36),
        ("but", 45),
        ("it's", 49),
        ("designed", 54),
        ("show", 65),
        ("how", 70),
        ("the", 74),
        ("splitter", 78),
        ("works", 87),
        ("with", 93),
        ("many", 98),
        ("different", 103),
        ("combos", 113),
        ("of", 120),
        ("words", 123),
        ("Also", 130),
        ("need", 135),
        ("to", 140),
        ("test", 144),
        ("the", 150),
        ("handling", 154),
        ("of", 163),
        ("quoted", 167),
        ("words", 175),
    ]


def test_unicode_basic():
    """Test tokenization of a basic unicode string."""
    input = "Ik ben geïnteresseerd in de coördinatie van mijn knieën, maar kan niet één à twee enquêtes vinden die recht doet aan mijn carrière op Curaçao"
    output = input.split(" ")
    output[8] = output[8][0:-1]
    for (itm_o, itm_v) in zip(output, tokenize_en(input)):
        assert itm_o == itm_v[0]
        assert input[itm_v[1] :].startswith(itm_o)


def test_bug1591450():
    """Check for tokenization regressions identified in bug #1591450."""
    input = """Testing <i>markup</i> and {y:i}so-forth...leading dots and trail--- well, you get-the-point. Also check numbers: 999 1,000 12:00 .45. Done?"""
    assert list(tokenize_en(input)) == [
        ("Testing", 0),
        ("i", 9),
        ("markup", 11),
        ("i", 19),
        ("and", 22),
        ("y", 27),
        ("i", 29),
        ("so", 31),
        ("forth", 34),
        ("leading", 42),
        ("dots", 50),
        ("and", 55),
        ("trail", 59),
        ("well", 68),
        ("you", 74),
        ("get", 78),
        ("the", 82),
        ("point", 86),
        ("Also", 93),
        ("check", 98),
        ("numbers", 104),
        ("Done", 134),
    ]


def test_bug2785373():
    """Testcases for bug #2785373"""
    input = "So, one dey when I wes 17, I left."
    for _ in tokenize_en(input):
        pass
    input = "So, one dey when I wes 17, I left."
    for _ in tokenize_en(input):
        pass


def test_finnish_text():
    """Test tokenizing some Finnish text.

    This really should work since there are no special rules to apply,
    just lots of non-ascii characters.
    """
    text = textwrap.dedent(
        """\
        Tämä on kappale. Eipä ole kovin 2 nen, mutta tarkoitus on näyttää miten sanastaja
         toimii useiden-erilaisten sanaryppäiden kimpussa.
        Pitääpä vielä 'tarkistaa' sanat jotka "lainausmerkeissä". Heittomerkki ja vaa'an.
        Ulkomaisia sanoja süss, spaß.
    """
    )
    assert list(tokenize_en(text)) == [
        ("Tämä", 0),
        ("on", 5),
        ("kappale", 8),
        ("Eipä", 17),
        ("ole", 22),
        ("kovin", 26),
        ("nen", 34),
        ("mutta", 39),
        ("tarkoitus", 45),
        ("on", 55),
        ("näyttää", 58),
        ("miten", 66),
        ("sanastaja", 72),
        ("toimii", 83),
        ("useiden", 90),
        ("erilaisten", 98),
        ("sanaryppäiden", 109),
        ("kimpussa", 123),
        ("Pitääpä", 133),
        ("vielä", 141),
        ("tarkistaa", 148),
        ("sanat", 159),
        ("jotka", 165),
        ("lainausmerkeissä", 172),
        ("Heittomerkki", 191),
        ("ja", 204),
        ("vaa'an", 207),
        ("Ulkomaisia", 215),
        ("sanoja", 226),
        ("süss", 233),
        ("spaß", 239),
    ]


def test_typographic_apostrophe():
    """ "Typographic apostrophes should be word separators in English."""
    text = "They\u2019re here"
    assert list(tokenize_en(text)) == [
        ("They", 0),
        ("re", 5),
        ("here", 8),
    ]


@pytest.mark.parametrize(
    "text,expected",
    [
        ("", []),
        (b"", []),
        (bytearray(), []),
        ("a", [("a", 0)]),
        (b"a", [(b"a", 0)]),
        (bytearray((97,)), [(bytearray((97,)), 0)]),
        ("ä", [("ä", 0)]),
        (b"\xc3", []),
        (b"\xc3\xa4", [(b"\xc3\xa4", 0)]),
        (bytearray((0xC3,)), []),
        (bytearray((0xC3, 0xA4)), [(bytearray((0xC3, 0xA4)), 0)]),
    ],
)
def test_tokenize_en_byte(text, expected):
    """Test tokenizing bytes."""
    assert list(tokenize_en(text)) == expected
