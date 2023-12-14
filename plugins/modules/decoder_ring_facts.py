#!/usr/bin/python

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: decoder_ring

author:
  - Tim Way (@timway)

short_description: Helps name resources deterministically

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

import dmw_decoder
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.parameters import env_fallback


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        api_key=dict(type='str', fallback=(env_fallback, ['DMW_DECODER_API_KEY']), required=True),
        building_id=dict(type='str', required=True),
	component=dict(type='str', required=True),
	device_function=dict(type='str', required=True),
	entity=dict(type='str', required=True),
    )
    
    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    decoder = dmw_decoder.Decoder(
        api_key=module.params['api_key']
    )
    dmw_decoder_hostname = decoder.create_netbios_compatible_name(
        module.params["building_id"],
        module.params["device_function"],
        module.params["entity"],
        module.params["component"],
    )

    result = dict(
        ansible_facts=dict(
            dmw_decoder_hostname=dmw_decoder_hostname
        ),
        changed=False,
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    #if module.check_mode:
    #    module.exit_json(**result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
