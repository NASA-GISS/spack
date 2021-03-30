# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Udunits(AutotoolsPackage):
    """Automated units conversion"""

    homepage = "http://www.unidata.ucar.edu/software/udunits"
    url      = "https://www.gfd-dennou.org/arch/ucar/unidata/pub/udunits/udunits-2.2.24.tar.gz"

    version('2.2.28',
        url='https://artifacts.unidata.ucar.edu/repository/downloads-udunits/udunits-2.2.28.tar.gz',
        sha256='590baec83161a3fd62c00efa66f6113cec8a7c461e3f61a5182167e0cc5d579e')

    # Previous 2.2.x versions were removed from UDUnits download

    depends_on('expat')
