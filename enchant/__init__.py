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
    enchant.py:  Access to the enchant spellchecking library

    This module provides several classes for performing spell checking
    via the Enchant spellchecking library.  For more details on Enchant,
    visit the project website:

        http://www.abisource.com/enchant/

    Spellchecking is performed using 'Dict' objects, which represent
    a language dictionary.  Their use is best demonstrated by a quick
    example:

        >>> import enchant
        >>> d = enchant.Dict("en_US")   # create dictionary for US English
        >>> d.check("enchant")
        True
        >>> d.check("enchnt")
        False
        >>> d.suggest("enchnt")
        ['enchant', 'enchants', 'enchanter', 'penchant', 'incant', 'enchain', 'enchanted']

    Languages are identified by standard string tags such as "en" (English)
    and "fr" (French).  Specific language dialects can be specified by
    including an additional code - for example, "en_AU" refers to Australian
    English.  The later form is preferred as it is more widely supported.

    To check whether a dictionary exists for a given language, the function
    'dict_exists' is available.  Dictionaries may also be created using the
    function 'request_dict'.

    A finer degree of control over the dictionaries and how they are created
    can be obtained using one or more 'Broker' objects.  These objects are
    responsible for locating dictionaries for a specific language.
    
    Unicode strings are supported transparently, as they are throughout
    Python - if a unicode string is given as an argument, the result will
    be a unicode string.  Note that Enchant works in UTF-8 internally,
    so passing an ASCII string to a dictionary for a language requiring
    Unicode may result in UTF-8 strings being returned.

    Errors that occur in this module are reported by raising 'Error'.

"""

# Make version info available
__ver_major__ = 1
__ver_minor__ = 1
__ver_patch__ = 2
__ver_sub__ = ""
__version__ = "%d.%d.%d%s" % (__ver_major__,__ver_minor__,
                              __ver_patch__,__ver_sub__)

import _enchant as _e
import os
import sys
import warnings

class Error(Exception):
    """Base exception class for the enchant module."""
    pass


class ProviderDesc(object):
    """Simple class describing an Enchant provider.
    Each provider has the following information associated with it:

        * name:        Internal provider name (e.g. "aspell")
        * desc:        Human-readable description (e.g. "Aspell Provider")
        * file:        Location of the library containing the provider

    """

    def __init__(self,name,desc,file):
        self.name = name
        self.desc = desc
        self.file = file

    def __str__(self):
        return "<Enchant: %s>" % self.desc

    def __repr__(self):
        return str(self)



class _EnchantObject(object):
    """Base class for enchant objects.
    
    This class implements some general functionality for interfacing with
    the '_enchant' C-library in a consistent way.  All public objects
    from the 'enchant' module are subclasses of this class.
    
    All enchant objects have an attribute '_this' which contains the
    pointer to the underlying C-library object.  The method '_check_this'
    can be called to ensure that this point is not None, raising an
    exception if it is.
    """
    
    def __init__(self):
        """_EnchantObject constructor."""
        self._this = None
        
    def _check_this(self,msg=None):
         """Check that self._this is set to a pointer, rather than None."""
         if msg is None:
             msg = "%s unusable: the underlying C-library object has been freed."
             msg = msg % (self.__class__.__name__,)
         if self._this is None:
             raise Error(msg)
             
    def _raise_error(self,default="Unspecified Error: No Information Available"):
         """Raise an exception based on available error messages.
         This method causes an Error to be raised.  Subclasses should
         override it to retreive an error indication from the underlying
         API if possible.  If such a message cannot be retreived, the
         argument value 'default' is used.
         """
         raise Error(default)



class Broker(_EnchantObject):
    """Broker object for the Enchant spellchecker.

    Broker objects are responsible for locating and managing dictionaries.
    Unless custom functionality is required, there is no need to use Broker
    objects directly. The 'enchant' module provides a default broker object
    so that 'Dict' objects can be created directly.

    The most important methods of this class include:

        * dict_exists:   check existence of a specific language dictionary
        * request_dict:  obtain a dictionary for specific language
        * set_ordering:  specify which dictionaries to try for for a
                         given language.

    """

    # Because of the way the underlying enchant library caches dictionary
    # objects, it's dangerous to free dictionaries when more than one has
    # been created for the same language.  To work around this transparently,
    # keep track of how many Dicts have been created for each language.
    # Only call the underlying dict_free when this reaches zero.  This is
    # done in the __live_dicts attribute.

    def __init__(self):
        """Broker object constructor.
        
        This method is the constructor for the 'Broker' object.  No
        arguments are required.
        """
        _EnchantObject.__init__(self)
        self._this = _e.enchant_broker_init()
        if not self._this:
            raise Error("Could not initialise an enchant broker.")
        self.__live_dicts = {}

    def __del__(self):
        """Broker object destructor."""
        # Calling _free() might fail if python is shutting down
        try:
            self._free()
        except AttributeError:
            pass
            
    def _raise_error(self,default="Unspecified Error: No Information Available"):
        """Overrides _EnchantObject._raise_error to check broker errors."""
        err = _e.enchant_broker_get_error(self._this)
        if err == "" or err is None:
            raise Error(default)
        raise Error(err)

    def _free(self):
        """Free system resource associated with a Broker object.
        
        This method can be called to free the underlying system resources
        associated with a Broker object.  It is called automatically when
        the object is garbage collected.  If called explicitly, the
        Broker and any associated Dict objects must no longer be used.
        """
        if self._this is not None:
            _e.enchant_broker_free(self._this)
            self._this = None
            self.__live_dicts.clear()
            
    def __inc_live_dicts(self,tag):
        """Increment the count of live Dict objects for the given tag.
        Returns the new count of live Dicts.
        """
        try:
            self.__live_dicts[tag] += 1
        except KeyError:
            self.__live_dicts[tag] = 1
        assert(self.__live_dicts[tag] > 0)
        return self.__live_dicts[tag]

    def __dec_live_dicts(self,tag):
        """Decrement the count of live Dict objects for the given tag.
        Returns the new count of live Dicts.
        """
        try:
            self.__live_dicts[tag] -= 1
        except KeyError:
            self.__live_dicts[tag] = 0
        assert(self.__live_dicts[tag] >= 0)
        return self.__live_dicts[tag]
        
    def request_dict(self,tag):
        """Request a Dict object for the language specified by 'tag'.
        
        This method constructs and returns a Dict object for the
        requested language.  'tag' should be a string of the appropriate
        form for specifying a language, such as "fr" (French) or "en_AU"
        (Australian English).  The existence of a specific language can
        be tested using the 'dict_exists' method.
        """
        new_dict = self._request_dict_data(tag)
        return Dict(None,self,new_dict)

    def _request_dict_data(self,tag):
        """Request raw C-object data for a dictionary.
        This method passed on the call to the C library, and does
        some internal bookkeeping.
        """
        self._check_this()
        new_dict = _e.enchant_broker_request_dict(self._this,tag)
        if new_dict is None:
            eStr = "Dictionary for language '%s' could not be found"
            self._raise_error(eStr % (tag,))
        self.__inc_live_dicts(tag)
        return new_dict

    def request_pwl_dict(self,pwl):
        """Request a Dict object for a personal word list.
        
        This method behaves as 'request_dict' but rather than returning
        a dictionary for a specific language, it returns a dictionary
        referencing a personal word list.  A personal word list is a file
        of custom dictionary entries, one word per line.
        """
        self._check_this()
        new_dict = _e.enchant_broker_request_pwl_dict(self._this,pwl)
        if new_dict is None:
            eStr = "Personal Word List file '%s' could not be loaded"
            self._raise_error(eStr % (pwl,))
            self._raise_error(eStr)
        self.__inc_live_dicts(pwl)
        return Dict(None,self,new_dict)

    def _free_dict(self,dict):
        """Free memory associated with a dictionary.
        
        This method frees system resources associated with a Dict object.
        It is equivalent to calling the object's 'free' method.  Once this
        method has been called on a dictionary, it must not be used again.
        """
        self._check_this()
        if self.__dec_live_dicts(dict.tag) == 0:
            _e.enchant_broker_free_dict(self._this,dict._this)
        dict._this = None
        dict._broker = None

    def dict_exists(self,tag):
        """Check availability of a dictionary.
        
        This method checks whether there is a dictionary available for
        the language specified by 'tag'.  It returns True if a dictionary
        is available, and False otherwise.
        """
        self._check_this()
        val = _e.enchant_broker_dict_exists(self._this,tag)
        return bool(val)

    def set_ordering(self,tag,ordering):
        """Set dictionary preferences for a language.
        
        The Enchant library supports the use of multiple dictionary programs
        and multiple languages.  This method specifies which dictionaries
        the broker should prefer when dealing with a given language.  'tag'
        must be an appropriate language specification and 'ordering' is a
        string listing the dictionaries in order of preference.  For example
        a valid ordering might be "aspell,myspell,ispell".
        The value of 'tag' can also be set to "*" to set a default ordering
        for all languages for which one has not been set explicitly.
        """
        self._check_this()
        _e.enchant_broker_set_ordering(self._this,tag,ordering)

    def describe(self):
        """Return list of provider descriptions.
        
        This method returns a list of descriptions of each of the
        dictionary providers available.  Each entry in the list is a 
        ProviderDesc object.
        """
        self._check_this()
        self.__describe_result = []
        _e.enchant_broker_describe_py(self._this,self.__describe_callback)
        return [ ProviderDesc(*r) for r in self.__describe_result]

    def __describe_callback(self,name,desc,file):
        """Collector callback for dictionary description.
        
        This method is used as a callback into the _enchant function
        'enchant_broker_describe_py'.  It collects the given arguments in
        a tuple and appends them to the list '__describe_result'.
        """
        name = name.decode("utf-8")
        desc = desc.decode("utf-8")
        file = file.decode("utf-8")
        self.__describe_result.append((name,desc,file))



class Dict(_EnchantObject):
    """Dictionary object for the Enchant spellchecker.

    Dictionary objects are responsible for checking the spelling of words
    and suggesting possible corrections.  Each dictionary is owned by a
    Broker object, but unless a new Broker has explicitly been created
    then this will be the 'enchant' module default Broker and is of little
    interest.

    The important methods of this class include:

        * check():              check whether a word id spelled correctly
        * suggest():            suggest correct spellings for a word
        * add_to_session():     add a word to the current spellcheck session
        * add_to_personal():    add a word to the personal dictionary
        * store_replacement():  indicate a replacement for a given word

    Information about the dictionary is available using the following
    attributes:

        * tag:        the language tag of the dictionary
        * provider:   a ProviderDesc object for the dictionary provider
    
    """

    def __init__(self,tag,broker=None,data=None):
        """Dict object constructor.
        
        A dictionary belongs to a specific language, identified by the
        string <tag>.  It must also have an associated Broker object which
        obtains the dictionary information from the underlying system. This
        may be specified using <broker>.  If not given, the default broker
        is used.
        
        System dictionary data can also be passed using <data>.  This should
        only be done when initialising a Dict object from an existing
        C-library dictionary pointer as created from the _enchant module.
        """
        # Sanity checking on arguments
        if tag is None and data is None:
            err = "Cannot create a dictionary without a language tag or "
            err = err + "data pointer."
            raise Error(err)
        if tag is not None and data is not None:
            err = "Cannot create a dictionary using both a language tag and "
            err = err + "a data pointer."
            raise Error(err)
        # Superclass initialisation
        _EnchantObject.__init__(self)
        # Use module-level broker if none given
        if broker is None:
            broker = _broker
        # Create data if not given
        if data is None:
            data = broker._request_dict_data(tag)
        self._this = data
        self._broker = broker
        # Set instance-level description attributes
        desc = self.__describe(check_this=False)
        self.tag = desc[0]
        self.provider = ProviderDesc(*desc[1:])

    def __del__(self):
        """Dict object constructor."""
        # Calling free() might fail if python is shutting down
        try:
            self._free()
        except AttributeError:
            pass
            
    def _check_this(self,msg=None):
        """Extend _EnchantObject._check_this() to check Broker validity.
        
        It is possible for the managing Broker object to be freed without
        freeing the Dict.  Thus validity checking must take into account
        self._broker._this as well as self._this.
        """
        if self._broker is None or self._broker._this is None:
            self._this = None
        _EnchantObject._check_this(self,msg)

    def _raise_error(self,default="Unspecified Error: No Information Available"):
        """Overrides _EnchantObject._raise_error to check dict errors."""
        err = _e.enchant_dict_get_error(self._this)
        if err == "" or err is None:
            raise Error(default)
        raise Error(err)

    def _free(self):
        """Free the system resources associated with a Dict object.
        
        This method frees underlying system resources for a Dict object.
        Once it has been called, the Dict object must no longer be used.
        It is called automatically when the object is garbage collected.
        """
        if self._broker is not None:
            self._broker._free_dict(self)

    def check(self,word):
        """Check spelling of a word.
        
        This method takes a word in the dictionary language and returns
        True if it is correctly spelled, and false otherwise.
        """
        self._check_this()
        if type(word) == unicode:
            inWord = word.encode("utf-8")
        else:
            inWord = word
        val = _e.enchant_dict_check(self._this,inWord,len(inWord))
        if val == 0:
            return True
        if val > 0:
            return False
        self._raise_error()

    def suggest(self,word):
        """Suggest possible spellings for a word.
        
        This method tries to guess the correct spelling for a given
        word, returning the possibilities in a list.
        """
        self._check_this()
        if type(word) == unicode:
            inWord = word.encode("utf-8")
        else:
            inWord = word
        suggs = _e.enchant_dict_suggest_py(self._this,inWord,len(inWord))
        if type(word) == unicode:
            uSuggs = [w.decode("utf-8") for w in suggs]
            return uSuggs
        return suggs

    def add_to_personal(self,word):
        """Add a word to the user's personal dictionary."""
        self._check_this()
        if type(word) == unicode:
            inWord = word.encode("utf-8")
        else:
            inWord = word
        _e.enchant_dict_add_to_personal(self._this,inWord,len(inWord))

    def add_to_session(self,word):
        """Add a word to the session list."""
        self._check_this()
        if type(word) == unicode:
            inWord = word.encode("utf-8")
        else:
            inWord = word
        _e.enchant_dict_add_to_session(self._this,inWord,len(inWord))

    def is_in_session(self,word):
        """Check whether a word is in the session list."""
        self._check_this()
        if type(word) == unicode:
            inWord = word.encode("utf-8")
        else:
            inWord = word
        return _e.enchant_dict_is_in_session(self._this,inWord,len(inWord))

    def store_replacement(self,mis,cor):
        """Store a replacement spelling for a miss-spelled word.
        
        This method makes a suggestion to the spellchecking engine that the 
        miss-spelled word 'mis' is in fact correctly spelled as 'cor'.  Such
        a suggestion will typically mean that 'cor' appears early in the
        list of suggested spellings offered for later instances of 'mis'.
        """
        self._check_this()
        if type(mis) == unicode:
            inMis = mis.encode("utf-8")
        else:
            inMis = mis
        if type(cor) == unicode:
            inCor = cor.encode("utf-8")
        else:
            inCor = cor
        _e.enchant_dict_store_replacement(self._this,inMis,len(inMis),inCor,len(inCor))

    def __describe(self,check_this=True):
        """Return a tuple describing the dictionary.
        
        This method returns a four-element tuple describing the underlying
        spellchecker system providing the dictionary.  It will contain the
        following strings:
            * language tag
            * name of dictionary provider
            * description of dictionary provider
            * dictionary file
        Use of this method is not recommended - instead, access this
        information through the 'tag' and 'provider' attributes.
        """
	if check_this:
            self._check_this()
        _e.enchant_dict_describe_py(self._this,self.__describe_callback)
        return self.__describe_result

    def __describe_callback(self,tag,name,desc,file):
        """Collector callback for dictionary description.
        
        This method is used as a callback into the _enchant function
        'enchant_dict_describe_py'.  It collects the given arguments in
        a tuple and stores them in the attribute '__describe_result'.
        """
        name = name.decode("utf-8")
        desc = desc.decode("utf-8")
        file = file.decode("utf-8")
        self.__describe_result = (tag,name,desc,file)



class DictWithPWL(Dict):
    """Dictionary with managed personal word list.
    
    This class behaves as the standard Dict class, but also manages a
    personal word list stored in a seperate file.  The file must be
    specified at creation time by the 'pwl' argument to the constructor.
    Words added to the dictionary using "add_to_personal" are automatically
    appended to the pwl file.
    
    The Dict object managing the PWL is available as the 'pwl' attribute.
    """
    
    def __init__(self,tag,pwl,broker=None,data=None):
        """DictWithPWL constructor.

        The argument 'pwl' must be supplied, naming a file containing
	    the personal word list.  If this file does not exist, it is
    	created with default permissions.
        """
        if pwl is None:
            raise Error("DictWithPWL must be given a PWL file.")
        if not os.path.exists(pwl):
            f = file(pwl,"wt")
	    f.close()
	    del f
        Dict.__init__(self,tag,broker,data)
        self.pwl = self._broker.request_pwl_dict(pwl)
     
    def _check_this(self,msg=None):
       """Extend Dict._check_this() to check PWL validity."""
       if self.pwl is None:
           self._free()
       Dict._check_this(self,msg)
       self.pwl._check_this(msg)

    def _free(self):
        """Extend Dict.free() to free the PWL as well."""
        if self.pwl is not None:
            self.pwl._free()
            self.pwl = None
        Dict.free(self)
        
    def check(self,word):
        """Check spelling of a word.
        
        This method takes a word in the dictionary language and returns
        True if it is correctly spelled, and false otherwise.  It checks
        both the dictionary and the personal wordlist.
        """
        if Dict.check(self,word):
            return True
        if self.pwl.check(word):
            return True
        return False
        
    def add_to_personal(self,word):
        """Add a word to the associated personal word list.
        
        This method adds the given word to the personal word list, and
        automatically saves the list to disk.
        """
        self._check_this()
        self.pwl.add_to_personal(word)
        # Also add_to_session on the Dict so that it appears in suggestions
        self.add_to_session(word) 


##  Check whether there are providers available, possibly point to
##  local enchant install if not.
_broker = Broker()
if len(_broker.describe()) == 0:
    if sys.platform == "win32":
        from enchant import utils
        utils.create_registry_keys()
        _broker = Broker()
if len(_broker.describe()) == 0:
    warnings.warn("No dictionary providers are available.")


##  Create a module-level default broker object, and make its important
##  methods available at the module level.
_broker = Broker()
request_dict = _broker.request_dict
request_pwl_dict = _broker.request_pwl_dict
dict_exists = _broker.dict_exists


