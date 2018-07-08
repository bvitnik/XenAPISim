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


class host(xenapi_object):
    """XenAPI host class.

    Attributes:
    """

    def __init__(self, xenapi, host_ref, dom0_vm_ref):
        """Inits host class.

        Args:
        """
        super(host, self).__init__(xenapi)

        self.field_def.update({
            "API_version_major": "0",
            "API_version_minor": "0",
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
            "memory_overhead": "0",
            "metrics": "OpaqueRef:NULL",
            "multipathing": False,
            "name_description": "",
            "name_label": "",
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
        ])

        self.unimplemented_methods.extend([
            "apply_edition",
            "assert_can_evacuate",
            "backup_rrds",
            "bugreport_upload",
            "call_extension",
            "call_plugin",
            "create_new_blob",
            "declare_dead",
            "disable_display",
            "disable_external_auth",
            "disable_local_storage_caching",
            "dmesg",
            "dmesg_clear",
            "emergency_ha_disable",
            "enable_display",
            "enable_external_auth",
            "enable_local_storage_caching",
            "evacuate",
            "forget_data_source_archives",
            "get_data_sources",
            "get_log",
            "get_server_certificate",
            "get_uncooperative_resident_VMs",
            "get_vms_which_prevent_evacuation",
            "has_extension",
            "license_add",
            "license_remove",
            "list_methods",
            "local_management_reconfigure",
            "management_disable",
            "management_reconfigure",
            "migrate_receive",
            "power_on",
            "query_data_source",
            "reboot",
            "record_data_source",
            "refresh_pack_info",
            "reset_cpu_features",
            "restart_agent",
            "retrieve_wlb_evacuate_recommendations",
            "send_debug_keys",
            "set_cpu_features",
            "set_power_on_mode",
            "shutdown",
            "shutdown_agent",
            "sync_data",
            "syslog_reconfigure",
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
            "edition": "enterprise-per-socket",
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
            "software_version": {'product_version': '7.5.0', 'product_version_text_short': '7.5', 'product_version_text': '7.5'},
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

    def compute_free_memory(self, host_ref):
        self._check_param_type(host_ref, 'ref')
        self._check_obj_ref(host_ref)

        time.sleep(20)

        return "0"

    def compute_memory_overhead(self, host_ref):
        self._check_param_type(host_ref, 'ref')
        self._check_obj_ref(host_ref)

        return "0"

    def destroy(self, host_ref):
        self._check_param_type(host_ref, 'ref')
        self._check_obj_ref(host_ref)

        del self.objs[host_ref]

    def disable(self, host_ref):
        self._check_param_type(host_ref, 'ref')
        self._check_obj_ref(host_ref)

        self.objs[host_ref]['enabled'] = False

    def enable(self, host_ref):
        self._check_param_type(host_ref, 'ref')
        self._check_obj_ref(host_ref)

        self.objs[host_ref]['enabled'] = True

    def get_management_interface(self, host_ref):
        self._check_param_type(host_ref, 'ref')
        self._check_obj_ref(host_ref)

        obj = self.objs[host_ref]

        if obj['PIFs']:
            return obj['PIFs'][0]

    def get_server_localtime(self, host_ref):
        self._check_param_type(host_ref, 'ref')
        self._check_obj_ref(host_ref)

        return datetime.now()

    def get_servertime(self, host_ref):
        self._check_param_type(host_ref, 'ref')
        self._check_obj_ref(host_ref)

        return datetime.utcnow()

    def get_system_status_capabilities(self, host_ref):
        self._check_param_type(host_ref, 'ref')
        self._check_obj_ref(host_ref)

        return ""

    def set_hostname_live(self, host_ref, hostname):
        self.set_hostname(host_ref, hostname)
