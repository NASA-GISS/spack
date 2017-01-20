.. _developing-software-tutorial:

==============================
Developing Software with Spack
==============================

This tutorial will guide you through the process of using Spack in the
creation of your own software packages.  We will lead you through the
use of ``spack setup`` to configure an existing CMake-based project in
your own directory; and then build and install it in Spack.  We will
then show how this can be used as a dependency for another CMake-based
project, providing seamless integration between your software and
third-party packages.

.. _basics-tutorial-install:

----------------------------
Manually Building Everytrace
----------------------------

We will use the package Everytrace as an example: it is small and easy
to build.  In this example, we will download, configure and build the
latest development branch of Everytrace, which is *not* a released
version.

.. code-block:: console

  $ git clone https://github.com/citibeth/everytrace.git -b develop
  Cloning into 'everytrace'...
  $ cd everytrace
  $ spack setup everytrace@develop
  ==> Installing everytrace
  ...
  ==> Generating config file spconfig.py [everytrace@develop%gcc@5.3.0+fortran+mpi arch=linux-suse_linux11-x86_64 -42qnpxw]
  ==> Successfully setup everytrace
    Config file is spconfig.py
  [+] /gpfsm/dnb53/rpfische/spack/opt/spack/linux-suse_linux11-x86_64/gcc-5.3.0/everytrace-develop-42qnpxwn4bqoxzbyfoclc7kxjpul6wif

Let's look at what was generated:

.. code-block:: console

  $ less spconfig.py

OK, now you can finish building the package:

.. code-block:: console

  $ mkdir build
  $ cd build
  rpfische@discover16:~/nobackup/git/everytrace/build> ../spconfig.py ..
  ...
  -- Configuring done
  -- Generating done
  -- Build files have been written to: /home/rpfische/nobackup/git/everytrace/build
  rpfische@discover16:~/nobackup/git/everytrace/build> make install
  Scanning dependencies of target everytrace_cf_mpi_refaddr
  [  9%] Building C object slib/CMakeFiles/everytrace_cf_mpi_refaddr.dir/everytrace_cf_mpi_refaddr.c.o
  ...
  -- Installing:
  ...

Your manually-built package is now fully installed in Spack, and works just like any other installed package:

.. code-block:: console

  $ spack find everytrace
  ==> 2 installed packages.
  -- linux-suse_linux11-x86_64 / gcc@5.3.0 ------------------------
  everytrace@0.2.0  everytrace@develop

  $ ls -l ``spack location -i everytrace``/lib
  -rw-r--r-- 1  everytrace_cf_mpi_refaddr.o
  -rw-r--r-- 1  everytrace_cf_refaddr.o
  -rw-r--r-- 1  everytrace_c_mpi_refaddr.o
  -rw-r--r-- 1  everytrace_c_refaddr.o
  -rwxr-xr-x 1  libeverytrace.so

Now let's build something that depends on this!

.. code-block:: console

  $ spack install everytrace-example ^everytrace@develop


Note that you can auto-build packages that depend on manually-built
packages.  In this way, you can manually build certain key packages in
your overall DAG.

---------------
Multiple Setups
---------------

The ``spack setup`` command allows you to manually build the top
package of a DAG.  In more complex settings, one needs to manually
build many packages in a DAG.  Here is how to do it, **as long as no
auto-built packages depend on manually-built packages**.  This example
will simultaneously set up ``everytrace`` and ``everytrace-example``:

.. code-block:: console

  $ spack install --setup everytrace --setup everytrace-example everytrace-example@develop ^everytrace@develop
  $ ls -ltrah
  -rwxrw---- everytrace-config.py
  -rwxrw---- everytrace-example-config.py

You can now use the generated ``*-config.py`` files to configure and
build both packages (make sure to build ``everytrace`` before
``everytrace-example``).
