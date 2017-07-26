..
  Brief:
  This tutorial is geared towards beginners to the Science Pipelines software.
  Our goal is to guide the reader through a small data processing project to show what it feels like to use the Science Pipelines.
  We want this tutorial to be kinetic; instead of getting bogged down in explanations and side-notes, we'll link to other documentation.
  Don't assume the user has any prior experience with the Pipelines; do assume a working knowledge of astronomy and the command line.

.. _getting-started-tutorial-data-setup:

######################################################################
Getting started tutorial part 1: setting up the Butler data repository
######################################################################

The LSST Science Pipelines can process data from several telescopes using LSST's algorithms.
In this :ref:`tutorial series <getting-started-tutorial>`, we'll calibrate and reduce Hyper Suprime-Cam (HSC) exposures into coadditions and catalogs of objects.

This hands-on tutorial is intended for anyone just getting started with the LSST Science Pipelines.
You'll get a feel for setting up a Pipelines environment, working with data repositories, running command line tasks, and working with the Pipelines' Python APIs.
Along the way we'll point you to additional documentation.

In this first part of the :ref:`tutorial series <getting-started-tutorial>` we will collect the raw observations and calibration data needed for the tutorial.
Along the way, you'll be introduced to the Butler, which is the Pipelines' interface for managing, reading, and writing datasets.

Setup check
===========

Before we get started, you'll need to install the LSST Science Pipelines.
Follow :doc:`installation tutorial <installation>` to get the Pipelines software using the recommended method.

To make sure the environment is set up properly, run:

.. code-block:: bash

   eups list lsst_distrib

The line printed out should contain the word ``setup``.
If not, :ref:`review the installation tutorials <getting-started-activate>` on activating the environment and setting up ``lsst_distrib``.

Let's get started.

Downloading the sample HSC data
===============================

Sample data for this tutorial comes from the `ci_hsc`_ package.
`ci_hsc`_ contains a small set of Hyper Suprime-Cam (HSC) exposures.
The Science Pipelines provides native integrations for many observatories, including HSC, CFHT/MegaCam, SDSS, and of course LSST.

`ci_hsc`_ is a Git LFS-backed package, so make sure you've :doc:`installed and configured Git LFS for LSST <../install/git-lfs>`.

First, clone `ci_hsc`_ using Git:

.. code-block:: bash

   git clone https://github.com/lsst/ci_hsc

Then :command:`setup` the package to add it to the EUPS stack:

.. code-block:: bash

   setup -j -r ci_hsc

.. tip::

   The ``-r ci_hsc`` argument points to the package's directory.

   The ``-j`` argument means that we're **just** setting up ``ci_hsc`` without affecting other packages.

Now run:

.. code-block:: bash

   echo $CI_HSC_DIR

The ``$CI_HSC_DIR`` environment variable should point to the `ci_hsc`_ directory.

Creating a Butler repository for HSC data
=========================================

In the LSST Science Pipelines you don't directly manage data files on disk.
Instead, you access data through the **Butler** client.
This gives you flexibility to work with data from different observatories without significantly changing your workflow.

The Butler manages data in **repositories.**
On a local filesystem, Butler repositories are simple directories.
Let's create a repository called :file:`DATA`:

.. code-block:: bash

   mkdir DATA

Then add a :file:`_mapper` file to the repository:

.. code-block:: bash

   echo "lsst.obs.hsc.HscMapper" > DATA/_mapper

The Butler uses the **mapper** to find and organize data in a format specific to each camera.
Here we're using the ``lsst.obs.hsc.HscMapper`` mapper because we're processing HSC data in this repository.

Ingesting raw data into the Butler repository
=============================================

Next, let's populate the repository with data from `ci_hsc`_.
The Pipelines' :command:`ingestImages.py` command (called a **command line task**) links raw images into a Butler repository, allowing the mapper to organize the data.
Run:

.. code-block:: bash

   ingestImages.py DATA $CI_HSC_DIR/raw/*.fits --mode=link

.. tip::

   Notice that the first argument to most command line tasks is the Butler repository.
   In this case it's the :file:`DATA` directory.

.. tip::

   You can learn about the arguments for command line tasks with the ``-h`` flag.
   For example:

   .. code-block:: bash

      ingestImages.py -h

Ingesting calibrations into the Butler repository
=================================================

Next, we'll add calibration images (such as dark, flat, and bias frames) associated with the raw data:

.. code-block:: bash

   ln -s $CI_HSC_DIR/CALIB/ DATA/CALIB

.. FIXME Why are we just doing a symlink here? Is this the standard pattern? Do we have documentation on how to arrange a calibration repository since a command like :command:`ingestImages.py` isn't helping us here.

Linking an astrometric reference catalog into the Butler repository
===================================================================

The Pipelines uses external stellar catalogs to refine the WCS of images.
`ci_hsc`_ includes a subset of the Pan-STARRS PS1 catalog that has been prepared as an astrometric reference catalog.
Let's link that catalog into the Butler repository:

.. code-block:: bash

   mkdir -p DATA/ref_cats
   ln -s $CI_HSC_DIR/ps1_pv3_3pi_20170110 DATA/ref_cats/ps1_pv3_3pi_20170110

.. seealso::

   Learn more about the PS1 reference catalog and how to use it with the LSST Science Pipelines in this `LSST Community forum topic <https://community.lsst.org/t/pan-starrs-reference-catalog-in-lsst-format/1572>`__.

..
   FIXME
   We'll need to link to additional documentation on reference catalogs and their preparation.
   And again, is manually linking a reference catalog our standard practice?

Next up
=======

In :doc:`part 2 of this tutorial series <processccd>` we will process the HSC data in the Butler repository into calibrated exposures.

.. _ci_hsc: https://github.com/lsst/ci_hsc
