..
  Brief:
  This tutorial is geared towards beginners to the Science Pipelines software.
  Our goal is to guide the reader through a small data processing project to show what it feels like to use the Science Pipelines.
  We want this tutorial to be kinetic; instead of getting bogged down in explanations and side-notes, we'll link to other documentation.
  Don't assume the user has any prior experience with the Pipelines; do assume a working knowledge of astronomy and the command line.

###############################################################################################
Getting started tutorial part 3: displaying exposures and source tables output by processCcd.py
###############################################################################################

This is part 3 of the :ref:`getting started tutorial series <getting-started-tutorial>`.
Before starting this tutorial, make sure you've completed the :doc:`previous parts <data-setup>`.

In the :doc:`last tutorial <processccd>` we used :command:`processCcd.py` to calibrate a set of raw Hyper Suprime-Cam images.
Now we'll learn how to use the LSST Science Pipelines to inspect :command:`processCcd.py`\ ’s outputs by displaying images and source catalogs in the `DS9 image viewer`_.
In the course of this tutorial you'll be introduced to some of the LSST Science Pipelines' Python APIs, including:

- Accessing datasets with the Butler.
- Displaying images in DS9 with ``lsst.afw.display``.
- Working with source catalogs using ``lsst.afw.table``.

Setup check
===========

Let's take a moment to make sure your command line environment is set up.
Run:

.. code-block:: bash

   eups list lsst_distrib

The printed output should contain the word ``setup``.
If not, :ref:`review the installation tutorials <getting-started-activate>` on activating the environment and setting up ``lsst_distrib``.

Your shell's working directory also needs to contain the Butler repository directory called :file:`DATA`.

You'll also need to `download and install the DS9 image viewer`_.

Let's get started.

Launch DS9 and start a Python interpreter
=========================================

In this tutorial we will use an interactive Python session to control DS9.

If you haven't already, launch the DS9 application.

Next, start up a Python interpreter.
You can use the default Python shell (:command:`python`), the `IPython shell`_, or even run from a `Jupyter Notebook`_.
Ensure that this Python session is running from the shell where you ran :command:`setup lsst_distrib`.

Creating a Butler client
========================

All data in the Pipelines flows through the Butler.
In the :doc:`previous tutorial <processccd>`, :command:`processCcd.py` read exposures from the Butler repository and persisted outputs back to the repository.
Although the Butler data repository is a directory on the filesystem (:file:`DATA`), we don't recommend directly accessing its files.
Instead, you use the Butler client from the ``lsst.daf.persistence`` module.
In the Python interpreter, run:

.. code-block:: python

   import lsst.daf.persistence as dafPersist
   butler = dafPersist.Butler(inputs='DATA/rerun/processCcdOutputs')

The Butler client reads from the data repository specified with the ``inputs`` argument.
In the previous tutorial we created the ``processCcdOutputs`` rerun to isolate the outputs of the :command:`processCcd.py` command line task.
Reruns act like repositories, so to work with the :command:`processCcd.py` outputs we specifically set ``inputs`` as the path to that rerun.

.. tip::

   Reruns are sub-directories of the :file:`rerun` directory of a root Butler data repository.

Listing available dataIds in the Butler
=======================================

To get data from the Butler you need to know two things: the **dataset type** and the **dataId**.

Every dataset stored by the Butler has a well-defined type.
Tasks read specific dataset types and output other specific dataset types.
The :command:`processCcd.py` command reads in ``raw`` datasets and outputs ``calexp``, or *calibrated exposure*, datasets (among others).
It's ``calexp`` datasets that we will display in this tutorial.

DataIds let us reference specific instances of a dataset.
On the command line we set dataIds with ``--id`` arguments, filtering by keys like ``visit``, ``ccd``, and ``filter``.

Let's use the Butler client to find what dataIds are available for the ``calexp`` dataset type:

.. code-block:: python

   butler.queryMetadata('calexp', ['visit', 'ccd'], dataId={'filter': 'HSC-R'})   

The printed output is a list of ``(visit, ccd)`` key tuples for all dataIds where the ``filter`` key is the ``HSC-R`` band:

.. code-block:: text

   [(903334, 16),
    (903334, 22),
    (903334, 23),
    (903334, 100),
    (903336, 17),
    (903336, 24),
    (903338, 18),
    (903338, 25),
    (903342, 4),
    (903342, 10),
    (903342, 100),
    (903344, 0),
    (903344, 5),
    (903344, 11),
    (903346, 1),
    (903346, 6),
    (903346, 12)]

.. note::

   The example ``butler.queryMetadata`` call is equivalent to this shell command that we used in the :doc:`previous tutorial <processccd>`:

   .. code-block:: bash

      processCcd.py DATA --rerun processCcdOutputs --id filter=HSC-R --show data

Get an exposure through the Butler
==================================

Knowing a specific dataId, let's get the dataset with the Butler client's ``get`` method:

.. code-block:: python

   calexp = butler.get('calexp', dataId={'filter': 'HSC-R', 'visit': 903334, 'ccd': 23})

This ``calexp`` is an ``ExposureF`` Python object.
Exposures are powerful representations of image data because they contain not only the image data, but also a variance image for uncertainty propagation, a bit mask image plane, and key-value metadata.
In the next steps we'll learn how to display an Exposure's image and mask.

Create a display
================

To display the ``calexp`` we will use the display framework, which is imported as:

.. code-block:: python

   import lsst.afw.display as afwDisplay

The display framework provides a uniform API for multiple display backends, including DS9_ and LSST's Firefly viewer.
For this tutorial we'll create a display with the ``ds9`` backend:

.. code-block:: python

   display = afwDisplay.getDisplay(backend='ds9')

Display the calexp (calibrated exposure)
========================================

Then use the display's ``mtv`` method to view the ``calexp`` in DS9:

.. code-block:: python

   display.mtv(calexp)

As soon as you execute the command a single Hyper Suprime-Cam calibrated exposure, the ``{'filter': 'HSC-R', 'visit': 903334, 'ccd': 23}`` dataId, should appear in the DS9 application.

Notice that the DS9 display is filled with colorful regions.
These are mask regions.
Each color reflects a different mask bit that correspond to detections and different types of detector artifacts.
We'll see how to interpret these colors :ref:`later <getting-started-display-mask-colors>`, but first you'll likely want to adjust the image display.

Improving the image display
===========================

The display framework gives you control over the image display to help bring out image details.

To make masked regions semi-transparent, so that underlying image features are visible, try:

.. code-block:: python

   display.setMaskTransparency(60)

The ``setMaskTransparency`` method's argument can range from ``0`` (fully opaque) to ``100`` (fully transparent).

You can also control the colorbar scaling algorithm with the display's ``scale`` method.
Try an ``asinh`` stretch with the ``zscale`` algorithm for automatically selecting the white and black points:

.. code-block:: python

   display.scale("asinh", "zscale")

Instead of an automatic algorithm like zscale (or ``minmax``) you can explicitly provide both a minimum (black) and maximum (white) value:

.. code-block:: python

   display.scale("asinh", -1, 30)

.. _getting-started-display-mask-colors:

Interpreting displayed mask colors
==================================

The display framework renders each plane of the mask in a different color (*plane* being a different bit in the mask).
To interpret these colors you can get a dictionary of mask planes from the ``calexp`` and query the display for the colors it rendered each mask plane with.
Run:

.. code-block:: python

   for maskName, maskBit in mask.getMaskPlaneDict().items():
       print('{}: {}'.format(maskName, display.getMaskPlaneColor(maskName)))

As an example, this result is:

.. code-block:: text

   DETECTED_NEGATIVE: cyan
   CROSSTALK: None
   INTRP: green
   DETECTED: blue
   UNMASKEDNAN: None
   NO_DATA: orange
   BAD: red
   EDGE: yellow
   SUSPECT: yellow
   NOT_DEBLENDED: None
   CR: magenta
   SAT: green

Footprints of detected sources are rendered in blue and the saturated cores of bright stars are drawn in green.

.. tip::

   Try customizing the color of a mask plane with the ``Display.setMaskPlaneColor`` method.
   You can choose any `X11 color`_.
   For example:

   .. code-block:: python

      display.setMaskPlaneColor('DETECTED', 'dodgerblue')
      display.mtv(calexp)

Getting the source catalog generated by processCcd.py
=====================================================

Besides the calibrated exposure (``calexp``), :command:`processCcd.py` also creates a table of the sources it used for PSF estimation as well as astrometric and photometric calibration.
The dataset type of this table is ``src``, which you can get from the Butler:

.. code-block:: python

   src = butler.get('src', dataId={'filter': 'HSC-R', 'visit': 903334, 'ccd': 23})

This ``src`` dataset is a ``SourceTable``, which is a table object from the ``lsst.afw.table`` module.

We'll explore ``SourceTable``\ s more in a later tutorial, but you can check its length with Python's `len` function:

.. code-block:: python

   print(len(src))

The columns of a table are defined in its schema.
You can print out the schema to see each column's name, data type, and description:

.. code-block:: python

   print(src.getSchema())

To get just the names of columns, run:

.. code-block:: python

   print(src.getSchema().getNames())

Given a name, you can get a column's values as a familiar Numpy array like this:

.. code-block:: python

   print(src['base_PsfFlux_flux'])

.. tip::

   If you are working in a Jupyter notebook you can see an HTML table rendering of any ``lsst.afw.table`` table object by getting an `astropy.table.Table`_ version of it:

   .. code-block:: python

      src.asAstropy()

   The returned Astropy Table is a view, not a copy, so it doesn't waste memory.

Plotting sources on the display
===============================

Now let's overplot sources from the ``src`` table onto the image display using the ``Display``\ ’s ``dot`` method for plotting markers.
``Display.dot`` plots markers individually, so we iterate iterate over rows in the ``SourceTable`` as usual.
It's more efficient to send a batch of updates to the display, though, so we'll enclose the loop in a ``display.Buffering`` context, like this:

.. code-block:: python

   with display.Buffering():
       for s in src:
           display.dot("o", s.getX(), s.getY(), size=10, ctype='orange')

Now orange circles should appear in the DS9 window over every detected source.

.. note::

   Notice the ``getX`` and ``getY`` methods for getting the (x,y) centroid of each source.
   These methods are shortcuts, using the table's *slot* system, to preferred columns for a source's centroid.
   Because the the ``src`` catalog contains measurements from several measurement plugins, slots are a way of easily using the pre-configured best measurements of a source.

Clearing markers
================

``Display.dot`` always adds new markers to the display.
To clear the display of all markers at any point, use the ``erase`` method:

.. code-block:: python

   display.erase()

Selecting PSF-fitting sources to plot on the display
====================================================

Now lets be more purposeful and use the display to understand what sources were used for PSF measurement.

The ``src`` table's ``calib_psfUsed`` column describes whether the source was used for PSF measurement.
Since columns are Numpy arrays we can iterate over rows where ``src['calib_psfUsed'] == True`` with Numpy's boolean array indexing:

.. code-block:: python

   with display.Buffering():
       for s in src[src['calib_psfUsed'] == True]:
           display.dot("x", s.getX(), s.getY(), size=10, ctype='red')

Red **x** symbols on the display mark all stars used by PSF measurement.

Some sources might be considered as PSF candidates, but later rejected.
In this statement we use a logical ``&`` (and) operator to combine boolean index arrays where both ``src['calib_psfCandidate'] == True`` and ``src['calib_psfUsed'] == False`` as well:

.. code-block:: python

   rejectedPsfSources = src[(src['calib_psfCandidate'] == True) &
                            (src['calib_psfUsed'] == False)]
   with display.Buffering():
       for s in rejectedPsfSources:
           display.dot("+", s.getX(), s.getY(), size=10, ctype='green')

Now all green plus (**+**) symbols on the display mark rejected PSF measurement sources.

The display framework, as we've seen, is a useful facility for inspecting images and tables.
This tutorial only covered the framework's basic functionality.
Explore the display framework documentation to learn how to display multiple images at once, and to work with different display backends.

Next up
=======

Continue this tutorial series in :doc:`part 4, where we'll coadd these processed images <coaddition>` into deeper mosaics.

.. _`DS9 image viewer`:
.. _`DS9`: http://ds9.si.edu/site/Home.html
.. _`download and install the DS9 image viewer`: http://ds9.si.edu/site/Download.html
.. _`IPython shell`: http://ipython.readthedocs.io/en/stable/
.. _`Jupyter Notebook`: http://jupyter-notebook.readthedocs.io/en/latest/
.. _`X11 color`: https://en.wikipedia.org/wiki/X11_color_names
.. _`astropy.table.Table`: http://docs.astropy.org/en/stable/table/index.html
