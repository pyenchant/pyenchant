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
"""

    enchant.tokenize.en:    Tokenizer for the English language
    
    This module implements a PyEnchant text tokenizer for the English
    language, based on very simple rules.

"""

import unittest
import unicodedata

import enchant.tokenize

from enchant.utils import unicode, raw_unicode

class tokenize(enchant.tokenize.tokenize):
    """Iterator splitting text into words, reporting position.
    
    This iterator takes a text string as input, and yields tuples
    representing each distinct word found in the text.  The tuples
    take the form:
        
        (<word>,<pos>)
        
    Where <word> is the word string found and <pos> is the position
    of the start of the word within the text.
    
    The optional argument <valid_chars> may be used to specify a
    list of additional characters that can form part of a word.
    By default, this list contains only the apostrophe ('). Note that
    these characters cannot appear at the start or end of a word.
    """

    _DOC_ERRORS = ["pos","pos"]
    
    def __init__(self,text,valid_chars=("'",)):
        self._valid_chars = valid_chars
        self._text = text
        self.offset = 0
        # Select proper implementation of self._consume_alpha.
        # 'text' may not be a string here (it could be e.g. a mutable array)
        # so we can't use isinstance(text,unicode) to detect unicode.
        # Instead we typetest the first character of the text.
        # If there's no characters then it doesn't matter what implementation
        # we use since it won't be called anyway. 
        try:
            char1 = text[0]
        except IndexError:
            self._consume_alpha = self._consume_alpha_b
        else:
            if isinstance(char1,unicode):
                self._consume_alpha = self._consume_alpha_u
            else:
                self._consume_alpha = self._consume_alpha_b
    
    def _consume_alpha_b(self,text,offset):
        """Consume an alphabetic character from the given bytestring.

        Given a bytestring and the current offset, this method returns
        the number of characters occupied by the next alphabetic character
        in the string.  Non-ASCII bytes are interpreted as utf-8 and can
        result in multiple characters being consumed.
        """
        assert offset < len(text)
        if text[offset].isalpha():
            return 1
        elif text[offset] >= "\x80":
            return self._consume_alpha_utf8(text,offset)
        return 0

    def _consume_alpha_utf8(self,text,offset):
        """Consume a sequence of utf8 bytes forming an alphabetic character."""
        incr = 2
        u = ""
        while not u and incr <= 4:
            try:
                u = text[offset:offset+incr].decode("utf8")
            except UnicodeDecodeError:
                incr += 1
        if not u:
            return 0
        if u.isalpha():
            return incr
        if unicodedata.category(u)[0] == "M":
            return incr
        return 0

    def _consume_alpha_u(self,text,offset):
        """Consume an alphabetic character from the given unicode string.

        Given a unicode string and the current offset, this method returns
        the number of characters occupied by the next alphabetic character
        in the string.  Trailing combining characters are consumed as a
        single letter.
        """
        assert offset < len(text)
        incr = 0
        if text[offset].isalpha():
            incr = 1
            while offset + incr < len(text):
                if unicodedata.category(text[offset+incr])[0] != "M":
                    break
                incr += 1
        return incr

    def next(self):
        text = self._text
        offset = self.offset
        while offset < len(text):
            # Find start of next word (must be alpha)
            while offset < len(text):
                incr = self._consume_alpha(text,offset)
                if incr:
                    break
                offset += 1
            curPos = offset
            # Find end of word using, allowing valid_chars
            while offset < len(text):
                incr = self._consume_alpha(text,offset)
                if not incr:
                    if text[offset] in self._valid_chars:
                        incr = 1
                    else:
                        break
                offset += incr
            # Return if word isnt empty
            if(curPos != offset):
                # Make sure word doesn't end with a valid_char
                while text[offset-1] in self._valid_chars:
                    offset = offset - 1
                self.offset = offset
                return (text[curPos:offset],curPos)
        self.offset = offset
        raise StopIteration()


class TestTokenizeEN(unittest.TestCase):
    """TestCases for checking behaviour of English tokenization."""
    
    def test_tokenize_en(self):
        """Simple regression test for English tokenization."""
        input = """This is a paragraph.  It's not very special, but it's designed
2 show how the splitter works with many-different combos
of words. Also need to "test" the handling of 'quoted' words."""
        output = [
                  ("This",0),("is",5),("a",8),("paragraph",10),("It's",22),
                  ("not",27),("very",31),("special",36),("but",45),("it's",49),
                  ("designed",54),("show",65),("how",70),("the",74),
                  ("splitter",78),("works",87),("with",93),("many",98),
                  ("different",103),("combos",113),("of",120),("words",123),
                  ("Also",130),("need",135),
                  ("to",140),("test",144),("the",150),("handling",154),
                  ("of",163),("quoted",167),("words",175)
                 ]
        for (itmO,itmV) in zip(output,tokenize(input)):
            self.assertEqual(itmO,itmV)

    def test_unicodeBasic(self):
        """Test tokenization of a basic unicode string."""
        input = raw_unicode(r"Ik ben ge\u00EFnteresseerd in de co\u00F6rdinatie van mijn knie\u00EBn, maar kan niet \u00E9\u00E9n \u00E0 twee enqu\u00EAtes vinden die recht doet aan mijn carri\u00E8re op Cura\u00E7ao")
        output = input.split(" ")
        output[8] = output[8][0:-1]
        for (itmO,itmV) in zip(output,tokenize(input)):
            self.assertEqual(itmO,itmV[0])
            self.assert_(input[itmV[1]:].startswith(itmO))

    def test_unicodeCombining(self):
        """Test tokenization with unicode combining symbols."""
        input = raw_unicode(r"Ik ben gei\u0308nteresseerd in de co\u00F6rdinatie van mijn knie\u00EBn, maar kan niet e\u0301e\u0301n \u00E0 twee enqu\u00EAtes vinden die recht doet aan mijn carri\u00E8re op Cura\u00E7ao")
        output = input.split(" ")
        output[8] = output[8][0:-1]
        for (itmO,itmV) in zip(output,tokenize(input)):
            self.assertEqual(itmO,itmV[0])
            self.assert_(input[itmV[1]:].startswith(itmO))

    def test_utf8_bytes(self):
        """Test tokenization of UTF8-encoded bytes (bug #2500184)."""
        input = 'A r\xc3\xa9sum\xc3\xa9, also spelled resum\xc3\xa9 or resume'
        output = input.split(" ")
        output[1] = output[1][0:-1]
        for (itmO,itmV) in zip(output,tokenize(input)):
            self.assertEqual(itmO,itmV[0])
            self.assert_(input[itmV[1]:].startswith(itmO))

    def test_bug1591450(self):
        """Check for tokenization regressions identified in bug #1591450."""
        input = """Testing <i>markup</i> and {y:i}so-forth...leading dots and trail--- well, you get-the-point. Also check numbers: 999 1,000 12:00 .45. Done?"""
        output = [
                  ("Testing",0),("i",9),("markup",11),("i",19),("and",22),
                  ("y",27),("i",29),("so",31),("forth",34),("leading",42),
                  ("dots",50),("and",55),("trail",59),("well",68),
                  ("you",74),("get",78),("the",82),("point",86),
                  ("Also",93),("check",98),("numbers",104),("Done",134),
                 ]
        for (itmO,itmV) in zip(output,tokenize(input)):
            self.assertEqual(itmO,itmV)

    def test_bug2785373(self):
        "Testcases for bug #2785373"
        input = "So, one dey when I wes 17, I left."
        for _ in tokenize(input):
            pass
        input = raw_unicode("So, one dey when I wes 17, I left.")
        for _ in tokenize(input):
            pass

