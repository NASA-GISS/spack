# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
from spack import *


class PyFindiff(PythonPackage):
    """A Python package for finite difference numerical derivatives and
    partial differential equations in any number of dimensions."""

    homepage = "https://www.example.com"
    url      = "https://files.pythonhosted.org/packages/dc/8d/3e7c2ff68baaca26d76318541172b20b2fe83eb9cc14d1e16cc56054ec36/findiff-0.8.0.tar.gz"

    maintainers = ['citibeth']

    version('0.8.0', sha256='0ace7658c6de07791537c795a65658399039a7aad048ef0a281e6389890d28ec')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.14.2:', type=('build', 'run'))
    depends_on('py-scipy@1.3.1:', type=('build', 'run'))
