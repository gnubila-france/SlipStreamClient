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

from distutils.core import setup

VERSION = '1.3-1'
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: Unix",
    "Operating System :: Microsoft :: Windows",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Topic :: Software Development :: Libraries :: Python Modules"
]

setup(name='slipstream-client',
      version=VERSION,
      description='SlipStream end-user client (CLI)',
      long_description='SlipStream client (CLI) to communicate with SlipStream server.',
      author='SixSq Sarl, (sixsq.com)',
      author_email='info@sixsq.com',
      license='Apache License, Version 2.0',
      platforms='Any',
      url='http://sixsq.com',

      scripts = ['bin/ss-abort',
                 'bin/ss-display',
                 'bin/ss-execute',
                 'bin/ss-get',
                 'bin/ss-set',
                 'bin/ss-module-get',
                 'bin/ss-module-put',
                 'bin/ss-run-get',
                 'bin/ss-user-get'],

      packages = ['slipstream',
                  'slipstream.contextualizers',
                  'slipstream.contextualizers.dummy'],

      package_dir = {'slipstream': 'lib/slipstream'},

      py_modules = ['slipstream.ConfigHolder',    
                    'slipstream.contextualizers.ContextualizerFactory',
                    'slipstream.CommandBase',
                    'slipstream.Client',
                    'slipstream.exceptions.Exceptions',
                    'slipstream.NodeDecorator',
                    'slipstream.HttpClient',
                    'slipstream.SlipStreamHttpClient',
                    'slipstream.util',
                    'slipstream.__version__'],
        
      requires=['httplib2'],

      classifiers=CLASSIFIERS
      )
