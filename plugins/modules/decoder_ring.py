#!/usr/bin/python

# SPDX-License-Identifier: MIT
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: decoder_ring

author:
  - Tim Way (@timway)

short_description: Helps name resources deterministically

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: 0.0.1

description: >-
  It helps to have a documented and automated way to determine the name for
  resources in an environment. This module takes in a variety of information
  deemed relavent to our fictional environment to deterministically provide
  the same name for that set of inputs reliably.
'''

EXAMPLES = r'''
- name: Determine the name for a resource
  chipy.decoder_ring.decoder_ring:
    building_id: building01
'''
