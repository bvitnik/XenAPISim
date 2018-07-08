#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, Bojan Vitnik <bvitnik@mainstream.rs>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import print_function

import uuid

from xenapi_object import xenapi_object
from xenapi_exception import xenapi_exception


class VLAN(xenapi_object):
    """XenAPI VLAN class.

    Attributes:
    """

    def __init__(self, xenapi):
        """Inits VLAN class.

        Args:
        """
        super(VLAN, self).__init__(xenapi)

        self.field_def.update({
            "tag": "-1",
            "tagged_PIF": "OpaqueRef:NULL",
            "untagged_PIF": "OpaqueRef:NULL",
        })

        VLAN_new = {
            "other_config": {},
            "tag": "0",
            "tagged_PIF": "OpaqueRef:NULL",
            "untagged_PIF": "OpaqueRef:NULL",
            "uuid": str(uuid.uuid4()),
        }

        VLAN_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[VLAN_ref] = VLAN_new

    def create(self, PIF_ref, tag, network_ref):
        self.xenapi.PIF._check_param_type(PIF_ref, 'ref')
        self._check_param_type(tag, 'int', 'tag')
        self.xenapi.network._check_param_type(network_ref, 'ref')

        # Do nothing for now.

    def destroy(self, VLAN_ref):
        self._check_param_type(VLAN_ref, 'ref')
        self._check_obj_ref(VLAN_ref)

        del self.objs[VLAN_ref]
