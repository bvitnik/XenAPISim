#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, Bojan Vitnik <bvitnik@mainstream.rs>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import print_function

import uuid

from xenapi_object import xenapi_object
from xenapi_exception import xenapi_exception


class PCI(xenapi_object):
    """XenAPI PCI class.

    Attributes:
    """

    def __init__(self, xenapi, host_ref):
        """Inits PCI class.

        Args:
        """
        super(PCI, self).__init__(xenapi)

        self.field_def.update({
            "class_name": "",
            "dependencies": [],
            "device_name": "",
            "driver_name": "",
            "host": "OpaqueRef:NULL",
            "pci_id": "",
            "subsystem_device_name": "",
            "subsystem_vendor_name": "",
            "vendor_name": "",
        })

        PCI_new = {
            "class_name": "Ethernet controller",
            "dependencies": [],
            "device_name": "XenAPISim NIC",
            "driver_name": "",
            "host": host_ref,
            "other_config": {},
            "pci_id": "0000:00:00.0",
            "subsystem_device_name": "XenAPISim 10Gb Adapter",
            "subsystem_vendor_name": "XenAPISim",
            "uuid": str(uuid.uuid4()),
            "vendor_name": "XenAPISim",
        }

        PCI_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[PCI_ref] = PCI_new
