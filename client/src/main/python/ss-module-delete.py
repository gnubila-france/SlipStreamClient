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

import sys
import os
from optparse import OptionParser

from slipstream.CommandBase import CommandBase
from slipstream.HttpClient import HttpClient   
from slipstream.ConfigHolder import ConfigHolder
import slipstream.util as util


class MainProgram(CommandBase):
    '''A command-line program to delete module definition(s).'''
    
    def __init__(self, argv=None):
        self.module = ''
        self.username = None
        self.password = None
        self.cookie = None
        self.endpoint = None
        super(MainProgram, self).__init__(argv)

    def parse(self):
        usage = '''usage: %prog [options] [<module-url>]

<module-uri>    Name of the module to delete. For example 
                Public/Tutorials/HelloWorld/client_server/1. If a version
                is provided (at the end of the module name) this specific
                version will be deleted, otherwise that last version will
                be delete.  If several versions exists, this command must
                be called repeatedly.'''

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

        self.options, self.args = self.parser.parse_args()

        self._checkArgs()

    def _checkArgs(self):
        if len(self.args) == 1:
            self.module = self.args[0]
        if len(self.args) > 1:
            self.usageExitTooManyArguments()
            
    def doWork(self):
        client = HttpClient(self.options.username, self.options.password)
        client.verboseLevel = self.verboseLevel

        uri = util.MODULE_URL_PATH
        if self.module:
            uri += '/' + self.module

        url = self.options.endpoint + uri

        client.delete(url)

if __name__ == "__main__":
    try:
        MainProgram()
    except KeyboardInterrupt:
        print '\n\nExecution interrupted by the user... goodbye!'
        sys.exit(-1)
