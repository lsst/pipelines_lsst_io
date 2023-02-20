..
  Brief:
  This tutorial is geared towards beginners to the Science Pipelines software.
  Our goal is to guide the reader through a small data processing project to show what it feels like to use the Science Pipelines.
  We want this tutorial to be kinetic; instead of getting bogged down in explanations and side-notes, we'll link to other documentation.
  Don't assume the user has any prior experience with the Pipelines; do assume a working knowledge of astronomy and the command line.

.. _getting-started-tutorial-coaddition:

################################################
Getting started tutorial part 5: coadding images
################################################

In this part of the :ref:`tutorial series <getting-started-tutorial>` you will combine the individual exposures produced by the ``singleFrame`` pipeline (from :doc:`part 2 <singleframe>`) into deeper coadds (mosaic images).
The dataset that defines how images are reprojected for coaddition is called a **skymap**.
The example repository has a skymap that we can use for this purpose.
We will warp (reproject) images into that skymap.
Then, you will coadd the warped images together into deep images.

Set up
======

Pick up your shell session where you left off in :doc:`part 4 <uber-cal>`.
For convenience, start in the top directory of the example git repository.

.. code-block:: bash

   cd $RC2_SUBSET_DIR

The ``lsst_distrib`` package also needs to be set up in your shell environment.
See :doc:`/install/setup` for details on doing this.

About skymaps
==============

Before you get started, let's talk about **skymaps.**

A skymap is a tiling of the celestial sphere, and is used as coordinate system for the final coadded image.
A skymap is composed of one or more **tracts**.
Those tracts contain smaller regions called **patches**.
Both tracts and patches overlap their neighbors.

Each tract has a different world coordinate system (WCS), but the WCSs of the patches within a given tract are just linearly-offset versions of the same WCS.

There are two general categories of skymaps:

1. Whole sky.
2. A skymap based on the bounding box of a set of input exposures.

Though the HSC dataset you are working with is small, the full dataset is large so we include the skymap computed from the full set and it is of the first type.
Using a skymap that describes the full sky has the benefit that you can compare directly with data products from larger data processing runs since the tracts and patches will align exactly.

Warping images onto the skymap
===============================

Before assembling the coadded image, you need to *warp* the exposures created by the ``singleFrame`` pipeline onto the pixel grids of patches described in the skymap.
You can use the ``makeWarp`` pipeline for this.

The data to process can be specified with a dataset query passed to the ``-d`` argument, short for ``--data-query``.
The example command below only creates coadds for a subset of the data.
The remaining sections only use a few patches that have coverage from all the input visits, so downsampling in the coadd generation phase can save time.
All the data can be coadded by simply leaving off the ``-d`` switch and the arguments to it.
Remember that when specifying the output ``tract`` and ``patch`` information, you must also specify a valid skymap.
In this case, the skymap, called ``hsc_ring_v1`` from a larger HSC run is used.
The filtering we will do here is:

.. code-block:: bash

   -d "tract = 9813 AND skymap = 'hsc_rings_v1' AND patch in (38, 39, 40, 41)"

The above dataset query has been tailored to work with the `example dataset`_ described in the first tutorial.

The ``patch in (38, 39, 40, 41)`` clause selects patches 38, 39, 40 and 41 in the skymap.
All five bands for each of the patches will be processed.
You can retrieve the skymap and interrogate it using the various member functions.

.. code-block:: python

   from lsst.daf.butler import Butler
   butler = Butler('SMALL_HSC')
   skymap = butler.get('skyMap', skymap='hsc_rings_v1', collections='HSC/RC2/defaults')
   tractInfo = skymap.generateTract(9813)
   patch = tractInfo[41]
   patch.getIndex()
   --> (5, 4)

The data queries will typically use the integer id for the patches, but you can use code like that above to find out the x and y indices into the tract's rectilinear grid of patches.
In this case, the patch with id 41 is located at the position (5, 4) in tract 9813.

To warp the images, you will use the ``pipetask run`` command again.
This time you will specify the ``makeWarp`` subset and an appropriate output collection.
This example uses ``coadds`` as the output collection.

.. code-block:: bash

   pipetask run --register-dataset-types \
   -b $RC2_SUBSET_DIR/SMALL_HSC/butler.yaml \
   -i u/$USER/source_calibration,u/$USER/jointcal,u/$USER/fgcm \
   -o u/$USER/warps \
   -p $DRP_PIPE_DIR/pipelines/HSC/DRP-RC2_subset.yaml#makeWarp \
   -d "skymap = 'hsc_rings_v1' AND tract = 9813 AND patch in (38, 39, 40, 41)"

Note that warping requires the ouptuts of both ``jointcal`` and ``FGCM``, so both of those collections need to be specified as inputs.
Again, this will warp all calibrated exposures.
If you wish to pare down the data to be processed, you can specify a data query like the one earlier in this section using the ``-d`` argument.

.. tip::

   As with the ``singleFrame`` pipeline, warping only needs the data from an input visit and the skymap.
   Each warp can be done independently of every other warp.
   That means it is a good candidate for running in parallel.
   If you have access to more than one core for processing, specifying the `-j<num cores>` argument will speed up this step.


Coadding warped images
======================

Now you'll assemble the warped images into coadditions for each patch with the ``assembleCoadd`` pipeline.
As before, we will run without a data query to process a subset of the data, but a selection can be made with the ``-d`` argument just as with warping.
In this case the the ``-d`` arguement could be omitted since the coaddition process will only find the warps from the previous command and will thus only produce coadds for those patches.

Run:

.. code-block:: bash

   pipetask run --register-dataset-types \
   -b $RC2_SUBSET_DIR/SMALL_HSC/butler.yaml \
   -i u/$USER/warps \
   -o u/$USER/coadds \
   -p $DRP_PIPE_DIR/pipelines/HSC/DRP-RC2_subset.yaml#assembleCoadd \
   -d "skymap = 'hsc_rings_v1' AND tract = 9813 AND patch in (38, 39, 40, 41)"

.. tip::

   While coaddition can be done in parallel, each process is more memory intensive than warping because multiple visits from multiple detectors may be put in memory at once.
   Still, if you have access to a machine with a fair amount of memory, the ``-j`` option may still speed up this step.

Wrap up
=======

In this tutorial, you've warped exposures into a pre-existing skymap, and then coadded the exposures to make deep mosaics.
Here are some key takeaways:

- Skymaps define the WCS of coadditions.
- Skymaps are composed of tracts, each of which is composed of smaller patches.
- The ``makeWarp`` pipeline warps exposures into the WCSs of the skymap.
- The ``assembleCoadd`` pipeline coadds warped exposures into deep mosaics.

Continue this tutorial in :doc:`part 6, where you'll measure sources <photometry>` in the coadds.

.. _example dataset: https://github.com/lsst-dm/rc2_subset
