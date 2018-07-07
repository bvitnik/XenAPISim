#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, Bojan Vitnik <bvitnik@mainstream.rs>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import print_function

import uuid

from xenapi_object import xenapi_object
from xenapi_exception import xenapi_exception


class VBD(xenapi_object):
    """XenAPI VBD class.

    Attributes:
    """

    def __init__(self, xenapi):
        """Inits VBD class.

        Args:
        """
        super(VBD, self).__init__(xenapi)

        self.field_def.update({
            "VDI": "OpaqueRef:NULL",
            "VM": "OpaqueRef:NULL",
            "allowed_operations": [],
            "bootable": True,
            "current_operations": {},
            "currently_attached": False,
            "device": "",
            "empty": False,
            "metrics": "OpaqueRef:NULL",
            "mode": "RW",
            "qos_algorithm_params": {},
            "qos_algorithm_type": "",
            "qos_supported_algorithms": [],
            "runtime_properties": {},
            "status_code": "0",
            "status_detail": "",
            "storage_lock": False,
            "type": "Disk",
            "unpluggable": True,
            "userdevice": "0",
        })

        self.rw_fields.extend([
            "bootable",
            "mode",
            "qos_algorithm_params",
            "qos_algorithm_type",
            "type",
            "unpluggable",
            "userdevice",
        ])

        self.map_fields.extend([
            "qos_algorithm_params",
        ])

        VBD_new = {
            "VDI": "OpaqueRef:NULL",
            "VM": "OpaqueRef:NULL",
            "allowed_operations": [
                "attach",
                "eject",
                "insert",
                "plug",
                "unplug",
                "unplug_force",
                "pause",
                "unpause",
            ],
            "bootable": True,
            "current_operations": {},
            "currently_attached": True,
            "device": "xvda",
            "empty": False,
            "metrics": "OpaqueRef:NULL",
            "mode": "RW",
            "other_config": {},
            "qos_algorithm_params": {},
            "qos_algorithm_type": "",
            "qos_supported_algorithms": [],
            "runtime_properties": {},
            "status_code": "0",
            "status_detail": "",
            "storage_lock": False,
            "type": "Disk",
            "unpluggable": True,
            "userdevice": "0",
            "uuid": str(uuid.uuid4()),
        }

        VBD_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[VBD_ref] = VBD_new

    def assert_attachable(self, VBD_ref):
        self._check_param_type(VBD_ref, 'ref')
        self._check_obj_ref(VBD_ref)

        # Do nothing, no VM ref, can't test anything.

    def create(self, args):
        self._check_param_type(args, 'struct')

        VBD_new = {
            "VDI": args.get("VDI", ""),
            "VM": args.get("VM", ""),
            "allowed_operations": [
                "attach",
                "eject",
                "insert",
                "plug",
                "unplug",
                "unplug_force",
                "pause",
                "unpause",
            ],
            "bootable": args.get("bootable", True),
            "current_operations": {},
            "currently_attached": True,
            "device": "xvda",
            "empty": args.get("empty", False),
            "metrics": "OpaqueRef:NULL",
            "mode": args.get("mode", ""),
            "other_config": args.get("other_config", {}),
            "qos_algorithm_params": args.get("qos_algorithm_params", {}),
            "qos_algorithm_type": args.get("qos_algorithm_type", ""),
            "qos_supported_algorithms": [],
            "runtime_properties": {},
            "status_code": "0",
            "status_detail": "",
            "storage_lock": False,
            "type": args.get("type", ""),
            "unpluggable": args.get("unpluggable", True),
            "userdevice": args.get("userdevice", "0"),
            "uuid": str(uuid.uuid4()),
        }

        # self.xenapi.VDI._check_param_type(VBD_new['VDI'], 'ref')
        # self.xenapi.VM._check_param_type(VBD_new['VM'], 'ref')
        self._check_param_type(VBD_new['bootable'], 'boolean', 'bootable')
        self._check_param_type(VBD_new['empty'], 'boolean', 'empty')
        self._check_param_type(VBD_new['mode'], 'string', 'mode')
        self._check_param_type(VBD_new['other_config'], 'struct', 'other_config')
        self._check_param_type(VBD_new['qos_algorithm_params'], 'struct', 'qos_algorithm_params')
        self._check_param_type(VBD_new['qos_algorithm_type'], 'string', 'qos_algorithm_type')
        self._check_param_type(VBD_new['type'], 'string', 'type')
        self._check_param_type(VBD_new['unpluggable'], 'boolean', 'unpluggable')
        self._check_param_type(VBD_new['userdevice'], 'string', 'userdevice')

        for field in ["VM", "VDI", "userdevice", "bootable", "mode", "type", "empty", "other_config", "qos_algorithm_type", "qos_algorithm_params"]:
            if not field in args:
                raise xenapi_exception(['FIELD_MISSING', field])

        VBD_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[VBD_ref] = VBD_new

        return VBD_ref

    def destroy(self, VBD_ref):
        self._check_param_type(VBD_ref, 'ref')
        self._check_obj_ref(VBD_ref)

        del self.objs[VBD_ref]

    def eject(self, VBD_ref):
        self._check_param_type(VBD_ref, 'ref')
        self._check_obj_ref(VBD_ref)

        if self.objs[VBD_ref]['type'] == "Disk":
            raise xenapi_exception(['VBD_NOT_REMOVABLE_MEDIA', VBD_ref])

        if self.objs[VBD_ref]['empty']:
            raise xenapi_exception(['VBD_IS_EMPTY', VBD_ref])

        self.objs[VBD_ref]['VDI'] = "OpaqueRef:NULL"
        self.objs[VBD_ref]['empty'] = True

    def insert(self, VBD_ref, VDI_ref):
        self._check_param_type(VBD_ref, 'ref')
        # self.xenapi.VDI._check_param_type(VBD_ref, 'ref')
        self._check_obj_ref(VBD_ref)
        # self.xenapi.VDI._check_obj_ref(VDI_ref)

        if self.objs[VBD_ref]['type'] == "Disk":
            raise xenapi_exception(['VBD_NOT_REMOVABLE_MEDIA', VBD_ref])

        if not self.objs[VBD_ref]['empty']:
            raise xenapi_exception(['VBD_NOT_EMPTY', VBD_ref])

        self.objs[VBD_ref]['VDI'] = VDI_ref
        self.objs[VBD_ref]['empty'] = False

    def plug(self, VBD_ref):
        self._check_param_type(VBD_ref, 'ref')
        self._check_obj_ref(VBD_ref)

        # Do nothing for now.

    def unplug(self, VBD_ref):
        self._check_param_type(VBD_ref, 'ref')
        self._check_obj_ref(VBD_ref)

        # Do nothing for now.

    def unplug_force(self, VBD_ref):
        self._check_param_type(VBD_ref, 'ref')
        self._check_obj_ref(VBD_ref)

        # Do nothing for now.
