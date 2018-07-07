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


class task(xenapi_object):
    """XenAPI task class.

    Attributes:
    """

    def __init__(self, xenapi):
        """Inits task class.

        Args:
        """
        super(task, self).__init__(xenapi)

        self.field_def.update({
            "allowed_operations": [],
            "backtrace": "",
            "created": datetime.now(),
            "current_operations": {},
            "error_info": [],
            "finished": datetime.now(),
            "name_description": "",
            "name_label": "",
            "progress": 0.0,
            "resident_on": "OpaqueRef:NULL",
            "result": "",
            "status": "pending",
            "subtask_of": "OpaqueRef:NULL",
            "subtasks": [],
            "type": "",
        })

        self.rw_fields.extend([
            "status",
        ])

        task_new = {
            "allowed_operations": ["cancel", "destroy"],
            "backtrace": "()",
            "created": datetime.now(),
            "current_operations": {},
            "error_info": [],
            "finished": None,
            "name_description": "",
            "name_label": "",
            "other_config": {},
            "progress": 0.0,
            "resident_on": "OpaqueRef:NULL",
            "result": "",
            "status": "pending",
            "subtask_of": "OpaqueRef:NULL",
            "subtasks": [],
            "type": "",
            "uuid": str(uuid.uuid4()),
        }

        task_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[task_ref] = task_new

    def cancel(self, task_ref):
        self._check_param_type(task_ref, 'ref')
        self._check_obj_ref(task_ref)

        if not "cancel" in self.objs[task_ref]['allowed_operations']:
            raise xenapi_exception(['OPERATION_NOT_ALLOWED', 'Task cannot be caneceled!'])

        # do nothing for now

    def create(self, label, description):
        self._check_param_type(label, 'string', 'label')
        self._check_param_type(description, 'string', 'description')

        task_new = {
            "allowed_operations": ["cancel", "destroy"],
            "backtrace": "()",
            "created": datetime.now(),
            "current_operations": {},
            "error_info": [],
            "finished": None,
            "name_description": description,
            "name_label": label,
            "other_config": {},
            "progress": 0.0,
            "resident_on": "OpaqueRef:NULL",
            "result": "",
            "status": "pending",
            "subtask_of": "OpaqueRef:NULL",
            "subtasks": [],
            "type": "",
            "uuid": str(uuid.uuid4()),
        }

        task_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[task_ref] = task_new

        return task_ref

    def destroy(self, task_ref):
        self._check_param_type(task_ref, 'ref')
        self._check_obj_ref(task_ref)

        del self.objs[task_ref]
