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
You'll get a feel for setting up a Pipelines environment, working with data repositories, running processing from the command-line, and working with the Pipelines' Python APIs.
Along the way we'll point you to additional documentation.

The LSST Science Pipelines can process data from several telescopes using LSST's algorithms.
In this :ref:`tutorial series <getting-started-tutorial>` you will calibrate and reduce Hyper Suprime-Cam (HSC) exposures into coadditions and catalogs of objects.

In this first part of the :ref:`tutorial series <getting-started-tutorial>` you'll set up the LSST Science Pipelines software, and obtain the data needed for the remainder of the tutorial.
Along the way, you'll be introduced to the Butler, which is the Pipelines' interface for managing, reading, and writing datasets.

Install the LSST Science Pipelines
==================================

If you haven't already, you'll need to install the LSST Science Pipelines.
We recommend that you install the pre-built binary packages by following the instructions at :doc:`/install/newinstall`.
This tutorial was developed using the ``w_2021_33`` tag of the ``lsst_distrib`` EUPS package.
We expect the tutorials to also work with newer versions of the science pipelines, however continuing development will eventually outpace the directions contained here.

When working with the LSST Science Pipelines, you need to remember to activate the installation and *set up* the package stack in each new shell session.
Follow the instructions :doc:`/install/setup` to do this.

To make sure the environment is set up properly, you can run:

.. code-block:: bash

   eups list lsst_distrib

The line printed out should contain the word ``setup``.
If not, review the :doc:`set up instructions </install/setup>`.
It may simply be that you're working in a brand new shell.

Downloading the sample HSC data
===============================

Sample data for this tutorial comes from the `rc2_subset`_ package.
`rc2_subset`_ contains a small set of Hyper Suprime-Cam (HSC) exposures.
The Science Pipelines provides native integrations for many observatories, including HSC, CFHT/MegaCam, and of course LSST.

`rc2_subset`_ is a Git LFS-backed package, so make sure you've :doc:`installed and configured Git LFS for LSST <../install/git-lfs>`.

.. important::

   Even if you've used Git LFS before, you do need to :doc:`configure it to work with LSST's servers <../install/git-lfs>`.

First, clone `rc2_subset`_ using Git:

.. jinja:: default

   .. code-block:: bash

     git clone -b {{ release_eups_tag }} https://github.com/lsst/rc2_subset

Then :command:`setup` the package to add it to the EUPS stack:

.. code-block:: bash

   setup -j -r rc2_subset

.. tip::

   The ``-r rc2_subset`` argument is the package's directory path (either absolute or relative).
   In this case

   The ``-j`` argument means that we're **just** setting up ``rc2_subset`` without affecting other packages.

Now run:

.. code-block:: bash

   echo $RC2_SUBSET_DIR

The ``$RC2_SUBSET_DIR`` environment variable should be the `rc2_subset`_ directory's path.

Creating a Butler object for HSC data
=========================================

In the LSST Science Pipelines you don't directly manage data files.
Instead, you access data through an instance of the **Butler** class.
This gives you flexibility to work with data from different observatories without significantly changing your workflow.

The Butler manages data in **repositories.**
Butler repositories can be remote (the data are on a server, across a network) or local (the data are on a local filesystem).
In this tutorial you'll create and use a local Butler repository, which is a simple directory.

The `rc2_subset`_ git repository has a Butler repository contained within it.
To construct a Butler that can manage data in that repository, from a python prompt say:

.. code-block:: python

   from lsst.daf.butler import Butler
   import os
   repo_path = os.path.join(os.environ['RC2_SUBSET_DIR'], 'SMALL_HSC')
   butler = Butler(repo_path)

Now you can explore the repository using the registry attribute of the Butler you created.  E.g.:

.. code-block:: python

   registry = butler.registry
   for col in registry.queryCollections():
       print(col)
   for ref in registry.queryDatasets('raw', collections='HSC/raw/all', instrument='HSC'):
       print(ref.dataId)

Read more about querying datasets :ref:`here <daf_butler_queries>`.

Notes on terminology
====================

First, a coherent set of pixels can have lots of names.
In this set of tutorials, you will run into three.
The term exposure, refers to a single image.
The camera produces exposures that can be ingested into a data butler.
Once ingested, exposures can be grouped together into visits via the ``define-visits`` subcommand to the ``butler`` command line tool.
Visits can be made up of more than one exposure as in the baseline plan for each visit to be made up of two "snaps" for the LSST.
You will also see mention of ``Exposure``.
This is the name of the python object, or instance thereof, that is used to manipulate pixel data within the Science Pipelines.
The python object will always be presented capitalized and in monospace.

Second, different projects call the instances of astrophysical bodies different names.
In this project, sources are specific measurements of an astrophysical object.
The term object refers to the astrophysical entity itself.
In other words, there is a unique record for each distinct object seen by the LSST, but multiple source measurements for each time the LSST revisits a particular part of the sky.

Third, you will see mention of pipelines.
Formally a ``Pipeline`` is made up of one or more ``PipelineTask`` objects.
These can be further grouped into other pipelines.
You will see reference to "subsets" of a pipeline.
This just means a named set of ``PipelineTask`` that make up a part of a larger pipeline, but that can be run independently.

Notes on processing
===================

The intention of this set of introductory recipes is to give you a realistic sense of how data are processed using the LSST Science Pipelines.
That includes taking raw images all the way through to coaddition and forced photometry.
Though the starting repository is small, a significant amount of processing needs to be done to produce all the datasets needed for downstream processing.
This means that some steps can be quite time consuming and you should be prepared to wait or perhaps run things overnight if you intend to follow these examples line by line.

The most time consuming steps are:

- Single frame processing: 11 hours
- Warping the images in preparation for coaddition: 90 minutes
- Coaddition: 70 minutes
- Coadd detection, deblending and measurement: 90 minutes
- Forced photometry: 75 minutes

These timings are all for a single serial thread.
Some steps can be sped up significantly if you have access to more than one core.
For example, to speed up the single frame processing, you can try adding the ``-j4`` argument.
This will attempt to run the processing on 4 cores simultaneously.

Wrap up
=======

In this tutorial, you've set up a Butler repository with the data you'll process in later steps.
Here are some key takeaways:

- The Butler is the interface between data and LSST Science Pipelines processing tasks.
- Butler repositories can be hosted on different backends, both remote and local. In this case you created a local Butler repository on your computer's filesystem.
- Butler repositories contain raw data, calibrations, and reference catalogs. As you'll see in future tutorials, the Butler repository also contains the outputs of processing tasks.
- If you are interested in creating a butler repository with your own data, the `Community Forum`_ is the right place to search for and ask questions.

In :doc:`part 2 of this tutorial series <singleframe>` you will process the HSC data in this newly-created Butler repository into calibrated exposures.

.. _rc2_subset: https://github.com/lsst/rc2_subset
.. _Community Forum: https://community.lsst.org
