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
        
        (<word>,<line>,<col>)
        
    The meanings of these fields should be clear: <word> is the word
    that was found, <line> is the line within the text on which it
    appears, and <col> is the column within that line at which the
    word starts.  Both <line> and <col> start at zero.
    
    To obtain an appropriate tokenisation function for the language
    identified by <tag>, use the function 'get_tokenizer(tag)'.
    
    This library is designed to be easily extendable by third-party
    authors.  To register a tokenisation function for the language
    <tag>, implement it as the function 'tokenize' within the
    module enchant.tokenize.<tag>.  The 'get_tokenizer' function
    will automatically detect it.
    
    Currently, a tokeniser has only been implemented for the English
    language.
    
"""

import enchant
class Error(enchant.Error):
    """Exception subclass for the tokenize module.
    This exception is raised for errors within the enchant.tokenize
    module.
    """
    pass

def get_tokenizer(tag):
    """Lookup an appropriate tokenizer by language tag.
    This requires importing the function 'tokenize' from an
    appropriate module.  Modules tried are named after the
    language tag, tried in the following order:
        * the entire tag (e.g. "en_AU.py")
        * the base country code of the tag (e.g. "en.py")
    If a suitable function cannot be found, raises Error.
    """
    # Try the whole tag
    tokenizer = _try_tokenizer(tag)
    if tokenizer is not None:
        return tokenizer
    # Try just the base
    base = tag.split("_")[0]
    tokenizer = _try_tokenizer(base)
    if tokenizer is not None:
        return tokenizer
    raise Error("No tokenizer found for language '%s'" % (tag,))

def _try_tokenizer(modName):
    """Look for a tokeniser in the named module.
    Returns the function is found, None otherwise.
    """
    modBase = "enchant.tokenize."
    funcName = "tokenize"
    modName = modBase + modName
    try:
        mod = __import__(modName,globals(),{},funcName)
        return getattr(mod,funcName)
    except ImportError:
       return None
    
    