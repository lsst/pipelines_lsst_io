..
  Brief:
  This tutorial is geared towards beginners to the Science Pipelines software.
  Our goal is to guide the reader through a small data processing project to show what it feels like to use the Science Pipelines.
  We want this tutorial to be kinetic; instead of getting bogged down in explanations and side-notes, we'll link to other documentation.
  Don't assume the user has any prior experience with the Pipelines; do assume a working knowledge of astronomy and the command line.

.. _getting-started-tutorial-uber-cal:

################################################################
Getting started tutorial part 4: Using all the data to calibrate
################################################################

In this part of the :ref:`tutorial series <getting-started-tutorial>` you will use all of the results from the ``singleFrame`` pipeline to improve the photometric and astrometric calibrations.
When there are overlapping datasets from multiple visits, it's possible to average out effects from the atmosphere and improve the overall calibration.
This is sometime referred to as ubercalibration.

Improving the photometric and astrometric calibrations can lead to better coadds down the line, and correspondingly better measurements of objects.

For photometric calibration the system is the Forward Global Calibration Method (`FGCM`_).
We use a reference catalog from Pan-STARRS.

Refined astrometric calibration is provided by an in-house algorithm called ``jointcal``.
For ``jointcal`` we use an astrometric reference catalog derived from the second data release of the `Gaia`_ source catalog.

It is out of scope to go into the details of the algorithms here, but you will learn how to run them.
Also worth noting is that, in this instance, we will not see much benefit from global calibration since our dataset is small, but for larger datasets it can be a big benefit.

Set up
======

Pick up your shell session where you left off in :doc:`part 2 <singleframe>`.
For convenience, start in the top directory of the example git repository.

.. code-block:: bash

   cd $RC2_SUBSET_DIR

The ``lsst_distrib`` package also needs to be set up in your shell environment.
See :doc:`/install/setup` for details on doing this.

FGCM
====

As in :doc:`part 2 <singleframe>` you will be running pipelines configured to produce the results we need for later steps.

.. code-block:: bash

   pipetask run -b $RC2_SUBSET_DIR/SMALL_HSC/butler.yaml \
                -p $RC2_SUBSET_DIR/pipelines/DRP.yaml#fgcm \
                -i u/$USER/single_frame \
                -o u/$USER/fgcm \
                --register-dataset-types

This should look very similar to the command executed in :doc:`part 2 <singleframe>`.
There are three differences: 1) the subset to execute changed from ``singleFrame`` to ``fgcm``, 2) the input is now ``single_frame``, which contains pointers to the inputs to and outputs from ``singleFrame``, and 3) the output collection is now ``fgcm``.

Note that unlike the ``singleFrame`` pipeline, FGCM must be run on only a single core.
Setting the ``-j`` switch to anything other than ``1`` will result in an error.

jointcal
========

You can do ``jointcal`` in much the same way as you did FGCM.
Change the subset name and collection name appropriately.
E.g.:

.. code-block:: bash

   pipetask run -b $RC2_SUBSET_DIR/SMALL_HSC/butler.yaml \
                -p $RC2_SUBSET_DIR/pipelines/DRP.yaml#jointcal \
                -i u/$USER/single_frame \
                -o u/$USER/jointcal \
                --register-dataset-types

Note the input collection is the same as you passed to ``FGCM`` since ``jointcal`` doesn't depend on any of the outputs of ``FGCM``.

Wrap up
=======

In this tutorial, you've computed the improved photometric and astrometric calibration from multiple visits.
Here are some key takeaways:

- ``FGCM`` provides improved photometric calibration.
- Astrometric calibration improvements are provided by running ``jointcal``.
- Given a pipeline description, e.g. ``DRP.yaml``, subset can be specified, so running multiple steps can be done with very similar command line syntax.

Continue this tutorial in :doc:`part 5, where you'll warp single frame images and stack them to make coadds <coaddition>`.

.. _FGCM: https://arxiv.org/pdf/1706.01542.pdf
.. _Gaia: https://www.cosmos.esa.int/web/gaia/dr2
