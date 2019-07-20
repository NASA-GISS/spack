# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDotcall64(RPackage):
    """Provides .C64(), which is an enhanced version of .C() and
    .Fortran() from the foreign function interface. .C64() supports
    long vectors, arguments of type 64-bit integer, and provides a
    mechanism to avoid unnecessary copies of read-only and write-only
    arguments. This makes it a convenient and fast interface to C/C++
    and Fortran code."""

    homepage = "https://git.math.uzh.ch/reinhard.furrer/dotCall64"
    url      = "https://cran.r-project.org/src/contrib/dotCall64_1.0-0.tar.gz"

    version('0.9-5.2', sha256='738809d87ff13d1fa06ebe903645989b72fca24e3117016b943bda92b89f80cb')
