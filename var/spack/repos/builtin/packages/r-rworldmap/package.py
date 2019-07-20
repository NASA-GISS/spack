# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRworldmap(RPackage):
    """Enables mapping of country level and gridded user datasets."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/AndySouth/rworldmap/"
    url      = "https://cran.r-project.org/src/contrib/rworldmap_1.3-6.tar.gz"

    version('1.3-1', sha256='1cbd511b14aaecd4fa4d829459d539d629ec3d48ad7755b64608af34ae322f73')

    depends_on('r-maptools', type=('build', 'run'))
    depends_on('r-fields', type=('build', 'run'))
