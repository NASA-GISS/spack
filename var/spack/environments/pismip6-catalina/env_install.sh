#!/bin/sh
#

# NOTE: Run with python2 (see spack/bin/spack script if needed to prefer python2).  We need to avoid python 3.8

# https://www.linuxquestions.org/questions/linux-newbie-8/configure-error-no-acceptable-ld-found-in-$path-102003/
export LD=ld
spack -e pismip6-catalina install

