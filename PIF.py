#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, Bojan Vitnik <bvitnik@mainstream.rs>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import print_function

import uuid

from xenapi_object import xenapi_object
from xenapi_exception import xenapi_exception


class PIF(xenapi_object):
    """XenAPI PIF class.

    Attributes:
    """

    def __init__(self, xenapi, host_ref):
        """Inits PIF class.

        Args:
        """
        super(PIF, self).__init__(xenapi)

        self.field_def.update({
            "DNS": "",
            "IP": "",
            "IPv6": [],
            "MAC": "",
            "MTU": "0",
            "PCI": "OpaqueRef:NULL",
            "VLAN": "0",
            "VLAN_master_of": "OpaqueRef:NULL",
            "VLAN_slave_of": [],
            "bond_master_of": [],
            "bond_slave_of": "OpaqueRef:NULL",
            "capabilities": [],
            "currently_attached": True,
            "device": "",
            "disallow_unplug": False,
            "gateway": "",
            "host": "OpaqueRef:NULL",
            "igmp_snooping_status": "unknown",
            "ip_configuration_mode": "None",
            "ipv6_configuration_mode": "None",
            "ipv6_gateway": "",
            "managed": True,
            "management": False,
            "metrics": "OpaqueRef:NULL",
            "netmask": "",
            "network": "OpaqueRef:NULL",
            "physical": False,
            "primary_address_type": "IPv4",
            "properties": {},
            "sriov_logical_PIF_of": [],
            "sriov_physical_PIF_of": [],
            "tunnel_access_PIF_of": [],
            "tunnel_transport_PIF_of": [],
        })

        self.rw_fields.extend([
            "disallow_unplug",
            "primary_address_type",
        ])

        self.unimplemented_methods.extend([
            "create_VLAN",
            "destroy",
            "scan",
        ])

        PIF_new = {
            "DNS": "127.0.0.254",
            "IP": "127.0.0.1",
            "IPv6": [],
            "MAC": "aa:bb:cc:dd:ee:ff",
            "MTU": "1500",
            "PCI": "OpaqueRef:NULL",
            "VLAN": "-1",
            "VLAN_master_of": "OpaqueRef:NULL",
            "VLAN_slave_of": [],
            "bond_master_of": [],
            "bond_slave_of": "OpaqueRef:NULL",
            "capabilities": [],
            "currently_attached": True,
            "device": "eth0",
            "disallow_unplug": False,
            "gateway": "127.0.0.254",
            "host": host_ref,
            "igmp_snooping_status": "unknown",
            "ip_configuration_mode": "Static",
            "ipv6_configuration_mode": "None",
            "ipv6_gateway": "",
            "managed": True,
            "management": True,
            "metrics": "OpaqueRef:NULL",
            "netmask": "255.255.255.0",
            "network": "OpaqueRef:NULL",
            "other_config": {},
            "physical": True,
            "primary_address_type": "IPv4",
            "properties": {'gro': 'on'},
            "sriov_logical_PIF_of": [],
            "sriov_physical_PIF_of": [],
            "tunnel_access_PIF_of": [],
            "tunnel_transport_PIF_of": [],
            "uuid": str(uuid.uuid4()),
        }

        PIF_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[PIF_ref] = PIF_new

    def db_forget(self, PIF_ref):
        self.forget(PIF_ref)

    def db_introduce(self,
                     device,
                     network_ref,
                     host_ref,
                     MAC,
                     MTU,
                     VLAN,
                     physical,
                     ip_configuration_mode,
                     IP,
                     netmask,
                     gateway,
                     DNS,
                     bond_slave_of,
                     VLAN_master_of,
                     management,
                     other_config,
                     disallow_unplug,
                     ipv6_configuration_mode,
                     IPv6,
                     ipv6_gateway,
                     primary_address_type,
                     managed,
                     properties):
        self._check_param_type(device, 'string', 'device')
        self.xenapi.network._check_param_type(network_ref, 'ref')
        self.xenapi.host._check_param_type(host_ref, 'ref')
        self._check_param_type(MAC, 'string', 'MAC')
        self._check_param_type(MTU, 'int', 'MTU')
        self._check_param_type(VLAN, 'int', 'VLAN')
        self._check_param_type(physical, 'boolean', 'physical')
        self._check_param_type(ip_configuration_mode, 'string', 'ip_configuration_mode')
        self._check_param_type(IP, 'string', 'IP')
        self._check_param_type(netmask, 'string', 'netmask')
        self._check_param_type(gateway, 'string', 'gateway')
        self._check_param_type(DNS, 'string', 'DNS')
        self.xenapi.Bond._check_param_type(bond_slave_of_ref, 'ref', 'bond_slave_of')
        # self.xenapi.VLAN._check_param_type(VLAN_master_of_ref, 'ref', 'VLAN_master_of')
        self._check_param_type(management, 'boolean', 'management')
        self._check_param_type(other_config, 'struct', 'other_config')
        self._check_param_type(disallow_unplug, 'boolean', 'disallow_unplug')
        self._check_param_type(ipv6_configuration_mode, 'string', 'ipv6_configuration_mode')
        self._check_param_type(IPv6, 'string', 'IPv6')
        self._check_param_type(ipv6_gateway, 'string', 'ipv6_gateway')
        self._check_param_type(primary_address_type, 'string', 'primary_address_type')
        self._check_param_type(managed, 'boolean', 'managed')
        self._check_param_type(properties, 'struct', 'properties')

        self.xenapi.network._check_obj_ref(network_ref)
        self.xenapi.host._check_obj_ref(host_ref)
        self.xenapi.Bond._check_obj_ref(bond_slave_of_ref)
        # self.xenapi.VLAN._check_obj_ref(VLAN_master_of_ref)

        PIF_new = {
            "DNS": DNS,
            "IP": IP,
            "IPv6": IPv6,
            "MAC": MAC,
            "MTU": MTU,
            "PCI": "OpaqueRef:NULL",
            "VLAN": VLAN,
            "VLAN_master_of": VLAN_master_of_ref,
            "VLAN_slave_of": [],
            "bond_master_of": [],
            "bond_slave_of": bond_slave_of_ref,
            "capabilities": [],
            "currently_attached": True,
            "device": device,
            "disallow_unplug": disallow_unplug,
            "gateway": gateway,
            "host": host_ref,
            "igmp_snooping_status": "unknown",
            "ip_configuration_mode": ip_configuration_mode,
            "ipv6_configuration_mode": ipv6_configuration_mode,
            "ipv6_gateway": ipv6_gateway,
            "managed": managed,
            "management": management,
            "metrics": "OpaqueRef:NULL",
            "netmask": netmask,
            "network": network_ref,
            "other_config": {},
            "physical": physical,
            "primary_address_type": primary_address_type,
            "properties": properties,
            "sriov_logical_PIF_of": [],
            "sriov_physical_PIF_of": [],
            "tunnel_access_PIF_of": [],
            "tunnel_transport_PIF_of": [],
            "uuid": str(uuid.uuid4()),
        }

        PIF_ref = "OpaqueRef:%s" % str(uuid.uuid4())

        self.objs[PIF_ref] = PIF_new

        return PIF_ref

    def forget(self, PIF_ref):
        self._check_param_type(PIF_ref, 'ref')
        self._check_obj_ref(PIF_ref)

        del self.objs[PIF_ref]

    def introduce(self, host_ref, MAC, device, managed):
        self.xenapi.host._check_param_type(host_ref, 'ref')
        self._check_param_type(MAC, 'string', 'MAC')
        self._check_param_type(device, 'string', 'device')
        self._check_param_type(managed, 'boolean', 'managed')

        PIF_new = {
            "DNS": "",
            "IP": "",
            "IPv6": "",
            "MAC": MAC,
            "MTU": "1500",
            "PCI": "OpaqueRef:NULL",
            "VLAN": "-1",
            "VLAN_master_of": "OpaqueRef:NULL",
            "VLAN_slave_of": [],
            "bond_master_of": [],
            "bond_slave_of": "OpaqueRef:NULL",
            "capabilities": [],
            "currently_attached": True,
            "device": device,
            "disallow_unplug": False,
            "gateway": "",
            "host": host_ref,
            "igmp_snooping_status": "unknown",
            "ip_configuration_mode": "None",
            "ipv6_configuration_mode": "None",
            "ipv6_gateway": "",
            "managed": managed,
            "management": False,
            "metrics": "OpaqueRef:NULL",
            "netmask": "",
            "network": "OpaqueRef:NULL",
            "other_config": {},
            "physical": True,
            "primary_address_type": "IPv4",
            "properties": {},
            "sriov_logical_PIF_of": [],
            "sriov_physical_PIF_of": [],
            "tunnel_access_PIF_of": [],
            "tunnel_transport_PIF_of": [],
            "uuid": str(uuid.uuid4()),
        }

        self.objs[PIF_ref] = PIF_new

        return PIF_ref

    def plug(self, PIF_ref):
        self._check_param_type(PIF_ref, 'ref')
        self._check_obj_ref(PIF_ref)

        self.objs[PIF_ref]['currently_attached'] = True

    def reconfigure_ip(self, PIF_ref, mode, IP, netmask, gateway, DNS):
        self._check_param_type(PIF_ref, 'ref')
        self._check_param_type(mode, 'string', 'mode')
        self._check_param_type(IP, 'string', 'IP')
        self._check_param_type(netmask, 'string', 'netmask')
        self._check_param_type(gateway, 'string', 'gateway')
        self._check_param_type(DNS, 'string', 'DNS')

        self._check_obj_ref(PIF_ref)

        PIF = self.objs[PIF_ref]

        PIF['ip_configuration_mode'] = mode
        PIF['IP'] = IP
        PIF['netmask'] = netmask
        PIF['gateway'] = gateway
        PIF['DNS'] = DNS

    def reconfigure_ipv6(self, PIF_ref, mode, IPv6, gateway, DNS):
        self._check_param_type(PIF_ref, 'ref')
        self._check_param_type(mode, 'string', 'mode')
        self._check_param_type(IPv6, 'string', 'IPv6')
        self._check_param_type(gateway, 'string', 'gateway')
        self._check_param_type(DNS, 'string', 'DNS')

        self._check_obj_ref(PIF_ref)

        PIF = self.objs[PIF_ref]

        PIF['ipv6_configuration_mode'] = mode
        PIF['IPv6'] = IP
        PIF['ipv6_gateway'] = gateway
        PIF['DNS'] = DNS

    def set_property(self, PIF_ref, name, value):
        self._check_param_type(PIF_ref, 'ref')
        self._check_param_type(name, 'string', 'name')
        self._check_param_type(value, 'string', 'value')

        self._check_obj_ref(PIF_ref)

        PIF = self.objs[PIF_ref]

        PIF['properties'].update({name: value})

    def unplug(self, PIF_ref):
        self._check_param_type(PIF_ref, 'ref')
        self._check_obj_ref(PIF_ref)

        self.objs[PIF_ref]['currently_attached'] = False
