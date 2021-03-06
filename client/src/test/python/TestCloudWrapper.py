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

import unittest
import base64
import shutil
import os

from mock import Mock

from slipstream.ConfigHolder import ConfigHolder
from slipstream.wrappers.CloudWrapper import CloudWrapper
from slipstream.util import CONFIGPARAM_CONNECTOR_MODULE_NAME
from slipstream.NodeDecorator import KEY_RUN_CATEGORY, RUN_CATEGORY_DEPLOYMENT

from TestCloudConnectorsBase import TestCloudConnectorsBase


class TestCloudWrapper(TestCloudConnectorsBase):

    def setUp(self):
        self.serviceurl = 'http://example.com'
        self.configHolder = ConfigHolder(
            {
                'username': base64.b64encode('user'),
                'password': base64.b64encode('pass'),
                'cookie_filename': 'cookies',
                'serviceurl': self.serviceurl
            },
            context={'foo': 'bar'},
            config={'foo': 'bar'})

        os.environ['SLIPSTREAM_CONNECTOR_INSTANCE'] = 'Test'

    def tearDown(self):
        os.environ.pop('SLIPSTREAM_CONNECTOR_INSTANCE')
        self.configHolder = None
        shutil.rmtree('%s/.cache/' % os.getcwd(), ignore_errors=True)

    def test_getCloudName(self):
        for module_name in self.get_cloudconnector_modulenames():
            setattr(self.configHolder, CONFIGPARAM_CONNECTOR_MODULE_NAME, module_name)
            setattr(self.configHolder, KEY_RUN_CATEGORY, RUN_CATEGORY_DEPLOYMENT)
            cw = CloudWrapper(self.configHolder)
            cw.initCloudConnector()

            assert cw.getCloudInstanceName() == 'Test'

    def test_putImageId(self):
        self.configHolder.set(CONFIGPARAM_CONNECTOR_MODULE_NAME,
                              self.get_cloudconnector_modulename_by_cloudname('local'))
        cw = CloudWrapper(self.configHolder)
        cw.initCloudConnector()

        cw.clientSlipStream.httpClient._call = Mock(return_value=('', ''))

        cw._updateSlipStreamImage('module/Name', 'ABC')
        cw.clientSlipStream.httpClient._call.assert_called_with(
            '%s/module/Name/Test' % self.serviceurl,
            'PUT', 'ABC', 'application/xml',
            'application/xml')

if __name__ == "__main__":
    unittest.main()
