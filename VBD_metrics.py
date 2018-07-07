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


class VBD_metrics(xenapi_object):
    """XenAPI VBD_metrics class.

    Attributes:
    """

    def __init__(self, xenapi):
        """Inits VBD_metrics class.

        Args:
        """
        super(VBD_metrics, self).__init__(xenapi)

        self.field_def.update({
            "io_read_kbs": 0.0,
            "io_write_kbs": 0.0,
            "last_updated": datetime.now(),
        })

        VBD_metrics_new = {
            "io_read_kbs": 0.0,
            "io_write_kbs": 0.0,
            "last_updated": datetime.now(),
            "other_config": {},
            "uuid": str(uuid.uuid4()),
        }

        VBD_metrics_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[VBD_metrics_ref] = VBD_metrics_new
