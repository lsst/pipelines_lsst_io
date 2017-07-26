..
  Brief:
  This tutorial is geared towards beginners to the Science Pipelines software.
  Our goal is to guide the reader through a small data processing project to show what it feels like to use the Science Pipelines.
  We want this tutorial to be kinetic; instead of getting bogged down in explanations and side-notes, we'll link to other documentation.
  Don't assume the user has any prior experience with the Pipelines; do assume a working knowledge of astronomy and the command line.

.. _getting-started-tutorial-coaddition:

################################################
Getting started tutorial part 3: coadding images
################################################

This is part 3 of the :ref:`getting started tutorial series <getting-started-tutorial>`.
Before starting this tutorial, make sure you've completed the previous parts.

In this part of the tutorial series we will combine the individual exposures produced by :command:`processCcd.py` into deeper coadds (mosaic images).
To do this we'll first define the pixel frame that we'll mosaic into, called a **sky map**, and then warp (reproject) images into the sky map.
Finally, we will coadd the warped images together into deep images.

Setup check
===========

Let's take a moment to make sure your command line environment is set up.
Run:

.. code-block:: bash

   eups list lsst_distrib

The printed output should contain the word ``setup``.
If not, :ref:`review the installation tutorials <getting-started-activate>` on activating the environment and setting up ``lsst_distrib``.

Your shell's working directory also needs to contain Butler repository directory called :file:`DATA`.

Let's get back to it.

Making a sky map
================

We want the sky map to cover exactly the exposures we've already processed.
The most convenient sky map type for this task is a *discrete sky map,* which we'll make with the :command:`makeDiscreteSkyMap.py` command line task:

.. code-block:: bash

   makeDiscreteSkyMap.py DATA --id --rerun processCcdOutputs:coadd --config skyMap.projection="TAN"

As you might guess from the previous commands, the ``--id`` wildcard argument implies that the :command:`makeDiscreteSkyMap.py` command will consider all exposures in the Butler repository, producing a sky map sized to encompass these images.

The ``--rerun`` argument introduces the concept of *chaining*.
The ``processCcdOutputs:coadd`` syntax creates a new rerun called ``coadd`` that's chained to ``processCcdOutputs``.
This means that we're writing outputs into the new ``coadd`` rerun without affecting the ``processCcdOutputs`` rerun in any way.

.. tip::

   Use chained reruns at every data processing phase to get flexibility to try different configurations without modifying the reruns of previous phases.

   The Butler follows the full depth of a chain to find a requested dataset.
   Thus the ``coadd`` rerun effectively contains not only the coadd outputs, but also outputs from :command:`processCcd.py` and the original raw data.

The last thing to notice about the :command:`makeDiscreteSkyMap.py` command is that we've set a task configuration: ``--config skyMap.projection="TAN"``.

You can discover available configurations by running the command with a ``--show config`` argument (similar to the ``--show data`` mode we already saw):

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

Simple configurations of string, int, float, and boolean value types can be made on the command line, like we did here.
Some configuration values are Python lists, dictionaries, or even class objects.
For these types you'll need to make a configuration file; we'll see an example of this later.

Aside: the sky map's tracts and patches
=======================================

The last line of the logging output from :command:`makeDiscreteSkyMap.py` reads:

.. code-block:: text

   makeDiscreteSkyMap INFO: tract 0 has corners (321.161, -0.605), (320.601, -0.605), (320.601, -0.045), (321.161, -0.045) (RA, Dec deg) and 3 x 3 patches

A **tract** is a large region of sky containing many **patches**.
All patches within a tract share the same WCS with only integer offsets between them.

The discrete sky map we constructed has, by definition, one tract (``tract 0``) covering all exposures.
That tract is divided into a 3-by-3 grid of patches.
When we make coadditions we'll make one coaddition per patch.

Warping images onto the sky map
===============================

Before assembling the coadded image we need to *warp* the exposures created by :command:`processCcd.py` onto the pixel grids of patches created by :command:`makeDiscreteSkyMap.py`.
We'll use the :command:`makeCoaddTempExp.py` command line task for this.

The way we select dataIds for warping and coaddition is slightly different than for processing individual exposures
because we must select both the exposures to use as inputs *and* what patches in the sky map to coadd into.

We select exposures to use as inputs with the ``--selectId`` argument.
This example selects ``HSC-R``-band exposures:

.. code-block:: text

   --selectId filter=HSC-R

The output is now specified with the familiar ``--id`` argument.
Instead of an exposure dataId, we specify the coaddition output according to filter, tract, and patch keys.
For example:

.. code-block:: text

   --id filter=HSC-R tract=0 patch=0,0

The ``patch=0,0`` key selects the patch at index ``0, 0``.
Likewise, the middle patch of the 3-by-3 grid is ``1, 1``.

We want to make coadditions for all nine patches.
Like we did with :command:`processCcd.py`, we can supply multiple patches that :command:`makeCoaddTempExp.py` will iterate over.
To specify multiple patches, we'll use the ``^`` (or) operator.
For example, this ``--id`` argument selects both the ``0,0`` and ``1,0`` patches:

.. code-block:: text

   --id filter HSC-R tract=0 patch=0,0^1,0

Putting this together, run the following command to warp ``HSC-R``-band exposures into all nine patches:

.. code-block:: bash

   makeCoaddTempExp.py DATA  --rerun coadd \
       --selectId filter=HSC-R \
       --id filter=HSC-R tract=0 patch=0,0^0,1^0,2^1,0^1,1^1,2^2,0^2,1^2,2 \
       --config doApplyUberCal=False

.. note::

   Since we didn't prepare an uber calibration for this tutorial, we needed to explicitly disable the uber calibration step that is enabled by default for HSC processing.

.. tip::

   :command:`makeCoaddTempExp.py` automatically filters out exposures that don't fit on a patch.

Next, repeat the warping step for ``HSC-I``-band images:

.. code-block:: bash

   makeCoaddTempExp.py DATA --rerun coadd \
       --selectId filter=HSC-I \
       --id filter=HSC-I tract=0 patch=0,0^0,1^0,2^1,0^1,1^1,2^2,0^2,1^2,2 \
       --config doApplyUberCal=False

Coadding warped images
======================

Now we'll assemble the warped images into coadditions for each patch with the :command:`assembleCoadd.py` task.
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

   While both the :command:`makeCoaddTempExp.py` and :command:`assembleCoadd.py` command line tasks iterate over patches, they cannot iterate over multiple filters.
   That's why we didn't write a ``--id filter=HSC-R^HSC-I`` argument.

Next up
=======

Continue this tutorial in :doc:`part 4, where we measure sources <photometry>` in the coadds.
