..
  Brief:
  This tutorial is geared towards beginners to the Science Pipelines software.
  Our goal is to guide the reader through a small data processing project to show what it feels like to use the Science Pipelines.
  We want this tutorial to be kinetic; instead of getting bogged down in explanations and side-notes, we'll link to other documentation.
  Don't assume the user has any prior experience with the Pipelines; do assume a working knowledge of astronomy and the command line.

.. _getting-started-tutorial-processccd:

#############################################################################
Getting started tutorial part 2: calibrating single frames with processCcd.py
#############################################################################

This is part 2 of the :ref:`getting started tutorial series <getting-started-tutorial>`.
Before starting this tutorial, make sure you've completed the :doc:`previous part <data-setup>`.

In this part we'll process individual raw HSC images in the Butler repository (which you assembled in :doc:`part 1 <data-setup>`) into calibrated exposures.
We'll use the :command:`processCcd.py` command line task to remove instrumental signatures with dark, bias and flat field calibration images.
:command:`processCcd.py` will also use the reference catalog to establish a preliminary WCS and photometric zeropoint solution.

Setup check
===========

Let's take a moment to make sure your command line environment is set up.
Run:

.. code-block:: bash

   eups list lsst_distrib

The printed output should contain the word ``setup``.
If not, :ref:`review the installation tutorials <getting-started-activate>` on activating the environment and setting up ``lsst_distrib``.

Your shell's working directory also needs contain the Butler repository directory called :file:`DATA`.

Let's get back to it.

Reviewing what data will be processed
=====================================

:command:`processCcd.py` can operate on a single image, or iterate over multiple images.
Let's do a dry-run to see what data will be processed in the Butler repository:

.. code-block:: bash

   processCcd.py DATA --rerun processCcdOutputs --id --show data

The important arguments here are ``--id`` and ``--show data``.

The ``--id`` argument allows you to select images to process by their dataIds.
Here, the plain ``--id`` argument acts as a wildcard that selects all data in the repository.

The ``--show data`` argument puts :command:`processCcd.py` into a dry-run mode that lists the dataIds that would be processed according to the ``--id`` argument rather than processing the data.

When you run the above command, several lines will be printed, each a fully-qualified dataIds for raw images in the Butler repository.
For example:

.. code-block:: text

   id dataRef.dataId = {'taiObs': '2013-06-17', 'pointing': 533, 'visit': 903334, 'dateObs': '2013-06-17', 'filter': 'HSC-R', 'field': 'STRIPE82L', 'ccd': 23, 'expTime': 30.0}

Notice the keys that describe each dataId, such as the ``visit`` (exposure identifier for the HSC camera), ``ccd`` (identifies a specific chip in the HSC camera) and ``filter``, among others.
With these keys you can select exactly what data we want to process.
For example, here's how to select just ``HSC-I``-band images:

.. code-block:: bash

   processCcd.py DATA --rerun processCcdOutputs --id filter=HSC-I --show data

Now only dataIds for ``HSC-I`` images are printed.
The ``--id`` argument supports a rich syntax for expressing dataIds by multiple selection criteria.

.. FIXME: Link to further documentation on DataIds and the selector language.

Running processCcd.py
=====================

For this tutorial, we want to process all data in the repository with :command:`processCcd.py`, so using the ``--id`` wildcard is appropriate.
Let's run :command:`processCcd.py`:

.. code-block:: bash

   processCcd.py DATA --rerun processCcdOutputs --id

.. tip::

   While :command:`processCcd.py` runs, let's discuss the ``--rerun`` argument.
   In this step the :command:`processCcd.py` outputs are being written to a rerun named ``processCcdOutputs``.

   *Reruns* allow you to isolate processing outputs in the Butler repository.
   You can run a command line task multiple times as different reruns to prevent one run from overwriting the other outputs.
   This is useful for experimenting with different configurations.

Next up
=======

Continue this tutorial in :doc:`part 3, where we'll coadd these processed images <coaddition>` into deeper mosaics.
