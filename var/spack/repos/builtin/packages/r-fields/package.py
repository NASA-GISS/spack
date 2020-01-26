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
    url      = "https://cran.r-project.org/src/contrib/Archive/fields/fields_9.8-3.tar.gz"

    version('9.8-3', sha256='010676e009d48ff605d9881bcedb903b95bc4a271da47eb629d5cbcf1a323de1')

    depends_on('r-spam', type=('build', 'run'))
    depends_on('r-maps', type=('build', 'run'))
