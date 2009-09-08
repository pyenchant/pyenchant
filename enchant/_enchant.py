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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPsE.  See the GNU
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

    enchant._enchant:  ctypes-based wrapper for enchant C library

    This module implements the low-level interface to the underlying
    C library for enchant.  The interface is based on ctypes and tries 
    to do as little as possible while making the higher-level components
    easier to write.

    The following conveniences are provided that differ from the underlying
    C API:

        * the "enchant" prefix has been removed from all functions, since
          python has a proper module system
        * callback functions do not take a user_data argument, since
          python has proper closures that can manage this internally
        * string lengths are not passed into functions such as dict_check,
          since python strings know how long they are

"""

import sys, os, os.path
from ctypes import *
from ctypes.util import find_library

from enchant import utils
from enchant.errors import *

# Locate and load the enchant dll.

if sys.platform == "win32":
  # Add our bundled enchant libraries to DLL search path
  try:
      mypath = os.path.dirname(utils.get_resource_filename("libenchant.dll"))
  except Error:
      mypath = os.path.dirname(utils.get_resource_filename("libenchant-1.dll"))
  os.environ['PATH'] = os.environ['PATH'] + ";" + mypath

def _e_path_possibilities():
    yield os.environ.get("PYENCHANT_LIBRARY_PATH")
    yield find_library("enchant")
    yield find_library("libenchant")
    yield find_library("libenchant-1")
    if sys.platform == 'darwin':
         # enchant lib installed by macports
         yield "/opt/local/lib/libenchant.dylib"

for e_path in _e_path_possibilities():
    if e_path is not None:
        try:
            e = cdll.LoadLibrary(e_path)
        except OSError:
            pass
        else:
            break
else:
   raise ImportError("enchant C library not found")


# Define various callback function types

t_broker_desc_func = CFUNCTYPE(None,c_char_p,c_char_p,c_char_p,c_void_p)
t_dict_desc_func = CFUNCTYPE(None,c_char_p,c_char_p,c_char_p,c_char_p,c_void_p)


# Simple typedefs for readability

t_broker = c_void_p
t_dict = c_void_p


# Now we can define the types of each function we are going to use

broker_init = e.enchant_broker_init
broker_init.argtypes = []
broker_init.restype = t_broker

broker_free = e.enchant_broker_free
broker_free.argtypes = [t_broker]
broker_free.restype = None

broker_request_dict = e.enchant_broker_request_dict
broker_request_dict.argtypes = [t_broker,c_char_p]
broker_request_dict.restype = t_dict

broker_request_pwl_dict = e.enchant_broker_request_pwl_dict
broker_request_pwl_dict.argtypes = [t_broker,c_char_p]
broker_request_pwl_dict.restype = t_dict

broker_free_dict = e.enchant_broker_free_dict
broker_free_dict.argtypes = [t_broker,t_dict]
broker_free_dict.restype = None

broker_dict_exists = e.enchant_broker_dict_exists
broker_dict_exists.argtypes = [t_broker,c_char_p]
broker_free_dict.restype = c_int

broker_set_ordering = e.enchant_broker_set_ordering
broker_set_ordering.argtypes = [t_broker,c_char_p,c_char_p]
broker_set_ordering.restype = None

broker_get_error = e.enchant_broker_get_error
broker_get_error.argtypes = [t_broker]
broker_get_error.restype = c_char_p

broker_describe1 = e.enchant_broker_describe
broker_describe1.argtypes = [t_broker,t_broker_desc_func,c_void_p]
broker_describe1.restype = None
def broker_describe(broker,cbfunc):
    def cbfunc1(*args):
        cbfunc(*args[:-1])
    broker_describe1(broker,t_broker_desc_func(cbfunc1),None)

broker_list_dicts1 = e.enchant_broker_list_dicts
broker_list_dicts1.argtypes = [t_broker,t_dict_desc_func,c_void_p]
broker_list_dicts1.restype = None
def broker_list_dicts(broker,cbfunc):
    def cbfunc1(*args):
        cbfunc(*args[:-1])
    broker_list_dicts1(broker,t_dict_desc_func(cbfunc1),None)

try:
    broker_get_param = e.enchant_broker_get_param
except AttributeError:
    #  Make the lookup error occur at runtime
    def broker_get_param(broker,param_name):
        return e.enchant_broker_get_param(param_name)
else:
    broker_get_param.argtypes = [t_broker,c_char_p]
    broker_get_param.restype = c_char_p

try:
    broker_set_param = e.enchant_broker_set_param
except AttributeError:
    #  Make the lookup error occur at runtime
    def broker_set_param(broker,param_name):
        return e.enchant_broker_set_param(param_name)
else:
    broker_set_param.argtypes = [t_broker,c_char_p,c_char_p]
    broker_set_param.restype = None


dict_check1 = e.enchant_dict_check
dict_check1.argtypes = [t_dict,c_char_p,c_size_t]
dict_check1.restype = c_int
def dict_check(dict,word):
    return dict_check1(dict,word,len(word))

dict_suggest1 = e.enchant_dict_suggest
dict_suggest1.argtypes = [t_dict,c_char_p,c_size_t,POINTER(c_size_t)]
dict_suggest1.restype = POINTER(c_char_p)
def dict_suggest(dict,word):
    numSuggsP = pointer(c_size_t(0))
    suggs_c = dict_suggest1(dict,word,len(word),numSuggsP)
    suggs = []
    n = 0
    while n < numSuggsP.contents.value:
        suggs.append(suggs_c[n])
        n = n + 1
    if numSuggsP.contents.value > 0:
        dict_free_string_list(dict,suggs_c)
    return suggs

dict_add1 = e.enchant_dict_add
dict_add1.argtypes = [t_dict,c_char_p,c_size_t]
dict_add1.restype = None
def dict_add(dict,word):
    return dict_add1(dict,word,len(word))

dict_add_to_pwl1 = e.enchant_dict_add
dict_add_to_pwl1.argtypes = [t_dict,c_char_p,c_size_t]
dict_add_to_pwl1.restype = None
def dict_add_to_pwl(dict,word):
    return dict_add_to_pwl1(dict,word,len(word))

dict_add_to_session1 = e.enchant_dict_add_to_session
dict_add_to_session1.argtypes = [t_dict,c_char_p,c_size_t]
dict_add_to_session1.restype = None
def dict_add_to_session(dict,word):
    return dict_add_to_session1(dict,word,len(word))

dict_remove1 = e.enchant_dict_remove
dict_remove1.argtypes = [t_dict,c_char_p,c_size_t]
dict_remove1.restype = None
def dict_remove(dict,word):
    return dict_remove1(dict,word,len(word))

dict_remove_from_session1 = e.enchant_dict_remove_from_session
dict_remove_from_session1.argtypes = [t_dict,c_char_p,c_size_t]
dict_remove_from_session1.restype = c_int
def dict_remove_from_session(dict,word):
    return dict_remove_from_session1(dict,word,len(word))

dict_is_added1 = e.enchant_dict_is_added
dict_is_added1.argtypes = [t_dict,c_char_p,c_size_t]
dict_is_added1.restype = c_int
def dict_is_added(dict,word):
    return dict_is_added1(dict,word,len(word))

dict_is_removed1 = e.enchant_dict_is_removed
dict_is_removed1.argtypes = [t_dict,c_char_p,c_size_t]
dict_is_removed1.restype = c_int
def dict_is_removed(dict,word):
    return dict_is_removed1(dict,word,len(word))

dict_is_in_session1 = e.enchant_dict_is_in_session
dict_is_in_session1.argtypes = [t_dict,c_char_p,c_size_t]
dict_is_in_session1.restype = c_int
def dict_is_in_session(dict,word):
    return dict_is_in_session1(dict,word,len(word))

dict_store_replacement1 = e.enchant_dict_store_replacement
dict_store_replacement1.argtypes = [t_dict,c_char_p,c_size_t,c_char_p,c_size_t]
dict_store_replacement1.restype = None
def dict_store_replacement(dict,mis,cor):
    return dict_store_replacement1(dict,mis,len(mis),cor,len(cor))

dict_free_string_list = e.enchant_dict_free_string_list
dict_free_string_list.argtypes = [t_dict,POINTER(c_char_p)]
dict_free_string_list.restype = None

dict_get_error = e.enchant_dict_get_error
dict_get_error.argtypes = [t_dict]
dict_get_error.restype = c_char_p

dict_describe1 = e.enchant_dict_describe
dict_describe1.argtypes = [t_dict,t_dict_desc_func,c_void_p]
dict_describe1.restype = None
def dict_describe(dict,cbfunc):
    def cbfunc1(*args):
        cbfunc(*args[:-1])
    dict_describe1(dict,t_dict_desc_func(cbfunc1),None)

