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

    enchant.tokenize:    String tokenisation functions for PyEnchant

    An important task in spellchecking is breaking up large bodies of
    text into their constituent words, each of which is then checked
    for correctness.  This package provides Python functions to split
    strings into words according to the rules of a particular language.
    
    Each tokenisation function accepts a string as its only positional
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
    have changed during the tokenisation process.
    
    To obtain an appropriate tokenisation function for the language
    identified by <tag>, use the function 'get_tokenizer(tag)'.
    
    This library is designed to be easily extendable by third-party
    authors.  To register a tokenisation function for the language
    <tag>, implement it as the function 'tokenize' within the
    module enchant.tokenize.<tag>.  The 'get_tokenizer' function
    will automatically detect it.  Note that the underscore must be
    used as the tag component seperator in this case, in order to
    form a valid python module name.
    
    Currently, a tokeniser has only been implemented for the English
    language.  Based on the author's limited experience, this should
    be at least partially suitable for other languages.

    This module also provides the Filter class and a variety of subclasses.
    These are designed to allow skipping over certain types of word
    during the spellchecking process.  For example, the following would
    produce a tokenizer for the English language that skips over URLs
    and WikiWords:
        
        tknzr = URLFilter(WikiWordsFilter(get_tokenizer("en_US")))
        
    It is then used in the same way as a tokenizer functionn:
        
        tkns = tknzr("text to be tokenized goes here")
        for (word,pos) in tkns:
            do_something(word)
        
"""

import unittest
import re

import enchant

class tokenize:
    """Base class for all tokenizer objects.
    Each tokenizer must be an interator and provide the 'offset'
    attribute as described in the documentation for this module.
    """
    def __init__(self,text):
        raise NotImplementedError()
    def next(self):
        raise NotImplementedError()
    def __iter__(self):
        return self


class Error(enchant.Error):
    """Exception subclass for the tokenize module.
    This exception is raised for errors within the enchant.tokenize
    module.
    """
    pass

def get_tokenizer(tag,fallback=False):
    """Lookup an appropriate tokenizer by language tag.
    This requires importing the function 'tokenize' from an
    appropriate module.  Modules tried are named after the
    language tag, tried in the following order:
        * the entire tag (e.g. "en_AU.py")
        * the base country code of the tag (e.g. "en.py")
    If a suitable function cannot be found, raises Error.
    If the optional argument <fallback> is True, languages for which
    a tokeniser cannot be found have the English tokeniser returned.
    It should do a 'reasonable' job in most cases.
    """
    # Ensure only '_' used as seperator
    tag = tag.replace("-","_")
    # Try the whole tag
    tokenizer = _try_tokenizer(tag)
    if tokenizer is not None:
        return tokenizer
    # Try just the base
    base = tag.split("_")[0]
    tokenizer = _try_tokenizer(base)
    if tokenizer is not None:
        return tokenizer
    if fallback:
        tokenizer = _try_tokenizer("en")
        if tokenizer is not None:
            return tokenizer
    raise Error("No tokenizer found for language '%s'" % (tag,))

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


class Filter:
    """Base class for token filtering functions.
    Filters are used to skip over certain special words during a spellchecking
    session, such as URLs or WikiWords.  A filter is designed to wrap a
    tokenizer (or another filter) and skip over tokens that match its
    particular check.  So you might use them as follows:
        
        tknzr = get_tokenizer("en_US")
        tknzr = URLFilter(WikiWordsFilter(tknzr))
        
    The object in <tknzr> would then be a tokenizer function for English text
    that skips over URLs and WikiWords.
    
    Subclasses has two basic options for customising their behavior.  The
    method _match(word) may be overridden to return True for words that
    should be skipped, and false otherwise.  If more complex behavior is
    needed, the inner class TokenFilter can be overriden.
    """
    
    def __init__(self,tokenizer):
        """Filter class constructor."""
        self._tokenizer = tokenizer
    
    def __call__(self,*args,**kwds):
        tkn = self._tokenizer(*args,**kwds)
        return self.TokenFilter(tkn,self._match)
    
    def _match(self,word):
        """Filter matching method.
        If this method returns true, the given word will be skipped by
        the filter.  This should be overriden in subclasses to produce the
        desired functionality.
        """
        return False
    
    class TokenFilter:
        def __init__(self,tokenizer,match):
            self._match = match
            self._tokenizer = tokenizer
    
        def __iter__(self):
            return self
    
        def next(self):
            """Iterator protocol method for Filter objects.
            The call to next is passed on to the underlying tokenizer,
            skipping over words matching against the filter.
            """
            (word,pos) = self._tokenizer.next()
            while self._match(word):
                (word,pos) = self._tokenizer.next()
            return (word,pos)
                
        # Pass on access to offset to the tokenizer.
        def _getOffset(self):
            return self._tokenizer.offset
        def _setOffset(self,val):
            self._tokenizer.offset = val
        offset = property(_getOffset,_setOffset)


#  Pre-defined filters start here

class URLFilter(Filter):
    """Filter skipping over URLs.
    This filter skips any words matching the following regular expression:
       
           ^[a-zA-z]+:\/\/[^\s].*
        
    That is, any words that are URLs.
    """
    _pattern = re.compile(r"^[a-zA-z]+:\/\/[^\s].*")
    def _match(self,word):
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
    def _match(self,word):
        if self._pattern.match(word):
            return True
        return False

class EmailFilter(Filter):
    """Filter skipping over email addreses.
    This filter skips any words matching the following regular expression:
       
           ^.+@[^\.].*\.[a-z]{2,}$
        
    That is, any words that resemble email addresses.
    """
    _pattern = re.compile(r"^.+@[^\.].*\.[a-z]{2,}$")
    def _match(self,word):
        if self._pattern.match(word):
            return True
        return False

#TODO: HTMLFilter


# Test cases begin here

class TestGetTokenizer(unittest.TestCase):
    """TestCases for testing the get_tokenizer() functionality."""
    
    def test_get_tokenizer(self):
        """Simple regression test for get_tokenizer."""
        from enchant.tokenize import en
        self.assert_(get_tokenizer("en") is en.tokenize)
        self.assert_(get_tokenizer("en_AU") is en.tokenize)
        self.assert_(get_tokenizer("en_US") is en.tokenize)
        self.assertRaises(Error,get_tokenizer,"nonexistant")
        self.assert_(get_tokenizer("nonexistant",fallback=True) is en.tokenize)
    

class TestFilters(unittest.TestCase):
    """TestCases for the various Filter subclasses."""
    
    text = """this text with http://url.com and SomeLinksLike
              ftp://my.site.com.au/some/file AndOthers not:/quite.a.url
              with-an@aemail.address as well"""
    
    def setUp(self):
        from enchant.tokenize import en
        self.tokenize = en.tokenize
    
    def test_URLFilter(self):
        """Test filtering of URLs"""
        tkns = URLFilter(self.tokenize)(self.text)
        out = [t for t in tkns]
        exp = [("this",0),("text",5),("with",10),("and",30),
               ("SomeLinksLike",34),("AndOthers",93),("not:/quite.a.url",103),
               ("with-an@aemail.address",134),("as",157),("well",160)]
        self.assertEquals(out,exp)
        
    def test_WikiWordFilter(self):
        """Test filtering of WikiWords"""
        tkns = WikiWordFilter(self.tokenize)(self.text)
        out = [t for t in tkns]
        exp = [("this",0),("text",5),("with",10),("http://url.com",15),
               ("and",30), ("ftp://my.site.com.au/some/file",62),
               ("not:/quite.a.url",103),
               ("with-an@aemail.address",134),("as",157),("well",160)]
        self.assertEquals(out,exp)
        
    def test_EmailFilter(self):
        """Test filtering of email addresses"""
        tkns = EmailFilter(self.tokenize)(self.text)
        out = [t for t in tkns]
        exp = [("this",0),("text",5),("with",10),("http://url.com",15),
               ("and",30),("SomeLinksLike",34),
               ("ftp://my.site.com.au/some/file",62),("AndOthers",93),
               ("not:/quite.a.url",103),
               ("as",157),("well",160)]
        self.assertEquals(out,exp)
        
    def test_CombinedFilter(self):
        """Test several filters combined"""
        tkns=EmailFilter(URLFilter(WikiWordFilter(self.tokenize)))(self.text)
        out = [t for t in tkns]
        exp = [("this",0),("text",5),("with",10),
               ("and",30),("not:/quite.a.url",103),
               ("as",157),("well",160)]
        self.assertEquals(out,exp)
        
        