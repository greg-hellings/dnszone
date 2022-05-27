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
with open(os.path.join(here, 'README.md')) as f:
    readme_lines = []
    for line in f:
        readme_lines.append(line)


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
    long_description=str("\n").join(readme_lines),
    long_description_content_type="text/markdown",
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
            "dnspython<2",
            "six",
        ],
        entry_points="""
        # -*- Entry points: -*-
        """,
    ))

setup(**setup_args)
