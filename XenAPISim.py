#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, Bojan Vitnik <bvitnik@mainstream.rs>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import print_function

import uuid, threading, time
from datetime import datetime, timedelta
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
            self.rw_fields = []

        def _check_obj_ref(self, obj_ref):
            """Checks if object reference is valid/exists.

            Args:
                obj_ref (str): XenAPI object reference to check.

            Raises:
                xenapi.xapi_exception: If object reference is invalid.
            """
            if not obj_ref in self.objs:
                raise xenapi.xapi_exception(['HANDLE_INVALID', self.__class__.__name__, obj_ref])

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
            def getter(obj_ref):
                """Generic XenAPI object getter method.

                Args:
                    obj_ref (str): XenAPI object reference to call getter
                        method on.

                Returns:
                    varying type: XenAPI object field value.

                Raises:
                    xenapi.xapi_exception: If unknown field is referenced i.e.
                    non existant getter method is called.
                """
                self._check_obj_ref(obj_ref)

                # Strip "get_" from method name to extract field name.
                field_name = method_name[4:]

                obj = self.objs[obj_ref]

                if field_name in obj:
                    return self.objs[obj_ref][field_name]
                else:
                    raise xenapi.xapi_exception(['MESSAGE_METHOD_UNKNOWN', "%s.%s" % (self.__class__.__name__, method_name)])

            def setter(obj_ref, value):
                """Generic XenAPI object setter method.

                Args:
                    obj_ref (str): XenAPI object reference to call setter
                        method on.
                    value(varying type): Value of XenAPI object field to set to.

                Raises:
                    xenapi.xapi_exception: If field is read only, if unknown
                    field is referenced i.e. nonexistant setter method is called
                    or value type differs from field type.
                """
                self._check_obj_ref(obj_ref)

                # Strip "set_" from method name to extract field name.
                field_name = method_name[4:]

                obj = self.objs[obj_ref]

                if field_name in self.rw_fields and field_name in obj:
                    if type(self.objs[obj_ref][field_name]) == type(value):
                        self.objs[obj_ref][field_name] = value
                    else:
                        raise xenapi.xapi_exception(['FIELD_TYPE_ERROR', 'value'])
                else:
                    raise xenapi.xapi_exception(['MESSAGE_METHOD_UNKNOWN', "%s.%s" % (self.__class__.__name__, method_name)])

            if method_name.startswith("get_"):
                return getter
            elif method_name.startswith("set_"):
                return setter
            else:
                raise xenapi.xapi_exception(['MESSAGE_METHOD_UNKNOWN', "%s.%s" % (self.__class__.__name__, method_name)])

        def get_all(self):
            """Gets all object references of the class.

            This method is not present in all XenAPI classes. It is implemented
            here in all classes for easier testing.

            Returns:
                list: List of all object references of given XenAPI class.
            """
            return self.objs.keys()

        def echo(self, string):
            """Echoes string back. Used for testing purposes.

            Args:
                string (str): String to echo back.
            """
            return string


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

            self.rw_fields.extend(["other_config"])

        def login_with_password(self, user_name, user_pwd, version="1.0", originator=""):
            # Authenticate user.
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

        def expire_old_sessions(self):
            """Expires sessions older than 24h."""
            for session_ref in self.objs.keys():
                session_last_active = self.objs[session_ref].get('last_active')

                if session_last_active and isinstance(session_last_active, datetime):
                    session_time_active = datetime.now() - session_last_active

                    if session_time_active.days >= 1:
                        del self.objs[session_ref]

        def update_last_active(self, session_ref):
            """Updates last_active field of session to current time.

            Args:
                session_ref (str): Session reference.
            """
            current_session = self.objs.get(session_ref)

            if current_session:
                current_session["last_active"] = datetime.utcnow()


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

            Calls xenapi.sessions.expire_old_sessions() every 5 minutes to
            expire old sessions.
            """
            while True:
                if self.sessions:
                    self.sessions.expire_old_sessions()

                time.sleep(300)


    def __init__(self):
        """Inits all XenAPI classes."""

        # Set our root user password.
        self.root_pwd = "xenserver"

        # Generate this host reference.
        self.this_host = "OpaqueRef:%s" % str(uuid.uuid4())

        # Create all our objects that represent XenAPI classes.
        self.classes = {
            "session": self.session(self.root_pwd, self.this_host)
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
            if method_name_split[1] == "get_all" or not method_name_split[1].startswith("get_") and not method_name_split[1].startswith("set_"):
                method_argcount -= 1

            # All methods except login methods have implicit session ref
            # parameter so real number of parameters is one less.
            if not method_name_split[1].startswith("login_") and not method_name_split[1].startswith("slave_local_login_"):
                method_paramcount -= 1

            # If number of method arguments and parameters differ, raise
            # XenAPI exception with appropriate error message.
            if method_argcount != method_paramcount:
                raise xenapi.xapi_exception(['MESSAGE_PARAMETER_COUNT_MISMATCH', str(method_argcount), str(method_paramcount)])

            # Check if session is valid and strip session reference from params.
            if not method_name_split[1].startswith("login_") and not method_name_split[1].startswith("slave_local_login_"):
                if len(params) > 0 and not params[0] in self.classes["session"].objs:
                    raise xenapi.xapi_exception(['SESSION_INVALID', params[0]])

                self.classes["session"].update_last_active(params[0])
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
