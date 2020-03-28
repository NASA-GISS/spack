# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Blitz(CMakePackage):
    """N-dimensional arrays for C++"""
    homepage = "http://github.com/blitzpp/blitz"
    url = "https://github.com/blitzpp/blitz/archive/1.0.2.tar.gz"

    # CMake...
    version('1.0.2', '500db9c3b2617e1f03d0e548977aec10d36811ba1c43bb5ef250c0e3853ae1c2')
    # Autotools... won't work with CMakePackage
    # version('1.0.1', 'fe43e2cf6c9258bc8b369264dd008971')
    # version('1.0.0', '971c43e22318bbfe8da016e6ef596234')

    depends_on('papi')
