from spack import *

class Btest(Package):
    version('1.0', url='http://')

    depends_on('m4', type='build')
    depends_on('netcdf-fortran')
