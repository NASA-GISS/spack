# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRnetcdf(RPackage):
    """An interface to the NetCDF file format designed by Unidata for
    efficient storage of array-oriented scientific data and
    descriptions. The R interface is closely based on the C API of the
    NetCDF library, and it includes calendar conversions from the
    Unidata UDUNITS library. The current implementation supports all
    operations on NetCDF datasets in classic and 64-bit offset file
    formats, and NetCDF4-classic format is supported for reading and
    modification of existing files."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://rnetcdf.r-forge.r-project.org"
    url      = "https://cran.r-project.org/src/contrib/RNetCDF_1.9-1.tar.gz"

    version('1.8-2', sha256='adf8a3028f1d67f38a725ffb509a4ee36f14e5859c6ffadcb4e71cb9c22fc45e')

    # FIXME: Add dependencies if required.
    depends_on('netcdf')
