#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, Bojan Vitnik <bvitnik@mainstream.rs>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import print_function

import uuid

from xenapi_object import xenapi_object
from xenapi_exception import xenapi_exception


class VM_appliance(xenapi_object):
    """XenAPI VM_appliance class.

    Attributes:
    """

    def __init__(self, xenapi):
        """Inits VM_appliance class.

        Args:
        """
        super(VM_appliance, self).__init__(xenapi)

        self.field_def.update({
            "VMs": [],
            "allowed_operations": [],
            "current_operations": {},
            "name_description": "",
            "name_label": "",
        })

        self.unimplemented_methods.extend([
            "assert_can_be_recovered",
            "get_SRs_required_for_recovery",
            "recover",
        ])

        VM_appliance_new = {
            "VMs": [],
            "allowed_operations": [
                "start",
                "clean_shutdown",
                "hard_shutdown",
                "shutdown",
            ],
            "current_operations": {},
            "name_description": "",
            "name_label": "VM-App-1",
            "uuid": str(uuid.uuid4()),
        }

        VM_appliance_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[VM_appliance_ref] = VM_appliance_new

    def clean_shutdown(self, VM_appliance_ref):
        self._check_param_type(VM_appliance_ref, 'ref')
        self._check_obj_ref(VM_appliance_ref)

        for VM_ref in self.objs[VM_appliance_ref]['VMs']:
            self.xenapi.VM.clean_shutdown(VM_ref)

    def create(self, args):
        self._check_param_type(args, 'struct')

        VM_appliance_new = {
            "VMs": [],
            "allowed_operations": [
                "start",
                "clean_shutdown",
                "hard_shutdown",
                "shutdown",
            ],
            "current_operations": {},
            "name_description": args.get("name_description", ""),
            "name_label": args.get("name_label", ""),
            "uuid": str(uuid.uuid4()),
        }

        self._check_param_type(VM_appliance_new['name_description'], 'string', 'name_description')
        self._check_param_type(VM_appliance_new['name_label'], 'string', 'name_label')

        VM_appliance_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[VM_appliance_ref] = VM_appliance_new

        return VM_appliance_ref

    def destroy(self, VM_appliance_ref):
        self._check_param_type(VM_appliance_ref, 'ref')
        self._check_obj_ref(VM_appliance_ref)

        del self.objs[VM_appliance_ref]

    def hard_shutdown(self, VM_appliance_ref):
        self._check_param_type(VM_appliance_ref, 'ref')
        self._check_obj_ref(VM_appliance_ref)

        for VM_ref in self.objs[VM_appliance_ref]['VMs']:
            self.xenapi.VM.hard_shutdown(VM_ref)

    def shutdown(self, VM_appliance_ref):
        self._check_param_type(VM_appliance_ref, 'ref')
        self._check_obj_ref(VM_appliance_ref)

        for VM_ref in self.objs[VM_appliance_ref]['VMs']:
            self.xenapi.VM.shutdown(VM_ref)

    def start(self, VM_appliance_ref):
        self._check_param_type(VM_appliance_ref, 'ref')
        self._check_obj_ref(VM_appliance_ref)

        for VM_ref in self.objs[VM_appliance_ref]['VMs']:
            self.xenapi.VM.start(VM_ref)
