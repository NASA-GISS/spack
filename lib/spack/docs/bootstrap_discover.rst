Need at last 250K inodes available in your quote to start

module load other/comp/gcc-4.9.2-sp3
rm $HOME/.spack/compilers.yaml
spack compilers

<remove all but the module-provided GCC 4.9.2>

nice spack install curl
<fix up ~/sh/curl>

nice spack install gcc@4.9.3
<add gcc@4.9.3 to compilers.yaml>

spack install cmake
spack install m4
~/sh/make_spackenv

spack install parallel-netcdf
cd ~/git/modelE
spack spcfong modele@local

