##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

import inspect
import platform
import sys
import string
import os

import llnl.util.tty as tty
import spack.build_environment
from llnl.util.filesystem import working_dir, join_path
from llnl.util.filesystem import set_executable
from spack.directives import depends_on
from spack.package import PackageBase


def spack_transitive_include_path():
    return ';'.join(
        os.path.join(dep, 'include')
        for dep in os.environ['SPACK_DEPENDENCIES'].split(os.pathsep)
    )


class CMakePackage(PackageBase):
    """Specialized class for packages that are built using CMake

    This class provides three phases that can be overridden:

    * cmake
    * build
    * install

    They all have sensible defaults and for many packages the only thing
    necessary will be to override ``cmake_args``

    Additionally, you may specify make targets for build and install
    phases by overriding ``build_targets`` and ``install_targets``
    """
    phases = ['cmake', 'build', 'install']
    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = 'CMakePackage'

    build_targets = []
    install_targets = ['install']

    depends_on('cmake', type='build')

    def build_type(self):
        """Override to provide the correct build_type in case a complex
        logic is needed
        """
        return 'RelWithDebInfo'

    def root_cmakelists_dir(self):
        """Directory where to find the root CMakeLists.txt"""
        return self.stage.source_path

    @property
    def std_cmake_args(self):
        """Standard cmake arguments provided as a property for
        convenience of package writers
        """
        # standard CMake arguments
        return CMakePackage._std_args(self)

    @staticmethod
    def _std_args(pkg):
        """Computes the standard cmake arguments for a generic package"""
        try:
            build_type = pkg.build_type()
        except AttributeError:
            build_type = 'RelWithDebInfo'

        args = ['-DCMAKE_INSTALL_PREFIX:PATH={0}'.format(pkg.prefix),
                '-DCMAKE_BUILD_TYPE:STRING={0}'.format(build_type),
                '-DCMAKE_VERBOSE_MAKEFILE:BOOL=ON']
        if platform.mac_ver()[0]:
            args.append('-DCMAKE_FIND_FRAMEWORK:STRING=LAST')

        # Set up CMake rpath
        args.append('-DCMAKE_INSTALL_RPATH_USE_LINK_PATH:BOOL=FALSE')
        rpaths = ':'.join(spack.build_environment.get_rpaths(pkg))
        args.append('-DCMAKE_INSTALL_RPATH:STRING={0}'.format(rpaths))
        return args

    def build_directory(self):
        """Override to provide another place to build the package"""
        return join_path(self.stage.source_path, 'spack-build')

    def cmake_args(self):
        """Method to be overridden. Should return an iterable containing
        all the arguments that must be passed to configure, except:

        * CMAKE_INSTALL_PREFIX
        * CMAKE_BUILD_TYPE
        """
        return []

    def cmake(self, spec, prefix):
        """Run cmake in the build directory"""
        options = [self.root_cmakelists_dir()] + self.std_cmake_args + \
            self.cmake_args()
        with working_dir(self.build_directory(), create=True):
            inspect.getmodule(self).cmake(*options)

    def build(self, spec, prefix):
        """Make the build targets"""
        with working_dir(self.build_directory()):
            inspect.getmodule(self).make(*self.build_targets)

    def install(self, spec, prefix):
        """Make the install targets"""
        with working_dir(self.build_directory()):
            inspect.getmodule(self).make(*self.install_targets)

    @PackageBase.sanity_check('build')
    @PackageBase.on_package_attributes(run_tests=True)
    def _run_default_function(self):
        """This function is run after build if ``self.run_tests == True``

        It will search for a method named ``check`` and run it. A sensible
        default is provided in the base class.
        """
        try:
            fn = getattr(self, 'check')
            tty.msg('Trying default build sanity checks [check]')
            fn()
        except AttributeError:
            tty.msg('Skipping default build sanity checks [method `check` not implemented]')  # NOQA: ignore=E501

    def check(self):
        """Default test: search the Makefile for the target ``test``
        and run them if found.
        """
        with working_dir(self.build_directory()):
            self._if_make_target_execute('test')

    # Check that self.prefix is there after installation
    PackageBase.sanity_check('install')(PackageBase.sanity_check_prefix)

    def write_spconfig(self, spconfig_fname):
        # Set-up the environment
        spack.build_environment.setup_package(self)

        _cmd = [str(spack.which('cmake'))] + \
            self.std_cmake_args + self.cmake_args()

        # No verbose makefile for interactive builds
        cmd = [x for x in _cmd if not x.startswith('-DCMAKE_VERBOSE_MAKEFILE')]

        env = dict()

        paths = os.environ['PATH'].split(':')
        paths = [item for item in paths if 'spack/env' not in item]
        env['PATH'] = ':'.join(paths)
        env['SPACK_TRANSITIVE_INCLUDE_PATH'] = spack_transitive_include_path()
        env['CMAKE_PREFIX_PATH'] = os.environ['CMAKE_PREFIX_PATH']
        env['CC'] = os.environ['SPACK_CC']
        env['CXX'] = os.environ['SPACK_CXX']
        env['FC'] = os.environ['SPACK_FC']

        with open(spconfig_fname, 'w') as fout:
            fout.write(
                r"""#!%s
#
# %s

import sys
import os
import subprocess

def cmdlist(str):
    return list(x.strip().replace("'",'') for x in str.split('\n') if x)
env = dict(os.environ)
""" % (sys.executable, ' '.join(sys.argv)))

            env_vars = sorted(list(env.keys()))
            for name in env_vars:
                val = env[name]
                if string.find(name, 'PATH') < 0:
                    fout.write('env[%s] = %s\n' % (repr(name), repr(val)))
                else:
                    if name == 'SPACK_TRANSITIVE_INCLUDE_PATH':
                        sep = ';'
                    else:
                        sep = ':'

                    fout.write(
                        'env[%s] = "%s".join(cmdlist("""\n' % (repr(name), sep))
                    for part in string.split(val, sep):
                        fout.write('    %s\n' % part)
                    fout.write('"""))\n')

            fout.write('\ncmd = cmdlist("""\n')
            fout.write('%s\n' % cmd[0])
            for arg in cmd[1:]:
                fout.write('    %s\n' % arg)
            fout.write('""") + sys.argv[1:]\n')
            fout.write('\nproc = subprocess.Popen(cmd, env=env)\nproc.wait()\n')
            set_executable(spconfig_fname)
            return spconfig_fname

