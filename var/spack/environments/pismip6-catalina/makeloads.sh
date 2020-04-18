#!/bin/sh
# 
# Generates the *loads* file

# Set up Spack and Modules
# http://stackoverflow.com/questions/59895/can-a-bash-script-tell-which-directory-it-is-stored-in

# macOS doesn't have readlink -f (but it can be obtained from GNU coreutils)
# https://stackoverflow.com/questions/5756524/how-to-get-absolute-path-name-of-shell-script-on-macos
pushd . >/dev/null
export SPACK_ENVX=$(cd "$SCRIPT_DIR" >/dev/null; pwd -P )
popd >/dev/null

export SPACK_ROOT=$(dirname $(dirname $(dirname $(dirname $SPACK_ENV))))


# Hack around evil stateful Spack Environment stuff

# spack env activate --sh doesn't work.
#source $SPACK_ROOT/share/spack/setup-env.sh
#$SPACK_ROOT/bin/spack env deactivate   # just in case
unset SPACK_ENV   # Ignore previous activations
$SPACK_ROOT/bin/spack env activate --sh pismip6-catalina --with-view >$SPACK_ENVX/loads
