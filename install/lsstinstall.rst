#########################################
Install with lsstinstall and eups distrib
#########################################

This page guides you through installing the LSST Science Pipelines software using the lsstinstall tool.
This installation method is recommended for anyone who uses or develops the Pipelines software.

If you have issues with the installation, here are two ways to get help:

- Review the :ref:`known installation issues <installation-issues>`.
- Ask a question on the `LSST Community support forum <https://community.lsst.org/c/support>`_.

.. _lsstinstall-prereqs:

1. Prerequisites
================

The LSST Science Pipelines are developed and tested primarily on AlmaLinux 9, but can be compiled and run on macOS, Debian, Ubuntu, and other Linux distributions.
See :ref:`prereq-platforms` for information about LSST's official reference platform and build reports with other platforms, and follow the instructions under :ref:`system-prereqs` to ensure you have installed the prerequisite software for your platform.

..
  TK recommended memory, disk space, and build time.

.. _lsstinstall-source-dir:

2. Make an installation directory
=================================

Create a directory where you want to install the LSST Science Pipelines into.
For example:

.. code-block:: bash

   mkdir -p lsst_stack
   cd lsst_stack

If you are installing the software for multiple users (a shared stack), see :ref:`lsstinstall-shared-permissions`.

.. _lsstinstall-run:

3. Run lsstinstall
==================

Run :command:`lsstinstall` to set up the environment you'll install the LSST Science Pipelines into.
For most use cases we recommend downloading and running :command:`lsstinstall` like this:

.. jinja:: default

   .. code-block:: bash

      curl -OL https://ls.st/lsstinstall
      chmod u+x lsstinstall
      ./lsstinstall -T {{ release_eups_tag }}

The :option:`-T` option specifies the eups tag associated with the release you would like to install.
You can use any release, including the official releases (starting with ``v``), the weekly releases (starting with ``w_``), or the daily releases (starting with ``d_``).

Then load the LSST software environment into your shell:

.. code-block:: bash

   source loadLSST.sh

To customize the conda environment used, set the ``LSST_CONDA_ENV_NAME`` environment variable to a conda enviroment name when sourcing the file.
For other conda environments installed by LSST tools, this name will be the ``rubin-env`` metapackage version prefixed with ``lsst-scipipe-``.

.. note::

   Here are ways to customize the :command:`lsstinstall` installation for specific needs:

   - :ref:`lsstinstall-user-conda`.
   - The recommended installation uses precompiled binary tarballs if they're available for your platform (and falls back to a source build).
     See :ref:`lsstinstall-binary-packages`.

   For background information about :command:`lsstinstall`, see:

   - :ref:`lsstinstall-background`.
   - :ref:`lsstinstall-miniforge3`.
   - :ref:`lsstinstall-reference`.

   To find the ``rubin-env`` conda metapackage version appropriate for a particular science pipelines release, see :ref:`release-history` or the release tag files at `https://eups.lsst.codes/stack/src/tags/`_.

.. _lsstinstall-install:

4. Install Science Pipelines packages
=====================================

.. jinja:: default

   The LSST Science Pipelines is distributed as the ``lsst_distrib`` EUPS package.
   Install the current official release version, ``{{ release_eups_tag }}``:

   .. code-block:: bash

      eups distrib install -t {{ release_eups_tag }} lsst_distrib
      setup lsst_distrib

You should use the same release tag here as you used for :command:`lsstinstall` above.
If you do not need all of ``lsst_distrib``, you can specify one or more lower-level EUPS packages.

If prebuilt binaries are available for your platform (and you did not specify the :option:`-B` argument to the :command:`lsstinstall` command) the installation should take roughly 10 minutes.
Otherwise, the installation falls back to a source build that can take two hours, depending on the top-level package and your machine's performance.
See :ref:`lsstinstall-find-binaries`.

.. TK add mention of how-to for debugging binary package root issues.

The last command, :command:`setup`, activates the installed packages in your shell environment.
You'll need to run :command:`setup` in each shell session you'll use the LSST Science Pipelines in.
See :doc:`setup` for more information.

.. note::

   - |eups-tag-mono| is the current version corresponding to this documentation.
     You can install other tagged versions of the LSST Science Pipelines, though.
     See :ref:`lsstinstall-other-tags`.


.. _lsstinstall-test:

5. Test your installation (optional)
====================================

Once the LSST Science Pipelines are installed, you can verify that it works by :doc:`running a demo pipeline <demo>`.

See :doc:`demo` for instructions.

.. _lsstinstall-next-steps:

Next steps
==========

Now that you have a working LSST Science Pipelines installation, these topics will help you learn and do more:

- :doc:`setup`.
- :doc:`top-level-packages`.
- :doc:`package-development`.

Advanced installation topics
============================

The above steps guided you through LSST's recommended installation.
These topics provide additional information about the installation and ways to customize it:

- :ref:`lsstinstall-shared-permissions`.
- :ref:`lsstinstall-background`.
- :ref:`lsstinstall-miniforge3`.
- :ref:`lsstinstall-user-conda`.
- :ref:`lsstinstall-rubin-env`.
- :ref:`lsstinstall-rubin-env-developer`.
- :ref:`lsstinstall-binary-packages`.
- :ref:`lsstinstall-find-binaries`.
- :ref:`lsstinstall-binary-compatibility`.
- :ref:`lsstinstall-other-tags`.
- :ref:`lsstinstall-reference`.

.. _lsstinstall-shared-permissions:

Setting unix permissions for shared installations
-------------------------------------------------

You can make a single LSST Science Pipelines installation accessible to multiple users on the same machine.

First, create a separate unix group (called ``lsst``, for example) with a ``umask`` of ``002`` (all access permissions for the group and allow other users to read/execute).

Then set the ownership of the installation directory to the ``lsst`` group, have the ``SGID`` (2000) bit set, and allow group read/write/execute (mode 2775).

After installing the conda environment, make sure to remove write permissions from the ``conda/pkgs/urls*`` files in the base conda installation.
If these files are writable, conda will attempt to record user environment information in the shared installation.

.. code-block:: bash

   chmod go-w ${CONDA_EXE%bin/conda}/pkgs/urls*

Making them unwritable may lead to spurious ``libmamba`` error messages when creating user environments, but these do not affect the installation.

.. _lsstinstall-background:

What lsstinstall does
---------------------

:command:`lsstinstall` creates a self-contained environment on your machine where you can install, run, and develop the LSST Science Pipelines.
You activate this environment in a shell by sourcing the :command:`loadLSST.sh` script in the installation directory (see :ref:`setup-howto`).

Here is how :command:`lsstinstall` prepares the environment:

- Identifies your operating system to determine what EUPS binary packages should be installed (the *EUPS package root,* see :ref:`lsstinstall-binary-packages`).
- Activates conda, installing it from Miniforge3_ if needed.
- Creates or updates a conda environment with conda packages that the LSST Science Pipelines depend on (see :ref:`system-prereqs`), including EUPS_, the package manager used by the LSST software stack.

For information about :command:`lsstinstall`\ ’s arguments, see :ref:`lsstinstall-reference`.

.. _lsstinstall-miniforge3:

About the Miniforge3 Python installed by lsstinstall
----------------------------------------------------

:command:`lsstinstall` by default installs a conda package manager based on Miniforge3_, a minimal version of Anaconda_ preconfigured to use packages from the curated ``conda-forge`` channel along with the ``mamba`` fast dependency solver.
This Python installation isn't required, but we recommend it.
See :ref:`lsstinstall-user-conda` if you would like to use your own pre-existing conda (but conda is required).

conda can maintain multiple environments, each with its own version of Python and other packages.
:command:`lsstinstall` will create one for each version of the Science Pipelines dependencies (currently managed by the rubin-env metapackage).
This includes the compilers and build tools as well as C++ and Python packages needed by the software.
You can add or install other packages into a Science Pipelines environment, or you can create independent environments composed of other packages or cloned from a Science Pipelines environment.

This Miniforge3 installation won't affect your other Python installations (like the system's Python, your own Anaconda or Miniconda, or virtual environments).
The LSST Miniconda environment is only active when you source the ``loadLSST`` script installed by :command:`lsstinstall` (see :doc:`setup`).

If you install other Python packages in a shell where the LSST Miniforge3 is activated (with :command:`pip install` or :command:`conda install`) those packages are installed into the LSST Miniforge3's :file:`site-packages`, not your system's.

.. _lsstinstall-user-conda:

How to use your own conda with lsstinstall
------------------------------------------

:command:`lsstinstall` installs a new conda based on Miniforge3 by default.
If desired, you can use your own pre-existing conda installation.

To do so, either have that conda activated when you run :command:`lsstinstall`, or provide the :option:`-p` option to :command:`lsstinstall` pointing to the conda installation's prefix.
Having :command:`mamba` installed in the ``base`` environment is recommended for faster dependency solves.

A Science Pipelines environment will still be created (unless you already have one).

.. _lsstinstall-rubin-env:

About the rubin-env metapackage
-------------------------------

The conda environment created by :command:`lsstinstall` is based on the rubin-env conda metapackage.
Each release of the LSST Science Pipelines is built with a particular rubin-env version.
A given rubin-env version is typically used to build many releases (daily, weekly, and sometimes major) of the Science Pipelines, and a given release of the Science Pipelines source is often compatible with more than one rubin-env version.

Note that a given rubin-env version does not itself exactly specify all versions of its dependencies.
We typically allow dependency versions to "float" to more recent updates in order to allow greater compatibility with user-installed packages and to pick up bug fixes.
We only restrict these updates if newer versions cause incompatibilities with the Science Pipelines source code.
This means that one user's installation of a given rubin-env version may be different from another's.
To assist with debugging, you may be asked to list the installed dependency versions with the :command:`conda env export` command.
In production, the dependencies are frozen at the versions that were tested when the :ref:`docker containers <docker>` were built.

You choose the version of the dependencies with the :command:`lsstinstall` arguments :option:`-T` (to match the version used to build a particular tag of the Science Pipelines), :option:`-X` (to use the exact packages used for that tag's build, not allowing any to float to more recent updates), or :option:`-v` (to specify a particular version manually).

You can update the versions of the rubin-env dependencies to the latest compatible ones for the rubin-env version specified by using :command:`lsstinstall` with the :option:`-u` option.

.. _lsstinstall-rubin-env-developer:

About the rubin-env-developer metapackage
-----------------------------------------

The rubin-env-developer metapackage adds tools and utilities that are useful for developers working on improving the LSST Science Pipelines but not necessarily for users processing data with them.
It can be installed on top of the rubin-env installation performed by :command:`lsstinstall` by specifying the :option:`-d` option.

Only rubin-env versions 5.0.0 and greater can use this option.


.. _lsstinstall-binary-packages:

About EUPS tarball packages
---------------------------

EUPS distrib binary (tarball) packages significantly speed up your installation.
Rather than compiling the LSST Science Pipelines from source, EUPS tarballs are prebuilt packages made specifically for supported platforms.

Platforms are defined by two factors:

1. Operating system.
2. rubin-env metapackage (Science Pipelines dependencies) version.

When you run :command:`lsstinstall`, it looks at your system to identify your operating system.

See :ref:`lsstinstall-rubin-env` for more about the rubin-env metapackage and how to select its version.
The EUPS packages that make up the Science Pipelines are installed within that environment, as they are only binary-compatible with its conda packages and tools.
The URLs used to retrieve EUPS packages are also stored within the environment in ``$EUPS_PATH/pkgroot``.
``loadLSST.sh`` will automatically read this file to enable proper use of :command:`eups distrib install` by setting the ``EUPS_PKGROOT`` environment variable.
Note that activating (or deactivating) conda environments does not automatically set this variable.

**See also:**

- :ref:`lsstinstall-find-binaries`
- :ref:`lsstinstall-binary-compatibility`

.. _lsstinstall-find-binaries:

How to determine if tarball packages are available for your platform
--------------------------------------------------------------------

When you run :ref:`eups distrib install <lsstinstall-install>`, it will attempt to install prebuilt binary packages first and fall back to compiling the Science Pipelines if binary packages aren't available for your platform (by default).
This fallback is automatic.
You'll know packages are being compiled from source if you see compiler processes (like :command:`gcc` or :command:`clang`) load your machine.

The instructions in this section will help you diagnose *why* :command:`eups distrib install` is falling back to a source installation.

First, get your EUPS package root URLs:

.. code-block:: bash

   eups distrib path

If the only URL listed is https://eups.lsst.codes/stack/src, it means that :command:`lsstinstall` configured your environment to not use binary packages.
Try re-running :command:`lsstinstall` (see :ref:`lsstinstall-run`) without the :option:`-B` argument, and check to make sure that your computing platform is supported for binary packages (currently Linux Intel and macOS Intel only).

If :command:`eups distrib path` includes an additional URL that doesn't end with ``/src`` (for example, ``https://eups.lsst.codes/stack/osx/10.9/conda-system/miniconda3-py38_4.9.2-0.8.0``), it means :command:`lsstinstall` has configured a binary package root.
The construction of the binary package root URL is based on your OS and rubin-env version (see :ref:`lsstinstall-binary-packages`).

:command:`eups distrib install` will only install binary packages if they exist on the binary package root.
To check this, open the binary package root URL in a web browser.
If the binary package root URL does not load in a browser it means LSST does not publish prebuilt binaries for your platform.
Either continue the installation from source or consider using the :doc:`LSST Docker images <docker>`.

If the URL does open, though, search for files with a ``.list`` extension.
A ``.list`` file is created for each release that has binary packages.
The name of the ``.list`` file matches the release tag (for example, ``w_2017_33.list``).
See :ref:`lsstinstall-other-tags` for more information about tags.

For example, if the binary package root is ``https://eups.lsst.codes/stack/osx/10.9/conda-system/miniconda3-4.9.2-0.7.0`` and you wish to install the ``w_2021_33`` tag, the file ``https://eups.lsst.codes/stack/osx/10.9/conda-system/miniconda3-4.9.2-0.7.0/w_2021_33.list`` must exist for a binary installation.

If the ``.list`` file does not exist for the tag you want to install, but does exist for other tags in that EUPS package root, it may be due to an issue with the LSST binary package publishing system.
You can either continue with an installation from source, consider switching to a tag that is known to have binary packages, or consider using :ref:`LSST's Docker images <docker>`.

.. _lsstinstall-binary-compatibility:

EUPS tarball packages and compiler compatibility
------------------------------------------------

EUPS binary tarball packages are prebuilt on LSST's continuous integration servers for a specific combination of operating system, compilers, Python, and Python dependencies.
The compilers and other linked dependencies are provided by conda-forge.
Compatibility with other compilers is not guaranteed.
Using a non-conda-forge compiler toolchain requires that the binary interface be the same as that used by the conda-forge toolchain.

.. _lsstinstall-other-tags:

Installing other releases (including daily and weekly tags)
-----------------------------------------------------------

The instructions on this page guide you through installing the current release of the LSST Science Pipelines corresponding to this documentation.
You can, however, install other releases by running :command:`lsstinstall -T <TAG>` and :command:`eups distrib install -t <TAG>` with a different tag.

Running :command:`lsstinstall -T <TAG>` creates the appropriate conda environment for the Science Pipelines if it doesn't already exist.
If you have more than one environment in a given installation, you can select between them by setting the ``LSST_CONDA_ENV_NAME`` environment variable before sourcing :command:`loadLSST.sh`.
You can then select between versions of the Science Pipelines within the same environment using :command:`setup -T <TAG>`.

The common types of tags are:

- **Major releases,** tagged as ``v<MAJOR>_<MINOR>_<PATCH>`` (for example, ``v14_0``).
- **Weekly builds,** tagged as ``w_<YEAR>_<N>`` (for example, ``w_2017_33`` is the 33rd weekly build in 2017).
- **Daily builds,** tagged as ``d_<YEAR>_<MONTH>_<DAY>`` (for example, ``d_2017_09_01`` is the daily build for September 1, 2017).

There are also tags pointing to the most recent releases:

- **Current major release,** tagged as ``current``.
- **Current weekly build,** tagged as ``w_latest``.
- **Current daily build,** tagged as ``d_latest``.

You can see all available tags at https://eups.lsst.codes/stack/src/tags (each tag has a ``.list`` file).

.. note::

   Binary installations may not be available for all tags.
   From https://eups.lsst.codes/stack, browse subdirectories corresponding to your platform and look for ``.list`` files of available tags.
   :command:`eups distrib install` automatically falls back to a source build if binaries are not available.

.. _lsstinstall-reference:

lsstinstall argument reference
--------------------------------

.. code-block:: text

   usage: lsstinstall [-n]
       [-T EUPS_TAG | -X EUPS_TAG | -v RUBINENV_VERSION]
       [-e ENV_NAME] [-u] [-d]
       [-p CONDA_PATH] [-P] [-C CHANNEL]
       [-E EUPS_URL]
       [-B] [-S]
       [-h]

.. option:: -n

    No-op.  Echo commands instead of running.

.. option:: -T <EUPS_TAG>

    Select the rubin-env version used to build the given EUPS_TAG.

.. option:: -X <EUPS_TAG>

    Select the exact environment used to build the given EUPS_TAG.

.. option:: -v <RUBINENV_VERSION>

    Select a particular rubin-env version (default=latest).

.. option:: -e <ENV_NAME>

    Specify the environment name to use; if it exists, assume that it is compatible and should be used.

.. option:: -u

    Update rubin-env in an existing environment to the latest build.

.. option:: -d

    Add a compatible rubin-env-developer to rubin-env (5.0.0 and later).

.. option:: -p <CONDA_PATH>

    Specify the path to the conda installation.
    If a conda installation already exists there, it will be used.
    If it does not exist, it will be created.
    If a conda is activated, it will be used, ignoring this option.

.. option:: -P

    DO NOT use an existing activated conda; always install a new one.

.. option:: -C <CHANNEL>

    Use the given conda channel before the conda-forge channel.
    May be repeated; first has highest priority.
    Useful primarily for testing new rubin-env versions in the ``dev`` channel.

.. option:: -E <EUPS_URL>

    Select a different EUPS distribution server root URL (default=``https://eups.lsst.codes/stack``).

.. option:: -B

    DO NOT use binary "tarball" eups packages.

.. option:: -S

    DO NOT use source eups packages.

.. option:: -b

    Ignored for backward compatibility.

.. option:: -c

    Ignored for backward compatibility.

.. option:: -t

    Ignored for backward compatibility.

.. option:: -h

    Display a help message.


.. _Miniforge3: https://mamba.readthedocs.io/en/latest/installation.html
.. _Anaconda: https://docs.anaconda.com
.. _lsstsw: https://github.com/lsst/lsstsw
.. _EUPS: https://github.com/RobertLuptonTheGood/eups
