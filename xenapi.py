#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, Bojan Vitnik <bvitnik@mainstream.rs>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import print_function

import uuid
from six import string_types

from session import session
from host import host
from host_cpu import host_cpu
from host_metrics import host_metrics
from pool import pool
from network import network
from PBD import PBD
from PIF import PIF
from PIF_metrics import PIF_metrics
from Bond import Bond
from PCI import PCI
from SR import SR
from task import task
from VBD import VBD
from VBD_metrics import VBD_metrics
from VDI import VDI
from VIF import VIF
from VIF_metrics import VIF_metrics
from VLAN import VLAN
from VM import VM
from VM_appliance import VM_appliance
from VM_guest_metrics import VM_guest_metrics
from VM_metrics import VM_metrics

import xenapi_threads

from xenapi_exception import xenapi_exception


class xenapi(object):
    """Class holding XenAPI classes.

    Attributes:
    """

    def __init__(self):
        """Inits all XenAPI classes."""

        # Set our root user password.
        root_pwd = "xenserver"

        # Generate this host reference.
        this_host = "OpaqueRef:%s" % str(uuid.uuid4())

        # Generate dom0 VM reference.
        dom0_vm_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        # Create all our objects that represent XenAPI classes.
        self.session = session(self, root_pwd, this_host)
        self.host = host(self, this_host, dom0_vm_ref)
        self.host_cpu = host_cpu(self, this_host)
        self.host_metrics = host_metrics(self)
        self.pool = pool(self, this_host)
        self.network = network(self)
        self.PBD = PBD(self, this_host)
        self.PIF = PIF(self, this_host)
        self.PIF_metrics = PIF_metrics(self)
        self.Bond = Bond(self)
        self.PCI = PCI(self, this_host)
        self.SR = SR(self)
        self.task = task(self)
        self.VBD = VBD(self)
        self.VBD_metrics = VBD_metrics(self)
        self.VDI = VDI(self)
        self.VIF = VIF(self)
        self.VIF_metrics = VIF_metrics(self)
        self.VLAN = VLAN(self)
        self.VM = VM(self)
        self.VM_appliance = VM_appliance(self)
        self.VM_guest_metrics = VM_guest_metrics(self)
        self.VM_metrics = VM_metrics(self)

        # Map all XenAPI classes.
        self.classes = {
            "session": self.session,
            "host": self.host,
            "host_cpu": self.host_cpu,
            "host_metrics": self.host_metrics,
            "pool": self.pool,
            "network": self.network,
            "PBD": self.PBD,
            "PIF": self.PIF,
            "PIF_metrics": self.PIF_metrics,
            "Bond": self.Bond,
            "PCI": self.PCI,
            "SR": self.SR,
            "task": self.task,
            "VBD": self.VBD,
            "VBD_metrics": self.VBD_metrics,
            "VDI": self.VDI,
            "VIF": self.VIF,
            "VIF_metrics": self.VIF_metrics,
            "VLAN": self.VLAN,
            "VM": self.VM,
            "VM_appliance": self.VM_appliance,
            "VM_guest_metrics": self.VM_guest_metrics,
            "VM_metrics": self.VM_metrics,
        }

        # Create and run thread that expires sessions.
        self.thread_sessions_expire = xenapi_threads.expire_sessions_thread("ExpireSessions", self)
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
                raise xenapi_exception(['MESSAGE_METHOD_UNKNOWN', method_name])

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
            try:
                # __getattribute__() will only find "real" methods. Generic
                # methods generated by __getattr__() will not be found.
                self.classes[method_name_split[0]].__getattribute__(method_name_split[1])
                method_argcount -= 1
            except AttributeError:
                pass

            # All methods except login methods have implicit session ref
            # parameter so real number of parameters is one less.
            if (not method_name_split[1].startswith("login_") and
                    not method_name_split[1].startswith("slave_local_login_") and
                    not method_name_split[1] in ["logout", "local_logout"]):
                method_paramcount -= 1

            # If number of method arguments and parameters differ, raise
            # XenAPI exception with appropriate error message.
            if method_argcount != method_paramcount:
                raise xenapi_exception(['MESSAGE_PARAMETER_COUNT_MISMATCH', method_name, str(method_argcount), str(method_paramcount)])

            # Check if session is valid.
            if not method_name_split[1].startswith("login_") and not method_name_split[1].startswith("slave_local_login_"):
                if not isinstance(params[0], string_types):
                    raise xenapi_exception(['FIELD_TYPE_ERROR', 'session_id'])

                if not params[0] in self.session.objs:
                    raise xenapi_exception(['SESSION_INVALID', params[0]])

                # Update current session last_active field.
                self.session._update_last_active(params[0])

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
        except xenapi_exception as e:
            return {
                "Status": "Failure",
                "ErrorDescription": e.details,
            }
