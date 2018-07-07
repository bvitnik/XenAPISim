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


class PIF_metrics(xenapi_object):
    """XenAPI PIF_metrics class.

    Attributes:
    """

    def __init__(self, xenapi):
        """Inits PIF_metrics class.

        Args:
        """
        super(PIF_metrics, self).__init__(xenapi)

        self.field_def.update({
            "carrier": True,
            "device_id": "",
            "device_name": "",
            "duplex": True,
            "io_read_kbs": 0.0,
            "io_write_kbs": 0.0,
            "last_updated": datetime.now(),
            "pci_bus_path": "",
            "speed": "0",
            "vendor_id": "",
            "vendor_name": "",
        })

        PIF_metrics_new = {
            "carrier": True,
            "device_id": "",
            "device_name": "XenAPISim NIC",
            "duplex": True,
            "io_read_kbs": 0.0,
            "io_write_kbs": 0.0,
            "last_updated": datetime.now(),
            "other_config": {},
            "pci_bus_path": "0000:00:00.0",
            "speed": "10000",
            "uuid": str(uuid.uuid4()),
            "vendor_id": "",
            "vendor_name": "XenAPISim",
        }

        PIF_metrics_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[PIF_metrics_ref] = PIF_metrics_new
