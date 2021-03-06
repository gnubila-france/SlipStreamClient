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
import sys

from slipstream.CommandBase import CommandBase
from slipstream.HttpClient import HttpClient
import slipstream.util as util
import slipstream.SlipStreamHttpClient as SlipStreamHttpClient

class MainProgram(CommandBase):
    '''A command-line program to show/list module definition(s).'''

    def __init__(self, argv=None):
        self.module = ''
        self.username = None
        self.password = None
        self.cookie = None
        self.endpoint = None
        super(MainProgram, self).__init__(argv)

    def parse(self):
        usage = '''usage: %prog [options] [<module-xml>]

<module-xml>    XML rendering of the module to update (e.g. as produced by ss-module-get).
                For example: ./ss-module-put "`cat module.xml`"'''

        self.parser.usage = usage

        self.parser.add_option('-u','--username', dest='username',
                               help='SlipStream username', metavar='USERNAME',
                               default=os.environ.get('SLIPSTREAM_USERNAME'))
        self.parser.add_option('-p','--password', dest='password',
                               help='SlipStream password', metavar='PASSWORD',
                               default=os.environ.get('SLIPSTREAM_PASSWORD'))

        self.parser.add_option('--cookie', dest='cookieFilename',
                               help='SlipStream cookie', metavar='FILE',
                               default=os.environ.get('SLIPSTREAM_COOKIEFILE',
                                                      os.path.join(util.TMPDIR, 'cookie')))

        self.parser.add_option('--endpoint', dest='endpoint',
                               help='SlipStream server endpoint', metavar='URL',
                               default=os.environ.get('SLIPSTREAM_ENDPOINT', 'http://slipstream.sixsq.com'))

        self.parser.add_option('-i','--ifile', dest='ifile',
                               help='Optional input file. Replaces <module-xml> argument', metavar='FILE')

        self.options, self.args = self.parser.parse_args()

        self._checkArgs()

    def _checkArgs(self):
        if self.options.ifile:
            file = self.options.ifile
        else:
            if len(self.args) < 1:
                self.parser.error('Missing module-xml')
            if len(self.args) > 1:
                self.usageExitTooManyArguments()
            file = self.args[0]
        self.module = self.read_input_file(file)

    def doWork(self):
        client = HttpClient(self.options.username, self.options.password)
        client.verboseLevel = self.verboseLevel

        dom = self.read_xml_and_exit_on_error(self.module)
        attrs = SlipStreamHttpClient.DomExtractor.getAttributes(dom)

        root_node_name = dom.tag
        if root_node_name == 'list':
            sys.stderr.write('Cannot update root project\n')
            sys.exit(-1)
        if not dom.tag in ('imageModule', 'projectModule', 'deploymentModule'):
            sys.stderr.write('Invalid xml\n')
            sys.exit(-1)

        parts = [attrs['parentUri'], attrs['shortName']]
        uri = '/' + '/'.join([part.strip('/') for part in parts])

        url = self.options.endpoint + uri

        client.put(url, self.module)

if __name__ == "__main__":
    try:
        MainProgram()
    except KeyboardInterrupt:
        print '\n\nExecution interrupted by the user... goodbye!'
        sys.exit(-1)
