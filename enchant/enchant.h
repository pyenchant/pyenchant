/* vim: set sw=8: -*- Mode: C; tab-width: 8; indent-tabs-mode: t; c-basic-offset: 8 -*- */
/* enchant
 * Copyright (C) 2003 Dom Lachowicz
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the
 * Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 *
 * In addition, as a special exception, Dom Lachowicz
 * gives permission to link the code of this program with
 * non-LGPL Spelling Provider libraries (eg: a MSFT Office
 * spell checker backend) and distribute linked combinations including
 * the two.  You must obey the GNU Lesser General Public License in all
 * respects for all of the code used other than said providers.  If you modify
 * this file, you may extend this exception to your version of the
 * file, but you are not obligated to do so.  If you do not wish to
 * do so, delete this exception statement from your version.
 */

#ifndef ENCHANT_H
#define ENCHANT_H

/* for size_t, ssize_t */
#include <sys/types.h>

#ifdef __cplusplus
extern "C" {
#endif

#ifdef _WIN32
#ifdef _ENCHANT_BUILD
#define ENCHANT_MODULE_EXPORT(x) __declspec(dllexport) x
#else
#define ENCHANT_MODULE_EXPORT(x) __declspec(dllimport) x
#endif
#else
#define ENCHANT_MODULE_EXPORT(x) x
#endif

typedef struct str_enchant_broker EnchantBroker;
typedef struct str_enchant_dict   EnchantDict;

ENCHANT_MODULE_EXPORT (EnchantBroker *) 
     enchant_broker_init (void);
ENCHANT_MODULE_EXPORT (void)
     enchant_broker_free (EnchantBroker * broker);

ENCHANT_MODULE_EXPORT (EnchantDict *)
     enchant_broker_request_dict (EnchantBroker * broker, const char *const tag);
ENCHANT_MODULE_EXPORT (EnchantDict *)
     enchant_broker_request_pwl_dict (EnchantBroker * broker, const char *const pwl);
ENCHANT_MODULE_EXPORT (void)
     enchant_broker_free_dict (EnchantBroker * broker, EnchantDict * dict);
ENCHANT_MODULE_EXPORT (int)
     enchant_broker_dict_exists (EnchantBroker * broker,
				 const char * const tag);
ENCHANT_MODULE_EXPORT (void)
     enchant_broker_set_ordering (EnchantBroker * broker,
				  const char * const tag,
				  const char * const ordering);
/* const */
ENCHANT_MODULE_EXPORT(char *)
     enchant_broker_get_error (EnchantBroker * broker);

/**
 * EnchantBrokerDescribeFn
 * @provider_name: The provider's identifier, such as "ispell" or "aspell" in UTF8 encoding
 * @provider_desc: A description of the provider, such as "Aspell 0.53" in UTF8 encoding
 * @provider_dll_file: The provider's DLL filename in Glib file encoding (UTF8 on Windows)
 * @user_data: Supplied user data, or %null if you don't care
 *
 * Callback used to enumerate and describe Enchant's various providers
 */
typedef void (*EnchantBrokerDescribeFn) (const char * const provider_name,
					 const char * const provider_desc,
					 const char * const provider_dll_file,
					 void * user_data);
	
ENCHANT_MODULE_EXPORT (void)
     enchant_broker_describe (EnchantBroker * broker,
			      EnchantBrokerDescribeFn fn,
			      void * user_data);

ENCHANT_MODULE_EXPORT (int)
     enchant_dict_check (EnchantDict * dict, const char *const word, ssize_t len);
ENCHANT_MODULE_EXPORT (char **)
     enchant_dict_suggest (EnchantDict * dict, const char *const word,
			   ssize_t len, size_t * out_n_suggs);
ENCHANT_MODULE_EXPORT (void)
     enchant_dict_add (EnchantDict * dict, const char *const word,
			      ssize_t len);
ENCHANT_MODULE_EXPORT (void)
     enchant_dict_add_to_session (EnchantDict * dict, const char *const word,
				  ssize_t len);
ENCHANT_MODULE_EXPORT (void)
     enchant_dict_remove (EnchantDict * dict, const char *const word,
			      ssize_t len);
ENCHANT_MODULE_EXPORT (void)
     enchant_dict_remove_from_session (EnchantDict * dict, const char *const word,
				  ssize_t len);
ENCHANT_MODULE_EXPORT (int)
     enchant_dict_is_added (EnchantDict * dict, const char *const word,
				 ssize_t len);
ENCHANT_MODULE_EXPORT (int)
     enchant_dict_is_removed (EnchantDict * dict, const char *const word,
				 ssize_t len);
ENCHANT_MODULE_EXPORT (void)
     enchant_dict_store_replacement (EnchantDict * dict,
				     const char *const mis, ssize_t mis_len,
				     const char *const cor, ssize_t cor_len);
ENCHANT_MODULE_EXPORT (void)
	     enchant_dict_free_string_list (EnchantDict * dict, char **string_list);

#ifndef ENCHANT_DISABLE_DEPRECATED
ENCHANT_MODULE_EXPORT (void)
     enchant_dict_free_suggestions (EnchantDict * dict, char **suggestions);
ENCHANT_MODULE_EXPORT (void)
     enchant_dict_add_to_personal (EnchantDict * dict, const char *const word,
				   ssize_t len);
ENCHANT_MODULE_EXPORT (void)
     enchant_dict_add_to_pwl (EnchantDict * dict, const char *const word,
			      ssize_t len);
ENCHANT_MODULE_EXPORT (int)
     enchant_dict_is_in_session (EnchantDict * dict, const char *const word,
				 ssize_t len);
#endif /* ENCHANT_DISABLE_DEPRECATED */

/* const */
ENCHANT_MODULE_EXPORT(char *)
     enchant_dict_get_error (EnchantDict * dict);

/**
 * EnchantDictDescribeFn
 * @lang_tag: The dictionary's language tag (eg: en_US, de_AT, ...)
 * @provider_name: The provider's name (eg: Aspell) in UTF8 encoding
 * @provider_desc: The provider's description (eg: Aspell 0.50.3) in UTF8 encoding
 * @provider_file: The DLL/SO where this dict's provider was loaded from in Glib file encoding (UTF8 on Windows)
 * @user_data: Supplied user data, or %null if you don't care
 *
 * Callback used to describe an individual dictionary
 */
typedef void (*EnchantDictDescribeFn) (const char * const lang_tag,
				       const char * const provider_name,
				       const char * const provider_desc,
				       const char * const provider_file,
				       void * user_data);

ENCHANT_MODULE_EXPORT (void)
     enchant_dict_describe (EnchantDict * dict,
			    EnchantDictDescribeFn fn,
			    void * user_data);

ENCHANT_MODULE_EXPORT (void)
     enchant_broker_list_dicts (EnchantBroker * broker,
				EnchantDictDescribeFn fn,
				void * user_data);

#ifdef __cplusplus
}
#endif

#endif /* ENCHANT_H */
