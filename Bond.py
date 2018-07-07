#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, Bojan Vitnik <bvitnik@mainstream.rs>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import print_function

import uuid

from xenapi_object import xenapi_object
from xenapi_exception import xenapi_exception


class Bond(xenapi_object):
    """XenAPI Bond class.

    Attributes:
    """

    def __init__(self, xenapi):
        """Inits Bond class.

        Args:
        """
        super(Bond, self).__init__(xenapi)

        self.field_def.update({
            "links_up": "0",
            "master": "OpaqueRef:NULL",
            "mode": "balance-slb",
            "primary_slave": "OpaqueRef:NULL",
            "properties": {},
            "slaves": [],
        })

        self.rw_fields.extend([
            "mode",
        ])

        Bond_new = {
            "links_up": "2",
            "master": "OpaqueRef:NULL",
            "mode": "balance-slb",
            "other_config": {},
            "primary_slave": "OpaqueRef:NULL",
            "properties": {},
            "slaves": ["OpaqueRef:NULL", "OpaqueRef:NULL"],
            "uuid": str(uuid.uuid4()),
        }

        Bond_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[Bond_ref] = Bond_new

    def create(self,
               network_ref,
               members,
               MAC,
               mode,
               properties):
        self.xenapi.network._check_param_type(network_ref, 'ref')
        self._check_param_type(members, 'array', 'members')
        self._check_param_type(MAC, 'string', 'MAC')
        self._check_param_type(mode, 'string', 'mode')
        self._check_param_type(properties, 'struct', 'properties')

        Bond_new = {
            "links_up": "2",
            "master": "OpaqueRef:NULL",
            "mode": "balance-slb",
            "other_config": {},
            "primary_slave": members[0],
            "properties": properties,
            "slaves": members,
            "uuid": str(uuid.uuid4()),
        }

        Bond_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[Bond_ref] = Bond_new

        return Bond_ref

    def destroy(self, Bond_ref):
        self._check_param_type(Bond_ref, 'ref')
        self._check_obj_ref(Bond_ref)

        del self.objs[Bond_ref]

    def set_property(self, Bond_ref, name, value):
        self._check_param_type(Bond_ref, 'ref')
        self._check_param_type(name, 'string', 'name')
        self._check_param_type(value, 'string', 'value')

        self._check_obj_ref(Bond_ref)

        Bond = self.objs[Bond_ref]

        Bond['properties'].update({name: value})
