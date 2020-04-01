# Standard stuff for any loads-x environment on discover12


## https://stackoverflow.com/questions/3430569/globbing-pathname-expansion-with-colon-as-separator
#function join() {
#    local IFS=$1
#    shift
#    echo "$*"
#}

PS1_SAVE="$PS1"    # Save command prompt; some modules destroy it

export SPACK_ENV_NAME=$(basename $SPACK_ENV)
export SPACK_ROOT=$(dirname $(dirname $(dirname $(dirname $SPACK_ENV))))
# This will be overwritten when the harness is created.

# Minimal Spack setup without invoking Spack's setup_env.sh stuff
#export MODULEPATH=$MODULEPATH:$(join ':' $SPACK_ROOT/share/spack/modules/*)
export MODULEPATH=$MODULEPATH:$SPACK_ROOT/share/spack/modules/linux-centos6-x86_64

export PATH=$PATH:SPACK_ROOT/bin

# Load the main environment
module purge

# icc also loads gcc-5.4.0
# module load compiler/GCC/5.4.0-2.26
module load compiler/icc/2018.5.274-GCC-5.4.0-2.26
module load compiler/ifort/2018.5.274-GCC-5.4.0-2.26
# Needed to get the right mpicc to link to the right libraries.
# Without this, it links to /usr/lib64/libstdc++
module load openmpi/intel/3.1.4
# We will build our own intel-mkl with Spack

# Bootstrap with Spack-built replacements of system tools
#source $SPACK_ENV/../tools-discover/loads

# Load Spack-generated modules
# For some reason, one module unsets the prompt env var PS1:
#        intel-mkl-2018.4.274-intel-18.5.274-doboyrw
source $SPACK_ENV/loads
export PS1="$PS1_SAVE"

# We will have to replace in it
#     '/opt/scyld/openmpi/3.1.4' --> '/home/eafischer2/om3.1.4'
#unset LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$(echo $LD_LIBRARY_PATH | sed 's@/opt/scyld/openmpi/3.1.4@/home/eafischer2/om3.1.4@g')
export PATH=$(echo $PATH | sed 's@/opt/scyld/openmpi/3.1.4@/home/eafischer2/om3.1.4@g')


# Make sure `ectl setup` (ModelE setup; see modele-control repo) can
# find MPI, and that we can do mpirun when needed.
export PATH=$PATH:/home/eafischer2/om3.1.4/intel/bin/


