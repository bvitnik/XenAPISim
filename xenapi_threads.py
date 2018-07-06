#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, Bojan Vitnik <bvitnik@mainstream.rs>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import print_function

import threading, time


class expire_sessions_thread(threading.Thread):
    """Thread class that is used to expire old sessions.

    Attributes:
        session: Reference to session class.
    """

    def __init__(self, thread_name, xenapi):
        """Inits session expire thread.

        Args:
            thread_name (str): Thread name.
            xenapi: Reference to xenapi object for accessing other class
                methods.
        """
        super(expire_sessions_thread, self).__init__(name=thread_name)

        self.xenapi = xenapi

    def run(self):
        """Overriden Thread.run() method.

        Calls xenapi.session._expire_old_sessions() every 5 minutes to
        expire old sessions.
        """
        while True:
            if self.xenapi:
                self.xenapi.session._expire_old_sessions()

            time.sleep(300)
