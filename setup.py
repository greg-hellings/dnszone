#
#  setup.py for easyzone package
#
#  Created by Chris Miles on 2007-01-29.
#  Copyright (c) 2007 Chris Miles. All rights reserved.
#

from distutils.core import setup, Command
from glob import glob
import os
import sys
from unittest import TextTestRunner, TestLoader

from easyzone.easyzone import __version__


class TestCommand(Command):
    user_options = []
    
    def initialize_options(self):
        self._dir = os.getcwd()
    
    def finalize_options(self):
        build = self.get_finalized_command('build')
        self.build_purelib = build.build_purelib
        self.build_platlib = build.build_platlib
    
    def run(self):
        '''Finds all the tests modules in tests/, and runs them.
        '''
        sys.path.insert(0, self.build_purelib)
        sys.path.insert(0, self.build_platlib)
        
        testfiles = []
        for t in glob(os.path.join(self._dir, 'tests', '*.py')):
            if not t.endswith('__init__.py'):
                testfiles.append('.'.join(
                    ['tests', os.path.splitext(os.path.basename(t))[0]])
                )
        
        tests = TestLoader().loadTestsFromNames(testfiles)
        t = TextTestRunner(verbosity = 2)
        t.run(tests)
    

class CleanCommand(Command):
    user_options = []
    
    def initialize_options(self):
        self._clean_me = []
        for root, dirs, files in os.walk('.'):
            for f in files:
                if f.endswith('.pyc'):
                    self._clean_me.append(os.path.join(root, f))
    
    def finalize_options(self):
        pass
    
    def run(self):
        for clean_me in self._clean_me:
            try:
                os.unlink(clean_me)
            except:
                pass
    


setup(
    name = 'easyzone',
    version = __version__,
    author = 'Chris Miles',
    author_email = 'miles.chris@gmail.com',
    description = 'Easy Zone - DNS Zone abstraction module',
    long_description = '''\
A module to manage the common record types of a zone file,
including SOA records.  This module sits on top of the
dnspython package and provides a higher level abstraction
for common zone file manipulation use cases.
''',
    url = 'http://www.python.org/',
    packages = ['easyzone'],
    cmdclass = { 'test': TestCommand, 'clean': CleanCommand }
)

