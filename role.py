#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, Bojan Vitnik <bvitnik@mainstream.rs>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import print_function

import uuid

from xenapi_object import xenapi_object

class role(xenapi_object):
    """XenAPI role class.

    Attributes:
    """

    def __init__(self, xenapi, host_ref):
        """Inits role class.

        Args:
        """
        super(role, self).__init__(xenapi)

        self.field_def.update({
            "name_description": "",
            "name_label": "",
            "subroles": "OpaqueRef:NULL",
            "uuid": ,
        })

        # role_new = {
        #     "name_description": "",
        #     "name_label": "",
        #     "subroles": "OpaqueRef:NULL",
        #     "uuid": str(uuid.uuid4()),
        # }

        # role_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        # self.objs[role_ref] = role_new
