:orphan: 1

.. NOTE: this page is not currently part of the built site, though it is intended for re-integration.

###############################################################
Developing a package with the installed Science Pipelines stack
###############################################################

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
