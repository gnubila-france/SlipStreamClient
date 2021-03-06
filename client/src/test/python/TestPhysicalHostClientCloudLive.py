#!/usr/bin/env python
"""
 SlipStream Client
 =====
 Copyright (C) 2013 SixSq Sarl (sixsq.com)
 =====
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import os
import unittest

from slipstream.cloudconnectors.physicalhost.PhysicalHostClientCloud import PhysicalHostClientCloud
from slipstream.ConfigHolder import ConfigHolder
from slipstream.SlipStreamHttpClient import UserInfo
from slipstream import util

CONFIG_FILE = os.path.join(os.path.dirname(__file__),
                           'pyunit.credentials.properties')
# Example configuration file.
"""
[Test]
physicalhost.private.key =
physicalhost.password = test
physicalhost.username = test
physicalhost.hosta = 192.168.1.101
physicalhost.hostb = 192.168.1.102
PHYSICALHOST_ORCHESTRATOR_HOST = 192.168.1.100
"""


class TestPhysicalHostClientCloud(unittest.TestCase):
    def setUp(self):

        os.environ['SLIPSTREAM_CONNECTOR_INSTANCE'] = 'physicalhost'
        os.environ['SLIPSTREAM_BOOTSTRAP_BIN'] = 'http://example.com/bootstrap'
        os.environ['SLIPSTREAM_DIID'] = '00000000-0000-0000-0000-000000000000'

        if not os.path.exists(CONFIG_FILE):
            raise Exception('Configuration file %s not found.' % CONFIG_FILE)

        self.ch = ConfigHolder(configFile=CONFIG_FILE, context={'foo': 'bar'})

        os.environ['PHYSICALHOST_ORCHESTRATOR_HOST'] = self.ch.config['PHYSICALHOST_ORCHESTRATOR_HOST']

        self.client = PhysicalHostClientCloud(self.ch)

        self.user_info = UserInfo('physicalhost')
        self.user_info['physicalhost.private.key'] = self.ch.config['physicalhost.private.key']
        self.user_info['physicalhost.password'] = self.ch.config['physicalhost.password']
        self.user_info['physicalhost.username'] = self.ch.config['physicalhost.username']
        hosta = self.ch.config['physicalhost.hosta']
        hostb = self.ch.config['physicalhost.hostb']

        self.nodes_info = [
            {
                'multiplicity': 1,
                'nodename': 'test_node_a',
                'image': {
                    'cloud_parameters': {
                        'physicalhost': {},
                        'Cloud': {
                            'network': 'private'
                        }
                    },
                    'attributes': {
                        'imageId': hosta,
                        'platform': 'Ubuntu'
                    },
                    'targets': {
                        'prerecipe':
"""#!/bin/sh
set -e
set -x

ls -l /tmp
dpkg -l | egrep "nano|lvm" || true
""",
                        'recipe':
"""#!/bin/sh
set -e
set -x

dpkg -l | egrep "nano|lvm" || true
lvs
""",
                        'packages': ['lvm2', 'nano']
                    }
                },
            }, {
                'multiplicity': 1,
                'nodename': 'test_node_b',
                'image': {
                    'cloud_parameters': {
                        'physicalhost': {},
                        'Cloud': {
                            'network': 'private'
                        }
                    },
                    'attributes': {
                        'imageId': hostb,
                        'platform': 'Ubuntu'
                    },
                    'targets': {
                        'prerecipe':
"""#!/bin/sh
set -e
set -x

ls -l /tmp
dpkg -l | egrep "nano|lvm" || true
""",
                        'recipe':
"""#!/bin/sh
set -e
set -x

dpkg -l | egrep "nano|lvm" || true
lvs
""",
                        'packages': ['lvm2', 'nano']
                    }
                },
            }]

    def tearDown(self):
        os.environ.pop('SLIPSTREAM_CONNECTOR_INSTANCE')
        os.environ.pop('SLIPSTREAM_BOOTSTRAP_BIN')
        self.client = None
        self.ch = None

    def xtest_1_startStopImages(self):

        self.client.startNodesAndClients(self.user_info, self.nodes_info)

        util.printAndFlush('Instances started')

        vms = self.client.getVms()
        assert len(vms) == 3

        # You need to put a breakpoint on the next line and manually check /tmp/slipstream* on the two nodes
        self.client.stopDeployment()


if __name__ == '__main__':
    unittest.main()
