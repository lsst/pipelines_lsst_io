.. _setup:

###########################################
Setting up installed LSST Science Pipelines
###########################################

Whenever you start a new command-line shell, you need to set up the LSST Science Pipelines software before you can use it.

.. _setup-howto:

Setting up
==========

Setting the LSST Science Pipelines in a shell is a two-step process:

1. Load the LSST environment by sourcing the ``loadLSST`` script in your installation directory:

   .. TODO Use sphinx-tabs here?

   .. code-block:: bash

      source loadLSST.bash # for bash
      source loadLSST.csh  # for csh
      source loadLSST.ksh  # for ksh
      source loadLSST.zsh  # for zsh

   To customize the conda environment used, set the ``LSST_CONDA_ENV_NAME`` environment variable to a conda enviroment name when sourcing the file.
   For other conda environments installed by LSST tools, this name will be the ``rubin-env`` metapackage version prefixed with ``lsst-scipipe-``.

   .. note::

      These installation are for :doc:`newinstall.sh <newinstall>`- and :doc:`lsstinstall`-based installations.
      For ``lsstsw``, follow :ref:`these instructions <lsstsw-setup>` instead.

      To find the ``rubin-env`` conda metapackage version appropriate for a particular science pipelines release, see :ref:`release-history` or the release tag files at `https://eups.lsst.codes/stack/src/tags/`_.


2. Set up a top-level package:

   .. code-block:: bash

      setup <package>

   For example, ``setup lsst_apps`` or ``setup lsst_distrib``.
   See :doc:`top-level-packages` for more about LSST's top-level packages.

.. _setup-list:

Listing what packages are set up
================================

To see what packages (and their versions) are currently set up:

.. code-block:: bash

   eups list -s

To see all packages that are installed, even if not currently set up, run:

.. code-block:: bash

   eups list
