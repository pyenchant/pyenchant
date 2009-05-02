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

    enchant.tokenize:    String tokenization functions for PyEnchant

    An important task in spellchecking is breaking up large bodies of
    text into their constituent words, each of which is then checked
    for correctness.  This package provides Python functions to split
    strings into words according to the rules of a particular language.
    
    Each tokenization function accepts a string as its only positional
    argument, and returns an iterator which will yield tuples of the
    following form, one for each word found:
        
        (<word>,<pos>)
        
    The meanings of these fields should be clear: <word> is the word
    that was found and <pos> is the position within the text at which
    the word began (zero indexed, of course).  The function will work
    on any string-like object that supports array-slicing - in
    particular, character-array objects from the 'array' module may
    be used.
    
    The iterator also provides the attribute 'offset' which may be used
    to get/set the current position of the tokenizer inside the string
    being split.  This can be used for example if the string's contents
    have changed during the tokenization process.
    
    To obtain an appropriate tokenization function for the language
    identified by <tag>, use the function 'get_tokenizer(tag)'.
    
    This library is designed to be easily extendible by third-party
    authors.  To register a tokenization function for the language
    <tag>, implement it as the function 'tokenize' within the
    module enchant.tokenize.<tag>.  The 'get_tokenizer' function
    will automatically detect it.  Note that the underscore must be
    used as the tag component separator in this case, in order to
    form a valid python module name. (e.g. "en_US" rather than "en-US")
    
    Currently, a tokenizer has only been implemented for the English
    language.  Based on the author's limited experience, this should
    be at least partially suitable for other languages.

    This module also provides the Filter class and a variety of subclasses.
    These are designed to allow skipping over certain types of word
    during the spellchecking process.  You can pass a list of filters to
    get_tokenizer as follows:
        
        tknzr = get_tokenizer("en_US",(URLFilter,WikiWordFilter))
        
    Use the tokenizer so returned as follows:
        
        tkns = tknzr("text to be tokenized goes here")
        for (word,pos) in tkns:
            do_something(word)
        
"""
_DOC_ERRORS = ["pos","pos","tknzr","URLFilter","WikiWordFilter",
               "tkns","tknzr","pos","tkns"]

import unittest
import re

import enchant

class Error(enchant.Error):
    """Exception subclass for the tokenize module.
    This exception is raised for errors within the enchant.tokenize
    module.
    """
    pass


class tokenize:
    """Base class for all tokenizer objects.
    
    Each tokenizer must be an iterator and provide the 'offset'
    attribute as described in the documentation for this module.
    
    While tokenizers are in fact classes, they should be treated
    like functions, and so are named using lower_case rather than
    the CamelCase more traditional of class names.
    """
    _DOC_ERRORS = ["CamelCase"]

    def __init__(self,text):
        self._text = text
        self.offset = 0

    def __next__(self):
        return self.next()

    def next(self):
        raise NotImplementedError()

    def __iter__(self):
        return self


class empty_tokenize(tokenize):
    """Tokenizer class that yields no elements."""
    _DOC_ERRORS = []

    def __init__(self):
        tokenize.__init__(self,"")
        
    def next(self):
        raise StopIteration()


class unit_tokenize(tokenize):
    """Tokenizer class that yields the text as a single token."""
    _DOC_ERRORS = []

    def __init__(self,text):
        tokenize.__init__(self,text)
        self._done = False

    def next(self):
        if self._done:
            raise StopIteration()
        self._done = True
        return (self._text,0)
    

class basic_tokenize(tokenize):
    """Tokenizer class that performs very basic word-finding.
    
    This tokenizer does the most basic thing that could work - it splits
    text into words based on whitespace boundaries, and removes basic
    punctuation symbols from the start and end of each word.
    """
    _DOC_ERRORS = []
    
    # Chars to remove from start/end of words
    strip_from_start = '"' + "'`(["
    strip_from_end = '"' + "'`]).!,?;:"
    
    def next(self):
        text = self._text
        offset = self.offset
        while True:
            if offset >= len(text):
                break
            # Find start of next word
            while offset < len(text) and text[offset].isspace():
                offset += 1
            sPos = offset
            # Find end of word
            while offset < len(text) and not text[offset].isspace():
                offset += 1
            ePos = offset
            self.offset = offset
            # Strip chars from font/end of word
            while sPos < len(text) and text[sPos] in self.strip_from_start:
                sPos += 1
            while 0 < ePos and text[ePos-1] in self.strip_from_end:
                    ePos -= 1
            # Return if word isnt empty
            if(sPos < ePos):
                return (text[sPos:ePos],sPos)
        raise StopIteration()


def get_tokenizer(tag,filters=None):
    """Locate an appropriate tokenizer by language tag.

    This requires importing the function 'tokenize' from an
    appropriate module.  Modules tried are named after the
    language tag, tried in the following order:
        * the entire tag (e.g. "en_AU.py")
        * the base country code of the tag (e.g. "en.py")

    If a suitable function cannot be found, raises Error.
    
    If given and not None, 'filters' must be a list of filter
    classes that will be applied to the tokenizer during creation.
    """
    # Ensure only '_' used as separator
    tag = tag.replace("-","_")
    # First try the whole tag
    tkFunc = _try_tokenizer(tag)
    if tkFunc is None:
        # Try just the base
        base = tag.split("_")[0]
        tkFunc = _try_tokenizer(base)
        if tkFunc is None:
            raise Error("No tokenizer found for language '%s'" % (tag,))
    # Given the language-specific tokenizer, we now build up the
    # end result as follows:
    #    * begin with basic whitespace tokenization
    #    * apply each of the given filters in turn
    #    * apply language-specific rules
    tokenizer = basic_tokenize
    if filters is not None:
        for f in filters:
            tokenizer = f(tokenizer)
    tokenizer = wrap_tokenizer(tokenizer,tkFunc)
    return tokenizer
get_tokenizer._DOC_ERRORS = ["py","py"]
    

def _try_tokenizer(modName):
    """Look for a tokenizer in the named module.
    Returns the function if found, None otherwise.
    """
    modBase = "enchant.tokenize."
    funcName = "tokenize"
    modName = modBase + modName
    try:
        mod = __import__(modName,globals(),{},funcName)
        return getattr(mod,funcName)
    except ImportError:
       return None


def wrap_tokenizer(tk1,tk2):
    """Wrap one tokenizer inside another.
 
    This function takes two tokenizer functions 'tk1' and 'tk2',
    and returns a new tokenizer function that passes the output
    of tk1 through tk2 before yielding it to the calling code.
    """
    # This logic is already implemented in the Filter class.
    # We simply use tk2 as the _split() method for a filter
    # around tk1.
    tkW = Filter(tk1)
    tkW._split = tk2
    return tkW
wrap_tokenizer._DOC_ERRORS = ["tk","tk","tk","tk"]


class Filter:
    """Base class for token filtering functions.
    
    A filter is designed to wrap a tokenizer (or another filter) and do
    two things:

      * skip over tokens
      * split tokens into sub-tokens

    Subclasses has two basic options for customising their behaviour.  The
    method _skip(word) may be overridden to return True for words that
    should be skipped, and false otherwise.  The method _split(word) may
    be overridden as tokenization function that will be applied to further
    tokenize any words that aren't skipped.
    """
    
    def __init__(self,tokenizer):
        """Filter class constructor."""
        self._tokenizer = tokenizer
    
    def __call__(self,*args,**kwds):
        tkn = self._tokenizer(*args,**kwds)
        return self._TokenFilter(tkn,self._skip,self._split)
    
    def _skip(self,word):
        """Filter method for identifying skippable tokens.
        
        If this method returns true, the given word will be skipped by
        the filter.  This should be overridden in subclasses to produce the
        desired functionality.  The default behaviour is not to skip any
        words.
        """
        return False

    def _split(self,word):
        """Filter method for sub-tokenization of tokens.
        
        This method must be a tokenization function that will split the
        given word into sub-tokens according to the needs of the filter.
        The default behaviour is not to split any words.
        """
        return unit_tokenize(word)


    class _TokenFilter(object):
        """Private inner class implementing the tokenizer-wrapping logic.
        
        This might seem convoluted, but we're trying to create something
        akin to a meta-class - when Filter(tknzr) is called it must return
        a *callable* that can then be applied to a particular string to
        perform the tokenization.  Since we need to manage a lot of state
        during tokenization, returning a class is the best option.
        """
        _DOC_ERRORS = ["tknzr"]
 
        def __init__(self,tokenizer,skip,split):
            self._skip = skip
            self._split = split
            self._tokenizer = tokenizer
            # for managing state of sub-tokenization
            self._curtok = empty_tokenize()
            self._curword = ""
            self._curpos = 0
    
        def __iter__(self):
            return self

        def __next__(self):
            return self.next()
    
        def next(self):
            # Try to get the next sub-token from word currently being split.
            # If unavailable, move on to the next word and try again.
            try:
                (word,pos) = self._curtok.next()
                return (word,pos + self._curpos)
            except StopIteration:
                (word,pos) = self._tokenizer.next()
                while self._skip(word):
                    (word,pos) = self._tokenizer.next()
                self._curword = word
                self._curpos = pos
                self._curtok = self._split(word)
                return self.next()
            
        
        # Pass on access to 'offset' to the underlying tokenizer.
        def _getOffset(self):
            return self._tokenizer.offset
        def _setOffset(self,val):
            self._tokenizer.offset = val
            # If we stay within the current word, also set on _curtok.
            # Otherwise, throw away _curtok and set to empty iterator.
            subval = val - self._curpos
            if subval >= 0 and subval < len(self._curword):
                self._curtok.offset = subval
            else:
                self._curtok = empty_tokenize()
                self._curword = ""
                self._curpos = 0
        offset = property(_getOffset,_setOffset)


#  Pre-defined filters start here

class URLFilter(Filter):
    """Filter skipping over URLs.
    This filter skips any words matching the following regular expression:
       
           ^[a-zA-z]+:\/\/[^\s].*
        
    That is, any words that are URLs.
    """
    _DOC_ERRORS = ["zA"]
    _pattern = re.compile(r"^[a-zA-z]+:\/\/[^\s].*")
    def _skip(self,word):
        if self._pattern.match(word):
            return True
        return False

class WikiWordFilter(Filter):
    """Filter skipping over WikiWords.
    This filter skips any words matching the following regular expression:
       
           ^([A-Z]\w+[A-Z]+\w+)
        
    That is, any words that are WikiWords.
    """
    _pattern = re.compile(r"^([A-Z]\w+[A-Z]+\w+)")
    def _skip(self,word):
        if self._pattern.match(word):
            return True
        return False

class EmailFilter(Filter):
    """Filter skipping over email addresses.
    This filter skips any words matching the following regular expression:
       
           ^.+@[^\.].*\.[a-z]{2,}$
        
    That is, any words that resemble email addresses.
    """
    _pattern = re.compile(r"^.+@[^\.].*\.[a-z]{2,}$")
    def _skip(self,word):
        if self._pattern.match(word):
            return True
        return False


#TODO: HTMLFilter, LaTeXFilter, ...


# Test cases begin here

class TestTokenization(unittest.TestCase):
    """TestCases for testing the basic tokenization functionality."""
    
    def test_basic_tokenize(self):
        """Simple regression test for basic white-space tokenization."""
        input = """This is a paragraph.  It's not very special, but it's designed
2 show how the splitter works with many-different combos
of words. Also need to "test" the (handling) of 'quoted' words."""
        output = [
                  ("This",0),("is",5),("a",8),("paragraph",10),("It's",22),
                  ("not",27),("very",31),("special",36),("but",45),("it's",49),
                  ("designed",54),("2",63), ("show",65),("how",70),("the",74),
                  ("splitter",78),("works",87),("with",93),("many-different",98),
                  ("combos",113),("of",120),("words",123),
                  ("Also",130),("need",135),
                  ("to",140),("test",144),("the",150),("handling",155),
                  ("of",165),("quoted",169),("words",177)
                 ]
        self.assertEqual(output,[i for i in basic_tokenize(input)])
        for (itmO,itmV) in zip(output,basic_tokenize(input)):
            self.assertEqual(itmO,itmV)

    def test_tokenize_strip(self):
        """Test special-char-stripping edge-cases in basic_tokenize."""
        input = "((' <this> \"\" 'text' has (lots) of (special chars} >>]"
        output = [ ("<this>",4),("text",15),("has",21),("lots",26),("of",32),
                   ("special",36),("chars}",44),(">>",51)]
        self.assertEqual(output,[i for i in basic_tokenize(input)])
        for (itmO,itmV) in zip(output,basic_tokenize(input)):
            self.assertEqual(itmO,itmV)
            
    def test_wrap_tokenizer(self):
        """Test wrapping of one tokenizer with another."""
        input = "this-string will be split@according to diff'rnt rules"
        from enchant.tokenize import en
        tknzr = wrap_tokenizer(basic_tokenize,en.tokenize)
        tknzr = tknzr(input)
        self.assertEquals(tknzr._tokenizer.__class__,basic_tokenize)
        self.assertEquals(tknzr._tokenizer.offset,0)
        for (n,(word,pos)) in enumerate(tknzr):
            if n == 0:
                self.assertEquals(pos,0)
                self.assertEquals(word,"this")
            if n == 1:
                self.assertEquals(pos,5)
                self.assertEquals(word,"string")
            if n == 2:
                self.assertEquals(pos,12)
                self.assertEquals(word,"will")
                # Test setting offset to a previous token
                tknzr.offset = 5
                self.assertEquals(tknzr.offset,5)
                self.assertEquals(tknzr._tokenizer.offset,5)
                self.assertEquals(tknzr._curtok.__class__,empty_tokenize)
            if n == 3:
                self.assertEquals(word,"string")
                self.assertEquals(pos,5)
            if n == 4:
                self.assertEquals(pos,12)
                self.assertEquals(word,"will")
            if n == 5:
                self.assertEquals(pos,17)
                self.assertEquals(word,"be")
                # Test setting offset past the current token
                tknzr.offset = 20
                self.assertEquals(tknzr.offset,20)
                self.assertEquals(tknzr._tokenizer.offset,20)
                self.assertEquals(tknzr._curtok.__class__,empty_tokenize)
            if n == 6:
                self.assertEquals(pos,20)
                self.assertEquals(word,"split")
            if n == 7:
                self.assertEquals(pos,26)
                self.assertEquals(word,"according")
                # Test setting offset to middle of current token
                tknzr.offset = 23
                self.assertEquals(tknzr.offset,23)
                self.assertEquals(tknzr._tokenizer.offset,23)
                self.assertEquals(tknzr._curtok.offset,3)
            if n == 8:
                self.assertEquals(pos,23)
                self.assertEquals(word,"it")
            # OK, I'm pretty happy with the behaviour, no need to
            # continue testing the rest of the string



class TestFilters(unittest.TestCase):
    """TestCases for the various Filter subclasses."""
    
    text = """this text with http://url.com and SomeLinksLike
              ftp://my.site.com.au/some/file AndOthers not:/quite.a.url
              with-an@aemail.address as well"""
    
    def setUp(self):
        pass
    
    def test_URLFilter(self):
        """Test filtering of URLs"""
        tkns = get_tokenizer("en_US",(URLFilter,))(self.text)
        out = [t for t in tkns]
        exp = [("this",0),("text",5),("with",10),("and",30),
               ("SomeLinksLike",34),("AndOthers",93),("not",103),("quite",108),
               ("a",114),("url",116),("with",134),("an",139),("aemail",142),
               ("address",149),("as",157),("well",160)]
        self.assertEquals(out,exp)
        
    def test_WikiWordFilter(self):
        """Test filtering of WikiWords"""
        tkns = get_tokenizer("en_US",(WikiWordFilter,))(self.text)
        out = [t for t in tkns]
        exp = [("this",0),("text",5),("with",10),("http",15),("url",22),("com",26),
               ("and",30), ("ftp",62),("my",68),("site",71),("com",76),("au",80),
               ("some",83),("file",88),("not",103),("quite",108),
               ("a",114),("url",116),("with",134),("an",139),("aemail",142),
               ("address",149),("as",157),("well",160)]
        self.assertEquals(out,exp)
        
    def test_EmailFilter(self):
        """Test filtering of email addresses"""
        tkns = get_tokenizer("en_US",(EmailFilter,))(self.text)
        out = [t for t in tkns]
        exp = [("this",0),("text",5),("with",10),("http",15),("url",22),("com",26),
               ("and",30),("SomeLinksLike",34),
               ("ftp",62),("my",68),("site",71),("com",76),("au",80),
               ("some",83),("file",88),("AndOthers",93),("not",103),("quite",108),
               ("a",114),("url",116),
               ("as",157),("well",160)]
        self.assertEquals(out,exp)
        
    def test_CombinedFilter(self):
        """Test several filters combined"""
        tkns=get_tokenizer("en_US",(URLFilter,WikiWordFilter,EmailFilter))(self.text)
        out = [t for t in tkns]
        exp = [("this",0),("text",5),("with",10),
               ("and",30),("not",103),("quite",108),
               ("a",114),("url",116),
               ("as",157),("well",160)]
        self.assertEquals(out,exp)
        
        
