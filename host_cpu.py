#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, Bojan Vitnik <bvitnik@mainstream.rs>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import print_function

import uuid

from xenapi_object import xenapi_object

class host_cpu(xenapi_object):
    """XenAPI host_cpu class.

    Attributes:
    """

    def __init__(self, xenapi, host_ref):
        """Inits host_cpu class.

        Args:
        """
        super(host_cpu, self).__init__(xenapi)

        self.field_def.update({
            "family": "0",
            "features": "",
            "flags": "",
            "host": "OpaqueRef:NULL",
            "model": "0",
            "modelname": "",
            "number": "0",
            "speed": "0",
            "stepping": "",
            "utilisation": 0.0,
            "vendor": "",
        })

        host_cpu_new = {
            "family": "0",
            "features": "",
            "flags": "",
            "host": host_ref,
            "model": "0",
            "modelname": "",
            "number": "0",
            "other_config": {},
            "speed": "0",
            "stepping": "",
            "uuid": str(uuid.uuid4()),
            "utilisation": 0.0,
            "vendor": "",
        }

        host_cpu_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[host_cpu_ref] = host_cpu_new
