# pyenchant
#
# Copyright (C) 2004 Ryan Kelly
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

    enchant.utils:    Misc utilities for the enchant package
    
    This module provies miscellaneous utilities for use with the
    enchant spellchecking package.  Currently, it's sort of a
    'play area' to try out new ideas.  It may stabilise into
    a useful set of tools in the near future.
    
    Current things to be implemented:
        
        * a stateful SpellChecker class which can be used as a backend
          to a standard dialog.  It would have things like ignore once,
          ignore always, replace always and so forth.
          
        * a tokeniser, to break paragraphs into individual words for
          spellchecking purposes.  We might be able to find an
          existing implementation...
          
        * perhaps some GUIs implemented in the common toolkits, e.g.
          Tkinter and wxPython, as examples of how to use it as well
          as for general use.
          
"""

def splitText(text,valid_chars=("'")):
    """Generator splitting text into words, reporting line and column.
    
    This generator takes a text string as input, and yields tuples
    representing each distinct word found in the text.  The tuples
    take the form:
        
        (word,line,column)
        
    Where <word> is the word string found, <line> is the numeric line
    number on which the word as found, and <column> is the numeric
    column number at which the word was found.  Both the line and
    column numbers start from zero.
    
    The optional argument <valid_chars> may be used to specify a
    list of additional characters that can form part of a word.
    By default, this list contains only the apostrophe (')
    """
    # Allow easy comparison for alphanumeracy
    def myIsAlpha(c):
        if c.isalpha() or c in valid_chars:
            return True
        return False
    # Run tokenisation on a per-line basis,
    # keeping track of line and column number
    lines = text.split("\n")
    curLine = 0
    curCol = 0
    baseCol = curCol
    for line in lines:
        offset = 0
        while True:
          if offset >= len(line):
              break
          while offset < len(line) and not line[offset].isalpha():
            offset += 1
          curCol = baseCol + offset
          while offset < len(line) and myIsAlpha(line[offset]):
            offset += 1
          if(curCol != offset):
              yield (line[curCol:offset],curLine,curCol)
        curLine += 1
        curCol = 0
        baseCol = curCol

if __name__ == "__main__":
    # Test out the splitter functionality
    input = """This is a paragraph.  It's not very special, but it's designed
2 show how the splitter works with many-different combos
of words.
            """
    for entry in splitText(input):
        print entry 
