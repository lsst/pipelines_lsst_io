##############################################################
Installing and Using LSST Science Pipelines as a Conda Package
##############################################################

This page will guide you through installing the LSST Science Pipelines as a Conda package for use in `Anaconda or Miniconda <https://www.continuum.io/why-anaconda>`__.
Anaconda is a popular Python distribution and package ecosystem.
With this installation method you don't compile source code, or even need to have an existing Python installation.

If you have difficulty installing LSST software:

- review the :ref:`known installation issues for your platform <installation-issues>`.
- reach out on the `Support forum at community.lsst.org <https://community.lsst.org/c/support>`_.

.. note::

   Users of LSST Simulations (such as the Metrics Analysis Framework, MAF) should following the `LSST Simulations Installation documentation <https://confluence.lsstcorp.org/display/SIM/Catalogs+and+MAF>`__ instead of this page.
   The Simulations group publishes their own Conda channel that includes compatibility patches for the Simulations stack.

1. Install Anaconda or Miniconda
================================

You might already have Anaconda or Miniconda as your main Python distribution.
If not, you can quickly get started by following Continuum's official installation instructions:

- `Install Anaconda <https://www.continuum.io/downloads>`__ if you want a complete, science-ready Python installation with minimal setup.
- Otherwise, `install the leaner Miniconda <http://conda.pydata.org/miniconda.html>`__ version and install packages as you need them.

If you're new to Anaconda, Continuum's `30-minute test drive <http://conda.pydata.org/docs/test-drive.html>`_ tutorial will get you up-to-speed.

.. warning::

   Don't reuse the Miniconda you might have previously obtained from an :doc:`eups distrib <newinstall>`\ -based installation.
   Open a new shell and install Anaconda/Miniconda from scratch.

Upgrading conda
---------------

If you have an existing Anaconda or Miniconda installation, you'll want to make sure the :command:`conda` command itself is up to date:

.. code-block:: bash

   conda update conda

See the `Conda documentation for more information about installing and managing conda and Anaconda/Miniconda <http://conda.pydata.org/docs/using/using.html>`__.

2. Install Science Pipelines in a Conda Environment
===================================================

These commands will download and activate the LSST Science Pipelines in a new Conda environment:

.. code-block:: bash
   :linenos:

   conda config --add channels http://conda.lsst.codes/stack  
   conda create --name lsst python=2
   source activate lsst
   conda install lsst-distrib
   source eups-setups.sh

Here's what these commands are doing, line-by-line:

1. Tell :command:`conda` about the LSST channel for Conda packages.
2. Create a Conda environment called ``lsst`` with Python 2.7.
   You can change the environment's name to anything you like.
   Conda environments are recommended since they help keep the Python dependencies of your projects separate.
   See the `Conda documentation on environments for more information <http://conda.pydata.org/docs/using/envs.html>`__.
3. Activate the ``lsst`` environment (use your environment's name if you chose a different one).
   The :command:`activate` command is provided by Anaconda/Miniconda (e.g. at :file:`~/miniconda2/bin/activate`).
4. Install the full suite of LSST science software, including Science Pipelines (``lsst-distrib``).
5. Setup LSST packages in your environment with EUPS.

.. warning::

   If the install fails with an error, check that your shell does not have another EUPS Stack configured (try ``echo $EUPS_STACK``).
   Conda packaged EUPS will use existing values of ``EUPS_PATH`` and ``EUPS_DIR``.
   If they exist, unset them before installing or using Conda packages.

.. _conda-install-activate:

3. Activating Science Pipelines in a new Shell
==============================================

Whenever you open a new shell or terminal session, use these commands to re-activate your previously-installed Science Pipelines:

.. code-block:: bash
   :linenos:

   source activate lsst
   source eups-setups.sh

These commands can also be used to switch from one Conda environment and LSST Science Pipelines installation to another.

.. _conda-install-test:

4. Testing Your Installation
============================

Once the LSST Science Pipelines are installed, you can verify that it works by :doc:`running a demo project <demo>`.
This demo processes a small amount of SDSS data.
