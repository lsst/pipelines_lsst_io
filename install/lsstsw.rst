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

You need to install some prerequisites to build the LSST Stack from source:

- Install prerequisites for your platform: :doc:`macOS <prereqs/macos>`, :doc:`Debian / Ubuntu <prereqs/debian>`, or :doc:`Centos / RedHat <prereqs/centos>`.
- If you opt not to use ``lsstsw`` \’s default Python environment you need to :ref:`install these Python dependencies <python-deps>`.
- If you intend to use a Git LFS repository, like `ci_hsc`_ or `afwdata`_, :doc:`install and configure Git LFS <git-lfs>`.

.. _lsstsw-deploy:

2. Obtaining a Development Stack with lsstsw
============================================

Code for the LSST Stack is distributed across many Git repositories (see `github.com/lsst <https://github.com/lsst>`_).
`lsstsw <https://github.com/lsst/lsstsw>`_ is a tool that helps you manage the codebase by automating the process of cloning all of these repositories and building that development Stack for testing.

Begin by choosing a working directory, then deploy ``lsstsw`` into it:

.. code-block:: bash
   :linenos:

   git clone https://github.com/lsst/lsstsw.git
   cd lsstsw
   ./bin/deploy
   . bin/setup.sh

The ``deploy`` script automates several things for you:

1. installs a miniconda_ Python environment specific to this lsstsw workspace,
2. installs EUPS_ in :file:`eups/current/`,
3. clones `lsst-build`_, which will run the build process for us,
4. clones versiondb_, a robot-made Git repository of package dependency information, and
5. creates an empty Stack *installation* directory, :file:`stack/`.

``lsstsw`` `clones repositories using HTTPS <https://github.com/lsst/lsstsw/blob/master/etc/repos.yaml>`_.
Our guide to `Setting up a Git credential helper <http://developer.lsst.io/en/latest/tools/git_lfs.html>`_ will allow you to push new commits up to GitHub without repeatedly entering your GitHub credentials.

.. The ``setup.sh`` step enables EUPS_, the package manager used by LSST.
.. **Whenever you open a new terminal session, you need to run '. bin/setup.sh' to activate your lsstsw environment.**

.. _lsst-build: https://github.com/lsst/lsst_build
.. _versiondb: https://github.com/lsst/versiondb
.. _EUPS: https://github.com/RobertLuptonTheGood/eups
.. _miniconda: http://conda.pydata.org/miniconda.html

.. _lsstsw-rebuild:

3. Build Science Pipelines
==========================

From the :file:`lsstsw` directory, run:

.. code-block:: bash

   rebuild lsst_distrib

Once the ``rebuild`` step finishes, note the build number printed on screen.
It is formatted as "``bNNNN``."
Tell EUPS this is the current build by making a clone of the build's EUPS tag and calling it "``current``:"

.. code-block:: bash

   eups tags --clone bNNNN current

The ``rebuild`` command accomplishes the following:

1. Clones all Science Pipelines packages from `github.com/lsst <https://github.com/lsst>`__.
   A high-bandwidth connection is helpful since the stack contains a non-trivial amount of code and test data.
2. Runs the Scons-based build process to compile C++, make Swig bindings, and ultimately create the :lmod:`lsst` Python package.
   The Stack is built and installed into the :file:`stack/` directory inside your :file:`lsstsw/` work directory.

Finally, set up the packages with EUPS:

.. code-block:: bash

   setup lsst_distrib

.. _lsstsw-setup:

4. Sourcing the Pipelines in a New Shell
========================================

In every new shell session you will need to 'setup' the Science Pipelines.
Do this by running the ``setup.sh`` from the ``lsstsw/`` directory:

.. code-block:: bash

   . bin/setup.sh
   setup lsst_distrib  # or an alternative top-level package

.. note::

   If you are using a tcsh shell, run ``. bin/setup.csh`` instead (note ``csh`` extension).

.. _lsstsw-testing-your-installation:

5. Testing Your Installation
============================

Once the LSST Science Pipelines are installed, you can verify that it works by :doc:`running a demo project <demo>`.
This demo processes a small amount of SDSS data.

.. _lsstsw-development:

6. Bonus: Developing a Package
==============================

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

.. _`ci_hsc`: https://github.com/lsst/ci_hsc
.. _`afwdata`: https://github.com/lsst/afwdata
