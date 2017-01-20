.. _spackenv-tutorial:

==================
Spack Environments
==================

Once you've built a set of Spack packages... how do you use them in a
user's environment?  The most obvious way is to put a series of
``spack load`` commands in ``.bashrc``; but that has many problems.
This tutorial will guide you through some more advanced ways to
generate and maintain environments of Spack-built software.

-------------------
Module Load Scripts
-------------------

The most direct way to create a Spack environment is with a script
containing a series of ``module load`` commands, to be put in or
sourced from ``.bashrc``.  This is achieved by providing the spec of
an installed package to ``spack module loads``; for example, the
following could be redirected to a file:

.. code-block:: console

  $ spack module loads everytrace-example
  # everytrace-example@develop%gcc@5.3.0 arch=linux-suse_linux11-x86_64 
  module load everytrace-example-develop-gcc-5.3.0-rvxbpyt

Because Spack embeds RPATHs in binaries, in many cases, it is
necessary to only load the modules one needs to directly use.
However, some packages do require their dependencies loaded as well to
work correclty --- this is usually the case, for example, with Python
packages.  In that case, ``spack module loads -r`` may be used:

.. code-block:: console

  $ spack module loads -r everytrace-example
  # everytrace@develop%gcc@5.3.0+fortran+mpi arch=linux-suse_linux11-x86_64 
  module load everytrace-develop-gcc-5.3.0-42qnpxw
  # everytrace-example@develop%gcc@5.3.0 arch=linux-suse_linux11-x86_64 
  module load everytrace-example-develop-gcc-5.3.0-rvxbpyt


---------------------------------
Spack Environments (Experimental)
---------------------------------

The correct Spack commands to generate module load scripts can become
long if many separate builds are required for a particular user
environment.  Also, like ``spack find``, the command ``spack module
loads`` is not guaranteed to always work: it depends on what happens
to have been built.

Spack environments provide a more automated way to create user
environments.  The contents of an environment is defined in an
``.env`` file.  When run on the ``.env`` file, Spack installs all
required packages for the environment, and also generates the
appropriate module load file.

Let's see how it works.  Create the file ``~/env/myenv.env`` (be
careful to include the line starting with ``# spack=``):

.. code-block:: bash

  # `spack install` args : `spack module loads` args
  #
  # Define configuration scopes used to generate this environment
  # spack=spack -c ~/myproject

  everytrace-example : --dependencies
  zlib :

You can now install all packages in this environment:

.. code-block:: console

  $ spackenv install ~/env/myenv.env

This generates the file ``~/env/myenv.log``, which you may review.  If
all looks good, the module load script may be genereated via:

.. code-block:: console

  $ spackenv loads ~/env/myenv.env

This generates the file ``~/env/myenv``, which may be sourced directly
by bash.

.. note::

  Spack environments as descried in this section are currently an
  experimental feature; the UI and environment file format are likely
  to change.



