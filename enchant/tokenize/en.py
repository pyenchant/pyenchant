# pyenchant
#
# Copyright (C) 2004-2005, Ryan Kelly
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

    enchant.tokenize.en:    Tokeniser for the English language
    
    This module implements a PyEnchant text tokenizer for the English
    language, based on very simple rules.

"""

import unittest
import unicodedata

import enchant.tokenize

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
    
    def __init__(self,text,valid_chars=("'",)):
        self._valid_chars = valid_chars
        self._text = text
        if isinstance(text,unicode):
            self._myIsAlpha = self._myIsAlpha_u
        else:
            self._myIsAlpha = self._myIsAlpha_a
        self.offset = 0
    
    def _myIsAlpha_a(self,c):
        if c.isalpha() or c in self._valid_chars:
            return True
        return False

    def _myIsAlpha_u(self,c):
        """Extra is-alpha tests for unicode characters.
        As well as letter characters, treat combining marks as letters.
        """
        if c.isalpha():
            return True
        if c in self._valid_chars:
            return True
        if unicodedata.category(c)[0] == "M":
            return True
        return False

    def next(self):
        text = self._text
        offset = self.offset
        while True:
            if offset >= len(text):
                break
            # Find start of next word (must be alpha)
            while offset < len(text) and not text[offset].isalpha():
                offset += 1
            curPos = offset
            # Find end of word using myIsAlpha
            while offset < len(text) and self._myIsAlpha(text[offset]):
                offset += 1
            # Return if word isnt empty
            if(curPos != offset):
                # Make sure word ends with an alpha
                while not text[offset-1].isalpha():
                    offset = offset - 1
                self.offset = offset
                return (text[curPos:offset],curPos)
        self.offset = offset
        raise StopIteration()


class TestTokenizeEN(unittest.TestCase):
    """TestCases for checking behavior of English tokenization."""
    
    def test_tokenize_en(self):
        """Simple regression test for english tokenization."""
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

    def test_unicodeBasic(self):
        """Test tokenization of a basic unicode string."""
        input = u"Ik ben ge\u00EFnteresseerd in de co\u00F6rdinatie van mijn knie\u00EBn, maar kan niet \u00E9\u00E9n \u00E0 twee enqu\u00EAtes vinden die recht doet aan mijn carri\u00E8re op Cura\u00E7ao"
        output = input.split(" ")
        output[8] = output[8][0:-1]
        for (itmO,itmV) in zip(output,tokenize(input)):
            self.assertEqual(itmO,itmV[0])
            self.assert_(input[itmV[1]:].startswith(itmO))

    def test_unicodeCombining(self):
        """Test tokenization with unicode combining symbols."""
        input = u"Ik ben gei\u0308nteresseerd in de co\u00F6rdinatie van mijn knie\u00EBn, maar kan niet e\u0301e\u0301n \u00E0 twee enqu\u00EAtes vinden die recht doet aan mijn carri\u00E8re op Cura\u00E7ao"
        output = input.split(" ")
        output[8] = output[8][0:-1]
        for (itmO,itmV) in zip(output,tokenize(input)):
            self.assertEqual(itmO,itmV[0])
            self.assert_(input[itmV[1]:].startswith(itmO))

