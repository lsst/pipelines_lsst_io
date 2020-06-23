#######################################
Installation with lsstsw and lsst-build
#######################################

This page guides you through installing the LSST Science Pipelines from source with lsstsw and lsst-build.
These are the same tools LSST Data Management uses to build and test the Science Pipelines.

Since lsstsw presents the Science Pipelines as a directory of Git repositories cloned from `github.com/lsst <https://github.com/lsst>`__, this installation method can be very convenient for developing Science Pipelines code.
Other methods of installing LSST Science Pipelines software are :doc:`newinstall.sh <newinstall>` and :doc:`Docker <docker>`.

If you have issues using lsstsw, here are two ways to get help:

- Review the :ref:`known installation issues <installation-issues>`.
- Ask a question on the `LSST Community support forum <https://community.lsst.org/c/support>`_.

.. _lsstsw-prerequisites:

1. Prerequisites
================

The LSST Science Pipelines are developed and tested primarily on CentOS, but can be compiled and run on macOS, Debian, Ubuntu, and other Linux distributions.
See :ref:`prereq-platforms` for information about LSST's official reference platform and build reports with other platforms, and follow the instructions under :ref:`system-prereqs` to ensure you have installed the prerequisite software for your platform.

Before you begin:

- If you intend to use a Git LFS repository, like `testdata_ci_hsc`_ or `afwdata`_, :doc:`install and configure Git LFS <git-lfs>`.

.. _lsstsw-deploy:

2. Deploy lsstsw
================

Begin by choosing a working directory, then deploy ``lsstsw`` into it:

.. code-block:: bash

   git clone https://github.com/lsst/lsstsw.git
   cd lsstsw
   ./bin/deploy
   source bin/envconfig.sh

For more information about the :command:`deploy` command, see :ref:`lsstsw-about-deploy`.

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

.. note::

   You can do more with the :command:`build` command, including building from branches of GitHub repositories.
   For more information:

   - :ref:`lsstsw-about-rebuild`.
   - :ref:`lsstsw-branches`.
   - :ref:`lsstsw-rebuild-ref`.

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

1. Activate the lsstsw software environment by sourcing the :file:`envconfig.sh` script in lsstsw's :file:`bin` directory:

   .. code-block:: bash

      source bin/envconfig.sh

   If you are running in a :command:`csh` or :command:`tcsh`, run this set up script instead:

   .. code-block:: bash

      source bin/envconfig.csh

2. Set up a :doc:`top-level package <top-level-packages>`:

   .. code-block:: bash

      setup lsst_distrib

   Instead of ``lsst_distrib``, you can set up a different top-level package like ``lsst_apps`` or any individual EUPS package you previously installed.
   See :doc:`top-level-packages`.

.. _lsstsw-next:

Next steps and advanced topics
==============================

- :ref:`lsstsw-about-deploy`.
- :ref:`lsstsw-about-rebuild`.
- :ref:`lsstsw-branches`.
- :ref:`lsstsw-deploy-ref`.
- :ref:`lsstsw-rebuild-ref`.

.. _lsstsw-about-deploy:

About the lsstsw deploy script
------------------------------

The ``deploy`` script automates several things to prepare an LSST development environment:

1. Installs Git.
2. Installs Git LFS (*you* are still responsible for :doc:`configuring it <git-lfs>`).
3. Installs a Miniconda_ Python 3 environment specific to this lsstsw workspace.
4. Installs EUPS_ into :file:`eups/current/`.
5. Clones `lsst-build`_, which runs the build process.
6. Clones versiondb_, a robot-managed Git repository of package dependency information.
7. Creates an empty stack *installation* directory, :file:`stack/`.

This environment, including the EUPS, Miniconda, Git, and Git LFS software, is only activated when you source the :file:`bin/envconfig.sh` or :file:`bin/envconfig.csh` scripts in a shell.
Otherwise, lsstsw does not affect the software installed on your computer.

See also: :ref:`lsstsw-deploy-ref`.

.. _lsstsw-about-rebuild:

About the lsstsw rebuild command
--------------------------------

The :command:`rebuild` command accomplishes the following:

1. Clones all Science Pipelines packages from `github.com/lsst <https://github.com/lsst>`__.
   The `repos.yaml`_ file in the https://github.com/lsst/repos repository maps package names to GitHub repositories.

2. Runs the Scons-based build process to compile C++, make Pybind11 bindings, and ultimately create the :lmod:`lsst` Python package.
   The stack is built and installed into the :file:`stack/` directory inside your :file:`lsstsw/` work directory.

lsstsw clones repositories using HTTPS (`see repos.yaml <https://github.com/lsst/repos/blob/master/etc/repos.yaml>`_).
Our guide to `Setting up a Git credential helper <http://developer.lsst.io/en/latest/tools/git_lfs.html>`_ will allow you to push new commits up to GitHub without repeatedly entering your GitHub credentials.

See also: :ref:`lsstsw-rebuild-ref`.

.. _lsstsw-branches:

Building from branches
----------------------

lsstsw's :command:`rebuild` command enables you to clone and build development branches.

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

   Install a Python 2-based Miniconda_ (not supported for ``v16_0`` of the LSST Science Pipelines and later)

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
.. _`repos.yaml`: https://github.com/lsst/repos/blob/master/etc/repos.yaml
.. _`testdata_ci_hsc`: https://github.com/lsst/testdata_ci_hsc
.. _`afwdata`: https://github.com/lsst/afwdata
