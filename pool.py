#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, Bojan Vitnik <bvitnik@mainstream.rs>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import print_function

import uuid
from datetime import datetime
from six import string_types

from xenapi_object import xenapi_object
from xenapi_exception import xenapi_exception


class pool(xenapi_object):
    """XenAPI pool class.

    Attributes:
    """

    def __init__(self, xenapi, host_ref):
        """Inits pool class.

        Args:
        """
        super(pool, self).__init__(xenapi)

        self.field_def.update({
            "allowed_operations": [],
            "blobs": {},
            "cpu_info": {},
            "crash_dump_SR": "OpaqueRef:NULL",
            "current_operations": {},
            "default_SR": "OpaqueRef:NULL",
            "guest_agent_config": {},
            "gui_config": {},
            "ha_allow_overcommit": False,
            "ha_cluster_stack": "",
            "ha_configuration": {},
            "ha_enabled": False,
            "ha_host_failures_to_tolerate": "0",
            "ha_overcommitted": False,
            "ha_plan_exists_for": "0",
            "ha_statefiles": [],
            "health_check_config": {},
            "igmp_snooping_enabled": False,
            "live_patching_disabled": False,
            "master": "OpaqueRef:NULL",
            "metadata_VDIs": [],
            "name_description": "",
            "name_label": "",
            "policy_no_vendor_device": False,
            "redo_log_enabled": False,
            "redo_log_vdi": "OpaqueRef:NULL",
            "restrictions": {},
            "suspend_image_SR": "OpaqueRef:NULL",
            "tags": [],
            "vswitch_controller": "",
            "wlb_enabled": False,
            "wlb_url": "",
            "wlb_username": "",
            "wlb_verify_cert": False,
        })

        self.rw_fields.extend([
            "crash_dump_sr",
            "default_SR",
            "gui_config",
            "ha_allow_overcommit",
            "health_check_config",
            "live_patching_disabled",
            "name_description",
            "name_label",
            "policy_no_vendor_device",
            "suspend_image_SR",
            "tags",
            "wlb_enabled",
            "wlb_verify_cert"
        ])

        self.list_fields.extend([
            "tags",
        ])

        self.map_fields.extend([
            "guest_agent_config",
            "gui_config",
            "health_check_config",
        ])

        self.unimplemented_methods.extend([
            "apply_edition",
            "certificate_install",
            "certificate_list",
            "certificate_sync",
            "certificate_uninstall",
            "create_VLAN",
            "create_VLAN_from_PIF",
            "create_new_blob",
            "crl_install",
            "crl_list",
            "crl_uninstall",
            "deconfigure_wlb",
            "detect_nonhomogeneous_external_auth",
            "disable_external_auth",
            "disable_ha",
            "disable_local_storage_caching",
            "disable_redo_log",
            "disable_ssl_legacy",
            "emergency_reset_master",
            "emergency_transition_to_master",
            "enable_external_auth",
            "enable_ha",
            "enable_local_storage_caching",
            "enable_redo_log",
            "enable_ssl_legacy",
            "ha_compute_hypothetical_max_host_failures_to_tolerate",
            "ha_compute_max_host_failures_to_tolerate",
            "ha_compute_vm_failover_plan",
            "ha_failover_plan_exists",
            "ha_prevent_restarts_for",
            "has_extension",
            "initialize_wlb",
            "join",
            "join_force",
            "management_reconfigure",
            "recover_slaves",
            "retrieve_wlb_configuration",
            "retrieve_wlb_recommendations",
            "send_test_post",
            "send_wlb_configuration",
            "sync_database",
            "test_archive_target",
        ])

        pool_new = {
            "allowed_operations": ['ha_enable'],
            "blobs": {},
            "cpu_info": {},
            "crash_dump_SR": "OpaqueRef:NULL",
            "current_operations": {},
            "default_SR": "OpaqueRef:NULL",
            "guest_agent_config": {},
            "gui_config": {},
            "ha_allow_overcommit": False,
            "ha_cluster_stack": "xhad",
            "ha_configuration": {},
            "ha_enabled": False,
            "ha_host_failures_to_tolerate": "0",
            "ha_overcommitted": False,
            "ha_plan_exists_for": "0",
            "ha_statefiles": [],
            "health_check_config": {},
            "igmp_snooping_enabled": False,
            "live_patching_disabled": False,
            "master": host_ref,
            "metadata_VDIs": [],
            "name_description": "",
            "name_label": "xenserver-pool",
            "other_config": {},
            "policy_no_vendor_device": False,
            "redo_log_enabled": False,
            "redo_log_vdi": "OpaqueRef:NULL",
            "restrictions": {},
            "suspend_image_SR": "OpaqueRef:NULL",
            "tags": [],
            "uuid": str(uuid.uuid4()),
            "vswitch_controller": "",
            "wlb_enabled": False,
            "wlb_url": "",
            "wlb_username": "",
            "wlb_verify_cert": False,
        }

        pool_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[pool_ref] = pool_new

    def designate_new_master(self, host_ref):
        self.xenapi.host._check_param_type(network_ref, 'ref')
        self.xenapi.host._check_obj_ref(network_ref)

        pool_ref = self.objs.keys()[0]
        self.objs[pool_ref]['master'] = host_ref

    def eject(self, host_ref):
        self.xenapi.host.destroy(host_ref)

    def get_license_state(self, pool_ref):
        self._check_param_type(pool_ref, 'ref')
        self._check_obj_ref(pool_ref)

        return {'edition': 'enterprise-per-socket', 'expiry': 'never'}
