#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013, 2014, 2015, 2016 Kevin Reid and the ShinySDR contributors
#
# This file is part of ShinySDR.
# 
# ShinySDR is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# ShinySDR is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with ShinySDR.  If not, see <http://www.gnu.org/licenses/>.

import urllib
import subprocess

from setuptools import find_packages, setup, Command

ASSETS = {
    'http://requirejs.org/docs/release/2.1.22/comments/require.js': 'shinysdr/deps/require.js',
    'https://raw.githubusercontent.com/requirejs/text/646db27aaf2236cea92ac4107f32cbe5ae7a8d3a/text.js': 'shinysdr/deps/text.js'
}


class DownloadAssets(Command):
    """Support setup.py retrieving assets from external sites"""

    description = 'download assets from external sites'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for k, v in ASSETS.items():
            print('downloading {} to {}'.format(k, v))
            urllib.urlretrieve(k, v)


class InitGitSubModules(Command):
    """Support setup.py Git submodule init"""

    description = 'Call git on each submodule and initilize it'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print('Calling git recurisively on on each sub module..')
        subprocess.call(['git', 'submodule', 'update', '--init'])


class FetchDeps(Command):
    """fetch dependencies command"""

    description = 'gathers external dependencies from various sources'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.run_command('git_init')
        self.run_command('retrieve_assets')


setup(
    name='ShinySDR',
    # version='...',  # No versioning is defined yet
    description='Software-defined radio receiver application built on GNU Radio with a web-based UI and plugins.',
    url='https://github.com/kpreid/shinysdr/',
    author='Kevin Reid',
    author_email='kpreid@switchb.org',
    classifiers=[
        # TODO: review/improve; this list was made by browsing <https://pypi.python.org/pypi?%3Aaction=list_classifiers>; can we add new items?
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Twisted',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',  # will probably fail on notPOSIX due to lack of portability work, not fundamentally
        'Topic :: Communications :: Ham Radio',  # non-exclusively ham
    ],
    license='GPLv3+',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # 'gnuradio',  # Not PyPI
        # 'osmosdr',  # Not PyPI
        'twisted',
        'txws',
        'ephem',
        'six',
        'pyserial',  # undeclared dependency of twisted.internet.serialport
        # Without the service_identity module, Twisted can perform only rudimentary TLS client hostname verification
        'service_identity', 
        'pyasn1>=0.4.1,<0.5.0',  # required to pin pyans1 support for pyasn1-modules
        'pyasn1-modules',  # required for service_identity
    ],
    dependency_links=[],
    # zip_safe: TODO: Investigate. I suspect unsafe due to serving web resources relative to __file__.
    zip_safe=False,
    entry_points={
        'console_scripts': {
            'shinysdr = shinysdr.main:main',
            'shinysdr-import = shinysdr.db_import.tool:import_main'
        }
    },
    cmdclass={
        'git_init': InitGitSubModules,
        'retrieve_assets': DownloadAssets,
        'fetch_deps': FetchDeps,
    },
)
