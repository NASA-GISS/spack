Spack Environemnts Overview
===========================

Spack Environemnts and related structures can be thought of as an expanded version of the current Spack Database.  Data structures consist of:

* Spack Environment:
  - envid: An environment ID (unique for each environment on a system)
  - A set of Install records
  - A Spack Database
  - Configs: a list of (location of) Spack configurations that should
    be loaded (in priority order) when processing with this Spack
    environemnt.

* Install Record:
  - userspec: A user-provided spec (as a string)
  - concspec: A fully concretized version of userspec (including the namespace of each package in the spec)
  - hashes: Hash of each package in concspec
  - hash: Hash of the DAG root in concspec
  - repo: The set of Spack packages needed to build this concspec.
  - priority: An integer; think of it as the order in which this
    Install Record was added to the Spack Environment.
  - setups: Set of packages in this install record where
    ``spconfig.py`` should be generated, instead of installing.
  - setups/: A directory used to contain the ``spconfig.py`` files
    generated when this Install Record is installed.  File sare named
    ``<package>-config.py``.

* Install Repo: A set of packages (pacakge.py directories) pulled from
  one or more Spack repos.

* Spack Database contains, per installed package:
  - hash
  - concspec # Spec from spec.yaml
  - path # path where this spec was installed
  - installed # whether this spec is actually installed anymore
  - ref_counts # number of packages that still need this one, separated by envid.  (Eg: {envid: refcount})
  - ref_count  # Sum of ref_counts across all envids

* Install Tree: A set of installed packages.

Spack Server
------------

Spack Environments are intended to work in a multi-user environment.
To that end, Spack functionality is separated into a "Spack Server"
and "Spack Client" (or just "Spack).  For now, the Spack Server will
simply be an API within Spack; later, it could be separated out into a
separate server to support multi-user Spack.

The Spack Server's purpose is to build software based on concretized
specs.  It is designed to be "stateless": as such, it does not engage
in concretization of specs or computation of hash values.  Spack
Clients call on the Spack Server with a fully concretized Spec, along
with all the Spack Packages needed to install that spec.

The Spack Server keeps a Spack Environment of everything it is asked
to install.  (Maybe only a Spack Database is needed.  If it keeps a
Spack Environemnt, some things will be missing; for example,
``userspec`` will always be ``None``).

Spack Client
------------

A Spack Client is a per-user system that encapsulates everything done
by that user; it should look and feel like a single Spack instance of
today.  The Spack Client will run on the same filesyste as the Spack
Server, since its users will access the Spack Server's installed
packages directly.  Spack Client is stateful: it depends on the
hashes, configurations and version of Spack the user happens to be
using.  (Different users running different Spack versions should be
able to share a Spack Server).

A Spack Client is associated with a single Spack Server.

A Spack Client maintains a single "root" Spack Environment, which
keeps everything the client has been asked to install.  Users can also
(optionally) specify a "current" environment for any Spack Command.
In this case, the Spack Client will add anything it installs to the
current environment as well as the root environment.


Spack Environments On-Disk Format
=================================

Suitable on-disk formats are to be devised for Spack Environments, Install Records and Spack Databases:

Spack Environment
-----------------

A Spack Environment is stored in a directory of a known name and location.  Users should be able to create a Spack Environment in any location they see fit; although Spack could also choose to keep an ``environments/`` folder somewhere in its tree for safekeeping.

A Spack Environment directory will consist of the following:

  * ``info.json``: Contains misc. information about the environment.
    Currently just the envid

  * ``spack-db/``: The Spack database (analogous to current
    ``$spack/opt/spack/.spack-db/index.json``).

  * ``installs/``: A directory of install records.  Each install
     record inside ``installs/`` is named by the install record's
     hash.


Install Record
--------------

An install record is written in a directory named after its hash.  The
userspec, concspec and hashes are written in a single JSON file.
There is also a `repo/` directory, which is the Install Repo for the
environment.

Install Repo
------------

An Install Repo mirrors the structure of existing Spack repos;
however, it must accomodate packages originally drawn from more than
one Spack repos.  Therefore, packages are stored in directories named
after ``<namespace>/<package>``.  An Install Repo will be used
directly when installing a piece of software.

Spack Database
--------------

Currently, a Spack Database is written in a single JSON file.  The
modifications proposed here to Spack Databases is minor, and will not
change the general approach to storage.  However, successful
implementation of the Spack Server might one day allow for locking
logic to be removed.

Install Tree
------------

The install tree format is identical to current Spack: a set of
install prefixes named after a concspec hash, along with a ``.spack/``
directory.  The contents of ``.spack/`` might need to change somewhat
in the future.




Spack Environment APIs
======================

The following APIs are used to manipulate Spack Environment data structures:

Spack Environment API
---------------------

* ``create(path)``: Initialize a new empty Spack Environment

* ``add(hash, concspec, hashes, repo, userspec=None, setup=False)``: Adds a new
  install record to the Spack Environment.

  - ``userspec`` is optional (see Spack Server below).

  - repo is a bystring representing the serialized version of the repo

  - If the record already exists, then everything except
    ``userspec`` must match.  Unless the newly supplied ``userspec``
    is ``None``, it should overwrite what is already there.

  - Calls ``spack_database.add()`` as appropriate.

* ``remove(hash)``: Removes an install record from the Spack Environment.

* ``install(hash)``: Installs a previously-added install record.

  - Installation is handled by calling ``spack_server.install()`` (see
    below), which returns the install ``path``.

  - Calls ``add(..., path=path)``.  This will (in theory) be done afer
    install, since it needs to know the install ``path``.

  - Must think about atomicity issues; what happens to these data
    structures if the install fails in the middle?

* ``install()``: Installs all Install Recs in this environment.

  - Calls ``spack_environment.install()`` repeatedly.

  - If stuff was already installed on the Spack Server, things will be
    pretty fast.

  - Generates the ``<package>-config.py`` files as appropriate.

* ``uninstall(hash)``: Uninstalls the Install Rec.

  - Calls ``remove()``

  - Calls ``spack_server.uninstall()``.

* ``uninstall()``: Uninstalls all Install Recs from this environment.

* ``validate(update=False)``: calls ``validate()`` on each install record.

* ``reorder()``: There needs to be some way for users to change the
  ``priority`` values on Install Records.  Maybe this will be done by
  manually editing a JSON file, at least at first.

* ``create_view(location)``: Creates a Spack View from the environment.

  - ``package.py`` functionality should be extended so packages can
    dictate how they should be merged into views.

* ``write_modules(..., location, ...)``: Generate the module files for
  an environment.

  - Options could include the module type (TCL/Lmod), the location to
    generate the modules, etc.

  - Existing modules would get overwritten...

  - Packages should be able to specify which sub-packages'
    environments they need at runtime.  See #3134.

* ``write_single_module()``: Generate a SINGLE module file that loads
  the appropraite environment.

  - Packages should be able to specify which sub-packages'
    environments they need at runtime.  See #3134.

  - Maybe ``write_modules()`` should be deprecated.  Generating
    modules with hashes has many problems, and maybe it's not what
    users want anyway.

Install Record API
------------------

* ``validate(update=False)``: Re-concretizes ``userspec`` with the
  current Spack version, configuration, etc. and notes any changes ---
  including changes in hashes or the actual ``package.py`` files.

  - If ``update=True``, then the Install Record will be overwritten
    based on the new concretize / package information.

Install Repo API
----------------

* ``load(namespace, package)``: Loads a Spack package from the Install
  Repo, returning a Spack ``Package`` class; to be used down the line
  to install, generate modules, etc.

Spack Database
--------------

* ``add(hash, concspec, path, envid)``: Adds a record to the Spack database.
  - ``envid`` is used to set / update ``ref_counts`` and ``ref_count``.
  - If the record already exists, then ``path`` should not be changed;
    or if it is, the *hash* of ``path`` should not be changed.

* ``validate()``: Checks to see that every package in the database is
  installed.  If not, sets ``installed=False``.


Spack Server
------------

* ``install(hash, concspec, hashes, repo, envid)``: Installs the
  package(s), and adds it to the Spack database.
  - Called by Spack Client
  - `envid` must be the Envirnoment ID of the *root* environment for
    the Spack Client that called this.

* ``uninstall(hash, envid)``: Reduces refcount on the package(s), and
  possibly uninstalls it.

* ``sync_refcounts(hash_counts, envid)``: Syncs refcounts with all the
  known refcounts on a client's root environment
  - ``hash_counts``: List of ``(hash, refcount)`` tuples.
  - Potentially uninstalls package if ``refcount`` goes to zero.
  - Reports an error if package is not found in the database.
  - Sets ``refcount`` (for this ``envid``) to zero for any hahes *not*
    listed in ``hash_counts``.

Spack Client
------------

* ``newenv(name, location)``: Creates a new environment and adds to
  Spack Client's list of managed environments.

  - Spack Client needs to know which environments it is managing, so
    it can keep refcounts up to date with the root environment (and
    the Spack Server).

* ``addenv(name, location)``: Adds an existing environment to Spack
  Client's list of managed environments.

  - Clears the Spack Database for that environment.  Subsequent calls
    to ``spackenv.install()`` will be very fast if the Spack Server
    happened to have already installed this stuff.

* ``getenv(name)``: Returns a managed Spack Environment of that name.

  - Caller can then call ``spackenv.install()``,
    ``spackenv.uninstall()``, ``spackenv.create_view()``, etc.

* ``set_current_env(name)``: Use the named environment as the current
  environment for subsequent calls to Spack Client API.

  - This can be overridden if the user sets the ``SPACKENV``
    environment variables.

  - Both can be overridden if the user puts ``--env=...` on the
    command line BEFORE The Spack command.  (eg: ``spack --env=myenv
    install netcdf``).

* ``add(userspec, env, install=False, setups=...)``: Concretizes ``userspec``, then
  calls ``spackenv.add()``.

  - If ``install=True``, also calls ``spackenv.install()``.

  - Concretization with respect to `env`.

  - ``setups`` is list of packages that should be setup, not installed.


User Interface
==============

This user interface is with respect to a single Spack Client.

* ``spack newenv``, ``spack addenv``, ``spack setenv``: Call through
  to Spack Client methods.

* ``spack install/add <spec> --setup=...``: Call through to
  ``client.add(...)``.

* ``spack uninstall <spec>|<hash>``: Call through to
  ``spackenv.uninstall()`` for the appropriate environment.

  - ``<spec>`` must be turned into a hash that matches an Install Rec.
    This will be done on a "best effort" basis.  Things to try
    include:

    - Look through the environment to see if anything "matches."

    - Try re-concretizing, see if anything matches.


* ``spack install <environment>``: Call through to ``spackenv.install()``.

* ``spack uninstall <environment>``: Call through to ``spackenv.uninstall()``.


