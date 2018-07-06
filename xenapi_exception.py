#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, Bojan Vitnik <bvitnik@mainstream.rs>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import print_function

class xenapi_exception(Exception):
    """Basic class for XenAPI exception handling."""

    def __init__(self, details):
        """Inits XenAPI exception.

        Args:
            details (list): List containing XenAPI error code as first
                element and other XenAPI error dependant info as other
                elements.
        """
        self.details = details
