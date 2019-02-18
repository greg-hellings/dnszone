#
#  setup.py for dnszone package
#
#  Created by Greg Hellings on 2019-02-18
#  Copyright (c) 2019 Greg Hellings. All rights reserved.
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

here = os.path.dirname(__file__)
with open(os.path.join(here, 'dnszone', 'dnszone.py')) as f:
    for line in f:
        if line.startswith('__version__ = '):
            __version__ = line.split(' = ')[-1].strip(" '\"\n")


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
        t = TextTestRunner(verbosity=2)
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
            except Exception:
                pass


setup_args = dict(
    name='dnszone',
    version=__version__,
    author='Greg Hellings',
    author_email='greg.hellings@gmail.com',
    description='Easy Zone - DNS Zone abstraction module',
    long_description='''\
dnszone
========

Overview
--------

DNSZone is a package to manage the common record types of a
zone file, including SOA records.  This module sits on top of
the dnspython package and provides a higher level abstraction
for common zone file manipulation use cases.

http://pypi.python.org/pypi/dnszone
https://github.come/greg-hellings/dnszone


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

  $ easy_install dnszone


Examples
--------

dnszone::

  >>> from dnszone import dnszone
  >>> z = dnszone.zone_from_file('example.com', '/var/namedb/example.com')
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

  >>> from dnszone.zone_check import ZoneCheck
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

  >>> from dnszone.zone_reload import ZoneReload
  >>> r = ZoneReload()
  >>> r.reload('example.com')
  zone reload up-to-date
  >>> r.reload('foo.com')
  rndc: 'reload' failed: not found
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "dnszone/zone_reload.py", line 51, in reload
      raise ZoneReloadError("rndc failed with return code %d" % r)
  dnszone.zone_reload.ZoneReloadError: rndc failed with return code 1
  >>>
  >>> r = ZoneReload(rndc='/usr/sbin/rndc')
  >>> r.reload('example.com')
  zone reload up-to-date
  >>>
''',
    url='https://github.com/greg-hellings/dnszone',
    packages=['dnszone'],
    cmdclass={'test': TestCommand, 'clean': CleanCommand},
)

if use_setuptools:
    setup_args.update(dict(
        classifiers=[
            "Development Status :: 4 - Beta",
            "License :: OSI Approved :: MIT License",
            "Topic :: Internet :: Name Service (DNS)",
            "Topic :: System :: Systems Administration",
        ],
        keywords='',
        license='MIT',
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            # -*- Extra requirements: -*-
            "dnspython",
            "six",
        ],
        entry_points="""
        # -*- Entry points: -*-
        """,
    ))

setup(**setup_args)
