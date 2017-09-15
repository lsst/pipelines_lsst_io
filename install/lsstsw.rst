#######################################
Installation with lsstsw and lsst-build
#######################################

This page will guide you through installing the LSST Science Pipelines from source with lsstsw and lsst-build.
These are the same tools LSST Data Management uses to build and test the Science Pipelines.

Since lsstsw presents the Science Pipelines as a directory of Git repositories clone from `github.com/lsst <https://github.com/lsst>`__, this installation method can be very convenient for developing Science Pipelines code.

Science Pipelines developers should also consult the `DM Developer Guide <https://developer.lsst.io>`_, and the `Workflow <https://developer.lsst.io/processes/workflow.html>`_ page in particular.

If you have difficulty installing LSST software:

- review the :ref:`known installation issues for your platform <installation-issues>`.
- reach out on the `Support forum at community.lsst.org <https://community.lsst.org/c/support>`_.

.. _lsstsw-prerequisites:

1. Prerequisites
================

Before you begin:

- `Install and configure Git LFS <https://developer.lsst.io/tools/git_lfs.html>`_ for LSST DM's data servers.
- Install prerequisites for your platform: :doc:`macOS <prereqs/macos>`, :doc:`Debian / Ubuntu <prereqs/debian>`, or :doc:`Centos / RedHat <prereqs/centos>`.
- If you opt not to use ``lsstsw`` \’s default Python environment you need to :ref:`install these Python dependencies <python-deps>`.

.. _lsstsw-deploy:

2. Deploy lsstsw
================

.. Code for the LSST Stack is distributed across many Git repositories (see `github.com/lsst <https://github.com/lsst>`_).
.. `lsstsw <https://github.com/lsst/lsstsw>`_ is a tool that helps you manage the codebase by automating the process of cloning all of these repositories and building that development Stack for testing.

Begin by choosing a working directory, then deploy ``lsstsw`` into it:

.. code-block:: bash

   git clone https://github.com/lsst/lsstsw.git
   cd lsstsw
   ./bin/deploy
   source bin/setup.sh

For more information about the :command:`deploy` command, such as using Python 2.7 instead of 3, see :ref:`lsstsw-about-deploy`.

.. The ``setup.sh`` step enables EUPS_, the package manager used by LSST.
.. **Whenever you open a new terminal session, you need to run '. bin/setup.sh' to activate your lsstsw environment.**

.. _lsstsw-rebuild:

3. Build the Science Pipelines packages
=======================================

From the :file:`lsstsw` directory, run:

.. code-block:: bash

   rebuild lsst_distrib

Once the ``rebuild`` step finishes, note the build number printed on screen.
It is formatted as "``bNNNN``."
Tag this build as ``current`` so that EUPS can set it up by default:

.. code-block:: bash

   eups tags --clone bNNNN current

Finally, set up the packages with EUPS:

.. code-block:: bash

   setup lsst_distrib

See :doc:`setup` for more information.

.. _lsstsw-testing-your-installation:

4. Testing Your installation (optional)
=======================================

Once the LSST Science Pipelines are installed, you can verify that it works by :doc:`running a demo project <demo>`.
This demo processes a small amount of SDSS data.

.. _lsstsw-setup:

Sourcing the Pipelines in a new shell
=====================================

In every new shell session you will need to set up the Science Pipelines environment and EUPS package stack.

Run these two steps:

1. Activate the lsstsw software environment by sourcing the :file:`setup.sh` script in lsstsw's :file:`bin` directory:

   .. code-block:: bash
   
      source bin/setup.sh

   If you are running in a :command:`csh` or :command:`tcsh`, run this set up script instead:

   .. code-block:: bash
   
      source bin/setup.csh

2. Set up a :doc:`top-level package <top-level-packages>`:

   .. code-block:: bash
   
      setup lsst_distrib

   Instead of ``lsst_distrib``, you can set up a different top-level package like ``lsst_apps`` or any individual EUPS package.
   See :doc:`top-level-packages`.

.. _lsstsw-next:

Next steps and advanced topics
==============================

- :ref:`lsstsw-about-deploy`.
- :ref:`lsstsw-py2`.
- :ref:`lsstsw-about-rebuild`.
- :ref:`lsstsw-branches`.
- :ref:`lsstsw-deploy-ref`.
- :ref:`lsstsw-rebuild-ref`.

.. _lsstsw-about-deploy:

About the lsstsw deploy script
------------------------------

The ``deploy`` script automates several things to prepare an LSST development environment:

1. Installs Git.
2. Installs Git LFS (*you* are still responsible for `configuring it <http://developer.lsst.io/en/latest/tools/git_lfs.html>`_).
3. Installs a Miniconda_ Python environment specific to this lsstsw workspace.
   The default Python is Python 3, but you can switch to Python 2.7 if necessary.
   See :ref:`lsstsw-py2`.
4. Installs EUPS_ into :file:`eups/current/`.
5. Clones `lsst-build`_, which runs the build process.
6. Clones versiondb_, a robot-managed Git repository of package dependency information.
7. Creates an empty stack *installation* directory, :file:`stack/`.

This environment, including the EUPS, Miniconda, Git, and Git LFS software, is only activated when you source the :file:`bin/setup.sh` or :file:`bin/setup.csh` scripts in a shell.
Otherwise, lsstsw does not affect the software installed on your computer.

See also: :ref:`lsstsw-deploy-ref`.

.. _lsstsw-py2:

How to use Python 2.7
---------------------

The lsstsw :command:`deploy` script installs Miniconda_ as self-contained Python environment.
By default, :command:`deploy` installs a Python 3 version of Miniconda_.
For testing Python 2.7 compatibility, you can create an lsstsw deployment with a Python 2.7 version of Miniconda using the :option:`deploy -2` argument:

.. code-block:: bash

   ./bin/deploy -2

.. _lsstsw-about-rebuild:

About the lsstsw rebuild command
--------------------------------

The :command:`rebuild` command accomplishes the following:

1. Clones all Science Pipelines packages from `github.com/lsst <https://github.com/lsst>`__.
   :command:`rebuild`

2. Runs the Scons-based build process to compile C++, make Pybind11 bindings, and ultimately create the :lmod:`lsst` Python package.
   The stack is built and installed into the :file:`stack/` directory inside your :file:`lsstsw/` work directory.

``lsstsw`` clones repositories using HTTPS (`see repos.yaml <https://github.com/lsst/repos/blob/master/etc/repos.yaml>`_.
Our guide to `Setting up a Git credential helper <http://developer.lsst.io/en/latest/tools/git_lfs.html>`_ will allow you to push new commits up to GitHub without repeatedly entering your GitHub credentials.

See also: :ref:`lsstsw-rebuild-ref`.

.. _lsstsw-branches:

Building from branches
----------------------

lsstsw's :command:`rebuild` enables you to clone and build development branches.

To build ``lsst_distrb``, but use the Git branch ``my-feature`` when it's available in a package's repository:

.. code-block:: bash

   rebuild -r my-feature lsst_distrib

Multiple ticket branches across multiple products can be built in order of priority:

.. code-block:: bash

   rebuild -r feature-1 -r feature-2 lsst_distrib

In this example, a ``feature-1`` branch will be used in any package's Git repository.
A ``feature-2`` branch will be used secondarily in repositories where ``feature-1`` doesn't exist.
Finally, ``lsstsw`` falls back to using the ``master`` branch for repositories that lack both ``feature-1`` and ``feature-2``.

.. _lsstsw-deploy-ref:

lsstsw deploy command reference
-------------------------------

.. program:: deploy

.. code-block:: text

   usage: deploy.sh [-2|-3] [-b] [-h]

.. option:: -2

   Install a Python 2-based Miniconda_.

.. option:: -3

   Use a Python 3-based Miniconda_ (default).

.. option:: -b

   Use bleeding-edge conda packages.

.. option:: -h

   Print the help message.

.. _lsstsw-rebuild-ref:

lsstsw rebuild command reference
--------------------------------

.. program:: rebuild

.. code-block:: text

   rebuild [-p] [-n] [-u] [-r <ref> [-r <ref2> [...]]] [-t <eupstag>] [product1 [product2 [...]]]

.. option:: -p

   Prep only.

.. option:: -n

   Do not run :command:`git fetch` in already-downloaded repositories.

.. option:: -u

   Update the :file:`repos.yaml` package index to the ``master`` branch on GitHub of https://github.com/lsst/repos.

.. option:: -r <git ref>

   Rebuild using the Git ref.
   A Git ref can be a branch name, tag, or commit SHA.
   Multiple ``-r`` arguments can be given, in order or priority.

.. option:: -t

   EUPS tag.

.. _lsst-build: https://github.com/lsst/lsst_build
.. _versiondb: https://github.com/lsst/versiondb
.. _EUPS: https://github.com/RobertLuptonTheGood/eups
.. _Miniconda: http://conda.pydata.org/miniconda.html

.. _lsstsw-development:

Developing a package
--------------------

An lsstsw-based installation is great for developing packages against the LSST Science Pipelines stack.
The `Developer Guide describes Data Management's workflow <https://developer.lsst.io/processes/workflow.html>`__, but this section will get your started with the basics related to lsstsw and EUPS.

1. Stack packages are found in the :file:`lsstsw/build/` directory.

2. Create a new branch in a package's Git repository,

   .. code-block:: bash

      git checkout -b {{ticket-name}}

   Then declare this package for EUPS and set it up:

   .. code-block:: bash

      eups declare -r . -t $USER {{package_name}} git
      setup -r . -t $USER
    
   Unpacking the ``eups declare`` arguments:
   
   - ``-r .`` is the path to the package's repository, which is the current working directory.
     You don't *need* to be in the repository's directory if you provide the path appropriately.
   - ``-t $USER`` sets the EUPS *tag*.
     We use this because your username (``$USER``) is an allowed EUPS tag.
   - ``git`` is used as an EUPS *version*.
     Semantically we default to calling the version "``git``" to indicate this package's version is the HEAD of a Git development branch.
   
   In the above ``eups declare`` command we associated the package version "``git``" with the tag "``$USER``."
   In running ``setup``, we told EUPS to setup the package *and its dependencies* with the version associated to the ``$USER`` tag.
   If the ``$USER`` tag isn't found for dependencies, EUPS will revert to using versions of dependencies linked to the ``current`` tag.
   This is why we initially declared the entire lsstsw repository to have the version ``current``.

3. Build the package with Scons:

   .. code-block:: bash
   
      scons -Q -j 6 opt=3 
   
   These flags tell SCons to build with flags:
   
   - ``-Q``: reduce logging to the terminal,
   - ``-j 6``: build in parallel (e.g., with '6' CPUs),
   - ``opt=3``: build with level 3 optimization.
   
   This ``scons`` command will run several targets by default, in sequence:
   
   1. ``lib``: build the C++ code and SWIG interface layer
   2. ``python``: install the Python code
   3. ``tests``: run the test suite
   4. ``example``: compile the examples,
   5. ``doc``: compile Doxygen-based documentation, and
   6. ``shebang``: convert the ``#!/usr/bin/env`` line in scripts for OS X compatibility (see `DMTN-001 <http://dmtn-001.lsst.io>`_).

   You can build a subset of these targets by specifying one explicitly.
   To simply compile C++, SWIG, build the Python package and run tests:
   
   .. code-block:: bash
   
      scons -q -j 6 opt=3 tests
