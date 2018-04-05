..
  Brief:
  This tutorial is geared towards beginners to data processing with the Science Pipelines.
  Our goal is to guide the reader through a small data processing project to show what it feels like to use the Science Pipelines.
  We want this tutorial to be kinetic; instead of getting bogged down in explanations and side-notes, we'll link to other documentation.
  Don't assume the user has any prior experience with the Pipelines; do assume a working knowledge of astronomy and the command line.

.. _getting-started-tutorial-processccd:

#############################################################################
Getting started tutorial part 2: calibrating single frames with processCcd.py
#############################################################################

In this part of the :ref:`tutorial series <getting-started-tutorial>` you'll process individual raw HSC images in the Butler repository (which you assembled in :doc:`part 1 <data-setup>`) into calibrated exposures.
We'll use the :command:`processCcd.py` command-line task to remove instrumental signatures with dark, bias and flat field calibration images.
:command:`processCcd.py` will also use the reference catalog to establish a preliminary WCS and photometric zeropoint solution.

Set up
======

Pick up your shell session where you left off in :doc:`part 1 <data-setup>`.
That means your current working directory must *contain* the :file:`DATA` directory (the Butler repository).

The ``lsst_distrib`` package also needs to be set up in your shell environment.
See :doc:`/install/setup` for details on doing this.

Reviewing what data will be processed
=====================================

:command:`processCcd.py` can operate on a single image or iterate over multiple images.
You can do a dry-run to see what data will be processed in the Butler repository:

.. code-block:: bash

   processCcd.py DATA --rerun processCcdOutputs --id --show data

The important arguments here are ``--id`` and ``--show data``.

The ``--id`` argument allows you to select datasets to process by their **data IDs**.
Data IDs describe individual datasets in the Butler repository.
Datasets also have *types*, and each command-line task will only process data of certain types.
In this case, :command:`processCcd.py` processes ``raw`` exposures (uncalibrated images from individual CCD chips).

In the above command, the plain ``--id`` argument acts as a wildcard that selects all ``raw``-type data in the repository (in a moment we'll see how to filter data IDs).

The ``--show data`` argument puts :command:`processCcd.py` into a dry-run mode that prints a list of data IDs to standard output that would be processed according to the ``--id`` argument rather than actually processing the data.
For example, one line of the output from a :command:`processCcd.py` run with ``--show data`` looks like:

.. code-block:: text

   id dataRef.dataId = {'taiObs': '2013-06-17', 'pointing': 533, 'visit': 903334, 'dateObs': '2013-06-17', 'filter': 'HSC-R', 'field': 'STRIPE82L', 'ccd': 23, 'expTime': 30.0}

Notice the keys that describe each data ID, such as the ``visit`` (exposure identifier for the HSC camera), ``ccd`` (identifies a specific chip in the HSC camera) and ``filter``, among others.
With these keys you can select exactly what data you want to process.
For example, here's how to select just ``HSC-I``-band datasets:

.. code-block:: bash

   processCcd.py DATA --rerun processCcdOutputs --id filter=HSC-I --show data

Now only data IDs for ``HSC-I`` datasets are printed.
The ``--id`` argument supports a rich syntax for expressing data IDs by multiple selection criteria.

.. FIXME: Link to further documentation on Data IDs and the selector language from the lsst.pipe.base package documentation.

Running processCcd.py
=====================

After learning about datasets, go ahead and run :command:`processCcd.py` on all ``raw`` datasets in the repository:

.. code-block:: bash

   processCcd.py DATA --rerun processCcdOutputs --id

Aside: reruns and output Butler repositories
============================================

While :command:`processCcd.py` runs, let's discuss the ``--rerun`` argument.
Command-line tasks, like :command:`processCcd.py`, write their output datasets to Butler data repositories.
There are two ways to specify an output data repository: with the ``--output`` argument, or with the ``--rerun`` command-line argument.

The rerun pattern is especially convenient, especially with local Butler repositories, because each rerun is packaged within the file system directory of the parent Butler data repository (the :file:`DATA` directory in this tutorial).
Above, when you ran :command:`processCcd.py`, you configured it to write outputs to a new rerun named ``processCcdOutputs``.

The idea is that you'll process data by running a sequence of individual command-line tasks.
At each stage, you will output datasets to a new rerun.
This is called *rerun chaining,* and you learn how to do this :ref:`in the next tutorial <getting-started-tutorial-chaining>`.

If you need to re-do a processing step, to experiment with a different command-line task configuration for example, you can do that safely by outputting to a new rerun.

.. important::

   Bottom line: a given rerun must contain data that was all processed consistently, with the same task configurations.
   If you mix outputs from multiple runs of a command-line task with different configurations, it may impossible to understand or use the results of the data processing.

Wrap up
=======

In this tutorial, you've used the :command:`processCcd.py` command-line task to calibrate ``raw`` images in a Butler repository.
Here are some key takeaways:

- The :command:`processCcd.py` command-line task processes ``raw`` datasets, applying both photometric and astrometric calibrations.
- Datasets are described by both a *type* and *data ID*.
  Data IDs are key-value pairs that describe a dataset (for example ``filter``, ``visit``, ``ccd``, ``field``).
- Command-line tasks have ``--id`` arguments that let you select which datasets to process.
  An empty ``--id`` arguments acts as a wildcard that selects all available datasets in the repository of the type the command-line task can processes.
- Command-line tasks write their outputs to a Butler data repository.
  Reruns (``--rerun`` argument) are a convenient way to create output data repositories.
  Make sure that all datasets in a rerun are processed consistently.

Continue this tutorial in :doc:`part 3, where you'll learn how display these calibrated exposures <display>`.
