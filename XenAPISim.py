#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, Bojan Vitnik <bvitnik@mainstream.rs>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import print_function

from six.moves.xmlrpc_server import SimpleXMLRPCServer

from xenapi import xenapi

bind_address = "localhost"
bind_port = 8080

# Use SimpleXMLRPCServer to serve XenAPI.
xapi_server = SimpleXMLRPCServer((bind_address, bind_port))
xapi_server.register_instance(xenapi())
xapi_server.register_introspection_functions()
xapi_server.serve_forever()
