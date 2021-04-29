This is what Elizabeth used to set up a Spack-based Python GEO environment on macOS Catalina.  No guarantees.

Setup your Mac
==============

1. Install XCode Command Line Tools.  This can be done at either:
   1. https://developer.apple.com/download/more/
   2. Run `git --version` from the command line.  If you don't have XCode Command Line Tools installed already, it will prompt you to install it.

**NOTE**: If you already run HomeBrew, this step is probably complete.

Download Spack
==============
```
cd ~
git clone git@github.com:citibeth/spack.git -b efischer/uaf
```

Setup Files
===========
Add to `.bash_profile`:
```
export PATH=$HOME/sh:$HOME/spack/bin:$PATH
```

Build the Environment
=====================
```
cd ~/spack/environments/pismip6-catalina
./env_concretize.sh
./env_install.sh
./env_loads.sh
```

Create a Harness with Current Source Code
=========================================
```
cd ~
mkdir -p harn/pismip6
cd harn/pismip6
ln -s ~/spack/environments/pismip6-catalina/harness-loads-x .
git clone git@github.com:pism/uafgi.git -b eaf/develop
```

Create a Directory for your Git Project / Source Code
=====================================================
```
cd ~/harn/pismip6
mkdir mycode
```

Add Convenience
===============
```
cd ~
ln -s harn/pismip6/uafgi .
ln -s harn/pismip6/mycode .
```

Use the Environment
===================
```
source ~/harn/pismip6/loads-x
cd ~/mycode
```

Add Other Software
==================
1. SmartGit: https://www.syntevo.com/smartgit/
2. QGIS: https://qgis.org/en/site/forusers/download.html
3. 
