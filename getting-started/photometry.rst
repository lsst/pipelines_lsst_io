..
  Brief:
  This tutorial is geared towards beginners to the Science Pipelines software.
  Our goal is to guide the reader through a small data processing project to show what it feels like to use the Science Pipelines.
  We want this tutorial to be kinetic; instead of getting bogged down in explanations and side-notes, we'll link to other documentation.
  Don't assume the user has any prior experience with the Pipelines; do assume a working knowledge of astronomy and the command line.

.. _getting-started-tutorial-measuring-sources:

##################################################
Getting started tutorial part 6: measuring sources
##################################################

In this step of the :ref:`tutorial series <getting-started-tutorial>` you'll measure the coadditions you assembled in :doc:`part 5 <coaddition>` to build catalogs of stars and galaxies.
This is the measurement strategy:

1. :ref:`Detect sources in individual coadd patches <getting-started-tutorial-detect-coadds>`.
2. :ref:`Merge those multi-band source detections into a single detection catalog <getting-started-tutorial-merge-coadd-detections>`.
3. :ref:`Deblend and measure sources in the individual coadds using the unified detection catalog <getting-started-tutorial-measure-coadds>`.
4. :ref:`Merge the multi-band catalogs of source measurements to identify the best positional measurements for each source <getting-started-tutorial-merge-coadds>`.
5. :ref:`Re-measure the coadds in each band using fixed positions (forced photometry) <getting-started-tutorial-forced-coadds>`.

Set up
======

Pick up your shell session where you left off in :doc:`part 5 <coaddition>`.
For convenience, start in the top directory of the example git repository.

.. code-block:: bash

   cd $RC2_SUBSET_DIR

The ``lsst_distrib`` package also needs to be set up in your shell environment.
See :doc:`/install/setup` for details on doing this.


Run detection pipeline task
===========================

Processing will be done in two blocks with two different pipelines.
The first will do steps 1 through 4 in the introduction.
The end result will be calibrated coadd object measurements and calibrated coadd exposures.

The following code executes steps 1 through 4 of the steps outlined in the introduction to this tutorial.
The code is executed here, but more information on each of the steps is included in sections following this code block.
The fifth and final step is executed in :ref:`this section <getting-started-tutorial-forced-coadds>`.

.. code-block:: bash

   pipetask run --register-dataset-types \
   -b $RC2_SUBSET_DIR/SMALL_HSC/butler.yaml \
   -i u/$USER/coadds \
   -o u/$USER/coadd_meas \
   -p $DRP_PIPE_DIR/pipelines/HSC/DRP-RC2_subset.yaml#coadd_measurement \
   -d "skymap = 'hsc_rings_v1' AND tract = 9813 AND patch in (38, 39, 40, 41)" \
   -c detection:detection.thresholdValue=250.0

.. note::

   The ``-c`` argument is used to set a configuration parameter.
   In this case, the detection threshold is set to 250.0.
   This is a high threshold, but it is used here to reduce the number of detections in the tutorial data.
   In a real analysis, you would want to set this to a lower value to detect fainter objects.

Notice that since this task operates on coadds, we can select the coadds using the ``tract``, and ``patch`` data ID keys.
In past sections, the examples left off the ``-d`` argument in order to process all available data.
This example, however, is selecting just four of the patches for this step.
Some algorithms are sensitive to how images are arranged on the sky.
For example, some algorithms expect multiple images to overlap, or multi-band coverage.
Those four patches have coverage from all 40 visits in the tutorial repository which means there doesn't need to be as much fine tuning to configurations, and we can process these patches just as the large scale HSC processing is done.
As with previous examples, the outputs will go in a collection placed under a namespace defined by your username.

.. note::

   The processing in this part can be quite expensive and take a long time.
   You can use the `-j<num cores>` argument to allow the processing to take more cores, if you have access to more than one.

.. _getting-started-tutorial-detect-coadds:

Detecting sources in coadded images
-----------------------------------

To start, detect sources in the coadded images to take advantage of their depth and high signal-to-noise ratio.
The ``detection`` subset is responsible for producing calibrated measurements from the input coadds.
Detection is done on each band and patch separately.

The resulting datasets are the ``deepCoadd_det`` detections and the ``deepCoadd_calexp`` calibrated coadd exposures.

.. _getting-started-tutorial-merge-coadd-detections:

Merging multi-band detection catalogs
-------------------------------------

Merging the detections from the multiple bands used to produce the coadds allows later steps to use multi-band information in their processing: e.g. deblending.
The ``mergeDetections`` subset created a ``deepCoadd_mergeDet`` dataset, which is a consistent table of sources across all filters.

.. _getting-started-tutorial-measure-coadds:

Deblending and measuring source catalogs on coadds
--------------------------------------------------

Seeded by the ``deepCoadd_mergeDet``, the deblender works on each detection to find the flux in each component.
Because it has information from multiple bands, the deblender can use color information to help it work out how to separate the flux into different components.
See the `SCARLET paper <https://arxiv.org/abs/1802.10157>`_ for further reading.
The ``deblend`` subset produces the ``deepCoadd_deblendedFlux`` data product.

The ``measure`` subset is responsible for measuring object properties on all of the deblended children produced by the deblender.
This produces the ``deepCoadd_meas`` catalog data product with flux and shape measurement information for each object.
You'll see how to access these tables later.

.. _getting-started-tutorial-merge-coadds:

Merging multi-band source catalogs from coadds
----------------------------------------------

After measurement the single band deblended and measured objects in single bands can again be merged into a single catalog.

Merging the single band detection catalogs into a single multi-band catalog allows for more complete and consistent multi-band photometry by measuring the same source in multiple bands at a fixed position (the forced photometry method) rather than fitting the source's location individually for each band.

For forced photometry you want to use the best position measurements for each source, which could be from different filters depending on the source.
We call the filter that best measures a source the **reference filter**.
The ``mergeMeasurements`` created a ``deepCoadd_ref`` dataset.
This is the seed catalog for computing forced photometry.

.. _getting-started-tutorial-forced-coadds:

Running forced photometry on coadds
===================================

Now you have accurate positions for all detected sources in the coadds.
Re-measure the coadds using these fixed source positions (the forced photometry method) to create the best possible photometry of sources in your coadds:

.. code-block:: bash

   pipetask run --register-dataset-types \
   -b $RC2_SUBSET_DIR/SMALL_HSC/butler.yaml \
   -i u/$USER/coadd_meas \
   -o u/$USER/objects \
   -p $DRP_PIPE_DIR/pipelines/HSC/DRP-RC2_subset.yaml#forced_objects \
   -d "skymap = 'hsc_rings_v1' AND tract = 9813 AND patch in (38, 39, 40, 41)"

As above, this selects just the patches that have full coverage.

The ``forced_objects`` subset of pipelines does several things:

1. Forced photometry on the coadds resulting in the ``deepCoadd_forced_src`` dataset
2. Forced photometry on the input single frame calibrated exposures, the ``forced_src`` dataset
3. Finally, it combines all object level forced measurements into a single tract scale catalog resulting in the ``objectTable_tract`` dataset

Wrap up
=======

In this tutorial, you've created forced photometry catalogs of sources in coadded images.
Here are some key takeaways:

- *Forced photometry* is a method of measuring sources in several bandpasses using a common source list.

:doc:`Continue this tutorial series in part 7 <multiband-analysis>` where you will analyze and plot the source catalogs that you've just measured.
