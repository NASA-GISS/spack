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

    homepage = "https://www.math.uzh.ch/pages/spam/"
    url      = "https://cran.r-project.org/src/contrib/spam_2.2-2.tar.gz"

    version('2.2-2', sha256='711fdbfdac1e51dc7f684b139740f1d8c8aa6c6c0ae6bfaa8f7a7727ad7b8d08')

    depends_on('r-dotcall64', type=('build', 'run'))
