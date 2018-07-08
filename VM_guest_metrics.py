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


class VM_guest_metrics(xenapi_object):
    """XenAPI VM_guest_metrics class.

    Attributes:
    """

    def __init__(self, xenapi):
        """Inits VM_guest_metrics class.

        Args:
        """
        super(VM_guest_metrics, self).__init__(xenapi)

        self.field_def.update({
            "PV_drivers_detected": False,
            "PV_drivers_up_to_date": False,
            "PV_drivers_version": {},
            "can_use_hotplug_vbd": "unspecified",
            "can_use_hotplug_vif": "unspecified",
            "disks": {},
            "last_updated": datetime.now(),
            "live": False,
            "memory": {},
            "networks": {},
            "os_version": {},
            "other": {},
        })

        VM_guest_metrics_new = {
            "PV_drivers_detected": True,
            "PV_drivers_up_to_date": True,
            "PV_drivers_version": {"micro": "0", "major": "6", "build": "59235", "minor": "1"},
            "can_use_hotplug_vbd": "unspecified",
            "can_use_hotplug_vif": "unspecified",
            "disks": {},
            "last_updated": datetime.now(),
            "live": True,
            "memory": {},
            "networks": {},
            "os_version": {},
            "other": {},
            "other_config": {},
            "uuid": str(uuid.uuid4()),
        }

        VM_guest_metrics_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[VM_guest_metrics_ref] = VM_guest_metrics_new
