..
  Brief:
  This particular page advocates the best installation practices for users.
  The /install/ directory has our installation reference documentation.
  This page should advocate an EUPS binary installation when that's available.
  For now, we'll still point users to the installation reference pages.
  Having more than one installation method in this Getting Started section only confuses things.

##########################################################
Getting started: installing the Science Pipelines software
##########################################################

This page will guide you through installing and activating the LSST Science Pipelines software using the method we recommend for most users.

.. _getting-started-newinstall:

Installing the LSST Science Pipelines with newinstall.sh
========================================================

There are :doc:`several ways to install <../install/index>` the LSST Science Pipelines, depending on your needs.
For getting started, we recommend the :doc:`newinstall method for installing the LSST Science Pipelines <../install/newinstall>`.
Follow the directions on that page to install system prerequisites, run the :command:`newinstall.sh` script, and ultimately the install ``lsst_distrib`` package that contains the LSST Science Pipelines software.

.. _getting-started-git-lfs:

Installing Git LFS for LSST
===========================

The tutorial requires Git LFS to download the sample datasets.
To install and configure Git LFS for LSST, follow the directions on the :doc:`../install/git-lfs` page.

.. _getting-started-activate:

Activating your Pipelines installation
======================================

Before using you can use your Pipelines installation, you'll first need to activate the environment and set up the Pipelines packages.

First, open a new command line shell.
Since the Pipelines adds environment variables to your shell, working in a new shell will make it easier to follow along.

Next, at your shell prompt activate your installation's environment.
The activation command you'll use depends on your installation method.
If you installed with :command:`newinstall.sh`, the activation command is:

.. code-block:: bash

   source <install-dir>/loadLSST.bash

.. note::

   If you aren't using the :command:`bash` shell, use a different loading script:

   - :command:`zsh` shell: :command:`loadLSST.zsh`
   - :command:`ksh` shell: :command:`loadLSST.ksh`
   - :command:`csh` and :command:`tcsh` shells: :command:`loadLSST.csh`

The ``loadLSST.bash`` script has only activated the software environment.
We still need to set up the LSST software; we'll do that next.

.. _getting-started-setup:

Setting up the lsst_distrib EUPS package
========================================

LSST Science Pipelines are distributed as EUPS packages.
To use any of the packages, you'll first need to set them up using EUPS's :command:`setup` command.

``lsst_distrib`` is a useful package to set up because it's a *top-level* package that depends on most packages LSST ships.
To set up ``lsst_distrib``, run:

.. code-block:: bash

   setup lsst_distrib

.. tip::

   You can see what packages have been set up by running:

   .. code-block:: bash
   
      eups list -s

   With the ``-s`` argument :command:`eups list` shows only set up packages; otherwise :command:`eups list` shows all packages that you *installed,* regardless of whether they're *set up* or not.

Next up
=======

Now that you have the LSST Science Pipelines installed and activated, let's learn how to process a dataset.

The :ref:`getting started tutorial series <getting-started-tutorial>` will guide you through calibrating and processing a collection of Hyper Suprime-Cam images to make coadditions and measure source catalogs.
Begin the tutorial at :doc:`data-setup`.
