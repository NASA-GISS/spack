# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-geojson
#
# You can edit this file again by typing:
#
#     spack edit py-geojson
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyGeojson(PythonPackage):
    """Functions for encoding and decoding GeoJSON formatted data"""

    homepage = "https://github.com/jazzband/geojson"
    url      = "https://files.pythonhosted.org/packages/b6/8d/c42d3fe6f9b5e5bd6a55d9f03813d674d65d853cb12e6bc56f154a2ceca0/geojson-2.5.0.tar.gz"

    maintainers = ['citibeth']

    version('2.5.0', sha256='6e4bb7ace4226a45d9c8c8b1348b3fc43540658359f93c3f7e03efa9f15f658a')

    # FIXME: Add dependencies if required. Only add the python dependency
    # if you need specific versions. A generic python dependency is
    # added implicity by the PythonPackage class.
    # depends_on('python@2.X:2.Y,3.Z:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    # depends_on('py-foo',        type=('build', 'run'))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
