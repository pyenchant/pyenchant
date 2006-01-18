/* pyenchant
 *
 * Copyright (C) 2004-2005 Ryan Kelly
 *
 * This code is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This code is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this code; if not, write to the
 * Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 *
 * In addition, as a special exception, you are
 * given permission to link the code of this program with
 * non-LGPL Spelling Provider libraries (eg: a MSFT Office
 * spell checker backend) and distribute linked combinations including
 * the two.  You must obey the GNU Lesser General Public License in all
 * respects for all of the code used other than said providers.  If you modify
 * this file, you may extend this exception to your version of the
 * file, but you are not obligated to do so.  If you do not wish to
 * do so, delete this exception statement from your version.
 *
 */


/*  NOTE:  SWIG must be used with the -noproxy option to get the
           desired result.
*/

/*  Straightforward import of enchant API  */
%module _enchant
%{
#include "enchant.h"
%}

typedef unsigned long size_t;
typedef unsigned long ssize_t;

%include "enchant.h"


/*  Add wrapper functions to perform some Python/C API transformations  */


/*  Allow proper passing of python callable objects as callbacks  */
%typemap(python,in) PyObject *py_callback {
    if(!PyCallable_Check($input)) {
        PyErr_SetString(PyExc_TypeError,"Callable object required.");
        return NULL;
    }
    $1 = $input;
}

%inline %{

    /*  Wrap enchant_dict_suggest to return a PyList of PyStrings  */
    PyObject* enchant_dict_suggest_py(EnchantDict *dict,const char * const word,
                                   size_t len)
    {
        size_t n_suggs;
        char** suggs;
        PyObject *suggs_list, *tmp_str;
        int i;
        suggs = enchant_dict_suggest(dict,word,len,&n_suggs);
        if(suggs == NULL) { n_suggs = 0; }
        suggs_list = PyList_New(n_suggs);
        if(suggs_list == NULL) { return NULL; }
        for(i = 0;i < n_suggs;i++) {
            tmp_str = PyString_FromString(suggs[i]);
            if(tmp_str == NULL) { return NULL; }
            PyList_SetItem(suggs_list,i,tmp_str);
        }
        if(suggs != NULL) {
            enchant_dict_free_string_list(dict,suggs);
        }
        return suggs_list;
    }


    /*  Allow Python callables to be used in encant_dict_describe  */
    /*  The user_data pointer is used to pass the PyObject         */
    void enchant_dict_describe_pycb(const char * const lang_tag,
                                    const char * const provider_name,
                                    const char * const provider_desc,
                                    const char * const provider_file,
                                    void *user_data)
    {
        PyObject *func, *args;
        PyObject *result;

        func = (PyObject*) user_data;
        args = Py_BuildValue("(ssss)",lang_tag,provider_name,
                                      provider_desc,provider_file);

        result = PyEval_CallObject(func,args);
        Py_DECREF(args);
        Py_XDECREF(result);
    }

    /*  Wrap enchant_dict_describe to take Python callables  */
    void enchant_dict_describe_py(EnchantDict *dict,PyObject *py_callback)
    {
        enchant_dict_describe(dict,enchant_dict_describe_pycb,
                              (void*)py_callback);
    }

    /*  Wrap enchant_broker_list_dicts to take Python callables  */
    void enchant_broker_list_dicts_py(EnchantBroker *broker,PyObject *py_callback)
    {
        enchant_broker_list_dicts(broker,enchant_dict_describe_pycb,
                                  (void*)py_callback);
    }

    /*  Allow Python callables to be used in encant_broker_describe  */
    /*  The user_data pointer is used to pass the PyObject           */
    void enchant_broker_describe_pycb(const char * const provider_name,
                                      const char * const provider_desc,
                                      const char * const provider_file,
                                      void *user_data)
    {
        PyObject *func, *args;
        PyObject *result;

        func = (PyObject*) user_data;
        args = Py_BuildValue("(sss)",provider_name,provider_desc,provider_file);

        result = PyEval_CallObject(func,args);
        Py_DECREF(args);
        Py_XDECREF(result);
    }

    /*  Wrap enchant_broker_describe to take Python callables  */
    void enchant_broker_describe_py(EnchantBroker *broker,PyObject *py_callback)
    {
        enchant_broker_describe(broker,enchant_broker_describe_pycb,
                                (void*)py_callback);
    }

%}

