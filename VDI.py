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


class VDI(xenapi_object):
    """XenAPI VDI class.

    Attributes:
    """

    def __init__(self, xenapi):
        """Inits VDI class.

        Args:
        """
        super(VDI, self).__init__(xenapi)

        self.field_def.update({
            "SR": "OpaqueRef:NULL",
            "VBDs": [],
            "allow_caching": False,
            "allowed_operations": [],
            "cbt_enabled": False,
            "crash_dumps": [],
            "current_operations": {},
            "is_a_snapshot": False,
            "is_tools_iso": False,
            "location": "",
            "managed": True,
            "metadata_latest": False,
            "metadata_of_pool": "OpaqueRef:NULL",
            "missing": False,
            "name_description": "",
            "name_label": "",
            "on_boot": "persist",
            "parent": "OpaqueRef:NULL",
            "physical_utilisation": "0",
            "read_only": False,
            "sharable": False,
            "sm_config": {},
            "snapshot_of": "OpaqueRef:NULL",
            "snapshot_time": datetime.now(),
            "snapshots": [],
            "storage_lock": False,
            "tags": [],
            "type": "user",
            "virtual_size": "0",
            "xenstore_data": {},
        })

        self.rw_fields.extend([
            "allow_caching",
            "name_description",
            "name_label",
            "on_boot",
            "read_only",
            "sharable",
            "sm_config",
            "tags",
            "xenstore_data",
        ])

        self.list_fields.extend([
            "tags",
        ])

        self.map_fields.extend([
            "sm_config",
            "xenstore_data",
        ])

        self.unimplemented_methods.extend([
            "data_destroy",
            "disable_cbt",
            "enable_cbt",
            "get_nbd_info",
            "introduce",
            "list_changed_blocks",
            "open_database",
            "read_database_pool_uuid",
            "resize_online",
        ])

        VDI_uuid = str(uuid.uuid4())

        VDI_new = {
            "SR": "OpaqueRef:NULL",
            "VBDs": [],
            "allow_caching": False,
            "allowed_operations": [
                "clone",
                "copy",
                "resize",
                "resize_online",
                "snapshot",
                "mirror",
                "destroy",
                "forget",
                "update",
                "force_unlock",
                "generate_config",
                "enable_cbt",
                "disable_cbt",
                "data_destroy",
                "list_changed_blocks",
                "set_on_boot",
                "blocked",
            ],
            "cbt_enabled": False,
            "crash_dumps": [],
            "current_operations": {},
            "is_a_snapshot": False,
            "is_tools_iso": False,
            "location": VDI_uuid,
            "managed": True,
            "metadata_latest": False,
            "metadata_of_pool": "OpaqueRef:NULL",
            "missing": False,
            "name_description": "",
            "name_label": "disk-1",
            "on_boot": "persist",
            "other_config": {},
            "parent": "OpaqueRef:NULL",
            "physical_utilisation": "8615100416",
            "read_only": False,
            "sharable": False,
            "sm_config": {},
            "snapshot_of": "OpaqueRef:NULL",
            "snapshot_time": datetime.fromtimestamp(0),
            "snapshots": [],
            "storage_lock": False,
            "tags": [],
            "type": "user",
            "uuid": VDI_uuid,
            "virtual_size": "8615100416",
            "xenstore_data": {},
        }

        VDI_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[VDI_ref] = VDI_new

    def clone(self, VDI_ref, driver_params):
        self._check_param_type(VDI_ref, 'ref')
        self._check_param_type(driver_params, 'struct', 'driver_params')

        self._check_obj_ref(VDI_ref)

        # Create new VDI and return.

    def copy(self, VDI_ref, SR_ref, base_vdi=None, into_vdi=None):
        self._check_param_type(VDI_ref, 'ref')
        self.xenapi.SR._check_param_type(SR_ref, 'ref')

        if base_vdi is not None:
            self._check_param_type(base_vdi, 'ref')

        if into_vdi is not None:
            self._check_param_type(into_vdi, 'ref')

        self._check_obj_ref(VDI_ref)
        self.xenapi.SR._check_obj_ref(SR_ref)

        if base_vdi is not None:
            self._check_obj_ref(base_vdi)

        if into_vdi is not None:
            self._check_obj_ref(into_vdi)

        # Create new VDI and return.

    def create(self, args):
        self._check_param_type(args, 'struct')

        VDI_uuid = str(uuid.uuid4())

        VDI_new = {
            "SR": args.get("SR", ""),
            "VBDs": [],
            "allow_caching": False,
            "allowed_operations": [
                "clone",
                "copy",
                "resize",
                "resize_online",
                "snapshot",
                "mirror",
                "destroy",
                "forget",
                "update",
                "force_unlock",
                "generate_config",
                "enable_cbt",
                "disable_cbt",
                "data_destroy",
                "list_changed_blocks",
                "set_on_boot",
                "blocked",
            ],
            "cbt_enabled": False,
            "crash_dumps": [],
            "current_operations": {},
            "is_a_snapshot": False,
            "is_tools_iso": False,
            "location": VDI_uuid,
            "managed": True,
            "metadata_latest": False,
            "metadata_of_pool": "OpaqueRef:NULL",
            "missing": False,
            "name_description": args.get("name_description", ""),
            "name_label": args.get("name_label", ""),
            "on_boot": "persist",
            "other_config": args.get("other_config", {}),
            "parent": "OpaqueRef:NULL",
            "physical_utilisation": "0",
            "read_only": args.get("read_only", False),
            "sharable": args.get("sharable", False),
            "sm_config": args.get("sm_config", {}),
            "snapshot_of": "OpaqueRef:NULL",
            "snapshot_time": datetime.strptime("19700101T00:00:00Z"),
            "snapshots": [],
            "storage_lock": False,
            "tags": args.get("tags", []),
            "type": args.get("type", ""),
            "uuid": VDI_uuid,
            "virtual_size": args.get("virtual_size", "0"),
            "xenstore_data": args.get("xenstore_data", {}),
        }

        self.xenapi.SR._check_param_type(VDI_new['SR'], 'ref')
        self._check_param_type(VDI_new['name_description'], 'string', 'name_description')
        self._check_param_type(VDI_new['name_label'], 'string', 'name_label')
        self._check_param_type(VDI_new['other_config'], 'struct', 'other_config')
        self._check_param_type(VDI_new['read_only'], 'boolean', 'read_only')
        self._check_param_type(VDI_new['sharable'], 'boolean', 'sharable')
        self._check_param_type(VDI_new['sm_config'], 'struct', 'sm_config')
        self._check_param_type(VDI_new['tags'], 'array', 'tags')
        self._check_param_type(VDI_new['type'], 'string', 'type')
        self._check_param_type(VDI_new['virtual_size'], 'int', 'virtual_size')
        self._check_param_type(VDI_new['xenstore_data'], 'struct', 'xenstore_data')

        for field in ["SR", "virtual_size", "type", "sharable", "read_only", "other_config"]:
            if not field in args:
                raise xenapi_exception(['FIELD_MISSING', field])

        VDI_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[VDI_ref] = VDI_new

        return VDI_ref

    def destroy(self, VDI_ref):
        self._check_param_type(VDI_ref, 'ref')
        self._check_obj_ref(VDI_ref)

        del self.objs[VDI_ref]

    def forget(self, VDI_ref):
        self._check_param_type(VDI_ref, 'ref')
        self._check_obj_ref(VDI_ref)

        del self.objs[VDI_ref]

    def pool_migrate(self, VDI_ref, SR_ref, options):
        self._check_param_type(VDI_ref, 'ref')
        self.xenapi.SR._check_param_type(SR_ref, 'ref')
        self._check_param_type(options, 'struct', 'options')

        self._check_obj_ref(VDI_ref)
        self.xenapi.SR._check_obj_ref(SR_ref)

        # Do nothing for now.
        return VDI_ref

    def resize(self, VDI_ref, size):
        self._check_param_type(VDI_ref, 'ref')
        self._check_param_type(size, 'int', 'size')

        self._check_obj_ref(VDI_ref)

        self.objs[VDI_ref]['virtual_size'] = size

    def snapshot(self, VDI_ref, driver_params):
        self._check_param_type(VDI_ref, 'ref')
        self._check_param_type(driver_params, 'struct', 'driver_params')

        self._check_obj_ref(VDI_ref)

        # Create new VDI and return.

    def update(self, VDI_ref):
        self._check_param_type(VDI_ref, 'ref')
        self._check_obj_ref(VDI_ref)

        # does nothing really.
