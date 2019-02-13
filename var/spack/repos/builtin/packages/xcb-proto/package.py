# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class XcbProto(AutotoolsPackage):
    """xcb-proto provides the XML-XCB protocol descriptions that libxcb uses to
    generate the majority of its code and API."""

    homepage = "http://xcb.freedesktop.org/"
    url      = "http://xcb.freedesktop.org/dist/xcb-proto-1.13.tar.gz"

    version('1.13', '0cc0294eb97e4af3a743e470e6a9d910')
    version('1.12', '5ee1ec124ea8d56bd9e83b8e9e0b84c4')
    version('1.11', 'c8c6cb72c84f58270f4db1f39607f66a')

    # TODO: uncomment once build deps can be resolved separately
    # See #7646, #4145, #4063, and #2548 for details
    # extends('python')

    patch('xcb-proto-1.12-schema-1.patch', when='@1.12')

    variant('python3', default=False,
       description='Enable if you are building a stack with Python3')

    depends_on('python@2.6:2.8', type='build', when='~python3')

    def setup_environment(self, spack_env, run_env):
        # Our Spack-installed Python3 breaks the build;
        # Remove it from the environment and hope the System
        # Python2 works for us.
        if '+python3' in self.spec:
            spack_env.unset('PYTHONPATH')
            spack_env.unset('PYTHONHOME')
            spack_env.unset('PYTHONSTARTUP')
