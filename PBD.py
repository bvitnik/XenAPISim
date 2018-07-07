#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, Bojan Vitnik <bvitnik@mainstream.rs>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import print_function

import uuid

from xenapi_object import xenapi_object
from xenapi_exception import xenapi_exception


class PBD(xenapi_object):
    """XenAPI PBD class.

    Attributes:
    """

    def __init__(self, xenapi, host_ref):
        """Inits PBD class.

        Args:
        """
        super(PBD, self).__init__(xenapi)

        self.field_def.update({
            "SR": "OpaqueRef:NULL",
            "currently_attached": True,
            "device_config": {},
            "host": "OpaqueRef:NULL",
        })

        self.rw_fields.extend([
            "device_config",
        ])

        self.map_fields.extend([
            "device_config",
        ])

        PBD_new = {
            "SR": "OpaqueRef:%s" % str(uuid.uuid4()),
            "currently_attached": True,
            "device_config": {'location': '/dev/xapi/block'},
            "host": host_ref,
            "other_config": {},
            "uuid": str(uuid.uuid4()),
        }

        PBD_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[PBD_ref] = PBD_new

    def create(self, args):
        self._check_param_type(args, 'struct')

        PBD_new = {
            "SR": args.get("SR", "OpaqueRef:NULL"),
            "currently_attached": True,
            "device_config": args.get("device_config", {}),
            "host": args.get("host", "OpaqueRef:NULL"),
            "other_config": args.get("other_config", {}),
            "uuid": str(uuid.uuid4()),
        }


        # self.xenapi.SR._check_param_type(PBD_new['SR'], 'ref')
        self._check_param_type(PBD_new['device_config'], 'struct', 'device_config')
        self.xenapi.host._check_param_type(PBD_new['host'], 'ref')
        self._check_param_type(PBD_new['other_config'], 'struct', 'other_config')

        for field in ["host", "SR", "device_config"]:
            if not field in args:
                raise xenapi_exception(['FIELD_MISSING', field])

        PBD_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[PBD_ref] = PBD_new

        return PBD_ref

    def destroy(self, PBD_ref):
        self._check_param_type(PBD_ref, 'ref')
        self._check_obj_ref(PBD_ref)

        del self.objs[PBD_ref]

    def plug(self, PBD_ref):
        self._check_param_type(PBD_ref, 'ref')
        self._check_obj_ref(PBD_ref)

        self.objs[PBD_ref]['currently_attached'] = True

    def unplug(self, PBD_ref):
        self._check_param_type(PBD_ref, 'ref')
        self._check_obj_ref(PBD_ref)

        self.objs[PBD_ref]['currently_attached'] = False
