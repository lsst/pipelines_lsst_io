..
  Brief:
  This tutorial is geared towards beginners to the Science Pipelines software.
  Our goal is to guide the reader through a small data processing project to show what it feels like to use the Science Pipelines.
  We want this tutorial to be kinetic; instead of getting bogged down in explanations and side-notes, we'll link to other documentation.
  Don't assume the user has any prior experience with the Pipelines; do assume a working knowledge of astronomy and the command line.

.. _getting-started-tutorial-measuring-sources:

##################################################
Getting started tutorial part 4: measuring sources
##################################################

This is part 4 of the :ref:`getting started tutorial series <getting-started-tutorial>`.
Before starting this tutorial, make sure you've completed the previous parts.

To recap, we collected raw data in a Butler repository (:doc:`part 1 <data-setup>`), calibrated that data (:doc:`part 2 <processccd>`), and made deep coadditions in HSC-R and HSC-I bands across nine patches of the sky (:doc:`part 3 <coaddition>`).
In this step, we'll measure these coadditions to build catalogs of stars and galaxies.

This is our measurement strategy:

1. :ref:`Detect sources in individual coadd patches <getting-started-tutorial-detect-coadds>`.
2. :ref:`Merge those multi-band source detections into a single detection catalog <getting-started-tutorial-merge-coadd-detections>`.
3. :ref:`Measure and deblend sources in the individual coadds using the unified detection catalog <getting-started-tutorial-measure-coadds>`.
4. :ref:`Merge the multi-band catalogs of source measurements to identify the best positional measurements for each source <getting-started-tutorial-merge-coadds>`.
5. :ref:`Re-measure the coadds in each band using fixed positions (forced photometry) <getting-started-tutorial-forced-coadds>`.

.. tip::

   Instead of running multiple command line tasks, like we'll do here, you could instead run the :command:`multiBandDriver.py` command as an integrated multi-band source measurement pipeline.

Setup check
===========

Let's take a moment to make sure your command line environment is set up.
Run:

.. code-block:: bash

   eups list lsst_distrib

The line printed out should contain the word ``setup``.
If not, :ref:`review the installation tutorials <getting-started-activate>` on activating the environment and setting up ``lsst_distrib``.

Your shell's working directory also needs to contain the Butler repository directory called :file:`DATA`.

Let's get back to it.

.. _getting-started-tutorial-detect-coadds:

Detecting sources in coadded images
===================================

To start, we will detect sources in the coadded images to take advantage of their depth and high signal-to-noise ratio.
We'll use the :command:`detectCoaddSources.py` command line task to accomplish this.
Run this command to detect sources in all ``HSC-R``-band patches:

.. code-block:: bash

   detectCoaddSources.py DATA --rerun coadd \
       --id filter=HSC-R tract=0 patch=0,0^0,1^0,2^1,0^1,1^1,2^2,0^2,1^2,2

Repeat source detection in ``HSC-I``-band patches:

.. code-block:: bash

   detectCoaddSources.py DATA --rerun coadd \
       --id filter=HSC-I tract=0 patch=0,0^0,1^0,2^1,0^1,1^1,2^2,0^2,1^2,2

.. .. note::

..    The :command:`detectCoaddSources.py` commands produce ``deepCoadd_det`` datasets in the Butler repository.
..    Typically these datasets are only used as inputs for the :command:`mergeCoaddDetections.py`, which we'll run next.

.. Data product is deepCoadd_det

.. _getting-started-tutorial-merge-coadd-detections:

Merging multi-band detection catalogs
=====================================

Next, use the :command:`mergeCoaddDetections.py` command to combine the individual ``HSC-R`` and ``HSC-I``-band detection catalogs.
Run:

.. code-block:: bash

   mergeCoaddDetections.py DATA --rerun coadd:coaddPhot --id filter=HSC-R^HSC-I

.. Data product is deepCoadd_mergeDet

.. _getting-started-tutorial-measure-coadds:

Measuring source catalogs on coadds
-----------------------------------

Now we'll use the merged detection catalog to measure sources in both the ``HSC-R`` and ``HSC-I`` coadd patches.
We'll accomplish this with :command:`measureCoaddSources.py`:

.. code-block:: bash

   measureCoaddSources.py DATA --rerun coaddPhot --id filter=HSC-R

And repeat with the ``HSC-I``-band coadd:

.. code-block:: bash

   measureCoaddSources.py DATA --rerun coaddPhot --id filter=HSC-I

.. .. tip::
.. 
..    The :command:`measureCoaddSources` command line task produces ``deepCoadd_meas`` datasets in the Butler data repository.
..    Because the same merged detection catalog is used for every filter, the ``HSC-R`` and ``HSC-I``-band ``deepCoadd_meas`` tables have consistent rows.
..    We'll see how to access these tables later.

.. Data product is deepCoadd_meas

.. _getting-started-tutorial-merge-coadds:

Merging multi-band source catalogs from coadds
----------------------------------------------

The previous step created measurement catalogs for each patch in both the ``HSC-R`` and ``HSC-I`` bands.
We get even more complete and consistent multi-band photometry by measuring the same source in multiple bands at a fixed position (the forced photometry method) rather than fitting the source's location individually for each band.

For forced photometry we want to use the best position measurements for each source, which could be from different filters depending on the source.
We call the filter that measures a source best the **reference filter**.
Let's use the :command:`mergeCoaddMeasurements.py` command to create a table that identifies the reference filter for each source in the tables we created with the previous step.
Run:

.. code-block:: bash

   mergeCoaddMeasurements.py DATA --rerun coaddPhot --id filter=HSC-R^HSC-I

.. Data product is deepCoadd_ref

.. _getting-started-tutorial-forced-coadds:

Running Forced photometry on coadds
-----------------------------------

Now we have accurate positions for sources in the patches.
Let's re-measure the coadds using these fixed source positions (the forced photometry method) to create the best possible photometry of sources in our coadds.
Run:

.. code-block:: bash

   forcedPhotCoadd.py DATA --rerun coaddPhot:coaddForcedPhot --id filter=HSC-R

Also run forced photometry on the ``HSC-I``-band coadds:

.. code-block:: bash

   forcedPhotCoadd.py DATA --rerun coaddForcedPhot --id filter=HSC-I

.. Data product is deepCoadd_forced_src

The :command:`forcedPhotCoadd.py` command creates table datasets called ``deepCoadd_forced_src`` in the Butler repository.
In the next part of this tutorial we'll see how to work with these tables.

.. note::

   You can also try the :command:`forcedPhotCcd.py` command to apply forced photometry to individual exposures, which may in principle yield better measurements.
   :command:`forcedPhotCcd.py` doesn't currently deblend sources, though.
   Thus forced coadd photometry, as we performed here, provides the best photometry of coadded sources.

Next up
=======

Congratulations, you've completed the last tutorial in the series (so far).

By now you're ready to start experimenting with the LSST Science Pipelines for your own projects.
The :doc:`rest of the docs <../index>` will help you along the way.

We'd also love to hear from you on our `LSST Community Forum`_.

.. _LSST Community Forum: https://community.lsst.org
