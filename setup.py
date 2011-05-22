#
#  setup.py for easyzone package
#
#  Created by Chris Miles on 2007-01-29.
#  Copyright (c) 2007-2011 Chris Miles. All rights reserved.
#

try:
    from setuptools import setup, Command
    use_setuptools = True
except ImportError:
    from distutils.core import setup, Command
    use_setuptools = False

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
    


setup_args = dict(
    name = 'easyzone',
    version = __version__,
    author = 'Chris Miles',
    author_email = 'miles.chris@gmail.com',
    description = 'Easy Zone - DNS Zone abstraction module',
    long_description = '''\
easyzone
========

Overview
--------

Easyzone is a package to manage the common record types of a
zone file, including SOA records.  This module sits on top of
the dnspython package and provides a higher level abstraction
for common zone file manipulation use cases.

http://www.psychofx.com/easyzone/
http://pypi.python.org/pypi/easyzone
https://bitbucket.org/chrismiles/easyzone/


Main features:

* A high-level abstraction on top of dnspython.
* Load a zone file into objects.
* Modify/add/delete zone/record objects.
* Save back to zone file.
* Auto-update serial (if necessary).


Requirements
------------

  * dnspython - http://www.dnspython.org/


Build/Test/Install
------------------

Build::

  $ python setup.py build

Test::

  $ python setup.py test

Install::

  $ python setup.py install


OR with setuptools::

  $ easy_install easyzone


Examples
--------

easyzone::

  >>> from easyzone import easyzone
  >>> z = easyzone.zone_from_file('example.com', '/var/namedb/example.com')
  >>> z.domain
  'example.com.'
  >>> z.root.soa.serial
  2007012902L
  >>> z.root.records('NS').items
  ['ns1.example.com.', 'ns2.example.com.']
  >>> z.root.records('MX').items
  [(10, 'mail.example.com.'), (20, 'mail2.example.com.')]
  >>> z.names['foo.example.com.'].records('A').items
  ['10.0.0.1']

  >>> ns = z.root.records('NS')
  >>> ns.add('ns3.example.com.')
  >>> ns.items
  ['ns1.example.com.', 'ns2.example.com.', 'ns3.example.com.']
  >>> ns.delete('ns2.example.com')
  >>> ns.items
  ['ns1.example.com.', 'ns3.example.com.']

  >>> z.save(autoserial=True)

ZoneCheck::

  >>> from easyzone.zone_check import ZoneCheck
  >>> c = ZoneCheck()
  >>> c.isValid('example.com', '/var/named/zones/example.com')
  True
  >>> c.isValid('foo.com', '/var/named/zones/example.com')
  False
  >>> c.error
  'Bad syntax'
  >>> 
  >>> c = ZoneCheck(checkzone='/usr/sbin/named-checkzone')
  >>> c.isValid('example.com', '/var/named/zones/example.com')
  True
  >>>

ZoneReload::

  >>> from easyzone.zone_reload import ZoneReload
  >>> r = ZoneReload()
  >>> r.reload('example.com')
  zone reload up-to-date
  >>> r.reload('foo.com')
  rndc: 'reload' failed: not found
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "easyzone/zone_reload.py", line 51, in reload
      raise ZoneReloadError("rndc failed with return code %d" % r)
  easyzone.zone_reload.ZoneReloadError: rndc failed with return code 1
  >>> 
  >>> r = ZoneReload(rndc='/usr/sbin/rndc')
  >>> r.reload('example.com')
  zone reload up-to-date
  >>>
''',
    url = 'http://www.psychofx.com/easyzone/',
    packages = ['easyzone'],
    cmdclass = { 'test': TestCommand, 'clean': CleanCommand },
)

if use_setuptools:
    setup_args.update(dict(
        classifiers=[
            "Development Status :: 4 - Beta",
            "License :: OSI Approved :: MIT License",
            "Topic :: Internet :: Name Service (DNS)",
            "Topic :: System :: Systems Administration",
        ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        keywords='',
        license='MIT',
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            # -*- Extra requirements: -*-
            "dnspython",
        ],
        entry_points="""
        # -*- Entry points: -*-
        """,
    ))

setup(**setup_args)
