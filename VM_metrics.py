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


class VM_metrics(xenapi_object):
    """XenAPI VM_metrics class.

    Attributes:
    """

    def __init__(self, xenapi):
        """Inits VM_metrics class.

        Args:
        """
        super(VM_metrics, self).__init__(xenapi)

        self.field_def.update({
            "VCPUs_CPU": {},
            "VCPUs_flags": {},
            "VCPUs_number": "0",
            "VCPUs_params": {},
            "VCPUs_utilisation": {},
            "current_domain_type": "unspecified",
            "hvm": False,
            "install_time": datetime.now(),
            "last_updated": datetime.now(),
            "memory_actual": "0",
            "nested_virt": False,
            "nomigrate": False,
            "start_time": datetime.now(),
            "state": [],
        })

        VM_metrics_new = {
            "VCPUs_CPU": {},
            "VCPUs_flags": {},
            "VCPUs_number": "1",
            "VCPUs_params": {},
            "VCPUs_utilisation": {},
            "current_domain_type": "unspecified",
            "hvm": True,
            "install_time": datetime.now(),
            "last_updated": datetime.now(),
            "memory_actual": "10477371392",
            "nested_virt": False,
            "nomigrate": False,
            "other_config": {},
            "start_time": datetime.now(),
            "state": [],
            "uuid": str(uuid.uuid4()),
        }

        VM_metrics_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[VM_metrics_ref] = VM_metrics_new
