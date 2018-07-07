#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, Bojan Vitnik <bvitnik@mainstream.rs>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import print_function

import uuid

from xenapi_object import xenapi_object
from xenapi_exception import xenapi_exception


class SR(xenapi_object):
    """XenAPI SR class.

    Attributes:
    """

    def __init__(self, xenapi):
        """Inits SR class.

        Args:
        """
        super(SR, self).__init__(xenapi)

        self.field_def.update({
            "PBDs": [],
            "VDIs": [],
            "allowed_operations": [],
            "blobs": {},
            "clustered": False,
            "content_type": "",
            "current_operations": {},
            "introduced_by": "OpaqueRef:NULL",
            "is_tools_sr": False,
            "local_cache_enabled": False,
            "name_description": "",
            "name_label": "",
            "physical_size": "0",
            "physical_utilisation": "0",
            "shared": False,
            "sm_config": {},
            "tags": [],
            "type": "",
            "virtual_allocation": "0",
        })

        self.rw_fields.extend([
            "name_description",
            "name_label",
            "physical_size",
            "shared",
            "sm_config",
            "tags",
        ])

        self.list_fields.extend([
            "tags",
        ])

        self.map_fields.extend([
            "sm_config",
        ])

        self.unimplemented_methods.extend([
            "create_new_blob",
            "disable_database_replication",
            "enable_database_replication",
            "forget_data_source_archives",
            "get_data_sources",
            "make",
            "probe_ext",
            "query_data_source",
            "record_data_source",
        ])

        SR_new = {
            "PBDs": [],
            "VDIs": [],
            "allowed_operations": [
                "scan",
                "destroy",
                "forget",
                "plug",
                "unplug",
                "update",
                "vdi_create",
                "vdi_introduce",
                "vdi_destroy",
                "vdi_resize",
                "vdi_clone",
                "vdi_snapshot",
                "vdi_mirror",
                "vdi_enable_cbt",
                "vdi_disable_cbt",
                "vdi_data_destroy",
                "vdi_list_changed_blocks",
                "vdi_set_on_boot",
                "pbd_create",
                "pbd_destroy",
            ],
            "blobs": {},
            "clustered": False,
            "content_type": "user",
            "current_operations": {},
            "introduced_by": "OpaqueRef:NULL",
            "is_tools_sr": False,
            "local_cache_enabled": True,
            "name_description": "",
            "name_label": "Local storage",
            "other_config": {
                "i18n-original-value-name_label": "Local storage",
                "i18n-key:": "local-storage"
            },
            "physical_size": "2199006478336",
            "physical_utilisation": "0",
            "shared": False,
            "sm_config": {"devserial": "scsi-355cd2e404b5f035e"},
            "tags": [],
            "type": "ext",
            "uuid": str(uuid.uuid4()),
            "virtual_allocation": "0",
        }

        SR_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[SR_ref] = SR_new

    def assert_can_host_ha_statefile(self, SR_ref):
        self._check_param_type(SR_ref, 'ref')
        self._check_obj_ref(SR_ref)

        if not len(self.objs[SR_ref]['PBDs']) > 1:
            raise xenapi_exception(['SR_HAS_NO_PBDS', SR_ref])

        if self.objs[SR_ref]['is_tools_sr']:
            raise xenapi_exception(['SR_OPERATION_NOT_SUPPORTED', SR_ref])

    def assert_supports_database_replication(self, SR_ref):
        self._check_param_type(SR_ref, 'ref')
        self._check_obj_ref(SR_ref)

        if not len(self.objs[SR_ref]['PBDs']) > 1:
            raise xenapi_exception(['SR_HAS_NO_PBDS', SR_ref])

        if self.objs[SR_ref]['is_tools_sr']:
            raise xenapi_exception(['SR_OPERATION_NOT_SUPPORTED', SR_ref])

    def create(self,
               host_ref,
               device_config,
               physical_size,
               name_label,
               name_description,
               type,
               content_type,
               shared,
               sm_config):
        self.xenapi.host._check_param_type(host_ref, 'ref')
        self._check_param_type(device_config, 'struct', 'device_config')
        self._check_param_type(physical_size, 'int', 'physical_size')
        self._check_param_type(name_label, 'string', 'name_label')
        self._check_param_type(name_description, 'struct', 'name_description')
        self._check_param_type(type, 'struct', 'type')
        self._check_param_type(content_type, 'struct', 'content_type')
        self._check_param_type(shared, 'boolean', 'shared')
        self._check_param_type(sm_config, 'struct', 'sm_config')

        SR_new = {
            "PBDs": ["OpaqueRef:NULL"],
            "VDIs": [],
            "allowed_operations": [
                "scan",
                "destroy",
                "forget",
                "plug",
                "unplug",
                "update",
                "vdi_create",
                "vdi_introduce",
                "vdi_destroy",
                "vdi_resize",
                "vdi_clone",
                "vdi_snapshot",
                "vdi_mirror",
                "vdi_enable_cbt",
                "vdi_disable_cbt",
                "vdi_data_destroy",
                "vdi_list_changed_blocks",
                "vdi_set_on_boot",
                "pbd_create",
                "pbd_destroy",
            ],
            "blobs": {},
            "clustered": False,
            "content_type": content_type,
            "current_operations": {},
            "introduced_by": "OpaqueRef:NULL",
            "is_tools_sr": False,
            "local_cache_enabled": True,
            "name_description": name_description,
            "name_label": name_label,
            "other_config": {
                "i18n-original-value-name_label": "Local storage",
                "i18n-key:": "local-storage"
            },
            "physical_size": physical_size,
            "physical_utilisation": "0",
            "shared": shared,
            "sm_config": sm_config,
            "tags": [],
            "type": type,
            "uuid": str(uuid.uuid4()),
            "virtual_allocation": "0",
        }

        SR_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[SR_ref] = SR_new

        return SR_ref

    def destroy(self, SR_ref):
        self._check_param_type(SR_ref, 'ref')
        self._check_obj_ref(SR_ref)

        del self.objs[SR_ref]

    def forget(self, SR_ref):
        self._check_param_type(SR_ref, 'ref')
        self._check_obj_ref(SR_ref)

        del self.objs[SR_ref]

    def get_supported_types(self):
        return ["smb", "iso", "lvm", "nfs", "hba", "lvmofcoe", "udev", "dummy", "ext", "lvmohba", "lvmoiscsi", "file", "iscsi"]

    def introduce(self,
                  uuid,
                  name_label,
                  name_description,
                  type,
                  content_type,
                  shared,
                  sm_config):
        self._check_param_type(uuid, 'struct', 'uuid')
        self._check_param_type(name_label, 'string', 'name_label')
        self._check_param_type(name_description, 'struct', 'name_description')
        self._check_param_type(type, 'struct', 'type')
        self._check_param_type(content_type, 'struct', 'content_type')
        self._check_param_type(shared, 'boolean', 'shared')
        self._check_param_type(sm_config, 'struct', 'sm_config')

        SR_new = {
            "PBDs": ["OpaqueRef:NULL"],
            "VDIs": [],
            "allowed_operations": [
                "scan",
                "destroy",
                "forget",
                "plug",
                "unplug",
                "update",
                "vdi_create",
                "vdi_introduce",
                "vdi_destroy",
                "vdi_resize",
                "vdi_clone",
                "vdi_snapshot",
                "vdi_mirror",
                "vdi_enable_cbt",
                "vdi_disable_cbt",
                "vdi_data_destroy",
                "vdi_list_changed_blocks",
                "vdi_set_on_boot",
                "pbd_create",
                "pbd_destroy",
            ],
            "blobs": {},
            "clustered": False,
            "content_type": content_type,
            "current_operations": {},
            "introduced_by": "OpaqueRef:NULL",
            "is_tools_sr": False,
            "local_cache_enabled": True,
            "name_description": name_description,
            "name_label": name_label,
            "other_config": {
                "i18n-original-value-name_label": "Local storage",
                "i18n-key:": "local-storage"
            },
            "physical_size": "0",
            "physical_utilisation": "0",
            "shared": shared,
            "sm_config": sm_config,
            "tags": [],
            "type": type,
            "uuid": uuid,
            "virtual_allocation": "0",
        }

        SR_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[SR_ref] = SR_new

        return SR_ref

    def probe(self, host_ref, device_config, type, sm_config):
        self.xenapi.host._check_param_type(host_ref, 'ref')
        self._check_param_type(device_config, 'struct', 'device_config')
        self._check_param_type(type, 'struct', 'type')
        self._check_param_type(sm_config, 'struct', 'sm_config')

        return ""

    def scan(self, SR_ref):
        self._check_param_type(SR_ref, 'ref')
        self._check_obj_ref(SR_ref)

        # does nothing really.

    def update(self, SR_ref):
        self._check_param_type(SR_ref, 'ref')
        self._check_obj_ref(SR_ref)

        # does nothing really.
