# Standard stuff for any loads-x environment on discover12

# https://stackoverflow.com/questions/3430569/globbing-pathname-expansion-with-colon-as-separator
function join() {
    local IFS=$1
    shift
    echo "$*"
}

export HARNESS=$SPACK_ENV

export SPACK_ENV_NAME=$(basename $SPACK_ENV)
export SPACK_ROOT=$(dirname $(dirname $(dirname $(dirname $SPACK_ENV))))
# This will be overwritten when the harness is created.

# Minimal Spack setup without invoking Spack's setup_env.sh stuff
export MODULEPATH=$MODULEPATH:$(join ':' $SPACK_ROOT/share/spack/modules/*)
export PATH=$PATH:SPACK_ROOT/bin

# Load the main environment
module purge

module load comp/gcc/9.2.0
module load comp/intel/20.0.0.166
module load mpi/impi/20.0.0.166

# Bootstrap with Spack-built replacements of system tools
#source $SPACK_ENV/../tools-discover/loads

# Load Spack-generated modules
source $SPACK_ENV/loads
