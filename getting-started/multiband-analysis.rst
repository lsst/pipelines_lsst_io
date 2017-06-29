..
  Brief:
  This tutorial is geared towards beginners to the Science Pipelines software.
  Our goal is to guide the reader through a small data processing project to show what it feels like to use the Science Pipelines.
  We want this tutorial to be kinetic; instead of getting bogged down in explanations and side-notes, we'll link to other documentation.
  Don't assume the user has any prior experience with the Pipelines; do assume a working knowledge of astronomy and the command line.

#################################################################################
Getting started tutorial part 6: analyzing measurement catalogs in multiple bands
#################################################################################

This is part 6 of the :ref:`getting started tutorial series <getting-started-tutorial>`.
Before starting this tutorial, make sure you've completed the previous parts.

In the :doc:`previous tutorial <photometry>` we measured coadded exposures using the :command:`forcedPhotCoadd.py` command line task.
Forced photometry is useful because sources are measured uniformly across each coadd in the same tract and patch, making multi-band analyses of objects straightforward.
In this tutorial we will explore some analysis scenarios with forced photometry measurement catalogs.

Setup check
===========

Let's take a moment to make sure your command line environment is set up.
Run:

.. code-block:: bash

   eups list lsst_distrib

The printed output should contain the word ``setup``.
If not, :ref:`review the installation tutorials <getting-started-activate>` on activating the environment and setting up ``lsst_distrib``.

Your shell's working directory also needs to contain Butler repository directory called :file:`DATA`.

For this tutorial you will be working from an interactive Python session.
We recommend using a `Jupyter Notebook`_ to see plots inline.
Ensure that the notebook session is running from a shell where you ran :command:`setup lsst_distrib`.

Let's get started.

Loading forced photometry measurement catalogs with the Butler
==============================================================

The :command:`forcedPhotCoadd.py` command line task created ``deepCoadd_forced_src`` datasets for each coadd in the example data repository.
Being forced photometry catalogs, rows in ``deepCoadd_forced_src`` correspond row-for-row, which makes them particularly convenient.

Let's use the Butler to get these datasets corresponding to the central patch (``1,1``) coadd for both the HSC-R and HSC-I filters.
In a Python session, first create a Butler:

.. code-block:: python

   import lsst.daf.persistence as dafPersist
   butler = dafPersist.Butler(inputs='DATA/rerun/coaddForcedPhot')

This Butler is using the ``coaddForcedPhot`` rerun we created for the :command:`forcePhotCoadd.py` command line task's outputs.

Next, use the Butler to get the ``deepCoadd_forced_src`` datasets for both filters:

.. code-block:: python

   rSources = butler.get('deepCoadd_forced_src', {'filter': 'HSC-R', 'tract': 0, 'patch': '1,1'})
   iSources = butler.get('deepCoadd_forced_src', {'filter': 'HSC-I', 'tract': 0, 'patch': '1,1'})

Getting calibrated PSF photometry
=================================

The ``base_PsfFlux_flux`` column of these ``deepCoadd_forced_src`` datasets is the flux from the linear least-squares fit of the PSF model to the source.
From the source table's schema we know this flux has units of counts:

.. code-block:: python

   iSources.getSchema().find('base_PsfFlux_flux').field.getUnits()

Transforming this flux into a magnitude requires knowing the coadd's zeropoint.
We'll get this metadata from the coadd dataset itself.
The coadd we made in :doc:`part 3 <coaddition>` with :command:`assembleCoadd.py` doesn't have calibration info attached to it, though.
Instead, we want the ``deepCoadd_calexp`` dataset that was created by the :command:`detectCoaddSources.py` command line task.
This ``deepCoadd_calexp`` is a coadd that includes calibration information attached by source detection tasks.

First, load the dataset for both filters:

.. code-block:: python

   rCoaddCalexp = butler.get('deepCoadd_calexp',  {'filter': 'HSC-R', 'tract': 0, 'patch': '1,1'})
   iCoaddCalexp = butler.get('deepCoadd_calexp',  {'filter': 'HSC-I', 'tract': 0, 'patch': '1,1'})

The calibration information for the ``rCoaddCalexp`` and ``iCoaddCalexp`` objects is stored inside a ``lsst.afw.image.calib.Calib`` object that's available from the ``getCalib()`` method:

.. code-block:: python

   rCoaddCalib = rCoaddCalexp.getCalib()
   iCoaddCalib = iCoaddCalexp.getCalib()

These ``Calib`` objects not only have methods for directing accessing calibration information, but also for applying those calibrations.
Let's use the ``Calib.getMagnitude()`` method to transform fluxes in counts to magnitudes in the HSC instrument's system (AB magnitudes):

.. code-block:: python

   rCoaddCalib.setThrowOnNegativeFlux(False)
   iCoaddCalib.setThrowOnNegativeFlux(False)

   rMags = rCoaddCalib.getMagnitude(rSources['base_PsfFlux_flux'])
   iMags = iCoaddCalib.getMagnitude(iSources['base_PsfFlux_flux'])

.. note::

   We called the ``Calib.setThrowOnNegativeFlux`` method to prevent an exception from being raised for sources with negative fluxes.
   This is commonly required for forced photometry analysis since some sources may not be visible in a band so that the flux measurement is effectively of blank sky.
   Because of background variance the measured flux of non-detections can sometimes be negative.

Filtering for unique, deblended sources with the detect_isPrimary flag
======================================================================

Before we go ahead and plot a color-magnitude diagram from the full source table, we need to do some basic filtering.
Exactly what filtering is done depends on the application, but source tables should *always* be filtered for unique sources.
There are two ways that measured sources might not be unique: deblended sources, and sources in patch overlaps.

Finding deblended sources
-------------------------

When objects are detected they are deblended.
Deblending involves decomposing a source into multiple child sources that have local flux peaks.
In source tables like ``rSources`` and ``iSources``, both the original (blended) *and* de-blended sources are included in the table.
This is done so that you can choose whether to use blended or deblended measurements in your analysis.
If you *don't* choose choose, though, the same flux will be included multiple times in your analysis.

Usually you will want to use fully deblended sources in your analysis.
The best way to identify fully deblended sources is those that have no children (*children* being sources deblended from that parent source) given the ``deblend_nChild`` column.
Let's make a boolean index array of deblended sources:

.. code-block:: python

   deblended = rSources['deblend_nChild'] == 0

Finding primary detections
--------------------------

The other reason a source in the table might not be unique is if it falls in the overlaps of patches, so it appears in multiple measurement tables.
If you are analyzing multiple patches, or multiple tracts, you want to use the *primary* detection for each source.
The Pipelines determine if a detection in a patch is primary, or not, by whether it falls in the *inner region* of that patch (and tract).
An inner region is a part of the sky map exclusively claimed by one patch.

The flag that indicates whether a source lies in the patche's inner region isn't in the ``deepCoadd_forced_src`` table though.
Instead we need to look at the ``deepCoadd_ref`` table made by :command:`mergeCoaddMeasurements.py` in the :ref:`previous tutorial <getting-started-tutorial-merge-coadds>`.
Let's get it for the patch we're analyzing:

.. code-block:: python

   refTable = butler.get('deepCoadd_ref', {'filter': 'HSC-R^HSC-I', 'tract': 0, 'patch': '1,1'})

Make an index array from the combination of ``detect_isPatchInner`` and ``detect_isTractInner`` flags:

.. code-block:: python

   inInnerRegions = refTable['detect_isPatchInner'] & refTable['detect_isTractInner']

The go-to flag: detect_isPrimary
--------------------------------

We actually want the combination of the ``isDeblended`` and ``inInnerRegions`` arrays we just made.
The ``deepCoadd_ref`` table provides a short-cut for this: the ``detect_isPrimary`` flag identifies sources that are both fully deblended and in inner regions.
Run:

.. code-block:: python

   isPrimary = refTable['detect_isPrimary']

Now we can use this array to slice the photometry arrays and get only primary sources, like this:

.. code-block:: python

   rMag[isPimary]
   iMag[isPimary]

.. note::

   The ``detect_isPrimary`` flag is defined by this algorithm:

   .. code-block:: text

      (deblend_nChild == 0) & detect_isPatchInner & detect_isTractInner

Quickly classifying stars and galaxies
======================================

Reliably classifying sources as stars and galaxies is not easy, but we can get a rough estimate based on the extendedness of sources.
The ``base_ClassificationExtendedness_value`` column is ``True`` for extended sources (galaxies) and ``False`` for point sources (like stars).
Let's create a boolean index of fully deblended sources that are also classified as point sources:

.. code-block:: python

   isStellar = iSources['base_ClassificationExtendedness_value'] == True

Now we know what the likely stars are in our catalog.

Using measurement flags
=======================

Lastly, we may want to work with only quality measurements.
Earlier, we got PSF fluxes of sources (``base_PsfFlux_flux``).
The ``base_PsfFlux`` measurement plugin also creates flags that describe measurement errors and issues.
You can find these flags, as usual, from the table schema.
Here's a way to find columns produced by the ``base_PsfFlux`` plugin:

.. code-block:: python

   iSources.getSchema().extract('base_PsfFlux_*')

Let's use the ``base_PsfFlux_flag``, which is the logical combination of specific ``base_PsfFlux`` error flags:

.. code-block:: python

   isGoodFlux = ~iSources['base_PsfFlux_flag']

Since the ``base_PsfFlux_flag`` is ``True`` for sources with measurement errors we used the unary invert operator (``~``) so that well-measured sources are ``True`` in the ``isGoodFlux`` array.

Finally, let's combine all these boolean index arrays together:

.. code-block:: python

   selected = isPrimary & isStellar & isGoodFlux

In the next step, we'll plot a color-magnitude diagram of the sources we've selected.

Plot a CMD
==========

The product of our effort will be an *r-i* color-magnitude diagram.
Let's use matplotlib_ to create this visualization:

.. code-block:: python

   import matplotlib.pyplot as plt

   plt.style.use('seaborn-notebook')
   plt.figure(1, figsize=(4, 4), dpi=140)
   plt.scatter(rMags[selected] - iMags[selected],
               iMags[selected],
               edgecolors='None', s=2, c='k')
   plt.xlim(-0.5, 3)
   plt.ylim(25, 14)
   plt.xlabel('$r-i$')
   plt.ylabel('$i$')
   plt.subplots_adjust(left=0.125, bottom=0.1)
   plt.show()

You should see a figure like this:

.. figure:: multiband-analysis-stars.png
   :alt: r-i color-magnitude diagram of stars.
   :height: 546
   :width: 546

   r-i color-magnitude diagram of stars.

Recap
=====

In this tutorial gained experience in working with source measurement catalogs created by the LSST Science Pipelines.
You've seen how to load forced-photometry source tables (``deepCoadd_forced_src``) from the Butler.
As you've seen, our multi-band analysis benefited from how forced-photometry produces source tables in multiple bands that correspond row-for-row.
We got calibrated photometric measurements with metadata in the calibrated exposure (``deepCoadd_calexp`` dataset).
You also learned how to filter sources for uniqueness (``detect_isPrimary`` column from the ``deepCoadd_ref`` dataset), separate stars and galaxies (``base_ClassificationExtendedness_value`` column), and good photometry (``base_PsfFlux_flag`` column).

In the end, we created a simple *r-i* color-magnitude diagram.
This is just the beginning, though.
With the dataset you've created in this tutorial, you can look at galaxies with measurements from the ``CModel`` plugin.
Or compare PSF-fitted photometric measurements with aperture photometry of stars.

When you're ready, dive into the rest of the :doc:`LSST Science Pipelines </index>` documentation to begin processing your own data.
As you're learning, don't hesitate to reach out with questions on the `LSST Community forum`_.

.. _`Jupyter Notebook`: http://jupyter-notebook.readthedocs.io/en/latest/
.. _matplotlib: http://matplotlib.org
.. _LSST Community forum: https://community.lsst.org
