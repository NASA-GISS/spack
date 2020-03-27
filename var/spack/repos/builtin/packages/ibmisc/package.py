# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ibmisc(CMakePackage):
    """Misc. reusable utilities used by IceBin."""

    homepage = "https://github.com/citibeth/ibmisc"
    url      = "https://github.com/citibeth/ibmisc/tarball/v0.1.3"

    maintainers = ['citibeth']

    version('0.2.0', 'f0c89a0889d1136795003639389db1513b56e1d5a65b0f6778af3630ba4bc981')
    version('0.1.3', 'bb1876a8d1f0710c1a031280c0fc3f2e')

    version('develop',
        git='https://github.com/citibeth/ibmisc.git',
        branch='develop')

    variant('everytrace', default=True,
            description='Report errors through Everytrace')
    variant('proj', default=True,
            description='Compile utilities for PROJ.4 library')
    variant('blitz', default=True,
            description='Compile utilities for Blitz library')
    variant('netcdf', default=True,
            description='Compile utilities for NetCDF library')
    variant('boost', default=True,
            description='Compile utilities for Boost library')
    variant('udunits2', default=True,
            description='Compile utilities for UDUNITS2 library')
    variant('googletest', default=True,
            description='Build unit tests')
    variant('python', default=True,
            description='Compile utilities for use with Python/Cython')
    variant('doc', default=False,
            description='Build the documentation')
    variant('copy', values=str, default='standard',
        description='Allow multiple copies of the "same" spec to be installed')

    extends('python', when='+python')
    depends_on('python@3:', when='+python')

    depends_on('eigen')
    depends_on('everytrace', when='+everytrace')
    depends_on('proj', when='+proj')
    depends_on('blitz', when='+blitz')
    depends_on('netcdf-cxx4', when='+netcdf')
    depends_on('netcdf', when='+netcdf')
    depends_on('udunits2', when='+udunits2')
    depends_on('googletest', when='+googletest', type='build')
    depends_on('py-cython', when='+python', type=('build', 'run'))
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    depends_on('boost', when='+boost')

    # Build dependencies
    depends_on('doxygen', when='+doc', type='build')

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DUSE_EVERYTRACE=%s' % ('YES' if '+everytrace' in spec else 'NO'),
            '-DBUILD_PYTHON=%s' % ('YES' if '+python' in spec else 'NO'),
            '-DUSE_PROJ4=%s' % ('YES' if '+proj' in spec else 'NO'),
            '-DUSE_BLITZ=%s' % ('YES' if '+blitz' in spec else 'NO'),
            '-DUSE_NETCDF=%s' % ('YES' if '+netcdf' in spec else 'NO'),
            '-DUSE_BOOST=%s' % ('YES' if '+boost' in spec else 'NO'),
            '-DUSE_UDUNITS2=%s' % ('YES' if '+udunits2' in spec else 'NO'),
            '-DUSE_GTEST=%s' % ('YES' if '+googletest' in spec else 'NO'),
            '-DBUILD_DOCS=%s' % ('YES' if '+doc' in spec else 'NO')]

        if '+python' in spec:
            args.append(
                '-DCYTHON_EXECUTABLE=%s' % spec['py-cython'].command.path)

        return args
