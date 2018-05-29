#############################################################
Building a package with the installed Science Pipelines stack
#############################################################

You can build packages alongside an LSST Science Pipelines stack that you have installed with :doc:`newinstall.sh <newinstall>`, :doc:`lsstsw <lsstsw>`, or :doc:`Docker <docker>`.
This pages describes how to build and set up packages cloned directly from GitHub.

.. note::

   If you are developing with the LSST Docker images, refer to :ref:`docker-develop`.
   That page describes Docker-specific patterns and complements the general information on this page.

.. _package-dev-prereq:

0. Prerequisites
================

Before developing an individual package, you need an installed Science Pipelines stack.
You can install the Pipelines through any of these methods: :doc:`newinstall.sh <newinstall>`, :doc:`lsstsw <lsstsw>`, or :doc:`Docker <docker>`.

Then set up the Pipelines software in a shell.
See :doc:`setup` for more information.

.. warning::

   **newinstall.sh users:** read :ref:`newinstall-binary-compatibility` if the installed Pipelines stack uses prebuilt binary packages.

.. _package-dev-clone:

1. Clone a package
==================

Use Git to clone the package you want to work on.
Most LSST packages are available in the LSST's GitHub organization (https://github.com/lsst).
The `repos.yaml file in the 'repos' repository <https://github.com/lsst/repos/blob/master/etc/repos.yaml>`_ also maps package names to repository URLs.

For example: 

.. code-block:: bash

   git clone https://github.com/lsst/pipe_tasks
   cd pipe_tasks

You can also create a new package repository, though this is beyond this document's scope.

You will work from a Git branch when developing a package.
The `DM Developer Guide <https://developer.lsst.io/processes/workflow.html>`_ describes the branching workflow that LSST staff use.

.. warning::

   **lsstsw users:** The :file:`lsstsw/build` directory already includes clones of Git repositories.
   These repositories are reset when you run :ref:`rebuild <lsstsw-rebuild>`, though, so you can potentially lose local changes.
   It's usually better to clone and work with Git repositories outside of the :file:`lsstsw` directory.

.. _package-dev-setup:

2. Checkout the appropriate version
===================================

In order for your local version of a package to work properly with the rest of
the LSST software that you've already installed, it is necessary to checkout the
matching version of your local package from git.

When releases of the Science Pipelines are made, the appropriate version of the
repository is tagged with that version string. For example, to checkout the
matching software for the 15.0 release:

.. code-block:: bash

   git checkout -t 15.0

If you have installed one of the weekly pipelines builds, the tag is in the form
``w.2018.28``. Note that the weekly git tags uses periods as a separator, while
the EUPS tags use underscores.

3. Set up the package
=====================

From the package's directory, set up the package itself in the EUPS stack:

.. code-block:: bash

   setup -r .

The ``-r .`` argument tells EUPS to use your current working directory as a
package.

This will make the package available in your current terminal session, supplanting
any other version that was previously setup. This only applies to your current
terminal and only for the duration of that session. Future sessions will need to
re-setup this package to continue development.

.. _package-dev-scons:

4. Build the package with Scons
===============================

.. code-block:: bash

   scons -Q -j 6 opt=3 

These flags configure Scons:

- ``-Q``: reduce logging to the terminal.
- ``-j 6``: build in parallel (for example, with '6' CPUs).
- ``opt=3``: build with level 3 optimization.
  Use ``opt=0`` (or ``opt=g`` with gcc compilers) for debugging.

This ``scons`` command will run several targets by default, in sequence:

1. ``lib``: build the C++ code and Pybind11 interface layer.
2. ``python``: install the Python code.
3. ``tests``: run the unit tests.
4. ``example``: compile the examples.
5. ``doc``: compile Doxygen-based documentation.
6. ``shebang``: convert the ``#!/usr/bin/env`` line in scripts for OS X compatibility (see `DMTN-001 <https://dmtn-001.lsst.io>`_).

You can build a subset of these targets by specifying one explicitly.
For example, to compile C++, build the Python package and run tests:

.. code-block:: bash

   scons -Q -j 6 opt=3 tests

.. _package-dev-next-steps:

Next steps
==========

By following these steps, you have built a package from source alongside an installed Science Pipelines software stack.
Now when you run the Science Pipelines, your new package will be used instead of the equivalent package provided by the Science Pipelines installation.
Here are some tasks related to maintaining this development software stack:

- :ref:`package-dev-eups-list`.
- :ref:`package-dev-setup-shell`.
- :ref:`package-dev-unsetup`.

.. _package-dev-eups-list:

Reviewing set up packages
-------------------------

Packages that are *set up* are part of the active Science Pipelines software stack.
You can see what packages are currently set up by running:

.. code-block:: bash

   eups list -s

You can also review what version of a single package is set up by running:

.. code-block:: bash

   eups list <package name>

.. _package-dev-setup-shell:

Setting up in a new shell
-------------------------

Whenever you open a new shell you need to set up both the LSST software environment and the LSST software stack.
See :doc:`setup` for the basic procedure.

In addition to setting up the installed Science Pipelines software, you separately need to set up the development package itself.
You can do this following the instruction in step :ref:`package-dev-setup`.

.. _package-dev-unsetup:

Un-set up the development package
---------------------------------

You can un-set up a development package to revert to the installed LSST Science Pipelines distribution.

To switch from a development package to the released package:

.. code-block:: bash

   setup -j <package name> -t current

``current`` is the default tag normally used for the installed LSST Science Pipelines software stack.

To un-set up a development package without replacing it:

.. code-block:: bash

   unsetup -j <package name> -t $USER

This is useful if you are developing a new package that is not part of the installed LSST Science Pipelines software stack.
