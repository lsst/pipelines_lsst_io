..
  Brief:
  This tutorial is geared towards beginners to the Science Pipelines software.
  Our goal is to guide the reader through a small data processing project to show what it feels like to use the Science Pipelines.
  We want this tutorial to be kinetic; instead of getting bogged down in explanations and side-notes, we'll link to other documentation.
  Don't assume the user has any prior experience with the Pipelines; do assume a working knowledge of astronomy and the command line.

.. _getting-started-tutorial-coaddition:

################################################
Getting started tutorial part 4: coadding images
################################################

In this part of the :ref:`tutorial series <getting-started-tutorial>` you will combine the individual exposures produced by :command:`processCcd.py` (from :doc:`part 2 <processccd>`) into deeper coadds (mosaic images).
To do this you'll first define the pixel frame that you'll mosaic into, called a **sky map**, and then warp (reproject) images into that sky map.
Finally, you will coadd the warped images together into deep images.

.. include:: /gen2tutorialdeprecation.txt

Set up
======

Pick up your shell session where you left off in :doc:`part 2 <processccd>`.
That means your current working directory must *contain* the :file:`DATA` directory (the Butler repository).

The ``lsst_distrib`` package also needs to be set up in your shell environment.
See :doc:`/install/setup` for details on doing this.

About sky maps
==============

Before you get started, let's talk about **sky maps.**

A sky map is a tiling of the celestial sphere, and is used as coordinate system for the final coadded image.
A sky map is composed of one or more **tracts**.
Those tracts contain smaller regions called **patches**.
Both tracts and patches overlap their neighbors.

Each tract has a different world coordinate system (WCS), but the WCSs of the patches within a given tract are just linearly-offset versions of the same WCS.

There are two general categories of sky maps:

1. Whole sky.
2. A selected region containing a set of exposures.
  
Since this HSC dataset covers a small part of the sky, you'll make the second type.

Making a sky map
================

Again, you want the sky map to cover exactly the exposures you've already processed.
The most convenient sky map type for this task is a *discrete sky map,* which you'll make with the :command:`makeDiscreteSkyMap.py` command-line task:

.. code-block:: bash

   makeDiscreteSkyMap.py DATA --id --rerun processCcdOutputs:coadd --config skyMap.projection="TAN"

As you might guess from the previous commands, the ``--id`` wildcard argument implies that the :command:`makeDiscreteSkyMap.py` command will consider all exposures in the Butler repository, producing a sky map sized to encompass these images.

The last line of the logging output from :command:`makeDiscreteSkyMap.py` reads:

.. code-block:: text

   makeDiscreteSkyMap INFO: tract 0 has corners (321.161, -0.605), (320.601, -0.605), (320.601, -0.045), (321.161, -0.045) (RA, Dec deg) and 3 x 3 patches

In other words, the sky map you've just created has a single tract covering all exposures.
That tract is divided into a 3-by-3 grid of patches.
When you make coadditions, you'll make one coaddition per patch, for each filter.

Before we move on, let's look at two of the other arguments you used with the :command:`makeDiscreteSkyMap.py` command: ``--rerun`` and ``--config``.

.. _getting-started-tutorial-chaining:

Rerun chaining
--------------

The ``--rerun`` argument introduces the concept of *chaining*.
The ``--rerun processCcdOutputs:coadd`` syntax creates a new rerun called ``coadd`` that's chained to ``processCcdOutputs`` as an input repository.
This means that you're writing outputs into the new ``coadd`` rerun without affecting the ``processCcdOutputs``.

.. tip::

   Use chained reruns at every data processing phase to get flexibility to try different configurations without modifying the reruns of previous phases.

   The Butler follows the full depth of a chain to find a requested dataset.
   Thus the ``coadd`` rerun effectively contains not only the coadd outputs, but also outputs from :command:`processCcd.py` in the ``processCcdOutputs`` rerun and the original raw data at the root of the repository.

Task configuration
------------------

The last thing to notice about the :command:`makeDiscreteSkyMap.py` command is that you've set a task configuration: ``--config skyMap.projection="TAN"``.

You can discover available configurations by running the command with a ``--show config`` argument (similar to the ``--show data`` mode you already saw):

.. code-block:: bash

   makeDiscreteSkyMap.py DATA --id --rerun processCcdOutputs:coadd --show config

These lines from the output briefly document the ``skyMap.projection`` configuration field:

.. code-block:: text

   # one of the FITS WCS projection codes, such as:
   #           - STG: stereographic projection
   #           - MOL: Molleweide's projection
   #           - TAN: tangent-plane projection
   #
   config.skyMap.projection='TAN'

Simple configurations of string, int, float, and boolean value types can be made on the command line, like you did here.
Some configuration values are Python lists, dictionaries, or even class objects.
For these types you'll need to make a configuration file; you'll see an example of this later.

Warping images onto the sky map
===============================

Before assembling the coadded image, you need to *warp* the exposures created by :command:`processCcd.py` onto the pixel grids of patches created by :command:`makeDiscreteSkyMap.py`.
You can use the :command:`makeCoaddTempExp.py` command-line task for this.

The way you select data IDs for warping and coaddition is slightly different than for processing individual exposures because you must select both the exposures to use as inputs *and* what patches in the sky map to coadd into.

You'll select exposures to use as inputs with the ``--selectId`` argument.
This example selects ``HSC-R``-band exposures:

.. code-block:: text

   --selectId filter=HSC-R

The output is now specified with the familiar ``--id`` argument.
Instead of an exposure data ID, you'll specify the coaddition output according to ``filter``, ``tract``, and ``patch`` keys.
For example:

.. code-block:: text

   --id filter=HSC-R tract=0 patch=0,0

The ``patch=0,0`` key selects the patch at index ``0, 0``.
Likewise, the middle patch of the 3-by-3 grid is ``1, 1``.

Now, you'll want to make coadditions for all nine patches.
Like you did with :command:`processCcd.py`, you can supply multiple patches that :command:`makeCoaddTempExp.py` will iterate over.
To specify multiple patches, you'll use the ``^`` (or) operator.
For example, this ``--id`` argument selects both the ``0,0`` and ``1,0`` patches:

.. code-block:: text

   --id filter=HSC-R tract=0 patch=0,0^1,0

.. important::

   When you run :command:`makeCoaddTempExp.py`, you *can't* omit the ``tract`` and ``patch`` data ID keys as a wild card pattern.
   You need to explicity define which patches to make warped exposures for.

Putting this together, run the following command to warp ``HSC-R``-band exposures into all nine patches:

.. code-block:: bash

   makeCoaddTempExp.py DATA --rerun coadd \
       --selectId filter=HSC-R \
       --id filter=HSC-R tract=0 patch=0,0^0,1^0,2^1,0^1,1^1,2^2,0^2,1^2,2 \
       --config doApplyExternalPhotoCalib=False doApplyExternalSkyWcs=False \
       doApplySkyCorr=False

.. tip::

   :command:`makeCoaddTempExp.py` automatically filters out exposures that don't fit on a patch.

.. note::

   Since this tutorial doesn't prepare an external calibration (producing replacement photometric calibration and WCS solutions) or sky correction, you needed to explicitly disable these calibration steps from the default HSC processing configuration.

Next, repeat the warping step for ``HSC-I``-band images:

.. code-block:: bash

   makeCoaddTempExp.py DATA --rerun coadd \
       --selectId filter=HSC-I \
       --id filter=HSC-I tract=0 patch=0,0^0,1^0,2^1,0^1,1^1,2^2,0^2,1^2,2 \
       --config doApplyExternalPhotoCalib=False doApplyExternalSkyWcs=False \
       doApplySkyCorr=False

Coadding warped images
======================

Now you'll assemble the warped images into coadditions for each patch with the :command:`assembleCoadd.py` task.
As before, the ``--selectId`` argument selects warped ``HSC-R``-band exposures while the ``--id`` argument specifies the patches that :command:`assembleCoadd.py` will make coadds for.
Run:

.. code-block:: bash

   assembleCoadd.py DATA --rerun coadd \
       --selectId filter=HSC-R \
       --id filter=HSC-R tract=0 patch=0,0^0,1^0,2^1,0^1,1^1,2^2,0^2,1^2,2

Run :command:`assembleCoadd.py` again to make ``HSC-I``-band coadds:

.. code-block:: bash

   assembleCoadd.py DATA --rerun coadd \
       --selectId filter=HSC-I \
       --id filter=HSC-I tract=0 patch=0,0^0,1^0,2^1,0^1,1^1,2^2,0^2,1^2,2

.. tip::

   While both the :command:`makeCoaddTempExp.py` and :command:`assembleCoadd.py` command-line tasks iterate over patches, they cannot iterate over multiple filters.
   That's why you couldn't write a ``--id filter=HSC-R^HSC-I`` argument.

Wrap up
=======

In this tutorial, you've made a sky map, warped exposures into it, and then coadded the exposures into deep mosaics.
Here are some key takeaways:

- Sky maps define the WCS of coadditions.
- Sky maps are composed of tracts, each of which is composed of smaller patches.
- The :command:`makeDiscreteSkyMap.py` command creates a sky map to encompass a given set of exposures.
- The :command:`makeCoaddTempExp.py` command warps exposures into the WCSs of the sky map.
- The :command:`assembleCoadd.py` command coadds warped exposures into deep mosaics for a given patch and filter combination.
- The ``--rerun rerunA:rerunB`` syntax lets you chain reruns together. Inputs are read from ``rerunA`` and outputs are written to ``rerunB``.

Continue this tutorial in :doc:`part 5, where you'll measure sources <photometry>` in the coadds.
