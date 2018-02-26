..
  Brief:
  This tutorial is geared towards new users of the LSST Science Pipelines software.
  Our goal is to guide the reader through a small data processing project to show what it feels like to use the Science Pipelines.
  We want this tutorial to be kinetic; instead of getting bogged down in explanations and side-notes, we'll link to other documentation.
  Don't assume the user has any prior experience with the Pipelines; do assume a working knowledge of astronomy and the command line.

.. _getting-started-tutorial-data-setup:

######################################################################
Getting started tutorial part 1: setting up the Butler data repository
######################################################################

This hands-on tutorial is intended for anyone getting started with using the LSST Science Pipelines for data processing.
You'll get a feel for setting up a Pipelines environment, working with data repositories, running command-line tasks, and working with the Pipelines' Python APIs.
Along the way we'll point you to additional documentation.

The LSST Science Pipelines can process data from several telescopes using LSST's algorithms.
In this :ref:`tutorial series <getting-started-tutorial>` you will calibrate and reduce Hyper Suprime-Cam (HSC) exposures into coadditions and catalogs of objects.

In this first part of the :ref:`tutorial series <getting-started-tutorial>` you'll set up the LSST Science Pipelines software, and collect the raw observations and calibration data needed for the tutorial.
Along the way, you'll be introduced to the Butler, which is the Pipelines' interface for managing, reading, and writing datasets.

Install the LSST Science Pipelines
==================================

If you haven't already, you'll need to install the LSST Science Pipelines.
We recommend that you install the pre-built binary packages by following the instructions at :doc:`/install/newinstall`.
This tutorial is intended to work with the latest release (|current-release|).

When working with the LSST Science Pipelines, you need to remember to activate the installation and *set up* the package stack in each new shell session.
Follow the instructions :doc:`/install/setup` to do this.
We recommend that you use ``lsst_distrib`` as a general top-level package.

To make sure the environment is set up properly, you can run:

.. code-block:: bash

   eups list lsst_distrib

The line printed out should contain the word ``setup``.
If not, review the :doc:`set up instructions </install/setup>`.
It may simply be that you're working in a brand new shell.

Downloading the sample HSC data
===============================

Sample data for this tutorial comes from the `ci_hsc`_ package.
`ci_hsc`_ contains a small set of Hyper Suprime-Cam (HSC) exposures.
The Science Pipelines provides native integrations for many observatories, including HSC, CFHT/MegaCam, SDSS, and of course LSST.

`ci_hsc`_ is a Git LFS-backed package, so make sure you've :doc:`installed and configured Git LFS for LSST <../install/git-lfs>`.

.. important::

   Even if you've used Git LFS before, you do need to :doc:`configure it to work with LSST's servers <../install/git-lfs>`.

First, clone `ci_hsc`_ using Git:

.. code-block:: bash

   git clone https://github.com/lsst/ci_hsc
   cd ci_hsc
   git checkout -b tutorial ffa10de
   cd ..

.. note::

   We're specifically checking out the ``ffa10de`` commit of ``ci_hsc`` to be compatible with the v14.0 release of the LSST Science Pipelines.

   If you're using a newer version of the Pipelines, it should be fine to use the ``master`` branch.
   However, if you don't see *r*-band images listed in later steps, that's because the v14.0 Pipelines cannot read the compressed FITS images in the ``ci_hsc`` repository.

Then :command:`setup` the package to add it to the EUPS stack:

.. code-block:: bash

   setup -j -r ci_hsc

.. tip::

   The ``-r ci_hsc`` argument is the the package's directory path (either absolute or relative).
   In this case

   The ``-j`` argument means that we're **just** setting up ``ci_hsc`` without affecting other packages.

Now run:

.. code-block:: bash

   echo $CI_HSC_DIR

The ``$CI_HSC_DIR`` environment variable should be the `ci_hsc`_ directory's path.

Creating a Butler repository for HSC data
=========================================

In the LSST Science Pipelines you don't directly manage data files.
Instead, you access data through the **Butler** client.
This gives you flexibility to work with data from different observatories without significantly changing your workflow.

The Butler manages data in **repositories.**
Butler repositories can be remote (the data is on a server, across a network) or local (the data in on a local filesystem).
In this tutorial you'll create and use a local Butler repository, which is a simple directory.

Go ahead and create the local Butler repository as a directory called :file:`DATA`:

.. code-block:: bash

   mkdir DATA

Then add a :file:`_mapper` file to the repository:

.. code-block:: bash

   echo "lsst.obs.hsc.HscMapper" > DATA/_mapper

The Butler uses the **mapper** to find and organize data in a format specific to each camera.
Here you're using the ``lsst.obs.hsc.HscMapper`` mapper because you're processing HSC data in this repository.

This is what your current working directory should look like right now:

.. code-block:: text

   ci_hsc/
   DATA/

Ingesting raw data into the Butler repository
=============================================

Next, populate the repository with data from `ci_hsc`_.
The Pipelines' :command:`ingestImages.py` command (called a **command-line task**) links raw images into a Butler repository, allowing the mapper to organize the data.
Run:

.. code-block:: bash

   ingestImages.py DATA $CI_HSC_DIR/raw/*.fits --mode=link

.. tip::

   Notice that the first argument to most command-line tasks is the Butler repository.
   In this case it's the :file:`DATA` directory.

.. tip::

   You can learn about the arguments for command-line tasks with the ``-h`` flag.
   For example:

   .. code-block:: bash

      ingestImages.py -h

Ingesting calibrations into the Butler repository
=================================================

Next, add calibration images (such as dark, flat, and bias frames) associated with the raw data:

.. code-block:: bash

   ln -s $CI_HSC_DIR/CALIB/ DATA/CALIB

.. note::

   In general, you can use the :command:`ingestCalibs.py` command-line task to ingest calibrations into a Butler repository.
   For this tutorial, we've taken a shortcut by manually symlinking pre-structured calibrations from the `ci_hsc`_ package.

Ingesting a reference catalog into the Butler repository
========================================================

The Pipelines use external stellar catalogs to refine the WCS and photometric calibration of images.
`ci_hsc`_ includes a subset of the Pan-STARRS PS1 catalog that has been prepared as an astrometric and photometric reference catalog.
Ingest that catalog into the Butler repository by creating a symlink:

.. code-block:: bash

   mkdir -p DATA/ref_cats
   ln -s $CI_HSC_DIR/ps1_pv3_3pi_20170110 DATA/ref_cats/ps1_pv3_3pi_20170110

.. Processing tasks use these reference catalogs through configurations.
.. The Pipelines will use this Pan-STARRS catalog by default 

.. seealso::

   Learn more about the PS1 reference catalog and how to use it with the LSST Science Pipelines in this `LSST Community forum topic <https://community.lsst.org/t/pan-starrs-reference-catalog-in-lsst-format/1572>`__.

..
   FIXME
   We'll need to link to additional documentation on reference catalogs and their preparation.
   Is manually linking a reference catalog our standard practice?

Wrap up
=======

In this tutorial, you've set up a Butler repository with the data you'll process in later steps.
Here are some key takeaways:

- The Butler is the interface between data and LSST Science Pipelines processing tasks.
- Butler repositories can be hosted on different backends, both remote and local. In this case you created a local Butler repository on your computer's filesystem.
- Butler repositories contain raw data, calibrations, and reference catalogs. As you'll see in future tutorials, the Butler repository also contains the outputs of processing tasks.
- Command-line tasks like :command:`ingestImages.py` and :command:`ingestCalibs.py` help you seed data into Butler repositories.

In :doc:`part 2 of this tutorial series <processccd>` you will process the HSC data in this newly-created Butler repository into calibrated exposures.

.. _ci_hsc: https://github.com/lsst/ci_hsc
