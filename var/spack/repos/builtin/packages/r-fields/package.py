# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFields(RPackage):
    """For curve, surface and function fitting with an emphasis on
    splines, spatial data, geostatistics, and spatial statistics. The
    major methods include cubic, and thin plate splines, Kriging, and
    compactly supported covariance functions for large data sets."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/NCAR/Fields"
    url      = "https://cran.r-project.org/src/contrib/fields_9.8-3.tar.gz"

    version('9.8-1', sha256='1b0c2a33c59e96a1dac94ad1ca8a000ac31165efb6848445a376f19aea2264fd')

    depends_on('r-spam', type=('build', 'run'))
    depends_on('r-maps', type=('build', 'run'))
