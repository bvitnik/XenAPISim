#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, Bojan Vitnik <bvitnik@mainstream.rs>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import print_function

import uuid, threading, time
from datetime import datetime, timedelta
from six import string_types
from six.moves.xmlrpc_server import SimpleXMLRPCServer


bind_address = "localhost"
bind_port = 8080


class xenapi(object):
    """Class holding XenAPI classes.

    Attributes:
    """

    class xapi_object(object):
        """Base class for all XenAPI classes.

        Attributes:
            objs (dict): Dictionary of all XenAPI objects of particular class.
                Each key is an object reference (OpaqueRef).
            rw_fields (list of str): List of object field names that can be
                rewritten at runtime (have a setter method).
        """

        def __init__(self):
            """Inits common XenAPI class atributes."""
            self.objs = {}
            self.field_def = {}
            self.rw_fields = []
            self.list_fields = []
            self.map_fields = []

        def __getattr__(self, method_name):
            """Returns generic getters and setters for XenAPI class fields.

            Args:
                method_name (str): Name of the called method.

            Return:
                function: Reference to a function implementing called getter or
                setter method.

            Raises:
                xenapi.xapi_exception: If unknown method is called.
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
                    xenapi.xapi_exception: If value type differs from field
                    type.
                """
                self._check_obj_ref_type(obj_ref)

                field_name = method_name[4:]

                if type(self.field_def[field_name]) != type(value):
                    raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'value'])

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
                    raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'value'])

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
                    raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'value'])

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
                    xenapi.xapi_exception: If key or value is not string or if
                    key already exists in map type field.
                """
                self._check_obj_ref_type(obj_ref)

                field_name = method_name[7:]

                if not isinstance(key, string_types):
                    raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'key'])

                if not isinstance(value, string_types):
                    raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'value'])

                self._check_obj_ref(obj_ref)

                obj = self.objs[obj_ref]

                if key in obj[field_name]:
                    raise xenapi.xapi_exception(['MAP_DUPLICATE_KEY', self.__class__.__name__, field_name, obj_ref, key])

                obj[field_name][key] = value

            def remove_from(obj_ref, key):
                """Generic XenAPI object map field remover method.

                Removes key and associated value from map type fields.

                Args:
                    key (str): Key to remove.

                Raises:
                    xenapi.xapi_exception: If key or value is not string.
                """
                self._check_obj_ref_type(obj_ref)

                field_name = method_name[12:]

                if not isinstance(key, string_types):
                    raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'key'])

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
            else:
                raise xenapi.xapi_exception(['MESSAGE_METHOD_UNKNOWN', "%s.%s" % (self.__class__.__name__, method_name)])

        #
        # Common utility methods
        #

        def _check_obj_ref_type(self, obj_ref):
            """Checks if object reference is of string type.

            Args:
                obj_ref (str): XenAPI object reference to check.

            Raises:
                xenapi.xapi_exception: If object reference is not valid type.
            """
            if not isinstance(obj_ref, string_types):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', self.__class__.__name__])

        def _check_obj_ref(self, obj_ref):
            """Checks if object reference is valid/exists.

            Args:
                obj_ref (str): XenAPI object reference to check.

            Raises:
                xenapi.xapi_exception: If object reference is invalid.
            """
            if not obj_ref in self.objs:
                raise xenapi.xapi_exception(['HANDLE_INVALID', self.__class__.__name__, obj_ref])

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
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'label'])

            obj_refs_found = []

            for obj_ref in self.objs:
                if self.objs[obj_ref]['name_label'] == label:
                    obj_refs_found.append(obj_ref)
                    break

            return obj_refs_found

        def get_by_uuid(self, uuid):
            if not isinstance(uuid, string_types):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'uuid'])

            obj_ref_found = None

            for obj_ref in self.objs:
                if self.objs[obj_ref]['uuid'] == uuid:
                    obj_ref_found = obj_ref
                    break

            if obj_ref_found is not None:
                return obj_ref_found
            else:
                raise xenapi.xapi_exception(['UUID_INVALID', self.__class__.__name__, uuid])

        def get_record(self, obj_ref):
            self._check_obj_ref_type(obj_ref)
            self._check_obj_ref(obj_ref)

            return self.objs[obj_ref]


    class session(xapi_object):
        """XenAPI session class.

        Attributes:
            root_pwd (str): XenAPI root user password in plain text.
            this_host (str): This host reference.
        """

        def __init__(self, root_pwd, this_host):
            """Inits session class.

            Args:
                root_pwd (str): XenAPI root user password in plain text.
                this_host (str): This host reference.
            """
            super(xenapi.session, self).__init__()

            self.root_pwd = root_pwd
            self.this_host = this_host

            self.field_def.update({
                "auth_user_name": "",
                "auth_user_sid": "",
                "is_local_superuser": False,
                "last_active": datetime.now(),
                "originator": "",
                "other_config": {},
                "parent": "OpaqueRef:NULL",
                "pool": False,
                "rbac_permissions": [],
                "subject": "OpaqueRef:NULL",
                "tasks": [],
                "this_host": "OpaqueRef:NULL",
                "this_user": "OpaqueRef:NULL",
                "uuid": "",
                "validation_time": datetime.now(),
            })

            self.rw_fields.extend([
                "other_config"
            ])

            self.map_fields.extend([
                "other_config"
            ])

        #
        # Utility methods
        #

        def _expire_old_sessions(self):
            """Expires sessions older than 24h."""
            for session_ref in self.objs.keys():
                session_last_active = self.objs[session_ref].get('last_active')

                if session_last_active and isinstance(session_last_active, datetime):
                    session_time_active = datetime.now() - session_last_active

                    if session_time_active.days >= 1:
                        del self.objs[session_ref]

        def _update_last_active(self, session_ref):
            """Updates last_active field of session to current time.

            Args:
                session_ref (str): Session reference.
            """
            current_session = self.objs.get(session_ref)

            if current_session:
                current_session["last_active"] = datetime.utcnow()

        #
        # XenAPI methods
        #

        def change_password(self, old_pwd, new_pwd):
            # old_pwd is just ignored because root account is always used.

            if not isinstance(old_pwd, string_types):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'old_pwd'])

            if not isinstance(new_pwd, string_types):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'new_pwd'])

            if not new_pwd:
                raise xenapi.xapi_exception(['CHANGE_PASSWORD_REJECTED', 'Authentication information cannot be recovered'])

            self.root_pwd = new_pwd

        def create_from_db_file(self, filename):
            # I don't really know what this method does. It's not well
            # documentented. I implemented this as a stub that returns first
            # session found.
            if not isinstance(filename, string_types):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'filename'])

            if self.objs:
                return self.objs.keys()[0]

        def get_all_subject_identifiers(self):
            # We don't support external authentication so we just return an
            # empty string here.
            return []

        def local_logout(self, session_ref):
            # We just pass this to session.logout().
            self.logout(session_ref)

        def login_with_password(self, user_name, user_pwd, version="1.0", originator=""):
            if not isinstance(user_name, string_types):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'uname'])

            if not isinstance(user_pwd, string_types):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'pwd'])

            if not isinstance(version, string_types):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'version'])

            if not isinstance(originator, string_types):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'originator'])

            # Check user name and password.
            if user_name != "root" or user_pwd != self.root_pwd:
                raise xenapi.xapi_exception(['SESSION_AUTHENTICATION_FAILED'])

            current_time = datetime.utcnow()

            # We passed authentication so we can now create new session object.
            session_new = {
                "auth_user_name": "root",
                "auth_user_sid": "",
                "is_local_superuser": True,
                "last_active": current_time,
                "originator": originator,
                "other_config": {},
                "parent": "OpaqueRef:NULL",
                "pool": False,
                "rbac_permissions": [],
                "subject": "OpaqueRef:NULL",
                "tasks": [],
                "this_host": self.this_host,
                "this_user": "OpaqueRef:NULL",
                "uuid": str(uuid.uuid4()),
                "validation_time": current_time
            }

            session_ref = "OpaqueRef:%s" % str(uuid.uuid4())

            self.objs[session_ref] = session_new

            return session_ref

        def logout(self, session_ref):
            del self.objs[session_ref]

        def slave_local_login_with_password(self, user_name, user_pwd):
            # We just pass this to session.login_with_password().
            return self.login_with_password(user_name, user_pwd)


    class host(xapi_object):
        """XenAPI host class.

        Attributes:
        """

        def __init__(self, host_ref, dom0_vm_ref):
            """Inits host class.

            Args:
            """
            super(xenapi.host, self).__init__()

            self.field_def.update({
                "API_version_major": "",
                "API_version_minor": "",
                "API_version_vendor": "",
                "API_version_vendor_implementation": {},
                "PBDs": [],
                "PCIs": [],
                "PGPUs": [],
                "PIFs": [],
                "PUSBs": [],
                "address": "",
                "allowed_operations": [],
                "bios_strings": {},
                "blobs": {},
                "capabilities": [],
                "chipset_info": {},
                "control_domain": "OpaqueRef:NULL",
                "cpu_configuration": {},
                "cpu_info": {},
                "crash_dump_sr": "OpaqueRef:NULL",
                "crashdumps": [],
                "current_operations": {},
                "display": "",
                "edition": "",
                "enabled": True,
                "external_auth_configuration": {},
                "external_auth_service_name": "",
                "external_auth_type": "",
                "features": [],
                "guest_VCPUs_params": {},
                "ha_network_peers": [],
                "ha_statefiles": [],
                "host_CPUs": [],
                "hostname": "",
                "iscsi_iqn": "",
                "license_params": {},
                "license_server": {},
                "local_cache_sr": "OpaqueRef:NULL",
                "logging": {},
                "memory_overhead": "",
                "metrics": "OpaqueRef:NULL",
                "multipathing": False,
                "name_description": "",
                "name_label": "",
                "other_config": {},
                "patches": [],
                "power_on_config": {},
                "power_on_mode": "",
                "resident_VMs": [],
                "sched_policy": "",
                "software_version": {},
                "ssl_legacy": True,
                "supported_bootloaders": [],
                "suspend_image_sr": "OpaqueRef:NULL",
                "tags": [],
                "updates": [],
                "updates_requiring_reboot": [],
                "uuid": "",
                "virtual_hardware_platform_versions": [],
            })

            self.rw_fields.extend([
                "address",
                "crash_dump_sr",
                "display",
                "guest_VCPUs_params",
                "hostname",
                "license_server",
                "logging",
                "name_description",
                "name_label",
                "other_config",
                "suspend_image_sr",
                "tags",
            ])

            self.list_fields.extend([
                "tags",
            ])

            self.map_fields.extend([
                "guest_VCPUs_params",
                "license_server",
                "logging",
                "other_config",
            ])

            host_new = {
                "API_version_major": "2",
                "API_version_minor": "10",
                "API_version_vendor": "XenAPISim",
                "API_version_vendor_implementation": {},
                "PBDs": [],
                "PCIs": [],
                "PGPUs": [],
                "PIFs": [],
                "PUSBs": [],
                "address": "127.0.0.1",
                "allowed_operations": ['provision', 'vm_start', 'vm_resume', 'vm_migrate', 'evacuate'],
                "bios_strings": {},
                "blobs": {},
                "capabilities": ['xen-3.0-x86_64', 'xen-3.0-x86_32p', 'hvm-3.0-x86_32', 'hvm-3.0-x86_32p', 'hvm-3.0-x86_64', ''],
                "chipset_info": {'iommu': 'true'},
                "control_domain": dom0_vm_ref,
                "cpu_configuration": {},
                "cpu_info": {},
                "crash_dump_sr": "OpaqueRef:NULL",
                "crashdumps": [],
                "current_operations": {},
                "display": "enabled",
                "edition": "free",
                "enabled": True,
                "external_auth_configuration": {},
                "external_auth_service_name": "",
                "external_auth_type": "",
                "features": [],
                "guest_VCPUs_params": {},
                "ha_network_peers": [],
                "ha_statefiles": [],
                "host_CPUs": [],
                "hostname": "xenserver-hv-1",
                "iscsi_iqn": "",
                "license_params": {},
                "license_server": {'address': 'localhost', 'port': '27000'},
                "local_cache_sr": "OpaqueRef:NULL",
                "logging": {},
                "memory_overhead": "5249974272",
                "metrics": "OpaqueRef:NULL",
                "multipathing": False,
                "name_description": "",
                "name_label": "xenserver-hv-1",
                "other_config": {},
                "patches": [],
                "power_on_config": {},
                "power_on_mode": "",
                "resident_VMs": [],
                "sched_policy": "credit",
                "software_version": {'product_version': '7.2.0', 'product_version_text_short': '7.2', 'product_version_text': '7.2'},
                "ssl_legacy": True,
                "supported_bootloaders": ['pygrub', 'eliloader'],
                "suspend_image_sr": "OpaqueRef:NULL",
                "tags": [],
                "updates": [],
                "updates_requiring_reboot": [],
                "uuid": str(uuid.uuid4()),
                "virtual_hardware_platform_versions": ['0', '1', '2'],
            }

            self.objs[host_ref] = host_new

        #
        # XenAPI methods
        #

        def apply_edition(self, host_ref, edition, force):
            self._check_obj_ref_type(host_ref)

            if not isinstance(edition, string_types):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'edition'])

            if not isinstance(force, bool):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'force'])

            if edition.lower() not in ['free', 'enterprise-per-socket', 'enterprise-per-user', 'standard-per-socket', 'desktop', 'desktop-plus']:
                raise xenapi.xapi_exception(['INVALID_EDITION', edition.lower()])

            self._check_obj_ref(host_ref)

            self.objs[host_ref]['edition'] = edition.lower()

        def assert_can_evacuate(self, host_ref):
            self._check_obj_ref_type(host_ref)
            self._check_obj_ref(host_ref)

            host = self.objs[host_ref]

            if not "evacuate" in host['allowed_operations']:
                raise xenapi.xapi_exception(['CANNOT_EVACUATE_HOST', "Unknown error"])

        def backup_rrds(self, host_ref, delay):
            self._check_obj_ref_type(host_ref)

            if not isinstance(delay, string_types):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'delay'])

            self._check_obj_ref(host_ref)

            # do nothing

        def bugreport_upload(self, host_ref, url, options):
            self._check_obj_ref_type(host_ref)

            if not isinstance(url, string_types):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'url'])

            if not isinstance(options, dict):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'options'])

            self._check_obj_ref(host_ref)

            # do nothing

        def call_extension(self, host_ref, call):
            self._check_obj_ref_type(host_ref)

            if not isinstance(call, string_types):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'call'])

            self._check_obj_ref(host_ref)

            return ""

        def call_plugin(self, host_ref, plugin, fn, args):
            self._check_obj_ref_type(host_ref)

            if not isinstance(plugin, string_types):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'plugin'])

            if not isinstance(fn, string_types):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'fn'])

            if not isinstance(args, dict):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'args'])

            self._check_obj_ref(host_ref)

            return ""

        def compute_free_memory(self, host_ref):
            self._check_obj_ref_type(host_ref)
            self._check_obj_ref(host_ref)

            return "0"

        def compute_memory_overhead(self, host_ref):
            self._check_obj_ref_type(host_ref)
            self._check_obj_ref(host_ref)

            return "0"

        def create_new_blob(self, host_ref, name, mime_type, public):
            self._check_obj_ref_type(host_ref)

            if not isinstance(name, string_types):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'name'])

            if not isinstance(mime_type, string_types):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'mime_type'])

            if not isinstance(public, bool):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'public'])

            self._check_obj_ref(host_ref)

            return "OpaqueRef:NULL"

        def declare_dead(self, host_ref):
            self._check_obj_ref_type(host_ref)
            self._check_obj_ref(host_ref)

        def destroy(self, host_ref):
            self._check_obj_ref_type(host_ref)
            self._check_obj_ref(host_ref)

            del self.objs[host_ref]

        def disable(self, host_ref):
            self._check_obj_ref_type(host_ref)
            self._check_obj_ref(host_ref)

            self.objs[host_ref]['enabled'] = False

        def disable_display(self, host_ref):
            self._check_obj_ref_type(host_ref)
            self._check_obj_ref(host_ref)

            if self.objs[host_ref]['display'] != 'disabled':
                self.objs[host_ref]['display'] = "disable_on_reboot"

            return self.objs[host_ref]['display']

        def disable_external_auth(self, host_ref, config):
            self._check_obj_ref_type(host_ref)

            if not isinstance(config, dict):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'config'])

            self._check_obj_ref(host_ref)

            self.objs[host_ref]['external_auth_configuration'] = config
            self.objs[host_ref]['external_auth_type'] = ""

        def disable_local_storage_caching(self, host_ref):
            self._check_obj_ref_type(host_ref)
            self._check_obj_ref(host_ref)

            self.objs[host_ref]['local_cache_sr'] = "OpaqueRef:NULL"

        def dmesg(self, host_ref):
            self._check_obj_ref_type(host_ref)
            self._check_obj_ref(host_ref)

            return "dmesg is empty"

        def dmesg_clear(self, host_ref):
            self.dmesg(host_ref)

        def emergency_ha_disable(self, soft):
            if not isinstance(soft, bool):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'soft'])

            # do nothing

        def enable(self, host_ref):
            self._check_obj_ref_type(host_ref)
            self._check_obj_ref(host_ref)

            self.objs[host_ref]['enabled'] = True

        def enable_display(self, host_ref):
            self._check_obj_ref_type(host_ref)
            self._check_obj_ref(host_ref)

            if self.objs[host_ref]['display'] != 'enabled':
                self.objs[host_ref]['display'] = "enable_on_reboot"

            return self.objs[host_ref]['display']

        def enable_external_auth(self, host_ref, config, service_name, auth_type):
            self._check_obj_ref_type(host_ref)

            if not isinstance(config, dict):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'config'])

            if not isinstance(service_name, string_types):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'service_name'])

            if not isinstance(auth_type, string_types):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'auth_type'])

            self._check_obj_ref(host_ref)

            self.objs[host_ref]['external_auth_configuration'] = config
            self.objs[host_ref]['external_auth_service_name'] = service_name
            self.objs[host_ref]['external_auth_type'] = auth_type

        def enable_local_storage_caching(self, host_ref, sr_ref):
            self._check_obj_ref_type(host_ref)
            # SR._check_obj_ref_type(sr_ref)

            self._check_obj_ref(host_ref)
            # SR._check_obj_ref(sr_ref)

            self.objs[host_ref]['local_cache_sr'] = sr_ref

        def evacuate(self, host_ref):
            self._check_obj_ref_type(host_ref)
            self._check_obj_ref(host_ref)

            # do nothing for now

        def forget_data_source_archives(self, host_ref, data_source):
            self._check_obj_ref_type(host_ref)

            if not isinstance(data_source, string_types):
                raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'data_source'])

            self._check_obj_ref(host_ref)

            # do nothing

        def get_data_sources(self, host_ref):
            self._check_obj_ref_type(host_ref)
            self._check_obj_ref(host_ref)

            return []

        def get_log(self, host_ref):
            self._check_obj_ref_type(host_ref)
            self._check_obj_ref(host_ref)

            return ""

        def get_management_interface(self, host_ref):
            self._check_obj_ref_type(host_ref)
            self._check_obj_ref(host_ref)

            obj = self.objs[host_ref]

            if obj['PIFs']:
                return obj['PIFs'][0]

        def get_server_certificate(self, host_ref):
            self._check_obj_ref_type(host_ref)
            self._check_obj_ref(host_ref)

            return ""

        def get_server_localtime(self, host_ref):
            self._check_obj_ref_type(host_ref)
            self._check_obj_ref(host_ref)

            return datetime.now()

        def get_servertime(self, host_ref):
            self._check_obj_ref_type(host_ref)
            self._check_obj_ref(host_ref)

            return datetime.utcnow()

        def get_system_status_capabilities(self, host_ref):
            self._check_obj_ref_type(host_ref)
            self._check_obj_ref(host_ref)

            return ""

        def get_uncooperative_resident_VMs(self, host_ref):
            self._check_obj_ref_type(host_ref)
            self._check_obj_ref(host_ref)

            return []

        def get_vms_which_prevent_evacuation(self, host_ref):
            self._check_obj_ref_type(host_ref)
            self._check_obj_ref(host_ref)

            return {}


    class xapi_exception(Exception):
        """Basic class for XenAPI exception handling."""

        def __init__(self, details):
            """Inits XenAPI exception.

            Args:
                details (list): List containing XenAPI error code as first
                    element and other XenAPI error dependant info as other
                    elements.
            """
            self.details = details


    class expire_sessions_thread(threading.Thread):
        """Thread class that is used to expire old sessions.

        Attributes:
            sessions: Reference to session class.
        """

        def __init__(self, thread_name, sessions):
            """Inits session expire thread.

            Args:
                thread_name (str): Thread name.
                sessions: Reference to session class.
            """
            super(xenapi.expire_sessions_thread, self).__init__(name=thread_name)

            self.sessions = sessions

        def run(self):
            """Overriden Thread.run() method.

            Calls xenapi.sessions._expire_old_sessions() every 5 minutes to
            expire old sessions.
            """
            while True:
                if self.sessions:
                    self.sessions._expire_old_sessions()

                time.sleep(300)


    def __init__(self):
        """Inits all XenAPI classes."""

        # Set our root user password.
        root_pwd = "xenserver"

        # Generate this host reference.
        this_host = "OpaqueRef:%s" % str(uuid.uuid4())

        # Generate dom0 VM reference.
        dom0_vm_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        # Create all our objects that represent XenAPI classes.
        self.classes = {
            "session": self.session(root_pwd, this_host),
            "host": self.host(this_host, dom0_vm_ref),
        }

        # Create and run thread that expires sessions.
        self.thread_sessions_expire = xenapi.expire_sessions_thread("ExpireSessions", self.classes['session'])
        self.thread_sessions_expire.daemon = True
        self.thread_sessions_expire.start()

    def _dispatch(self, method_name, params):
        """Dispatches methods.

        Args:
            method_name (str): Name of the method to call.
            params (tuple): Parameters passed to method.

        Returns:
            dict: A dictionary with key "Status" and value either "Success" or
            "Failure" and key "Value" with returned value if "Status" is
            "Success" or key "ErrorDescription" with XenAPI error description if
            "Status" is "Failure".
        """
        try:
            # Split class name from method name.
            method_name_split = method_name.split(".")

            # Check if method and class are known.
            if len(method_name_split) != 2 or not method_name_split[0] in self.classes:
                raise xenapi.xapi_exception(['MESSAGE_METHOD_UNKNOWN', method_name])

            # Find given method. Exception will be raised if not found.
            method = getattr(self.classes[method_name_split[0]], method_name_split[1])

            # We need to test if number of method parameters matches the number
            # of method arguments and return a friendly error message if not.
            # We do this by using "co_argcount" which is a little hacky. Notify
            # me if there is a better way to do this.
            method_argcount = method.__code__.co_argcount
            method_paramcount = len(params)

            # All methods except generic getter and setter methods have implicit
            # argument 'self' so real number of arguments is one less.
            if (not method_name_split[1].startswith("get_") and
                not method_name_split[1].startswith("set_") and
                not method_name_split[1].startswith("add_") and
                not method_name_split[1].startswith("remove_") or
                method_name_split[1] in ["get_all", "get_all_records", "get_all_subject_identifiers", "get_by_name_label", "get_by_uuid", "get_record"]):
                method_argcount -= 1

            # All methods except login methods have implicit session ref
            # parameter so real number of parameters is one less.
            if (not method_name_split[1].startswith("login_") and
                    not method_name_split[1].startswith("slave_local_login_") and
                    not method_name_split[1] in ["logout", "local_logout"]):
                method_paramcount -= 1

            # If number of method arguments and parameters differ, raise
            # XenAPI exception with appropriate error message.
            if method_argcount != method_paramcount:
                raise xenapi.xapi_exception(['MESSAGE_PARAMETER_COUNT_MISMATCH', method_name, str(method_argcount), str(method_paramcount)])

            # Check if session is valid.
            if not method_name_split[1].startswith("login_") and not method_name_split[1].startswith("slave_local_login_"):
                if not isinstance(params[0], string_types):
                    raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'session_id'])

                if not params[0] in self.classes["session"].objs:
                    raise xenapi.xapi_exception(['SESSION_INVALID', params[0]])

                # Update current session last_active field.
                self.classes["session"]._update_last_active(params[0])

                # Strip session from input params if method is not
                # session.logout() of session.local_logout().
                if not method_name_split[1] in ["logout", "local_logout"]:
                    params = params[1:]

            # Call method.
            value = method(*params)

            # If method does not return value, return an empty string.
            if value is None:
                value = ""

            return {
                "Status": "Success",
                "Value": value
            }
        except xenapi.xapi_exception as e:
            return {
                "Status": "Failure",
                "ErrorDescription": e.details,
            }

# Use SimpleXMLRPCServer to serve XenAPI.
xapi_server = SimpleXMLRPCServer((bind_address, bind_port))
xapi_server.register_instance(xenapi())
xapi_server.register_introspection_functions()
xapi_server.serve_forever()
