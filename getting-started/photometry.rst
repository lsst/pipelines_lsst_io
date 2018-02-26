..
  Brief:
  This tutorial is geared towards beginners to the Science Pipelines software.
  Our goal is to guide the reader through a small data processing project to show what it feels like to use the Science Pipelines.
  We want this tutorial to be kinetic; instead of getting bogged down in explanations and side-notes, we'll link to other documentation.
  Don't assume the user has any prior experience with the Pipelines; do assume a working knowledge of astronomy and the command line.

.. _getting-started-tutorial-measuring-sources:

##################################################
Getting started tutorial part 5: measuring sources
##################################################

In this step of the :ref:`tutorial series <getting-started-tutorial>` you'll measure the coadditions you assembled in :doc:`part 4 <coaddition>` to build catalogs of stars and galaxies.
This is the measurement strategy:

1. :ref:`Detect sources in individual coadd patches <getting-started-tutorial-detect-coadds>`.
2. :ref:`Merge those multi-band source detections into a single detection catalog <getting-started-tutorial-merge-coadd-detections>`.
3. :ref:`Measure and deblend sources in the individual coadds using the unified detection catalog <getting-started-tutorial-measure-coadds>`.
4. :ref:`Merge the multi-band catalogs of source measurements to identify the best positional measurements for each source <getting-started-tutorial-merge-coadds>`.
5. :ref:`Re-measure the coadds in each band using fixed positions (forced photometry) <getting-started-tutorial-forced-coadds>`.

.. tip::

   Instead of running multiple command-line tasks, like you'll do here, you could instead run the :command:`multiBandDriver.py` command as an integrated multi-band source measurement pipeline.

Set up
======

Pick up your shell session where you left off in :doc:`part 4 <coaddition>`.
That means your current working directory must *contain* the :file:`DATA` directory (the Butler repository).

The ``lsst_distrib`` package also needs to be set up in your shell environment.
See :doc:`/install/setup` for details on doing this.

.. _getting-started-tutorial-detect-coadds:

Detecting sources in coadded images
===================================

To start, you can detect sources in the coadded images to take advantage of their depth and high signal-to-noise ratio.
Use the :command:`detectCoaddSources.py` command-line task to accomplish this:

.. code-block:: bash

   detectCoaddSources.py DATA --rerun coadd:coaddPhot \
       --id filter=HSC-R tract=0 patch=0,0^0,1^0,2^1,0^1,1^1,2^2,0^2,1^2,2

Notice that since this task operates on coadds, we need to select the coadds using the ``filter``, ``tract``, and ``patch`` data ID keys.

Also notice that you've created a new rerun for the photometry outputs, ``coaddPhot``, that is chained to the ``coadd`` rerun.

Now repeat source detection in ``HSC-I``-band patches:

.. code-block:: bash

   detectCoaddSources.py DATA --rerun coaddPhot \
       --id filter=HSC-I tract=0 patch=0,0^0,1^0,2^1,0^1,1^1,2^2,0^2,1^2,2

The :command:`detectCoaddSources.py` commands produce ``deepCoadd_det`` datasets in the Butler repository.
Typically these datasets are only used as inputs for the :command:`mergeCoaddDetections.py` command, which you'll run next.

.. _getting-started-tutorial-merge-coadd-detections:

Merging multi-band detection catalogs
=====================================

Next, use the :command:`mergeCoaddDetections.py` command to combine the individual ``HSC-R`` and ``HSC-I``-band detection catalogs:

.. code-block:: bash

   mergeCoaddDetections.py DATA --rerun coaddPhot --id filter=HSC-R^HSC-I

This command created a ``deepCoadd_mergeDet`` dataset, which is a consistent table of sources across all filters.

.. _getting-started-tutorial-measure-coadds:

Measuring source catalogs on coadds
-----------------------------------

Now, use the merged detection catalog to measure sources in both the ``HSC-R`` and ``HSC-I`` coadd patches.
You can accomplish this with :command:`measureCoaddSources.py`:

.. code-block:: bash

   measureCoaddSources.py DATA --rerun coaddPhot --id filter=HSC-R

And repeat with the ``HSC-I``-band coadd:

.. code-block:: bash

   measureCoaddSources.py DATA --rerun coaddPhot --id filter=HSC-I

The :command:`measureCoaddSources` command-line task produces ``deepCoadd_meas`` datasets in the Butler data repository.
Because the same merged detection catalog is used for every filter, the ``HSC-R`` and ``HSC-I``-band ``deepCoadd_meas`` tables have consistent rows.
You'll see how to access these tables later.

.. _getting-started-tutorial-merge-coadds:

Merging multi-band source catalogs from coadds
----------------------------------------------

The previous step you created measurement catalogs for each patch in both the ``HSC-R`` and ``HSC-I`` bands.
You'll get even more complete and consistent multi-band photometry by measuring the same source in multiple bands at a fixed position (the forced photometry method) rather than fitting the source's location individually for each band.

For forced photometry you want to use the best position measurements for each source, which could be from different filters depending on the source.
We call the filter that best measures a source the **reference filter**.
Go ahead and run the :command:`mergeCoaddMeasurements.py` command to create a table that identifies the reference filter for each source in the tables you created with the previous step:

.. code-block:: bash

   mergeCoaddMeasurements.py DATA --rerun coaddPhot --id filter=HSC-R^HSC-I

This command created a ``deepCoadd_ref`` dataset.

.. _getting-started-tutorial-forced-coadds:

Running Forced photometry on coadds
-----------------------------------

Now you have accurate positions for all detected sources in the coadds.
Re-measure the coadds using these fixed source positions (the forced photometry method) to create the best possible photometry of sources in your coadds:

.. code-block:: bash

   forcedPhotCoadd.py DATA --rerun coaddPhot:coaddForcedPhot --id filter=HSC-R

Also run forced photometry on the ``HSC-I``-band coadds:

.. code-block:: bash

   forcedPhotCoadd.py DATA --rerun coaddForcedPhot --id filter=HSC-I

The :command:`forcedPhotCoadd.py` command creates table datasets called ``deepCoadd_forced_src`` in the Butler repository.
In a future tutorial you'll see how to work with these tables.

.. TODO update with link

.. note::

   You can also try the :command:`forcedPhotCcd.py` command to apply forced photometry to individual exposures, which may in principle yield better measurements.
   :command:`forcedPhotCcd.py` doesn't currently deblend sources, though.
   Thus forced coadd photometry, as you've performed here, provides the best source photometry.

Wrap up
=======

In this tutorial, you've created forced photometry catalogs of sources in coadded images.
Here are some key takeaways:

- *Forced photometry* is a method of measuring sources in several bandpasses using a common source list.
- The pipeline for forced photometry consists of the :command:`detectCoaddSources.py`, :command:`mergeCoaddDetections.py`, :command:`measureCoaddDetections.py`, :command:`mergeCoaddMeasurements.py`, and :command:`forcedPhotCoadd.py` command-line tasks.

Congratulations, you've completed the last part of this tutorial series (so far).
The :doc:`rest of the docs <../index>` will help you learn more about the LSST Science Pipelines software.

We'd also love to hear from you on our `LSST Community Forum`_.

.. _LSST Community Forum: https://community.lsst.org
