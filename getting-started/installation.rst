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

.. seealso::

   The :doc:`Installation section <../install/index>` of the documentation site describes all of the Science Pipelines installation patterns in detail.

.. _getting-started-newinstall:

Installing the Pipelines
========================

First, you'll need to download and install the LSST Science Pipelines software.
If you haven't already, :doc:`follow one of our installation methods <../install/index>`.

.. TODO::

   Change to suggest a binary installation only.

.. _getting-started-activate:

Activating your Pipelines installation
======================================

Before using you can use your Pipelines installation, you'll first need to activate the environment and set up the Pipelines packages.

First, open a new command line shell.
Since the Pipelines adds environment variables to your shell, working in a new shell will make it easier to follow along.

Next, at your shell prompt activate your installation's environment.
The activation command you'll use depends on your installation method:

- If you used :doc:`newinstall.sh <../install/newinstall>`, run ``source loadLSST.bash`` from the installation directory.
  If you aren't using :command:`bash`, you might need :ref:`a different <install-from-source-setup>` ``loadLSST`` script.
- If you are using :doc:`lsstsw <../install/lsstsw>`, run ``source bin/setup.sh`` from the :file:`lsstsw` directory.
  See :ref:`Sourcing the Pipelines in a New Shell <lsstsw-setup>` for details.

The ``loadLSST.bash`` or ``setup.sh`` script has only activated the software environment.
We still need to set up LSST Software; we'll do that next.

.. todo::

   Add a note to know whether the command has succeeded; or is even necessary.
   Perhaps use :command:`echo $EUPS_PATH`?

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
