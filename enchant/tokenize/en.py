"""

    enchant.tokenize.en:    Tokeniser for the English language
    
    This module implements a PyEnchant text tokeniser for the English
    language, based on very simple rules.

"""

def tokenize(text,valid_chars=("'")):
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
    # Test out the tokenizer functionality
    input = """This is a paragraph.  It's not very special, but it's designed
2 show how the splitter works with many-different combos
of words."""
    for entry in tokenize(input):
        print entry
        
