#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, Bojan Vitnik <bvitnik@mainstream.rs>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import print_function

import uuid
from datetime import datetime

from xenapi_object import xenapi_object
from xenapi_exception import xenapi_exception


class session(xenapi_object):
    """XenAPI session class.

    Attributes:
        xenapi: Reference to xenapi object for accessing other class methods.
        root_pwd (str): XenAPI root user password in plain text.
        this_host (str): This host reference.
    """

    def __init__(self, xenapi, root_pwd, this_host):
        """Inits session class.

        Args:
            root_pwd (str): XenAPI root user password in plain text.
            this_host (str): This host reference.
        """
        super(session, self).__init__(xenapi)

        self.root_pwd = root_pwd
        self.this_host = this_host

        self.field_def.update({
            "auth_user_name": "",
            "auth_user_sid": "",
            "is_local_superuser": False,
            "last_active": datetime.now(),
            "originator": "",
            "parent": "OpaqueRef:NULL",
            "pool": False,
            "rbac_permissions": [],
            "subject": "OpaqueRef:NULL",
            "tasks": [],
            "this_host": "OpaqueRef:NULL",
            "this_user": "OpaqueRef:NULL",
            "validation_time": datetime.now(),
        })

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

        self._check_param_type(old_pwd, 'string', 'old_pwd')
        self._check_param_type(new_pwd, 'string', 'new_pwd')

        if not new_pwd:
            raise xenapi_exception(['CHANGE_PASSWORD_REJECTED', 'Authentication information cannot be recovered'])

        self.root_pwd = new_pwd

    def create_from_db_file(self, filename):
        # I don't really know what this method does. It's not well
        # documentented. I implemented this as a stub that returns first
        # session found.
        self._check_param_type(filename, 'string', 'filename')

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
        self._check_param_type(user_name, 'string', 'user_name')
        self._check_param_type(user_pwd, 'string', 'user_pwd')
        self._check_param_type(version, 'string', 'version')
        self._check_param_type(originator, 'string', 'originator')

        # Check user name and password.
        if user_name != "root" or user_pwd != self.root_pwd:
            raise xenapi_exception(['SESSION_AUTHENTICATION_FAILED'])

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
