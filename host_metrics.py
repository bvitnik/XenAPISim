#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, Bojan Vitnik <bvitnik@mainstream.rs>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import print_function

import uuid
from datetime import datetime

from xenapi_object import xenapi_object

class host_metrics(xenapi_object):
    """XenAPI host_metrics class.

    Attributes:
    """

    def __init__(self, xenapi):
        """Inits host_metrics class.

        Args:
        """
        super(host_metrics, self).__init__(xenapi)

        self.field_def.update({
            "last_updated": datetime.now(),
            "live": True,
            "memory_free": "0",
            "memory_total": "0",
        })

        host_metrics_new = {
            "last_updated": datetime.now(),
            "live": True,
            "memory_free": "0",
            "memory_total": "0",
            "other_config": {},
            "uuid": str(uuid.uuid4()),
        }

        host_metrics_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[host_metrics_ref] = host_metrics_new
