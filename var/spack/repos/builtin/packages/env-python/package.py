##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class EnvPython(Package):
    """General Python environment for GISS."""
    homepage = ""

    version('1.0')

    # -------- Python post-processing environment
    depends_on('python@3:')
    depends_on('py-cython')
    depends_on('py-scipy')
    depends_on('py-netcdf')
    depends_on('py-matplotlib')
    depends_on('py-basemap')
#    depends_on('py-git2')
    depends_on('py-xarray')
    depends_on('py-proj')
#    depends_on('py-bsddb3')
    depends_on('py-udunits')
    depends_on('py-more-itertools')
    depends_on('py-rtree')
    depends_on('py-giss')
    depends_on('py-pyside')


    def url_for_version(self, version):
        return 'https://github.com/citibeth/dummy/tarball/v1.0'

    def install(self, spec, prefix):
        with open(os.path.join(spec.prefix, 'dummy.txt'), 'w') as out:
            out.write('This is a bundle\n')

