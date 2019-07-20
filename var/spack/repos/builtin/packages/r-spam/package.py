# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSpam(RPackage):
    """Set of functions for sparse matrix algebra. Differences with other
    sparse matrix packages are: (1) we only support (essentially) one
    sparse matrix format, (2) based on transparent and simple
    structure(s), (3) tailored for MCMC calculations within
    G(M)RF. (4) and it is fast and scalable (with the extension
    package spam64)."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.math.uzh.ch/pages/spam/"
    url      = "https://cran.r-project.org/src/contrib/spam_2.2-2.tar.gz"

    version('2.2-1', sha256='224f8d859c2fd1627dcc3b6a45e5406caef26363819b49e8ca7004a02ce76e11')

    depends_on('r-dotcall64', type=('build', 'run'))
