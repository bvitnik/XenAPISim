#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, Bojan Vitnik <bvitnik@mainstream.rs>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import print_function

from six import string_types

from xenapi_exception import xenapi_exception


class xenapi_object(object):
    """Base class for all XenAPI classes.

    Attributes:
        objs (dict): Dictionary of all XenAPI objects of particular class.
            Each key is an object reference (OpaqueRef).
        rw_fields (list of str): List of object field names that can be
            rewritten at runtime (have a setter method).
    """

    def __init__(self, xenapi):
        """Inits common XenAPI class atributes."""
        self.xenapi = xenapi

        self.objs = {}

        self.field_def = {
            "other_config": {},
            "uuid": "",
        }

        self.rw_fields = [
            "other_config"
        ]

        self.list_fields = []

        self.map_fields = [
            "other_config"
        ]

        self.unimplemented_methods = []

    def __getattr__(self, method_name):
        """Returns generic getters and setters for XenAPI class fields.

        Args:
            method_name (str): Name of the called method.

        Return:
            function: Reference to a function implementing called getter or
            setter method.

        Raises:
            xenapi_exception: If unknown method is called.
        """
        def get(obj_ref):
            """Generic XenAPI object getter method.

            Args:
                obj_ref (str): XenAPI object reference to call getter
                    method on.

            Returns:
                varying type: XenAPI object field value.
            """
            self._check_obj_ref_type(obj_ref)

            field_name = method_name[4:]

            self._check_obj_ref(obj_ref)

            return self.objs[obj_ref][field_name]

        def set(obj_ref, value):
            """Generic XenAPI object setter method.

            Args:
                obj_ref (str): XenAPI object reference to call setter
                    method on.
                value (varying type): Value of XenAPI object field to
                    set to.

            Raises:
                xenapi_exception: If value type differs from field type.
            """
            self._check_obj_ref_type(obj_ref)

            field_name = method_name[4:]

            if type(self.field_def[field_name]) != type(value):
                raise xenapi_exception(['FIELD_TYPE_ERROR', 'value'])

            self._check_obj_ref(obj_ref)

            obj = self.objs[obj_ref]

            obj[field_name] = value

        def add(obj_ref, value):
            """Generic XenAPI object list field adder method.

            Adds value to list type fields.

            Args:
                value (str) Value to add.
            """
            self._check_obj_ref_type(obj_ref)

            field_name = method_name[4:]

            if not isinstance(value, string_types):
                raise xenapi_exception(['FIELD_TYPE_ERROR', 'value'])

            self._check_obj_ref(obj_ref)

            obj = self.objs[obj_ref]

            if not value in obj[field_name]:
                obj[field_name].append(value)

        def remove(obj_ref, value):
            """Generic XenAPI object list field remover method.

            Removes value from list type fields.

            Args:
                value (str) Value to remove.
            """
            self._check_obj_ref_type(obj_ref)

            field_name = method_name[7:]

            if not isinstance(value, string_types):
                raise xenapi_exception(['FIELD_TYPE_ERROR', 'value'])

            self._check_obj_ref(obj_ref)

            obj = self.objs[obj_ref]

            if value in obj[field_name]:
                obj[field_name].remove(value)

        def add_to(obj_ref, key, value):
            """Generic XenAPI object map field adder method.

            Adds key and value to map type fields.

            Args:
                key (str): Key to add.
                value (str) Value to add.

            Raises:
                xenapi_exception: If key or value is not string or if key already
                exists in map type field.
            """
            self._check_obj_ref_type(obj_ref)

            field_name = method_name[7:]

            if not isinstance(key, string_types):
                raise xenapi_exception(['FIELD_TYPE_ERROR', 'key'])

            if not isinstance(value, string_types):
                raise xenapi_exception(['FIELD_TYPE_ERROR', 'value'])

            self._check_obj_ref(obj_ref)

            obj = self.objs[obj_ref]

            if key in obj[field_name]:
                raise xenapi_exception(['MAP_DUPLICATE_KEY', self.__class__.__name__, field_name, obj_ref, key])

            obj[field_name][key] = value

        def remove_from(obj_ref, key):
            """Generic XenAPI object map field remover method.

            Removes key and associated value from map type fields.

            Args:
                key (str): Key to remove.

            Raises:
                xenapi_exception: If key or value is not string.
            """
            self._check_obj_ref_type(obj_ref)

            field_name = method_name[12:]

            if not isinstance(key, string_types):
                raise xenapi_exception(['FIELD_TYPE_ERROR', 'key'])

            self._check_obj_ref(obj_ref)

            obj = self.objs[obj_ref]

            if key in obj[field_name]:
                del obj[field_name][key]

        if method_name.startswith("get_") and method_name[4:] in self.field_def.keys():
            return get
        elif method_name.startswith("set_") and method_name[4:] in self.rw_fields:
            return set
        elif method_name.startswith("add_to_") and method_name[7:] in self.map_fields:
            return add_to
        elif method_name.startswith("remove_from_") and method_name[12:] in self.map_fields:
            return remove_from
        elif method_name.startswith("add_") and method_name[4:] in self.list_fields:
            return add
        elif method_name.startswith("remove_") and method_name[7:] in self.list_fields:
            return remove
        elif method_name in self.unimplemented_methods:
            raise xenapi_exception(['NOT_IMPLEMENTED', method_name])
        else:
            raise xenapi_exception(['MESSAGE_METHOD_UNKNOWN', "%s.%s" % (self.__class__.__name__, method_name)])

    #
    # Common utility methods
    #

    def _check_obj_ref_type(self, obj_ref):
        """Checks if object reference is of string type.

        Args:
            obj_ref (str): XenAPI object reference to check.

        Raises:
            xenapi_exception: If object reference is not valid type.
        """
        if not isinstance(obj_ref, string_types):
            raise xenapi_exception(['FIELD_TYPE_ERROR', self.__class__.__name__])

    def _check_obj_ref(self, obj_ref):
        """Checks if object reference is valid/exists.

        Args:
            obj_ref (str): XenAPI object reference to check.

        Raises:
            xenapi_exception: If object reference is invalid.
        """
        if not obj_ref in self.objs:
            raise xenapi_exception(['HANDLE_INVALID', self.__class__.__name__, obj_ref])

    def echo(self, string):
        """Echoes string back. Used for testing purposes.

        Args:
            string (str): String to echo back.
        """
        return string

    #
    # Common XenAPI methods
    #

    def get_all(self):
        """
        This method is not present in all XenAPI classes. It is implemented
        here in all classes for easier testing.
        """
        return self.objs.keys()

    def get_all_records(self):
        """
        This method is not present in all XenAPI classes. It is implemented
        here in all classes for easier testing.
        """
        return self.objs

    def get_by_name_label(self, label):
        if not isinstance(label, string_types):
            raise xenapi_exception(['FIELD_TYPE_ERROR', 'label'])

        obj_refs_found = []

        for obj_ref in self.objs:
            if self.objs[obj_ref]['name_label'] == label:
                obj_refs_found.append(obj_ref)
                break

        return obj_refs_found

    def get_by_uuid(self, uuid):
        if not isinstance(uuid, string_types):
            raise xenapi_exception(['FIELD_TYPE_ERROR', 'uuid'])

        obj_ref_found = None

        for obj_ref in self.objs:
            if self.objs[obj_ref]['uuid'] == uuid:
                obj_ref_found = obj_ref
                break

        if obj_ref_found is not None:
            return obj_ref_found
        else:
            raise xenapi_exception(['UUID_INVALID', self.__class__.__name__, uuid])

    def get_record(self, obj_ref):
        self._check_obj_ref_type(obj_ref)
        self._check_obj_ref(obj_ref)

        return self.objs[obj_ref]
