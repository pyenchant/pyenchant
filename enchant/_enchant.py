
from ctypes import *

e = CDLL("libenchant.so")

t_broker = c_void_p
t_dict = c_void_p

t_broker_desc_func = CFUNCTYPE(None,c_char_p,c_char_p,c_char_p,c_void_p)
t_dict_desc_func = CFUNCTYPE(None,c_char_p,c_char_p,c_char_p,c_char_p,c_void_p)

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

dict_check = e.enchant_dict_check
dict_check.argtypes = [t_dict,c_char_p,c_size_t]
dict_check.restype = c_int

dict_suggest1 = e.enchant_dict_suggest
dict_suggest1.argtypes = [t_dict,c_char_p,c_size_t,POINTER(c_size_t)]
dict_suggest1.restype = POINTER(c_char_p)
def dict_suggest(dict,word,size):
    numSuggsP = pointer(c_size_t(0))
    suggs_c = dict_suggest1(dict,word,size,numSuggsP)
    suggs = []
    n = 0
    while n < numSuggsP.contents.value:
        suggs.append(suggs_c[n])
        n = n + 1
    dict_free_string_list(dict,suggs_c)
    return suggs

dict_add = e.enchant_dict_add
dict_add.argtypes = [t_dict,c_char_p,c_size_t]
dict_add.restype = None

dict_add_to_pwl = e.enchant_dict_add
dict_add_to_pwl.argtypes = [t_dict,c_char_p,c_size_t]
dict_add_to_pwl.restype = None

dict_add_to_session = e.enchant_dict_add_to_session
dict_add_to_session.argtypes = [t_dict,c_char_p,c_size_t]
dict_add_to_session.restype = None

dict_remove = e.enchant_dict_remove
dict_remove.argtypes = [t_dict,c_char_p,c_size_t]
dict_remove.restype = None

dict_remove_from_session = e.enchant_dict_remove_from_session
dict_remove_from_session.argtypes = [t_dict,c_char_p,c_size_t]
dict_remove_from_session.restype = c_int

dict_is_added = e.enchant_dict_is_added
dict_is_added.argtypes = [t_dict,c_char_p,c_size_t]
dict_is_added.restype = c_int

dict_is_removed = e.enchant_dict_is_removed
dict_is_removed.argtypes = [t_dict,c_char_p,c_size_t]
dict_is_removed.restype = c_int

dict_is_in_session = e.enchant_dict_is_in_session
dict_is_in_session.argtypes = [t_dict,c_char_p,c_size_t]
dict_is_in_session.restype = c_int

dict_store_replacement = e.enchant_dict_store_replacement
dict_store_replacement.argtypes = [t_dict,c_char_p,c_size_t,c_char_p,c_size_t]
dict_store_replacement.restype = None

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

broker_list_dicts1 = e.enchant_broker_list_dicts
broker_list_dicts1.argtypes = [t_broker,t_dict_desc_func,c_void_p]
broker_list_dicts1.restype = None
def broker_list_dicts(broker,cbfunc):
    def cbfunc1(*args):
        cbfunc(*args[:-1])
    broker_list_dicts1(broker,t_dict_desc_func(cbfunc1),None)

