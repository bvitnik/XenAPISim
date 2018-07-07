#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, Bojan Vitnik <bvitnik@mainstream.rs>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import print_function

import uuid

from xenapi_object import xenapi_object
from xenapi_exception import xenapi_exception


class network(xenapi_object):
    """XenAPI network class.

    Attributes:
    """

    def __init__(self, xenapi):
        """Inits network class.

        Args:
        """
        super(network, self).__init__(xenapi)

        self.field_def.update({
            "MTU": "0",
            "PIFs": [],
            "VIFs": [],
            "allowed_operations": [],
            "assigned_ips": {},
            "blobs": {},
            "bridge": "",
            "current_operations": {},
            "default_locking_mode": "",
            "managed": True,
            "name_description": "",
            "name_label": "",
            "purpose": [],
            "tags": [],
        })

        self.rw_fields.extend([
            "MTU",
            "name_description",
            "name_label",
            "tags",
        ])

        self.list_fields.extend([
            "purpose",
            "tags",
        ])

        self.bridge_num_next = 1

        network_new = {
            "MTU": "1500",
            "PIFs": [],
            "VIFs": [],
            "allowed_operations": [],
            "assigned_ips": {},
            "blobs": {},
            "bridge": "xenapi",
            "current_operations": {},
            "default_locking_mode": "unlocked",
            "managed": True,
            "name_description": 'Network on which guests will be assigned a private link-local IP address which can be used to talk XenAPI',
            "name_label": 'Host internal management network',
            "other_config": {
                'is_guest_installer_network': 'true',
                'netmask': '255.255.0.0',
                'is_host_internal_management_network': 'true',
                'ip_begin': '169.254.0.1',
                'ip_end': '169.254.255.254'
            },
            "purpose": [],
            "tags": [],
            "uuid": str(uuid.uuid4()),
        }

        network_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[network_ref] = network_new

    def create(self, args):
        self._check_param_type(args, 'struct')

        network_new = {
            "MTU": args.get("MTU", "1500"),
            "PIFs": [],
            "VIFs": [],
            "allowed_operations": [],
            "assigned_ips": {},
            "blobs": {},
            "bridge": args.get("bridge", "xapi%s" % bridge_num_next),
            "current_operations": {},
            "default_locking_mode": "unlocked",
            "managed": args.get("managed", True),
            "name_description": args.get("name_description", ""),
            "name_label": args.get("name_label", ""),
            "other_config": args.get("other_config", {}),
            "purpose": [],
            "tags": args.get("tags", []),
            "uuid": str(uuid.uuid4()),
        }

        self._check_param_type(network_new['MTU'], 'int', 'MTU')
        self._check_param_type(network_new['bridge'], 'string', 'bridge')
        self._check_param_type(network_new['managed'], 'boolean', 'managed')
        self._check_param_type(network_new['name_description'], 'string', 'name_description')
        self._check_param_type(network_new['name_label'], 'string', 'name_label')
        self._check_param_type(network_new['other_config'], 'struct', 'other_config')
        self._check_param_type(network_new['tags'], 'array', 'tags')

        if not "other_config" in args:
            raise xenapi_exception(['FIELD_MISSING', 'other_config'])

        network_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[network_ref] = network_new

        bridge_num_next += 1

        return network_ref

    def destroy(self, network_ref):
        self._check_param_type(network_ref, 'ref')
        self._check_obj_ref(network_ref)

        del self.objs[network_ref]
