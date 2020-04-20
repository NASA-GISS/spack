# Standard stuff for any loads-x environment on catalina

# Enable Enviornment Modules (We're not using env modules)
#source /Users/eafischer2/spack/opt/spack/darwin-catalina-x86_64/clang-11.0.3-apple/environment-modules-4.5.0-gxhm7oddr7rmyyc6zfud6atczhklk5gp/init/profile.sh


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

# Load the main environment
#module purge

# Load Spack-generated modules (or view-based env)
source $SPACK_ENV/loads

export PATH=$PATH:$SPACK_ROOT/bin
