#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, Bojan Vitnik <bvitnik@mainstream.rs>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import print_function

import uuid, time
from datetime import datetime

from xenapi_object import xenapi_object
from xenapi_exception import xenapi_exception


class VM(xenapi_object):
    """XenAPI VM class.

    Attributes:
    """

    def __init__(self, xenapi):
        """Inits VM class.

        Args:
        """
        super(VM, self).__init__(xenapi)

        self.field_def.update({
            "HVM_boot_params": {},
            "HVM_boot_policy": "",
            "HVM_shadow_multiplier": 0.0,
            "PCI_bus": "",
            "PV_args": "",
            "PV_bootloader": "",
            "PV_bootloader_args": "",
            "PV_kernel": "",
            "PV_legacy_args": "",
            "PV_ramdisk": "",
            "VBDs": [],
            "VCPUs_at_startup": "0",
            "VCPUs_max": "0",
            "VCPUs_params": {},
            "VGPUs": [],
            "VIFs": [],
            "VTPMs": [],
            "VUSBs": [],
            "actions_after_crash": "restart",
            "actions_after_reboot": "restart",
            "actions_after_shutdown": "destroy",
            "affinity": "OpaqueRef:NULL",
            "allowed_operations": [],
            "appliance": "OpaqueRef:NULL",
            "attached_PCIs": [],
            "bios_strings": {},
            "blobs": {},
            "blocked_operations": {},
            "children": [],
            "consoles": [],
            "crash_dumps": [],
            "current_operations": {},
            "domain_type": "unspecified",
            "domarch": "",
            "domid": "0",
            "generation_id": "",
            "guest_metrics": "OpaqueRef:NULL",
            "ha_always_run": False,
            "ha_restart_priority": "",
            "hardware_platform_version": "0",
            "has_vendor_device": False,
            "is_a_snapshot": False,
            "is_a_template": False,
            "is_control_domain": False,
            "is_default_template": False,
            "is_snapshot_from_vmpp": False,
            "is_vmss_snapshot": False,
            "last_boot_CPU_flags": {},
            "last_booted_record": "",
            "memory_dynamic_max": "0",
            "memory_dynamic_min": "0",
            "memory_overhead": "0",
            "memory_static_max": "0",
            "memory_static_min": "0",
            "memory_target": "0",
            "metrics": "OpaqueRef:NULL",
            "name_description": "",
            "name_label": "",
            "order": "0",
            "parent": "OpaqueRef:NULL",
            "platform": {},
            "power_state": "Halted",
            "protection_policy": "OpaqueRef:NULL",
            "recommendations": "",
            "reference_label": "",
            "requires_reboot": False,
            "resident_on": "OpaqueRef:NULL",
            "shutdown_delay": "0",
            "snapshot_info": {},
            "snapshot_metadata": "",
            "snapshot_of": "OpaqueRef:NULL",
            "snapshot_schedule": "OpaqueRef:NULL",
            "snapshot_time": datetime.now(),
            "snapshots": [],
            "start_delay": "0",
            "suspend_SR": "OpaqueRef:NULL",
            "suspend_VDI": "OpaqueRef:NULL",
            "tags": [],
            "transportable_snapshot_id": "",
            "user_version": "0",
            "version": "0",
            "xenstore_data": {},
        })

        self.rw_fields.extend([
            "HVM_boot_params",
            "HVM_boot_policy",
            "HVM_shadow_multiplier",
            "PCI_bus",
            "PV_args",
            "PV_bootloader",
            "PV_bootloader_args",
            "PV_kernel",
            "PV_legacy_args",
            "PV_ramdisk",
            "VCPUs_at_startup",
            "VCPUs_max",
            "VCPUs_params",
            "actions_after_crash",
            "actions_after_reboot",
            "actions_after_shutdown",
            "affinity",
            "bios_strings",
            "blocked_operations",
            "domain_type",
            "ha_always_run",
            "ha_restart_priority",
            "hardware_platform_version",
            "has_vendor_device",
            "is_a_template",
            "memory_dynamic_max",
            "memory_dynamic_min",
            "memory_static_max",
            "memory_static_min",
            "name_description",
            "name_label",
            "order",
            "platform",
            "protection_policy",
            "recommendations",
            "shutdown_delay",
            "snapshot_schedule",
            "start_delay",
            "suspend_SR",
            "suspend_VDI",
            "tags",
            "user_version",
            "xenstore_data",
        ])

        self.list_fields.extend([
            "tags",
        ])

        self.map_fields.extend([
            "HVM_boot_params",
            "VCPUs_params",
            "blocked_operations",
            "platform",
            "xenstore_data",
        ])

        self.unimplemented_methods.extend([
            "assert_can_be_recovered",
            "call_plugin",
            "create_new_blob",
            "forget_data_source_archives",
            "get_SRs_required_for_recovery",
            "get_boot_record",
            "get_cooperative",
            "get_data_sources",
            "import",
            "import_convert",
            "maximise_memory",
            "query_data_source",
            "query_services",
            "record_data_source",
            "recover",
            "retrieve_wlb_recommendations",
            "send_sysrq",
            "send_trigger",
            "set_memory_target_live",
            "snapshot_with_quiesce",
            "wait_memory_target_live",
        ])

        VM_new = {
            "HVM_boot_params": {},
            "HVM_boot_policy": "",
            "HVM_shadow_multiplier": 0.0,
            "PCI_bus": "",
            "PV_args": "",
            "PV_bootloader": "",
            "PV_bootloader_args": "",
            "PV_kernel": "",
            "PV_legacy_args": "",
            "PV_ramdisk": "",
            "VBDs": [],
            "VCPUs_at_startup": "0",
            "VCPUs_max": "0",
            "VCPUs_params": {},
            "VGPUs": [],
            "VIFs": [],
            "VTPMs": [],
            "VUSBs": [],
            "actions_after_crash": "restart",
            "actions_after_reboot": "restart",
            "actions_after_shutdown": "destroy",
            "affinity": "OpaqueRef:NULL",
            "allowed_operations": [],
            "appliance": "OpaqueRef:NULL",
            "attached_PCIs": [],
            "bios_strings": {},
            "blobs": {},
            "blocked_operations": {},
            "children": [],
            "consoles": [],
            "crash_dumps": [],
            "current_operations": {},
            "domain_type": "unspecified",
            "domarch": "",
            "domid": "0",
            "generation_id": "",
            "guest_metrics": "OpaqueRef:NULL",
            "ha_always_run": False,
            "ha_restart_priority": "",
            "hardware_platform_version": "0",
            "has_vendor_device": False,
            "is_a_snapshot": False,
            "is_a_template": False,
            "is_control_domain": False,
            "is_default_template": False,
            "is_snapshot_from_vmpp": False,
            "is_vmss_snapshot": False,
            "last_boot_CPU_flags": {},
            "last_booted_record": "",
            "memory_dynamic_max": "0",
            "memory_dynamic_min": "0",
            "memory_overhead": "0",
            "memory_static_max": "0",
            "memory_static_min": "0",
            "memory_target": "0",
            "metrics": "OpaqueRef:NULL",
            "name_description": "",
            "name_label": "",
            "order": "0",
            "other_config": {},
            "parent": "OpaqueRef:NULL",
            "platform": {},
            "power_state": "Halted",
            "protection_policy": "OpaqueRef:NULL",
            "recommendations": "",
            "reference_label": "",
            "requires_reboot": False,
            "resident_on": "OpaqueRef:NULL",
            "shutdown_delay": "0",
            "snapshot_info": {},
            "snapshot_metadata": "",
            "snapshot_of": "OpaqueRef:NULL",
            "snapshot_schedule": "OpaqueRef:NULL",
            "snapshot_time": datetime.now(),
            "snapshots": [],
            "start_delay": "0",
            "suspend_SR": "OpaqueRef:NULL",
            "suspend_VDI": "OpaqueRef:NULL",
            "tags": [],
            "transportable_snapshot_id": "",
            "user_version": "0",
            "uuid": str(uuid.uuid4()),
            "version": "0",
            "xenstore_data": {},
        }

        VM_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[VM_ref] = VM_new

    #
    # XenAPI methods
    #

    def assert_agile(self, VM_ref):
        self._check_param_type(VM_ref, 'ref')
        self._check_obj_ref(VM_ref)

        # Do nothing for now.

    def assert_can_boot_here(self, VM_ref, host_ref):
        self._check_param_type(VM_ref, 'ref')
        self.xenapi.host._check_param_type(host_ref, 'ref')

        self._check_obj_ref(VM_ref)
        self.xenapi.host._check_obj_ref(host_ref)

        # Do nothing for now.

    def assert_can_migrate(self, VM_ref, dest, live, vdi_map, vif_map, options, vgpu_map):
        self._check_param_type(VM_ref, 'ref')
        self._check_param_type(dest, 'struct', 'dest')
        self._check_param_type(live, 'boolean', 'live')
        self._check_param_type(vdi_map, 'struct', 'vdi_map')
        self._check_param_type(vif_map, 'struct', 'vif_map')
        self._check_param_type(options, 'struct', 'options')
        self._check_param_type(vgpu_map, 'struct', 'vgpu_map')

        self._check_obj_ref(VM_ref)

        # Do nothing for now.

    def assert_operation_valid(self, VM_ref, op):
        self._check_param_type(VM_ref, 'ref')
        self._check_param_type(op, 'string', 'op')

        self._check_obj_ref(VM_ref)

        # Do nothing for now.

    def checkpoint(self, VM_ref, new_name):
        self._check_param_type(VM_ref, 'ref')
        self._check_param_type(new_name, 'string', 'new_name')

        self._check_obj_ref(VM_ref)

        # Do nothing for now.
        return VM_ref

    def clean_reboot(self, VM_ref):
        self._check_param_type(VM_ref, 'ref')
        self._check_obj_ref(VM_ref)

        # Do nothing for now.

    def clean_shutdown(self, VM_ref):
        self._check_param_type(VM_ref, 'ref')
        self._check_obj_ref(VM_ref)

        # Do nothing for now.

    def clone(self, VM_ref, new_name):
        self._check_param_type(VM_ref, 'ref')
        self._check_param_type(new_name, 'string', 'new_name')

        self._check_obj_ref(VM_ref)

        # Do nothing for now.
        return VM_ref

    def compute_memory_overhead(self, VM_ref):
        self._check_param_type(VM_ref, 'ref')
        self._check_obj_ref(VM_ref)

        # Do nothing for now.
        return "0"

    def copy(self, VM_ref, new_name, SR_ref):
        self._check_param_type(VM_ref, 'ref')
        self._check_param_type(new_name, 'string', 'new_name')
        self.xenapi.SR._check_param_type(SR_ref, 'ref')

        self._check_obj_ref(VM_ref)
        self.xenapi.SR._check_obj_ref(SR_ref)

        # Do nothing for now.
        return VM_ref

    def copy_bios_strings(self, VM_ref, host_ref):
        self._check_param_type(VM_ref, 'ref')
        self.xenapi.host._check_param_type(host_ref, 'ref')

        self._check_obj_ref(VM_ref)
        self.xenapi.host._check_obj_ref(host_ref)

        self.objs[VM_ref]['bios_strings'] = self.xenapi.host.objs[host_ref]['bios_strings']

    def create(self, args):
        self._check_param_type(args, 'struct')

        VM_new = {
            "HVM_boot_params": args.get("HVM_boot_params", {}),
            "HVM_boot_policy": args.get("HVM_boot_policy", ""),
            "HVM_shadow_multiplier": args.get("HVM_shadow_multiplier", 0.0),
            "PCI_bus": args.get("PCI_bus", ""),
            "PV_args": args.get("PV_args", ""),
            "PV_bootloader": args.get("PV_bootloader", ""),
            "PV_bootloader_args": args.get("PV_bootloader_args", ""),
            "PV_kernel": args.get("PV_kernel", ""),
            "PV_legacy_args": args.get("PV_legacy_args", ""),
            "PV_ramdisk": args.get("PV_ramdisk", ""),
            "VBDs": [],
            "VCPUs_at_startup": args.get("VCPUs_at_startup", "0"),
            "VCPUs_max": args.get("VCPUs_max", "0"),
            "VCPUs_params": args.get("VCPUs_params", {}),
            "VGPUs": [],
            "VIFs": [],
            "VTPMs": [],
            "VUSBs": [],
            "actions_after_crash": args.get("actions_after_crash", "restart"),
            "actions_after_reboot": args.get("actions_after_reboot", "restart"),
            "actions_after_shutdown": args.get("actions_after_shutdown", "destroy"),
            "affinity": args.get("affinity", "OpaqueRef:NULL"),
            "allowed_operations": [],
            "appliance": args.get("appliance", "OpaqueRef:NULL"),
            "attached_PCIs": [],
            "bios_strings": {},
            "blobs": {},
            "blocked_operations": args.get("blocked_operations", {}),
            "children": [],
            "consoles": [],
            "crash_dumps": [],
            "current_operations": {},
            "domain_type": args.get("domain_type", "unspecified"),
            "domarch": "",
            "domid": "0",
            "generation_id": args.get("generation_id", ""),
            "guest_metrics": "OpaqueRef:NULL",
            "ha_always_run": args.get("ha_always_run", False),
            "ha_restart_priority": args.get("ha_restart_priority", ""),
            "hardware_platform_version": args.get("hardware_platform_version", "0"),
            "has_vendor_device": args.get("has_vendor_device", False),
            "is_a_snapshot": False,
            "is_a_template": args.get("is_a_template", False),
            "is_control_domain": False,
            "is_default_template": False,
            "is_snapshot_from_vmpp": args.get("is_snapshot_from_vmpp", False),
            "is_vmss_snapshot": args.get("is_vmss_snapshot", False),
            "last_boot_CPU_flags": {},
            "last_booted_record": "",
            "memory_dynamic_max": args.get("memory_dynamic_max", "0"),
            "memory_dynamic_min": args.get("memory_dynamic_min", "0"),
            "memory_overhead": "0",
            "memory_static_max": args.get("memory_static_max", "0"),
            "memory_static_min": args.get("memory_static_min", "0"),
            "memory_target": args.get("memory_target", "0"),
            "metrics": "OpaqueRef:NULL",
            "name_description": args.get("name_description", ""),
            "name_label": args.get("name_label", ""),
            "order": args.get("order", "0"),
            "other_config": args.get("other_config", {}),
            "parent": "OpaqueRef:NULL",
            "platform": args.get("platform", {}),
            "power_state": "Halted",
            "protection_policy": args.get("protection_policy", "OpaqueRef:NULL"),
            "recommendations": args.get("recommendations", ""),
            "reference_label": args.get("reference_label", ""),
            "requires_reboot": False,
            "resident_on": "OpaqueRef:NULL",
            "shutdown_delay": args.get("shutdown_delay", "0"),
            "snapshot_info": {},
            "snapshot_metadata": "",
            "snapshot_of": "OpaqueRef:NULL",
            "snapshot_schedule": args.get("snapshot_schedule", "OpaqueRef:NULL"),
            "snapshot_time": datetime.now(),
            "snapshots": [],
            "start_delay": args.get("start_delay", "0"),
            "suspend_SR": args.get("suspend_SR", "OpaqueRef:NULL"),
            "suspend_VDI": "OpaqueRef:NULL",
            "tags": args.get("tags", []),
            "transportable_snapshot_id": "",
            "user_version": args.get("user_version", "0"),
            "uuid": str(uuid.uuid4()),
            "version": args.get("version", "0"),
            "xenstore_data": args.get("xenstore_data", {}),
        }

        self._check_param_type(VM_new['HVM_boot_params'], 'struct', 'HVM_boot_params')
        self._check_param_type(VM_new['HVM_boot_policy'], 'string', 'HVM_boot_policy')
        self._check_param_type(VM_new['HVM_shadow_multiplier'], 'double', 'HVM_shadow_multiplier')
        self._check_param_type(VM_new['PCI_bus'], 'string', 'PCI_bus')
        self._check_param_type(VM_new['PV_args'], 'string', 'PV_args')
        self._check_param_type(VM_new['PV_bootloader'], 'string', 'PV_bootloader')
        self._check_param_type(VM_new['PV_bootloader_args'], 'string', 'PV_bootloader_args')
        self._check_param_type(VM_new['PV_kernel'], 'string', 'PV_kernel')
        self._check_param_type(VM_new['PV_legacy_args'], 'string', 'PV_legacy_args')
        self._check_param_type(VM_new['PV_ramdisk'], 'string', 'PV_ramdisk')
        self._check_param_type(VM_new['VCPUs_at_startup'], 'int', 'VCPUs_at_startup')
        self._check_param_type(VM_new['VCPUs_max'], 'int', 'VCPUs_max')
        self._check_param_type(VM_new['VCPUs_params'], 'struct', 'VCPUs_params')
        self._check_param_type(VM_new['actions_after_crash'], 'string', 'actions_after_crash')
        self._check_param_type(VM_new['actions_after_reboot'], 'string', 'actions_after_reboot')
        self._check_param_type(VM_new['actions_after_shutdown'], 'string', 'actions_after_shutdown')
        self._check_param_type(VM_new['affinity'], 'ref', 'affinity')
        self._check_param_type(VM_new['appliance'], 'ref', 'appliance')
        self._check_param_type(VM_new['blocked_operations'], 'struct', 'blocked_operations')
        self._check_param_type(VM_new['domain_type'], 'string', 'domain_type')
        self._check_param_type(VM_new['generation_id'], 'string', 'generation_id')
        self._check_param_type(VM_new['ha_always_run'], 'boolean', 'ha_always_run')
        self._check_param_type(VM_new['ha_restart_priority'], 'string', 'ha_restart_priority')
        self._check_param_type(VM_new['hardware_platform_version'], 'int', 'hardware_platform_version')
        self._check_param_type(VM_new['has_vendor_device'], 'boolean', 'has_vendor_device')
        self._check_param_type(VM_new['is_a_template'], 'boolean', 'is_a_template')
        self._check_param_type(VM_new['is_snapshot_from_vmpp'], 'boolean', 'is_snapshot_from_vmpp')
        self._check_param_type(VM_new['is_vmss_snapshot'], 'boolean', 'is_vmss_snapshot')
        self._check_param_type(VM_new['memory_dynamic_max'], 'int', 'memory_dynamic_max')
        self._check_param_type(VM_new['memory_dynamic_min'], 'int', 'memory_dynamic_min')
        self._check_param_type(VM_new['memory_static_max'], 'int', 'memory_static_max')
        self._check_param_type(VM_new['memory_static_min'], 'int', 'memory_static_min')
        self._check_param_type(VM_new['memory_target'], 'int', 'memory_target')
        self._check_param_type(VM_new['name_description'], 'string', 'name_description')
        self._check_param_type(VM_new['name_label'], 'string', 'name_label')
        self._check_param_type(VM_new['other_config'], 'struct', 'other_config')
        self._check_param_type(VM_new['platform'], 'struct', 'platform')
        self._check_param_type(VM_new['protection_policy'], 'ref', 'protection_policy')
        self._check_param_type(VM_new['recommendations'], 'string', 'recommendations')
        self._check_param_type(VM_new['reference_label'], 'string', 'reference_label')
        self._check_param_type(VM_new['shutdown_delay'], 'int', 'shutdown_delay')
        self._check_param_type(VM_new['snapshot_schedule'], 'ref', 'snapshot_schedule')
        self._check_param_type(VM_new['start_delay'], 'int', 'start_delay')
        self._check_param_type(VM_new['suspend_SR'], 'ref', 'suspend_SR')
        self._check_param_type(VM_new['tags'], 'array', 'tags')
        self._check_param_type(VM_new['user_version'], 'int', 'user_version')
        self._check_param_type(VM_new['version'], 'int', 'version')
        self._check_param_type(VM_new['xenstore_data'], 'struct', 'xenstore_data')

        required_fields = [
            "user_version",
            "is_a_template",
            "affinity",
            "memory_static_max",
            "memory_dynamic_max",
            "memory_dynamic_min",
            "memory_static_min",
            "VCPUs_params",
            "VCPUs_max",
            "VCPUs_at_startup",
            "actions_after_shutdown",
            "actions_after_reboot",
            "actions_after_crash",
            "PV_bootloader",
            "PV_kernel",
            "PV_ramdisk",
            "PV_args",
            "PV_bootloader_args",
            "PV_legacy_args",
            "HVM_boot_policy",
            "HVM_boot_params",
            "platform",
            "PCI_bus",
            "other_config",
            "recommendations",
        ]

        for field in required_fields:
            if not field in args:
                raise xenapi_exception(['FIELD_MISSING', field])

        VM_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[VM_ref] = VM_new

        return VM_ref

    def destroy(self, VM_ref):
        self._check_param_type(VM_ref, 'ref')
        self._check_obj_ref(VM_ref)

        del self.objs[VM_ref]

    def get_allowed_VBD_devices(self, VM_ref):
        self._check_param_type(VM_ref, 'ref')
        self._check_obj_ref(VM_ref)

        # Do nothing for now.
        return []

    def get_allowed_VIF_devices(self, VM_ref):
        self._check_param_type(VM_ref, 'ref')
        self._check_obj_ref(VM_ref)

        # Do nothing for now.
        return []

    def get_possible_hosts(self, VM_ref):
        self._check_param_type(VM_ref, 'ref')
        self._check_obj_ref(VM_ref)

        # Do nothing for now.
        return []

    def hard_reboot(self, VM_ref):
        self._check_param_type(VM_ref, 'ref')
        self._check_obj_ref(VM_ref)

        # Do nothing for now.

    def hard_shutdown(self, VM_ref):
        self._check_param_type(VM_ref, 'ref')
        self._check_obj_ref(VM_ref)

        # Do nothing for now.

    def migrate_send(self, VM_ref, dest, live, vdi_map, vif_map, options, vgpu_map):
        self._check_param_type(VM_ref, 'ref')
        self._check_param_type(dest, 'struct', 'dest')
        self._check_param_type(live, 'boolean', 'live')
        self._check_param_type(vdi_map, 'struct', 'vdi_map')
        self._check_param_type(vif_map, 'struct', 'vif_map')
        self._check_param_type(options, 'struct', 'options')
        self._check_param_type(vgpu_map, 'struct', 'vgpu_map')

        self._check_obj_ref(VM_ref)

        # Do nothing for now.

    def pause(self, VM_ref):
        self._check_param_type(VM_ref, 'ref')
        self._check_obj_ref(VM_ref)

        # Do nothing for now.

    def pool_migrate(self, VM_ref, host_ref, options):
        self._check_param_type(VM_ref, 'ref')
        self.xenapi.host._check_param_type(host_ref, 'ref')
        self._check_param_type(options, 'struct', 'options')

        self._check_obj_ref(VM_ref)
        self.xenapi.host._check_obj_ref(host_ref)

        # Do nothing for now.

    def power_state_reset(self, VM_ref):
        self._check_param_type(VM_ref, 'ref')
        self._check_obj_ref(VM_ref)

        self.objs[VM_ref]['power_state'] = "Halted"

    def provision(self, VM_ref):
        self._check_param_type(VM_ref, 'ref')
        self._check_obj_ref(VM_ref)

        # Do nothing for now.

    def resume(self, VM_ref, start_paused, force):
        self._check_param_type(VM_ref, 'ref')
        self._check_param_type(start_paused, 'boolean', 'start_paused')
        self._check_param_type(force, 'boolean', 'force')

        self._check_obj_ref(VM_ref)

        # Do nothing for now.

    def resume_on(self, VM_ref, host_ref, start_paused, force):
        self._check_param_type(VM_ref, 'ref')
        self.xenapi.host._check_param_type(host_ref, 'ref')
        self._check_param_type(start_paused, 'boolean', 'start_paused')
        self._check_param_type(force, 'boolean', 'force')

        self._check_obj_ref(VM_ref)
        self.xenapi.host._check_obj_ref(host_ref)

        # Do nothing for now.

    def revert(self, VM_ref):
        self._check_param_type(VM_ref, 'ref')
        self._check_obj_ref(VM_ref)

        # Do nothing for now.

    def set_VCPUs_number_live(self, VM_ref, nvcpu):
        self._check_param_type(VM_ref, 'ref')
        self._check_param_type(nvcpu, 'int', 'nvcpu')

        self._check_obj_ref(VM_ref)

        self.objs[VM_ref]['VCPUs_at_startup'] = nvcpu
        self.objs[VM_ref]['VCPUs_max'] = nvcpu

    def set_memory(self, VM_ref, value):
        self._check_param_type(VM_ref, 'ref')
        self._check_param_type(value, 'int', 'value')

        self._check_obj_ref(VM_ref)

        self.objs[VM_ref]['memory_static_max'] = value
        self.objs[VM_ref]['memory_dynamic_max'] = value
        self.objs[VM_ref]['memory_dynamic_min'] = value

    def set_memory_dynamic_range(self, VM_ref, min, ):
        self._check_param_type(VM_ref, 'ref')
        self._check_param_type(min, 'int', 'min')
        self._check_param_type(max, 'int', 'max')

        self._check_obj_ref(VM_ref)

        self.objs[VM_ref]['memory_dynamic_max'] = max
        self.objs[VM_ref]['memory_dynamic_min'] = min

    def set_memory_limits(self, VM_ref, static_min, static_max, dynamic_min, dynamic_max):
        self._check_param_type(VM_ref, 'ref')
        self._check_param_type(static_min, 'int', 'static_min')
        self._check_param_type(static_max, 'int', 'static_max')
        self._check_param_type(dynamic_min, 'int', 'dynamic_min')
        self._check_param_type(dynamic_max, 'int', 'dynamic_max')

        self._check_obj_ref(VM_ref)

        # Do nothing for now.

    def set_memory_static_range(self, VM_ref, min, ):
        self._check_param_type(VM_ref, 'ref')
        self._check_param_type(min, 'int', 'min')
        self._check_param_type(max, 'int', 'max')

        self._check_obj_ref(VM_ref)

        self.objs[VM_ref]['memory_static_max'] = max
        self.objs[VM_ref]['memory_static_min'] = min

    def shutdown(self, VM_ref):
        self._check_param_type(VM_ref, 'ref')
        self._check_obj_ref(VM_ref)

        # Do nothing for now.

    def snapshot(self, VM_ref, new_name):
        self._check_param_type(VM_ref, 'ref')
        self._check_param_type(new_name, 'string', 'new_name')

        self._check_obj_ref(VM_ref)

        # Do nothing for now.
        return VM_ref

    def start(self, VM_ref, start_paused, force):
        self._check_param_type(VM_ref, 'ref')
        self._check_param_type(start_paused, 'boolean', 'start_paused')
        self._check_param_type(force, 'boolean', 'force')

        self._check_obj_ref(VM_ref)

        # Do nothing for now.

    def start_on(self, VM_ref, host_ref, start_paused, force):
        self._check_param_type(VM_ref, 'ref')
        self.xenapi.host._check_param_type(host_ref, 'ref')
        self._check_param_type(start_paused, 'boolean', 'start_paused')
        self._check_param_type(force, 'boolean', 'force')

        self._check_obj_ref(VM_ref)
        self.xenapi.host._check_obj_ref(host_ref)

        # Do nothing for now.

    def suspend(self, VM_ref):
        self._check_param_type(VM_ref, 'ref')
        self._check_obj_ref(VM_ref)

        # Do nothing for now.

    def unpause(self, VM_ref):
        self._check_param_type(VM_ref, 'ref')
        self._check_obj_ref(VM_ref)

        # Do nothing for now.

    def update_allowed_operations(self, VM_ref):
        self._check_param_type(VM_ref, 'ref')
        self._check_obj_ref(VM_ref)

        # Do nothing for now.
