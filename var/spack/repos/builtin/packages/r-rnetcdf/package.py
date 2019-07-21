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

    homepage = "http://rnetcdf.r-forge.r-project.org"
    url      = "https://cran.r-project.org/src/contrib/RNetCDF_1.9-1.tar.gz"

    version('1.9-1', sha256='7d5a1e47ba3f41050e92ac27fe12c9ffd8dea67e132c43ff071dcdb0fad4ae45')

    depends_on('netcdf')
    depends_on('udunits2')

