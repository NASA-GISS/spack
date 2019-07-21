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

    version('1.3-6', sha256='53eec8637a39754b87cbcf625bf644b26ddd5a82996b107abba5828c930530e0')

    depends_on('r-maptools', type=('build', 'run'))
    depends_on('r-fields', type=('build', 'run'))
