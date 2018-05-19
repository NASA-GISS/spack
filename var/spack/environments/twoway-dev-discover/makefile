# Download source used for Spack Setup or similar

all : git/modelE git/ibmisc git/icebin git/pism git/pygiss git/modele-control


git :
	mkdir git

# Spack Setup

git/modelE : git
	cd git; git clone simplex.giss.nasa.gov:/giss/gitrepo/modelE.git -b e3/landice

git/ibmisc : git
	cd git; git clone git@github.com:citibeth/ibmisc.git -b develop

git/icebin : git
	cd git; git clone git@github.com:citibeth/icebin.git -b develop

git/pism : git
	cd git; git clone git@github.com:pism/pism.git -b efischer/dev

# No Spack Setup, just adjust PYTHONPATH
git/pygiss : git
	cd git; git clone git@github.com:citibeth/pygiss.git -b develop

git/modele-control : git
	cd git; git clone git@github.com:citibeth/modele-control.git -b develop

# No need because we're not doing Spack Setup / PYTHONPATH adjustment on these
# everytrace
