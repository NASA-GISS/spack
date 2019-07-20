# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.prefix import Prefix
from spack import *

import llnl.util.tty as tty
import os


class Openjdk(Package):
    """Java Development Kit builds, from Oracle"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://jdk.java.net"
    url      = "https://download.java.net/java/GA/jdk12.0.2/e482c34c86bd4bf8b56c0b35558996b9/10/GPL/openjdk-12.0.2_linux-x64_bin.tar.gz"

    version('12.0.2', sha256='75998a6ebf477467aa5fb68227a67733f0e77e01f737d4dfbc01e617e59106ed')

    provides('java')
    provides('java@12', when='@12.0:12.999')

    # FIXME:
    # 1. `extends('java')` doesn't work, you need to use `extends('jdk')`
    # 2. Packages cannot extend multiple packages, see #987
    # 3. Update `YamlFilesystemView.merge` to allow a Package to completely
    #    override how it is symlinked into a view prefix. Then, spack activate
    #    can symlink all *.jar files to `prefix.lib.ext`
    extendable = True

    @property
    def home(self):
        """Most of the time, ``JAVA_HOME`` is simply ``spec['java'].prefix``.
        However, if the user is using an externally installed JDK, it may be
        symlinked. For example, on macOS, the ``java`` executable can be found
        in ``/usr/bin``, but ``JAVA_HOME`` is actually
        ``/Library/Java/JavaVirtualMachines/jdk-10.0.1.jdk/Contents/Home``.
        Users may not know the actual installation directory and add ``/usr``
        to their ``packages.yaml`` unknowingly. Run ``java_home`` if it exists
        to determine exactly where it is installed. Specify which version we
        are expecting in case multiple Java versions are installed.
        See ``man java_home`` for more details."""

        prefix = self.prefix
        java_home = prefix.libexec.java_home
        if os.path.exists(java_home):
            java_home = Executable(java_home)
            version = str(self.version.up_to(2))
            prefix = java_home('--version', version, output=str).strip()
            prefix = Prefix(prefix)

        return prefix

    @property
    def libs(self):
        """Depending on the version number and whether the full JDK or just
        the JRE was installed, Java libraries can be in several locations:
        * ``lib/libjvm.so``
        * ``jre/lib/libjvm.dylib``
        Search recursively to find the correct library location."""

        return find_libraries(['libjvm'], root=self.home, recursive=True)

    @run_before('install')
    def macos_check(self):
        if self.spec.satisfies('platform=darwin'):
            msg = """\
Spack's JDK package only supports Linux. If you need to install JDK on macOS,
manually download the .dmg from:
    {0}
and double-click to install. Once JDK is installed, you can tell Spack where
to find it like so. To find the JDK installation directory, run:
    $ /usr/libexec/java_home
If you have multiple versions of JDK installed, you can specify a particular
version to search for with the --version flag. To find the exact version
number, run:
    $ java -version
If the version number contains a '+' symbol, replace it with '_', otherwise
Spack will think it is a variant. Add JDK as an external package by running:
    $ spack config edit packages
and adding entries for each installation:
    packages:
        jdk:
            paths:
                jdk@10.0.1_10:    /path/to/jdk/Home
                jdk@1.7.0_45-b18: /path/to/jdk/Home
            buildable: False""".format(self.homepage)

            tty.die(msg)

    def install(self, spec, prefix):
        install_tree('.', prefix)

    def setup_environment(self, spack_env, run_env):
        """Set JAVA_HOME."""

        run_env.set('JAVA_HOME', self.home)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        """Set JAVA_HOME and CLASSPATH.
        CLASSPATH contains the installation prefix for the extension and any
        other Java extensions it depends on."""

        spack_env.set('JAVA_HOME', self.home)

        class_paths = []
        for d in dependent_spec.traverse(deptype=('build', 'run', 'test')):
            if d.package.extends(self.spec):
                class_paths.extend(find(d.prefix, '*.jar'))

        classpath = os.pathsep.join(class_paths)
        spack_env.set('CLASSPATH', classpath)

        # For runtime environment set only the path for
        # dependent_spec and prepend it to CLASSPATH
        if dependent_spec.package.extends(self.spec):
            class_paths = find(dependent_spec.prefix, '*.jar')
            classpath = os.pathsep.join(class_paths)
            run_env.prepend_path('CLASSPATH', classpath)

    def setup_dependent_package(self, module, dependent_spec):
        """Allows spec['java'].home to work."""

        self.spec.home = self.home
