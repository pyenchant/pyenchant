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
        self.offset = 0
    
    def _myIsAlpha(self,c):
        if c.isalpha() or c in self._valid_chars:
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


def _test_tokenize_en():
    """Simple regression test for english tokenization."""
    print "TESTING tokenize.en.tokenize"
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
        assert(itmO == itmV)
    print "...ALL PASSED!"


if __name__ == "__main__":
    _test_tokenize_en()
    
    
        
