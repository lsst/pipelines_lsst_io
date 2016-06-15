..
  Template for release notes

  dot dot _release-vNN-N:

  Cycle 20XY Release (vNN_N)
  ==========================
  
  +---------------------------------------------+------------+
  | Source                                      | Identifier |
  +=============================================+============+
  | Git tag                                     | 11.0       |
  +---------------------------------------------+------------+
  | :doc:`EUPS distrib <../install/newinstall>` | v11\_0     |
  +---------------------------------------------+------------+
  
  *See also:*

  - :doc:`Installation instructions <../install/index>`
  - :doc:`Known issues <known-issues>`
  - :doc:`Measurements & Characterization <metrics/v11_0/index>`
  - `Qserv release notes <https://confluence.lsstcorp.org/display/DM/Summer+2015+Qserv+Release>`_
  - `Webserv release notes <https://confluence.lsstcorp.org/display/DM/Summer+2015+WebServ+Release>`_
  - `Science User Interface release notes <https://confluence.lsstcorp.org/pages/viewpage.action?pageId=41785820>`_

  .. Note: delete the known issues and install links from older versions.

  .. Note: Use :jirab:`DM-NNNN` to link to tickets.

  dot dot _release-vNN-N-major-changes:

  Major Functionality and Interface Changes
  -----------------------------------------

  ...

  dot dot _release-vNN-N-bug-fixes:

  Bug Fixes
  ---------

  ...

  dot dot _release-vNN-N-internal-improvements:

  Build and Code Improvements
  ---------------------------

  ...

#############
Release Notes
#############

- :ref:`release-v12-0` --- current
- :ref:`release-v11-0`

.. _release-v12-0:

Winter 2016 & X2016 Release (v12_0)
===================================

+---------------------------------------------+------------+
| Source                                      | Identifier |
+=============================================+============+
| Git tag                                     | 12.0       |
+---------------------------------------------+------------+
| :doc:`EUPS distrib <../install/newinstall>` | v12\_0     |
+---------------------------------------------+------------+

- :ref:`release-v12-0-major-changes`
- :ref:`release-v12-0-bug-fixes`
- :ref:`release-v12-0-internal-improvements`

*See also:*

- :doc:`Installation instructions <../install/index>`
- :doc:`Known issues <known-issues>`

.. - :doc:`Measurements & Characterization <metrics/v11_0/index>`

.. _release-v12-0-major-changes:

Major Functionality and Interface Changes
-----------------------------------------

- :ref:`release-v12-0-mask-planes-before-coaddition`
- :ref:`release-v12-0-dumping-task-config-params-includes-docs`
- :ref:`release-v12-0-clean-up-interpolation-tasks`
- :ref:`release-v12-0-avoid-io-race-config-writes`
- :ref:`release-v12-0-safeclipassemblecoaddtask`
- :ref:`release-v12-0-reserve-psf-candidates-from-fitting`
- :ref:`release-v12-0-update-pipeline-config`
- :ref:`release-v12-0-vignetting-polygons`
- :ref:`release-v12-0-rerun`
- :ref:`release-v12-0-fakes`
- :ref:`release-v12-0-tract-routines`
- :ref:`release-v12-0-xytransform`
- :ref:`release-v12-0-getcoordsystem`
- :ref:`release-v12-0-jointmatchlistwithcatalog`
- :ref:`release-v12-0-visualize-skymaps`
- :ref:`release-v12-0-unpacked-matches`
- :ref:`release-v12-0-focal-plane-coords`
- :ref:`release-v12-0-jacobian-position-src`
- :ref:`release-v12-0-record-images-contributing-to-coadds`
- :ref:`release-v12-0-variance-at-source`
- :ref:`release-v12-0-source-flux-in-ap`
- :ref:`release-v12-0-blendedness`
- :ref:`release-v12-0-simple-shape-meas`
- :ref:`release-v12-0-mirata-seljak-mandelbaum`
- :ref:`release-v12-0-interp-background`
- :ref:`release-v12-0-averagecoord`
- :ref:`release-v12-0-hsc-support`
- :ref:`release-v12-0-psf-shapelet`
- :ref:`release-v12-0-propagate-flags-to-coadds`
- :ref:`release-v12-0-apcorr-coadd-meas`
- :ref:`release-v12-0-grown-footprints`
- :ref:`release-v12-0-meas-sky-objs`
- :ref:`release-v12-0-specify-output-dir`
- :ref:`release-v12-0-bright-object-masks`
- :ref:`release-v12-0-cmodel-improvements`
- :ref:`release-v12-0-astropy-table-views`
- :ref:`release-v12-0-afterburner-measurements`
- :ref:`release-v12-0-task-registry`
- :ref:`release-v12-0-afw-test-utilities`
- :ref:`release-v12-0-non-linearity-corrections`
- :ref:`release-v12-0-amplifier-catalogs`
- :ref:`release-v12-0-background-subtraction`
- :ref:`release-v12-0-star-selectors`
- :ref:`release-v12-0-processccdtask`

.. _release-v12-0-mask-planes-before-coaddition:

Add the option of excluding mask planes before coaddition
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The user-configurable parameter ``removeMaskPlanes`` has been added to :lclass:`AssembleCoaddConfig`.
This is a list of mask planes which will not be propagated to the coadd; by default, the ``CROSSTALK`` and ``NOT_DEBLENDED`` mask planes are removed.
:jirab:`DM-4866`

.. _release-v12-0-dumping-task-config-params-includes-docs:

Dumping task configuration parameters now includes documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

That is, running ``${TASK} ... --show config`` displays not only the names and values of the configuration but also associated documentation.
:jirab:`DM-3811`

.. _release-v12-0-clean-up-interpolation-tasks:

Clean up interpolation tasks and implement useFallbackValueAtEdge
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``interpImageTask`` in pipe_tasks has been refactored to implement a single run function for interpolation over a list of defects in an image. 
This run function will accept an :lmod:`afw` image type of either :lclass:`MaskedImage` or :lclass:`Exposure`.
A defects list can be passed in directly *or* the name of mask plane can be passed from which a defects list will be created.
If a PSF is attached to the image, it will be used as the (required) argument for the :lfunc:`interpolateoverDefects` function in ``meas_algorithms`` used for the interpolation.
Otherwise a FWHM (in pixels) can be provided or the ``defaultFWHM`` value in ``meas_algorithms``\ ' :lclass:`GaussianFactory` is used.
Note that while the PSF is a required argument for ``meas_algorithms``\ ' :lfunc:`interpolateOverDefects` function it is currently not being used, so it is not necessary to pass in an accurate PSF.

The ``useFallbackValueAtEdge`` option is now implemented.
This tapers the interpolation to a ``fallbackValue`` towards the image edge.
The ``fallbackValue`` can be set via config parameters to be either computed as a statistical representation of the image data (``MEAN``, ``MEDIAN``, or ``MEANCLIP``) or set by providing a specific value.
Allowance for a negative ``fallbackValue`` is also controlled though a config parameter.

:jirab:`DM-3677`

.. _release-v12-0-avoid-io-race-config-writes:

HSC backport: Avoid I/O race conditions config write out
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This adds functionality to avoid potential I/O race conditions when running multiple simultaneous process.
This is accomplished by writing to temporary files and then renaming them to the correct destination filename in a single operation.
Also, to avoid similar race conditions in the backup file creation (e.g. :file:`config.py~1`, :file:`config.py~2`, …), a ``--no-backup-config`` option (to be used with ``--clobber-config``) is added here to prevent the backup copies being made.
The outcome for this option is that the config that are still recorded are for the most recent run.
:jirab:`DM-3911`

.. _release-v12-0-safeclipassemblecoaddtask:

HSC backport: Introduce SafeClipAssembleCoaddTask which extends AssembleCoaddTask to make clipping safer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:lclass:`SafeClipAssembleCoaddTask` does the following, 

- build both clipped and unclipped coadds and difference them first
- detect on the difference
- identify difference footprints that overlap appreciably with only one input image
- use identified difference footprints as a mask into a final coadd
- set a "clipped" bit on the final coadd for any pixel that did not include all input frames within the valid polygons.

To support the new coadd task, the pixel flags measurement plugin has been modified to accept two new configuration parameters.
These new parameters, named ``masksFpCenter`` and ``masksFpAnywhere``, each accept a list of mask planes.
When the pixel flags measurement plugin searches for mask planes to set corresponding flags, it will now additionally search the user supplied mask plane lists.
The ``masksFpCenter`` parameter specifies mask planes that, if found within the center of a footprint, will have a corresponding pixel flag set.
The ``masksFpCenter`` parameter specifies mask planes that, if found anywhere in a footprint, will have a corresponding pixel flag set.
The ``masksFpAnywhere`` parameter now has it's defaults set within the stack which specify the clipped mask plane created by :lclass:`SafeClipAssembleCoaddTask`.

:lclass:`SafeClipAssebleCoaddTask` is now the default method for building a coadd within the LSST Stack.
The :command:`assembleCoadd.py` :lclass:`CommandLineTask` now supports the ``--legacy`` command line flag which will allow the original :lclass:`AssembleCoaddTask` to be run.
If the legacy task is run, the clipped mask plane must be removed from the ``masksFpAnywhere`` configuration parameter.

:jirab:`DM-2915`

.. _release-v12-0-reserve-psf-candidates-from-fitting:

HSC backport: Allow for some fraction of PSF Candidates to be reserved from PSF fitting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This adds functionality that allows for the reservation of a fraction of the PSF Candidates from PSF fitting.
The reserved fraction can then be used to test for over-fitting, do cross-validation, etc..
To support this functionality, the run methods of :lclass:`CalibrateTask` and :lclass:`MeasurePsfTask` now accept the additional keyword argument ``expId``.
Dummy versions of this keyword were added to the :lclass:`SdssCalibrateTask` and :lclass:`CfhtCalibrateTask` to maintain a consistent API.
:jirab:`DM-3692`

.. _release-v12-0-update-pipeline-config:

Updated pipeline configuration based on Hyper Suprime-Cam experience
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Configuration defaults and metadata through the LSST single-processing pipeline have been updated to match the current best practice established on HSC.
Major changes include:

- Support for narrow band filters;
- Updated CCD defect lists;
- Optimized (in terms of CPU time) deblender settings;
- Avoiding failure in certain corner cases (e.g. operating on zero-length arrays, taking log\ :sub:`10` of zero).

:jirab:`DM-3942`

.. _release-v12-0-vignetting-polygons:

Define polygon bounds for CCDs based on vignetted regions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This adds a function in ip_isr's :command:`isrTask.py` to set a "valid polygon" for a given CCD exposure as the intersection of a polygon defined in focal plane coordinates and the CCD corners.
It is currently being used in ``obs_subaru``\ 's :command:`isr.py` to set the polygon bounds (added in :jira:`DM-2981`) for a CCD exposure to include the non-vignetted regions.
The settings for the vignetted region is in a separate config file so that it can be used in different places in the code.
:jirab:`DM-3259`

.. _release-v12-0-rerun:

Introduce ``--rerun`` option for command line tasks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This new command line option streamlines the process of specifying input and output repositories for command line tasks.
In its simplest form, the ``--rerun`` option is a shorthand for specifying an output repository: output is written to a location relative to the input.
Thus

.. code-block:: bash

   CmdLineTask /path/to/inputroot --rerun useroutput

is equivalent to

.. code-block:: bash

   CmdLineTask /path/to/inputroot --output /path/to/inputroot/rerun/useroutput

Often, one task will process the output of a previous rerun.
For this situation, ``--rerun`` provides a two-valued form which specifies relative locations of both input and output.
In this mode,

.. code-block:: bash

   CmdLineTask /path/to/inputroot --rerun process1:useroutput

is equivalent to

.. code-block:: bash

   CmdLineTask /path/to/inputroot --input /path/to/inputroot/rerun/process1 --output /path/to/inputroot/rerun/useroutput

:jirab:`RFC-95,DM-3371`

.. _release-v12-0-fakes:

Introduce framework for injecting fake sources into data processing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A new boolean option (``doFakes``) and a retargetable task (:command:`fakes`) have been introduced into the :lclass:`ProcessCcdTask`.
This (along with a new class called :lclass:`BaseFakeSourcesTask`) sets up a frame work that others may use to introduce known fake sources into the data processing stream.
However, this framework itself does not actually insert any fake data itself, but provides an interface others may use to define their own fake source injection task.
To implement a fake injection task one must create a child class of :lclass:`BaseFakeSourcesTask` (located in :lmod:`lsst.pipe.tasks.fakes`) and overload the run method to do the work of injecting the sources.
Each source that is injected should have a corresponding bit set in the ``FAKE`` maskplane which can be accessed with the ``bitmask`` attribute of :lclass:`BaseFakeSourcesTask`.
Once a task has been created, the config field fakes in :command:`processCcd` must be retargeted to point to the user created task.
Additionally, the task will not be run unless the ``doFakes`` configuration option in :command:`processCcd` is set to ``True``.
However, if this variable is set to ``True``, and the task is not retargeted :command:`processCcd` will fail.
:jirab:`DM-3380`

.. _release-v12-0-tract-routines:

Add convenience routines for working with tracts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Added two new data id containers:

1. :lclass:`PerTractCcdDataIdContainer`: determines the set of tracts each visit touches and adds a data reference with those tracts for each of the visit components.
   This allows for the user to run a command line task :command:`forcedPhotCcd.py` for a given visit without having to know which tracts overlap the visit.
   *Note this will also be used by meas\_mosaic if/when it gets incorporated into the LSST Stack.*

2. :lclass:`TractDataIdContainer`: generates a list of data references for patches within a given tract (effectively a "data reference list" that points to the entire tract).
   *Note that, at the time of writing, this is only being used by a QA analysis script currently under development.*

:jirab:`DM-4373`

.. _release-v12-0-xytransform:

Warp images based on an XYTransform 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Added the ability to warp images using a transformation defined by an :lclass:`lsst::afw::geom::XYTransform`.
:jirab:`DM-4162`

.. _release-v12-0-getcoordsystem:

Add getCoordSystem to Coord and add UNKNOWN CoordSystem enum
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Added method :lmeth:`getCoordSystem` to :lclass:`lsst::afw::coord::Coord`.
Also added ``UNKNOWN=-1`` as a new :class:`CoordSystem` enum (the existing enums retain their existing value).
:lclass:`DM-4606`

.. _release-v12-0-jointmatchlistwithcatalog:

Adapt joinMatchListWithCatalog to facilitate and simplify denormalizing a match list
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The match lists created when performing image calibration (astrometry and photometry) are normalized (i.e. stripped down to a list of the matched reference and source ids and their distance) prior to being persisted.
The ability to denormalize a match catalog is very useful (for post QA analysis, for example).
This can now be done using the :lfunc:`joinMatchListWithCatalog` function in ``meas_algorithms``\ 's :lclass:`LoadReferenceObjectsTask`.
It has been moved from ``meas_astrom``\ 's :lclass:`ANetBasicAstrometryTask` so that it can be easily accessed (requiring only that a reference object loader be initiated) and to allow it to work with any kind of reference catalog (i.e. other than ``a_net``).
:jirab:`DM-3633`

.. _release-v12-0-visualize-skymaps:

Add a script for visualizing skymaps and CCDs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``skymap`` package now contains the script :command:`showVisitSkyMap.py` which provides a convenient way of visualizing the tracts, patches and CCDs contained in a set of visits.
:jirab:`DM-4095`

.. _release-v12-0-unpacked-matches:

Add functions to generate "unpacked matches" to and from a catalog
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Functions have been added to :lmod:`lsst::afw::catalogMatches` to provide the ability to convert a match list into a catalog and vice versa (this can be useful for post-processing analyses; QA analysis, for example).
:jirab:`DM-4729`

.. _release-v12-0-focal-plane-coords:

Add a measurement algorithm which records the focal plane coordinates of sources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :lclass:`SingleFrameFPPositionPlugin` measurement plugin, available in ``meas_base``, records the positions of source centroids in focal plane coordinates (which may be convenient for plotting).
This plugin is not enabled by default, but may be switched on by requesting ``base_FPPosition`` in measurement configuration.
:jirab:`DM-4234`

.. _release-v12-0-jacobian-position-src:

Add a measurement algorithm which records the Jacobian at the positions of sources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :lclass:`SingleFrameJacobianPlugin` calculates the ratio between the nominal Jacobian determinant at the source centroid (as determined by a user-specified pixel scale) and the actual Jacobian determinant as derived from the astrometric solution.
This plugin is not enabled by default, but may be switched on by requesting ``base_Jacobian`` in measurement configuration.
:jirab:`DM-4234`

.. _release-v12-0-record-images-contributing-to-coadds:

Add a measurement algorithm which records the number of input images contributing to a coadd sources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When run on a source detected on a coadd, :lclass:`SingleFrameInputCountPlugin` records the number of input images which were stacked to create the coadd at the position corresponding to the source centroid.
The plugin is referred to as ``base_CountInputs``, and is enabled by default when performing measurement on coadded images.
It is not appropriate to enable this plugin when processing single visit (i.e., not coadded) images.
:jirab:`DM-4235`

.. _release-v12-0-variance-at-source:

Add a measurement algorithm which records the variance at the positions of sources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :lclass:`SingleFrameVariancePlugin` records the median variance in the background around the position of the source being measured.
The plugin is referred to as ``base_Variance`` and is enabled by default when performing single frame measurement.
:jirab:`DM-4235,DM-5427`

.. _release-v12-0-source-flux-in-ap:

Add a measurement algorithm which records source flux in an aperture scaled to the PSF
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :lclass:`ScaledApertureFluxAlgorithm` measures the flux in a circular aperture with radius scaled to some user-specified multiple of the PSF FWHM.
This plugin is not enabled by default, but may be switched on by requesting the ``base_ScaledApertureFlux`` in measurement configuration.
:jirab:`DM-3257`

.. _release-v12-0-blendedness:

Add a measurement algorithm which quantifies the amount of "blendedness" of an object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :lclass:`BlendednessAlgorithm` measures the amount to which an object is blended.
Both the flux and shape of each child object are compared to measurements at the same point on the full image.
The size of the weight function used on both images is determined from the child object.
The blendedness metric implemented is defined as ``1-childFlux/parentFlux``.
The plugin is referred to as ``base_Blendedness`` and is not enabled by default. 
:jirab:`DM-4847`

.. _release-v12-0-simple-shape-meas:

Add a "simple" shape measurement algorithm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :lclass:`SimpleShape` algorithm, provided in the ``meas_extensions_simpleShape`` package, computes the non-adaptive elliptical Gaussian-weighted moments of an image.
The plugin is referred to as ``ext_simpleShape_SimpleShape`` and is not enabled by default.
:jirab:`DM-5284`

.. _release-v12-0-mirata-seljak-mandelbaum:

Add Hirata-Seljak-Mandelbaum shape measurement algorithms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``meas_extensions_shapeHSM`` package has been added to the distribution.
This provides a series of measurement algorithms based on the work by `Hirata and Seljak (2003) <https://ui.adsabs.harvard.edu/#abs/2003MNRAS.343..459H/abstract>`__ and `Mandelbaum et al (2005) <https://ui.adsabs.harvard.edu/#abs/2005MNRAS.361.1287M/abstract>`__.
Please cite those works if publishing results based on this code.
These algorithms are disabled by default; they can be enabled by requesting ``ext_shapeHSM_HsmShapeBj``, ``ext_shapeHSM_HsmShapeLinear``, ``ext_shapeHSM_HsmShapeKsb``, ``ext_shapeHSM_HsmShapeRegauss``, ``ext_shapeHSM_HsmSourceMoments`` and/or ``ext_shapeHSM_HsmPsfMoments`` in the measurement configuration.
:jirab:`DM-2141,DM-3384,DM-4780`

.. _release-v12-0-interp-background:

Add option to temporarily remove an interpolated background prior to detection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This has the potential for removing a large number of junk detections around bright objects due to noise fluctuations in the elevated local background.
The extra subtracted interpolated background is added back in after detection.
Currently, the default setting for the config parameter ``doTempLocalBackround`` is set to ``False``.
:jirab:`DM-4821`

.. _release-v12-0-averagecoord:

Add function to average coordinates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Added function :lfunc:`lsst.afw.coord.averageCoord`, which will return an average coordinate (accounting for spherical geometry) given a list of input coordinates.
:jirab:`DM-4933`

.. _release-v12-0-hsc-support:

Integrate support for Hyper Suprime-Cam
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``obs_subaru`` camera package, which enables the stack to operate on data taken with the Suprime-Cam and Hyper Suprime-Cam instruments on Subaru, has been modernized, resolving build and test issues and integrating it with LSST's continuous integration system.
It will now be included as part of the lsst\_distrib release.
*Note, though, that usage of Suprime-Cam with the stack is unsupported and unmaintained at present.*
:jirab:`DM-3518,DONE DM-4358,DM-5007`

.. _release-v12-0-psf-shapelet:

Reimplement PSF Shapelet approximations for CModel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A new algorithm for computing multi-shapelet approximations (:lclass:`DoubleShapeletPsfApprox`) has been added to ``meas_modelfit``.
This is simpler and more robust than the old algorithm, which has been renamed to :lclass:`GeneralShapeletPsfApprox`.
The new algorithm is recommended for production use, and is now the default.
:jirab:`DM-5197`

.. _release-v12-0-propagate-flags-to-coadds:

Propagate flags from individual visits to coadds
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A task has been added which can propagate flags from individual visit catalogs to coadd catalogs.
This is useful, for example, to track which stars in the coadd were used for measuring PSFs on the individual visits.
:jirab:`DM-4878,DM-5084`

.. _release-v12-0-prototype-bfc:

Prototype Brighter-Fatter correction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Code for correcting for the Brighter-Fatter effect on CCDs is now available in the stack.
It is enabled using the ``doBrighterFatter`` configuration option to :lclass:`IsrTask`.
It requires a pre-generated correction kernel.
Calculation of this kernel is not currently performed within the stack: a prototype exists, and will be merged to the Calibration Products Pipeline in a future cycle.
:jirab:`DM-4837,DM-5082,DM-5130`

.. _release-v12-0-apcorr-coadd-meas:

Aperture correction on coadd measurements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Aperture corrections are now enabled for measurements performed on coadds.
:jirab:`DM-5086`

.. _release-v12-0-grown-footprints:

Return grown Footprints from detection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, :lclass:`Footprints` returned by :lclass:`SourceDetectionTask` are now grown by a multiple of the PSF size.
:jirab:`DM-4410`

.. _release-v12-0-meas-sky-objs:

Enable measurement of "sky objects" in coadd processing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sky objects correspond to source properties measured at positions when no objects have been detected.
This enables us to better characterize the depth of the survey.
This functionality is enabled by default; it can be disabled by setting ``nSkySourcesPerPatch`` to zero in the configuration of :lclass:`MergeDetectionsTask`.
:jirab:`DM-4840,DM-5288`

.. _release-v12-0-specify-output-dir:

Specification of output directory is now mandatory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When running a command line task which produces output it is now mandatory to specify an output directory (previously, if no output location was specified, data products were written back to the input repository).
Output locations may be specified with the ``--rerun`` or ``--output`` command line options.
More information is available on `community.lsst.org <https://community.lsst.org/t/output-directory-soon-required-for-cmdlinetasks/598>`__.
:jirab:`DM-4236`

.. _release-v12-0-bright-object-masks:

Bright object masks
^^^^^^^^^^^^^^^^^^^

Given an input catalog listing the known positions and sizes of bright objects, a bit is set in the mask plane for every pixel lying within the object's footprint.
:jirab:`DM-4831`

.. _release-v12-0-cmodel-improvements:

CModel fitting improvements
^^^^^^^^^^^^^^^^^^^^^^^^^^^

CModel is a model fitting approach in which a pure exponential and pure de Vaucouleur are each fit separately, and then their linear combination is fit while the ellipse parameters are held fixed.
Improvements in this release make CModel fitting faster and improves results on objects which are detected with an unphysically large likelihood radius.
This has been achieved in three ways:

- The initial approximate exponential fit that is used to determine the starting parameters and pixel region to use for the exp and dev fit now uses per-pixel variances;
- The method used to determine the pixel region used in fitting has been adjusted to make smarter choices, using fewer pixels on average for all objects and many fewer pixels for unphysically large objects;
- A new semi-empirical Bayesian prior on radius and ellipticity based on COSMOS distributions has been introduced.

:jirab:`DM-4768`

.. _release-v12-0-astropy-table-views:

Astropy Table views into LSST Catalog objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`Astropy Table <http://docs.astropy.org/en/stable/api/astropy.table.Table.html>`__ views into LSST catalog objects can now be created.
These views share underlying data buffers (aside from flag fields), making them read-write, but rows and columns added on either side will not be visible in the other.
Two equivalent interfaces are available:

.. code-block:: python

   astropy_table = lsst_catalog.asAstropy()

and (in Astropy >= v1.2):

.. code-block:: python

   astropy_table = astropy.table.Table(lsst_catalog)

`QTable <http://docs.astropy.org/en/stable/api/astropy.table.QTable.html>`__ objects can also be used, resulting in columns that use Astropy's `units <http://docs.astropy.org/en/stable/units/>`__ package to enforce unit correctness.
These interfaces have multiple options to control the details of the view, including how to handle columns that require copies; see the Python on-line help for :lmeth:`asAstropy` for more information.

While LSST's catalog objects have features that make them particularly useful in building pipelines, Astropy's are much more appropriate for most analysis tasks, and we strongly recommend using them for any analysis tasks that need to add columns to tables or combine columns from multiple tables.

:jirab:`DM-5641,DM-5642,DM-5643`

.. _release-v12-0-afterburner-measurements:

Add an "afterburner" measurement facility
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This new functionality makes it possible to register plugins to calculate quantities based on the results of pixel measurement algorithms.
This might include, for example, star-galaxy separation or applying aperture corrections.
Afterburners of this type are run after measurement plugins, and do not have access to pixel data.
:jirab:`DM-4887`

.. _release-v12-0-task-registry:

Tasks can now be kept in registries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. https://community.lsst.org/t/tasks-can-now-be-kept-in-registries/839

Related sets of tasks should now be kept in a registry as per :jira:`RFC-183`, with a common abstract base class.

Tasks can now use an :lclass:`lsst.pex.config.RegistryField` config field to specify a subtask if that subtask is in a registry :jirap:`DM-6074`.
The task is built and used the same way as if it was specified in an :lclass:`lsst.pex.config.ConfigurableField`, but retargeting and overriding config parameters is different.
See `task documentation <http://lsst-web.ncsa.illinois.edu/doxygen/x_masterDoxyDoc/pipe_base.html>`__ for more information.
See also `How to Write a Task <http://lsst-web.ncsa.illinois.edu/doxygen/x_masterDoxyDoc/pipe_tasks_write_task.html>`__ for guidelines for choosing between using :lclass:`lsst.pex.config.RegistryField` and :lclass:`lsst.pex.config.ConfigurableField` to hold a subtask.

PSF determiners are now tasks that inherit from an abstract base class :lclass:`lsst.meas.algorithms.PsfDeterminerTask` :jirap:`DM-6077`.
However, the effect on existing code was negligible because they were already configurables used from a registry.
The way you retarget PSF determiners and override their config parameters remains unchanged.

Reimplemented the registry for star selectors that was lost in :jira:`DM-5532`: :lclass:`lsst.meas.algorithms.starSelectorRegistry` :jirap:`DM-6474` 

One backwards incompatible change: in :jirab:`DM-6474` :lclass:`MeasurePsfTask` and :lclass:`MeasureApCorrTask` both now specify their star selectors using an :lclass:`lsst.pex.config.RegistryField`.
This means the format for retargeting star selectors and overriding their config parameters has changed.
The config override files in the various ``obs_`` packages are updated accordingly.

.. _release-v12-0-afw-test-utilities:

New test utilities in afw: BoxGrid and makeRampImage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. https://community.lsst.org/t/new-test-utilities-in-afw-boxgrid-and-makerampimage/837

:lclass:`lsst.afw.geom.testUtils.BoxGrid` divides a bounding box into ``nCol x nRow`` equal sized sub-boxes (as equal sized as possible for integer boxes that do not divide evenly) that tile the larger box and have the same type.

:lfunc:`lsst.afw.image.testUtils.makeRampImage` makes an image (``ImageX`` where ``X`` is any available type) with values that increase linearly between specified limits (linearly to the extent possible, for integer images).

:jirab:`DM-5462`

.. _release-v12-0-non-linearity-corrections:

Correcting non-linearity
^^^^^^^^^^^^^^^^^^^^^^^^

.. https://community.lsst.org/t/correcting-non-linearity/816

Introduced a standard way to correct non-linearity (linearize data) as part of Instrument Signature Removal (ISR).
Linearization is performed by new functors in ``ip_isr``:

- :lclass:`LinearizeBase` is an abstract base class.
  It is called with an image and the detector information and the correction is performed in place (like all other ISR corrections in :lclass:`IsrTask`).
- :lclass:`LinearizeSquared` performs a simple square correction: ``corrImage = uncorrImage + c0*uncorrImage^2`` where ``c0`` is the first coefficient in in the linearity coefficients of the amp into catalog.
  This is the model used by ``obs_subaru`` for SuprimeCam and HSC.
- :lclass:`LinearizeLookupTable` uses a lookup table to determine an offset (read the code doc string for details).
  The lookup table is saved with the linearizer, but the linearizer also performs a sanity check against the provided detector when called.
- You can easily add other linearizers as desired.
- Each linearizer has a class variable ``LinearizationType``, a string whose value should be used as the linearization type in the amplifier info catalog.
  The linearizer checks this value when performing linearization.

All detector in a camera must use the same type of linearizer.
However linearization can easily be disabled on a detector-by-detector basis by setting linearity type to :lclass:`lsst.afw.cameraGeom.NullLinearityType`.
For a camera that does not need linearization, do this for all detectors.

Linearizers are obtained from the butler, like any other calibration product.

- For :lclass:`LinearizeSquared` and other linearizers that get coefficients from the amplifier info catalog, only one instance is needed for all detectors.
  In that case the simplest technique is to define :lmeth:`map_linearize` and :lmeth:`bypass_linearize` methods on the camera mapper to return an instance.
  See the ``obs_subaru`` package for an example.
- For :lclass:`LinearizeLookupTable` and other linearizers that store detector-specific data, the ``obs_`` package developer must pickle one linearizer for each detector and make them available as dataset type "linearizer".
- If the camera does not want linearization then no "linearizer" dataset type is required because :lclass:`IsrTask` realizes linearization is not wanted before it tries to unpersist the linearizer.
  You may leave ``IsrConfig.doLinearize`` set to its default value of ``True`` without significant performance penalty.

:jirab:`DM-5462,RFC-164`

.. _release-v12-0-amplifier-catalogs:

Amplifier information catalogs have changed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. https://community.lsst.org/t/amplifier-information-catalogs-have-changed/801

The format of amplifier information catalogs has changed.
**Your versions of afw and associated obs_ packages must be compatible** or else you will get errors when building a camera mapper (thus when running any nearly any command-line task).

Amplifier information catalogs have a new field as of :jira:`DM-6147`: suspect level.
If the value is not ``nan`` then pixels whose values are above this level are masked as ``SUSPECT``.

The only cameras that specify a suspect level, so far, are HSC and SuprimeCam.
However, a value can be set for any camera, if desired.
``SUSPECT`` is intended to indicate pixels with doubtful values due to  errors that are difficult to correct accurately, e.g. a regime where linearity correction is not very stable.

In addition, saturation level in the amplifier information catalog is now a floating point value (instead of an integer) and a value of ``nan`` means 'do not mask pixels as SAT.'

:jirab:`DM-6147`

.. _release-v12-0-background-subtraction:

Changes in how background subtraction is done
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. https://community.lsst.org/t/changes-in-how-background-subtraction-is-done/756

Background estimation in Python is now done using different routines in ``meas_algorithms``.

There is a new task :lclass:`SubtractBackgroundTask`, with full documentation and a working example.

The existing function :lfunc:`getBackground` (which fits a background) is replaced by :lmeth:`SubtractBackgroundTask.fitBackground`.
Changes from :lfunc:`getBackground` are:

- :lmeth:`getBackground` could return ``None`` if the fit failed; in that situation :lmeth:`fitBackround` will raise :exc:`RuntimeError` instead of returning ``None``.
- The argument ``image`` was renamed to ``maskedImage``, for clarity.
- The config is not passed as an argument.
- The debug display code uses different keys and is updated to use :lmod:`afw.display`.

The existing function :lfunc:`estimateBackground` (which subtract a background from an exposure) is replaced by :lmeth:`SubtractBackgroundTask.run`.
Changes from :lfunc:`estimateBackground` are:

- You may pass in a background model (an :lclass:`lsst.afw.math.BackgroundList`).
- It returns a struct containing the updated background model.
- The config is not passed as an argument.
- The debug display code displays the unsubtracted image and uses different keys and is updated to use :lmeth:`afw.display`.

The task's config :lclass:`SubtractBackgroundConfig` replaces the old :lclass:`BackgroundConfig`.
The field ``algorithm`` may no longer be ``None``; you must use the string ``"NONE"``, instead.
See `discussion on Community <https://community.lsst.org/t/changes-in-how-background-subtraction-is-done/756/3>`__ for details.

:jirab:`DM-5323,RFC-155`

.. _release-v12-0-star-selectors:

Star selectors have changed
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. https://community.lsst.org/t/star-selectors-have-changed/639

Star selectors are now tasks.
They were already configurable and many added logs; now they are standard tasks.

The star selector registry ``starSelectorRegistry`` was gone for awhile.
Now that it is back, using a registry field from that registry is the preferred way to specify a star selector as a subtask of another task.

Added :lclass:`BaseStarSelectorTask` (but for awhile it was called :lclass:`StarSelectorTask`) an abstract base class for star selectors with the following methods:

- :lmeth:`selectStars` an abstract method that takes a catalog of sources and returns a catalog of stars.
- :lmeth:`makePsfCandidates` a concrete method that takes a catalog of stars (as returned by `selectStars` and produces PSF candidates; it also returns a sub-catalog of those stars that were successfully turned into PSF candidates (which is usually all of them).
- :lmeth:`run` a concrete method that selects stars, makes them into PSF candidates and optionally flags the stars.

:jirab:`RFC-154,DM-5532`

.. _release-v12-0-processccdtask:

Backward-incompatible changes to ProcessCcdTask and subtasks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. https://community.lsst.org/t/backward-incompatible-changes-to-processccdtask-and-subtasks/581

Code changes
""""""""""""

- :lclass:`ProcessCoaddTask` is gone, along with all bin scripts that run it.
  Use the new `Multi-Band <https://confluence.lsstcorp.org/display/DM/S15+Multi-Band+Coadd+Processing+Prototype>`__ code, instead.
- :class:`ProcessCcdTask` has been rewritten, so its config has changed.
  Config override files will need to be updated.
  This will be done for the ``obs_`` packages as part of the merge, but if you have personal config override files then you will probably need to update them.
- Camera-specific variants of :lclass:`ProcessCcdTask`.
  You will run :command:`processCcdTask.py` to process images for all cameras.
- For DECam :command:`processCcdTask.py` will use the LSST Stack's ISR by default.
  To read ``instcal`` files from the DECam Community Pipeline, replace the ISR task with ``DecamNullIsrTask`` by using a config override file containing the following:

  .. code-block:: python

     from lsst.obs.decam.decamNullIsr import DecamNullIsrTask
     config.isr.retarget(DecamNullIsrTask)

- A new dynamic dataset type is available for adding data ID arguments to the argument parser for command-line tasks: :lclass:`ConfigDatasetType` obtains the dataset type from a config parameter.
- Various subtasks have changed, including:

  - New camera-specific ISR task variants for SDSS and DECam: :lclass:`SdssNullIsrTask` and :lclass:`DecamNullIsrTask`.
  - New task :lclass:`DetectAndMeasureTask` detects and deblends sources and performs single-frame measurement.
  - New task :lclass:`CharacterizeImageTask` measures PSF and aperture correction, among other things.
  - :lclass:`CalibrateTask` has been rewritten.
    It now performs deep detection and measurement, astrometry and photometry.
  - Camera-specific variants of :lclass:`CalibrateTask` are gone.
  - :lclass:`ProcessImageTask` (formerly a base class for :lclass:`ProcessCcdTask` and :lclass:`ProcessCoaddTask`) is gone.

Data product changes
""""""""""""""""""""

- ``icSrc`` no longer includes RA/Dec coordinate data, because the fit WCS is not available when the catalog is constructed.
  You will have to set the coord field yourself if you need it.
- ``icExp`` and ``icExpBackground`` can optionally be written by :lclass:`CharacterizeImageTask`.
  They are so close to ``calexp`` and ``calexpBackground`` that they are not written by default.
- ``icMatch`` is no longer being written.

Algorithm changes
"""""""""""""""""

- PSF is fit somewhat differently.
  The new task fits the PSF in using a configurable number of iterations.
  By default each iteration starts with a simple Gaussian PSF whose sigma matches the PSF of the previous fit, but you can use the actual PSF each time.
  Using a Gaussian causes convergence in 2 iterations. Using the fit PSF slows convergence.
- Sources in the ``icSrc`` catalog should have a more consistent minimum SNR for varying seeing.
  The old code detected once, using a Gaussian PSF with FWHM set by a config parameter.
  The new code performs detection using the PSF in the final PSF iteration.
- The default star selector for ``MeasurePsfTask`` is ``objectSize`` rather than ``sizeMagnitude``.
  The ``objectSize`` star selector is preferred and was already being specified as an override by HSC.
- The icSrc catalog is not matched to an astrometric reference catalog unless the star selector used to measure PSF can use the matches (which is unusual).
- The astrometric and photometric solution now use the deeper ``src`` catalog instead of the shallower ``icSrc`` catalog, though with a new SNR cutoff whose default provides a depth similar to the ``icSrc`` catalog.
- Fake source handling is temporarily missing; it will be re-added in :jira:`DM-5310`.

:jirab:`DM-4692,DM-5348`

.. _release-v12-0-bug-fixes:

Bug Fixes
---------

- :ref:`release-v12-0-persist-ltvn-header`
- :ref:`release-v12-0-identifying-peaks-in-merge`
- :ref:`release-v12-0-getchildren`
- :ref:`release-v12-0-warping-wcs-diff-systems`
- :ref:`release-v12-0-mininitialradius`
- :ref:`release-v12-0-fix-cmodel-math`
- :ref:`release-v12-0-dipole-centroid-slot`
- :ref:`release-v12-0-example-updates`
- :ref:`release-v12-0-log-task-failures`
- :ref:`release-v12-0-skymap`
- :ref:`release-v12-0-coadd-variance`
- :ref:`release-v12-0-deblended-variance`
- :ref:`release-v12-0-apcorr-logic`
- :ref:`release-v12-0-catalog-columns`
- :ref:`release-v12-0-wcslib`
- :ref:`release-v12-0-obs-subaru-rotation`
- :ref:`release-v12-0-conf-overrides-failure`
- :ref:`release-v12-0-sdssshape-flags`
- :ref:`release-v12-0-contant-background-interpolation`
- :ref:`release-v12-0-filter-fallback-message`
- :ref:`release-v12-0-pixel-padding`

.. _release-v12-0-persist-ltvn-header:

Persist LTVn headers as floating point numbers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When persisting to a FITS file, these header cards were previously, incorrectly, stored as integers.
:jirab:`DM-4133`

.. _release-v12-0-identifying-peaks-in-merge:

Fix bug when identifying existing peaks in a merge
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If two separate footprints from the same catalog are merged due to an existing merged object which overlaps both of them the flags of which peaks are being detected were not being propagated.
This issue caused apparent dropouts of sources and has now been fixed.
:jirab:`DM-2978`

.. _release-v12-0-getchildren:

Fix situation in which the getChildren method of SourceCatalog may return the wrong information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :lmeth:`getChildren` method requires that the result must be sorted by parent.
This is naturally the case when the catalog is produced by detection or deblending tasks.
However, if multiple catalogs are concatenated together this condition may no longer be true.
The :lmeth:`getChildren` method was updated to raise an exception if the precondition of sorting is not met.
:jirab:`DM-2976`

.. _release-v12-0-warping-wcs-diff-systems:

Fix warping when the WCS have different coordinate systems
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Warping assumed that the sky representation of both WCS was identical.
:jirab:`DM-4162`

.. _release-v12-0-mininitialradius:

Correct bad default minInitialRadius for CModel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``minInitialRadius`` configuration parameter had a default that is too small, causing many galaxies to be fit with point source models, leading to bad star/galaxy classifications.
:jirab:`DM-3821`

.. _release-v12-0-fix-cmodel-math:

Correct algebraic error in CModel uncertainty calculation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There was a simple but important algebra error in the uncertainty calculation, making the uncertainty a strong function of magnitude.
:jirab:`DM-3821`

.. _release-v12-0-dipole-centroid-slot:

NaiveDipoleCentroid and NaiveDipoleFlux algorithms no longer require a centroid slot
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Previously, initializing these algorithms was only possible if a centroid was already defined.
That was not only unnecessary, but also made them more complicated to use, particularly in testing.
:jirab:`DM-3940`

.. _release-v12-0-example-updates:

Update (some) example code to run with recent stack versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Changes in :lmod:`afw::table` had broken :file:`examples/calibrateTask.py` in ``pipe_tasks``.
It has now been updated to comply with the latest :lmod:`afw::table` API.
:jirab:`DM-4125`

.. _release-v12-0-log-task-failures:

Fix a failure to appropriately log failed task execution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When task execution fails, we add a message to the log (with level ``FATAL``).
In some cases, the very act of attempting to log this message could throw an exception, and information about the original error was lost.
This has now been resolved.
:jirab:`DM-4218`

.. _release-v12-0-skymap:

Updates to Skymap packages
^^^^^^^^^^^^^^^^^^^^^^^^^^

Add functions to return patches and tracts which contain given coordinates, i.e. conversions between celestial coordinates and ``tract,patch`` indices.
Functions include :lfunc:`findClosestTractPatchList`, :lfunc:`findAllTract`, and :lfunc:`findTractPatchList` which finds the closets tract and patch that overlaps coordinates, finds all tracts which include the specified coordinate, and finds tracts and patches that overlap a region respectively.
:jirab:`DM-3775`

.. _release-v12-0-coadd-variance:

Fix variance in coadded images
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Warping images in order to coadd them loses variance into covariance.
This is mitigated by scaling the variance plane of the coadd.
The scaling was being applied incorrectly in some cases.
This has now been fixed.
:jirab:`DM-4798`

.. _release-v12-0-deblended-variance:

Fix variance in deblended sources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The deblender incorrectly scaled the variance plane in deblended sources with the fraction of the total flux assigned to the source.
This has been corrected.
:jirab:`DM-4845`

.. _release-v12-0-apcorr-logic:

Fix logic for applying aperture corrections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This fixes a bug whereby the aperture corrections were being applied only after all the measurement plugins had run through, independent of their execution order.
This resulted in plugins whose measurements rely on aperture corrected fluxes (i.e. with execution order > ``APCORR_ORDER``) being applied prior to the aperture correction, leading to erroneous results.
The only plugin that was affected by this at this time was ``base_ClassificationExtendedness``.
:jirab:`DM-4836`

.. _release-v12-0-catalog-columns:

More uniform support for assigning to catalog columns
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Assignment of scalars or NumPy arrays to columns of afw.table.Catalog objects (e.g. ``catalog["column"] = value``) is now more uniformly supported across types (support was inconsistent before, and never allowed scalar or augmented assignment).
Flag columns still do not support column assignment, and Flag column access still returns a copy, not a view, because Flag values are stored internally as individual bits within a larger integer.
:jirab:`DM-4856`

.. _release-v12-0-wcslib:

Upgraded WCSLIB to version 5.13
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Version 5.13 of WCSLIB resolves memory corruption errors that could crash the stack in some circumstances.
:jirab:`DM-4904,RFC-89,DM-4946,DM-3793`

.. _release-v12-0-obs-subaru-rotation:

Fix rotation for instrument signature removal in obs_subaru
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Approximately half of the HSC CCDs are rotated 180 deg with respect to the others.
Two others have 90 deg rotations and another two have 270 deg rotations (see HSC CCD layout).
The raw images for the rotated CCDs thus need to be rotated to match the rotation of their associated calibration frames (in the context of how they have currently been ingested) prior to applying the corrections.
This is accomplished by rotating the exposure using the rotated context manager function in ``obs_subaru``\ 's :command:`isr.py` and the ``nQuarter`` specification in the policy file for each CCD.
Currently, rotated uses ``afw``\ 's ``rotateImageBy90`` (which apparently rotates in a counter-clockwise direction) to rotated the exposure by ``4 - nQuarter`` turns.
This turns out to be the wrong rotation for the odd ``nQuarter`` CCDs.
This issue fixes this bug, leading to much improved processing of HSC CCD's 100, 101, 102, and 103.
Note that, in the future, the ingestion of the calibration data will be updated such that no rotations are necessary (so they will then be removed from  ``obs_subaru`` accordingly).
:jirab:`DM-4998`

.. _release-v12-0-conf-overrides-failure:

Fix a silent failure to apply config overrides
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When applying a config override, using a variable which hadn't been defined should throw a ``NameError``, which ultimately propagates to the end user to notify them that something has gone awry.
This warning was being incorrectly suppressed.
:jirab:`DM-5729`

.. _release-v12-0-sdssshape-flags:

Correctly set flags for bad SdssShape measurements.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :lclass:`SdssShape` algorithm provides both shape and flux measurements.
In some cases, a failed shape measurement could go un-noticed, resulting in an incorrect and unflagged flux measurement being associated with that source.
This is now checked for, and bad fluxes are appropriately flagged.
:jirab:`DM-3935`

.. _release-v12-0-contant-background-interpolation:

Fix CONSTANT background interpolation of bad data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When performing interpolation over bad data (e.g. every pixel masked), all interpolation types other than ``CONSTANT`` would return ``NaN``\ s; ``CONSTANT`` would throw.
This has now been changed so that ``CONSTANT`` also returns ``NaN``\ s.
:jirab:`DM-5797`

.. _release-v12-0-pixel-padding:

Accommodate pixel padding when unpersisting reference catalog matches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The reference object loader in ``meas_algorithm``\ 's :command:`loadReferenceObjects.py` grows the ``bbox`` by the config parameter ``pixelMargin`` (padding to add to 4 all edges of the bounding box [pixels]) when setting the radius of the sky circle to be searched in the reference catalog.
This is set to 50 by default but was not reflected by the radius parameter set in the metadata, which left open the possibility that some matches could reside outside the circle searched within the unpersisted radius.
Additionally, the match metadata was being set after the exposure's WCS had been updated, also leading to an inconsistency with the sky circle that was actually searched.
We now ensure that the actual sky circle that was searched for reference objects is the one set and persisted in the match metadata.
:jirab:`DM-5686`

.. _release-v12-0-filter-fallback-message:

Correct misleading filter fallback error message
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When failing to load a ``calib``, if ``fallbackFilterName`` was not set, a confusing and apparently unrelated error message would be generated (``Unknown value type for filter: <type 'NoneType'>``).
This has been corrected to properly inform the user about the issue.
:jirab:`DM-6151`

.. _release-v12-0-internal-improvements:

Build and Code Improvements
---------------------------

- :ref:`release-v12-0-numpy-110`
- :ref:`release-v12-0-boost-warning`
- :ref:`release-v12-0-remove-task-display`
- :ref:`release-v12-0-mask-to-defectlists`
- :ref:`release-v12-0-ctrl-pool`
- :ref:`release-v12-0-pipe-drivers`
- :ref:`release-v12-0-test-tolerances`
- :ref:`release-v12-0-filter-canonical-name`
- :ref:`release-v12-0-clang-issues`
- :ref:`release-v12-0-cmake-anaconda`
- :ref:`release-v12-0-afwdata-tests`
- :ref:`release-v12-0-disable-implicit-threading`
- :ref:`release-v12-0-migrate-smart-pointers`

.. _release-v12-0-numpy-110:

Work-around incompatibilities with NumPy 1.10
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

NumPy 1.10 introduced API changes which were incompatible with existing usage in the stack.
The latter has been updated to match.
:jirab:`DM-4063,DM-4071,DM-4238`.

.. _release-v12-0-boost-warning:

When building boost warn user if user-config.jam or site-config.jam exists
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Building boost can fail if a :file:`user-config.jam` or :file:`site-config.jam` exist and have options which conflict with the LSST build configuration process.
Introduce a warning message if either of these files are found to notify the user.
:jirab:`DM-4198`

.. _release-v12-0-remove-task-display:

Remove deprecated Task.display() method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method has been deprecated since release 9.2 (S14).
It has been removed from the codebase, and all stack code updated to directly interface with :lmod:`afw.display` or to use helper functions defined in ``meas_astrom``.
:jirab:`DM-4428`

.. _release-v12-0-mask-to-defectlists:

Efficiency improvement in converting Masks to DefectLists
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The previous version of routine was extremely memory intensive when large numbers of pixels were masked.
:jirab:`DM-4800`

.. _release-v12-0-ctrl-pool:

Add a new task parallelization framework
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``ctrl_pool`` package has been added to the LSST stack.
This is a high-level parallelization framework used for distributing Task execution across a cluster, based on an MPI process pool.
It is based on work carried out on Hyper Suprime-Cam.
It is not intended to be the long-term solution to parallelized processing in the LSST stack, but meets our data processing needs until the fully-fledged parallelization middleware is available.
:jirab:`DM-2983,DM-4835,DM-5409`

.. _release-v12-0-pipe-drivers:

Add parallel-processing top level tasks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The new ``pipe_drivers`` package builds upon ``ctrl_pool``, above, to provide command-line scripts which coordinate distributed execution of the single-frame, coaddition and multiband processing steps using either the Python multiprocessing module or with a SLURM batch scheduler on a cluster.
:jirab:`DM-3368,DM-3369,DM-3370`

.. _release-v12-0-test-tolerances:

Adjust test tolerances to be compatible with MKL-based NumPy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Anaconda 2.5 ships, by default, with a version of NumPy built against Intel MKL rather than OpenBLAS.
This can change some numerical results slightly, necessitating a change to test tolerances.
:jirab:`DM-5108`

.. _release-v12-0-filter-canonical-name:

Now possible to directly get a Filter's canonical name and aliases
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Added the convenience methods :lmeth:`getCanonicalName` and :lmeth:`getAliases` to :lmod:`lsst.afw.image.Filter`, accessible from both C++ and Python.
These return the canonical name and the aliases, respectively, of the filter. This information was previously only available through an awkward sequence of method calls.
:jirab:`DM-4816`

.. _release-v12-0-clang-issues:

Fix build issues with recent clang
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Recent releases of the clang C/C++ compiler, as shipped with Apple XCode, caused build failures in the stack.
Although we believe this may be a problem with clang, we have worked around it within the stack code.
We hope to track down the source of the error and, if appropriate, report it to the clang developers in future.
:jirab:`DM-5590,DM-5609`

.. _release-v12-0-cmake-anaconda:

Fix incorrect linking against Anaconda-provided libraries when using CMake
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some external packages---mariadb and mariadbclient---use a CMake based build system.
This can incorrectly link against some libraries bundled with the Anaconda Python distribution, rather than the system-provided equivalents, resulting in a build failure.
We have adjusted the build process of the affected packages to work around this error.
:jirab:`DM-5595`

.. _release-v12-0-afwdata-tests:

Execute afw test suite when afwdata is not available
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some tests in the ``afw`` package rely on data from the ``afwdata`` package.
The test suite would search for ``afwdata``, and skip all of the afw tests if ``afwdata`` is not available.
This check has been made smarter, so that only tests which actually require ``afwdata`` are now skipped.
:jirab:`DM-609`

.. _release-v12-0-disable-implicit-threading:

Disable implicit threading
^^^^^^^^^^^^^^^^^^^^^^^^^^

Low-level threading packages (such as OpenBLAS or MKL) can implicitly use many threads.
Since the LSST stack also parallelizes at a higher level (e.g. using Python's multiprocessing module), this can cause undesirable contention.
We now disable implicit threading when explicitly parallelizing at a higher level to protect the user from this.
Implicit threading can be re-enabled by setting the ``LSST_ALLOW_IMPLICIT_THREADS`` environment variable.
For more details, see this `Community post <https://community.lsst.org/t/implicit-threading-intervention/728>`__.
:jirab:`DM-4719`

.. _release-v12-0-migrate-smart-pointers:

Migrate to standard smart pointers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

C++11 introduced new smart pointer types (``std::unique_ptr``, ``std::shared_ptr`` and ``std::weak_ptr``).
We have migrated from the previously used Boost smart pointers to their standard equivalents.
:jirab:`DM-5879,DM-4008,RFC-100,DM-5966`

.. _release-v11-0:

Summer 2015 Release (v11_0)
===========================

These release notes document notable changes since 10.1, which was the
Winter 2015 release.

+---------------------------------------------+------------+
| Source                                      | Identifier |
+=============================================+============+
| Git tag                                     | 11.0       |
+---------------------------------------------+------------+
| :doc:`EUPS distrib <../install/newinstall>` | v11\_0     |
+---------------------------------------------+------------+

*See also:*

- :doc:`Measurements & Characterization <metrics/v11_0/index>`
- `Qserv release notes <https://confluence.lsstcorp.org/display/DM/Summer+2015+Qserv+Release>`_
- `Webserv release notes <https://confluence.lsstcorp.org/display/DM/Summer+2015+WebServ+Release>`_
- `Science User Interface release notes <https://confluence.lsstcorp.org/pages/viewpage.action?pageId=41785820>`_

.. _release-11-0-major-changes:

Major Functionality and Interface Changes
-----------------------------------------

Improved semantics for loading ``Exposure``\ s and ``MaskedImage``\ s from arbitrary FITS files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``Exposure`` and ``MaskedImage`` represent image data with
associated mask and variance information. When serialized to FITS, these
are stored as three consecutive extensions in the FITS files. It is
possible to load ``Exposure``\ s and ``MaskedImage``\ s from
multi-extension FITS files which were not generated by LSST, but, due to
the limitations of the FITS data model, it is not possible to ensure
that the creator of the file adhered to the LSST convention: while an
image object may be successfully instantiated, its contents may not be
logically consistent.

We now go to greater lengths to check that the information in the file
is consistent with the LSST standard, warning the user---and in some
cases refusing to proceed---if it does not.
:jirab:`DM-2599`

Improved support for non-standard FITS headers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The LSST stack is now capable of loading FITS files which contain
non-standard headers of the form ``PVi_nn`` (``i=1..x``, ``nn=5..16``),
as written by SCAMP, and ``EQUINOX`` headers with a "``J``\ " prefix, as
written by SkyMapper.
:jirab:`DM-2883,DM-2924,DM-3196`

It is now possible to perform instrument signal removal on an ``Exposure`` which has no ``Detector``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``FakeAmp``, a ``Detector``-like object object which supports returning
gain and saturation level, was added to make it possible to run
``updateVariance`` and ``saturationDetection`` if required.
(`DM-2890 <https://jira.lsstcorp.org/browse/DM-2890>`_)

``PVi_j`` header cards are correctly saved to FITS files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This makes it possible to round-trip TPV headers, for example.
:jirab:`DM-2926`

Changes to compound fields and delimiters in catalog schemas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the older ("version 0") approach to table schemas, we had several
compound field types (``Point``, ``Moments``, ``Covariance``, ``Coord``)
which behaved differently from other field types - the square bracket
``[]`` operators could not be used to access them, and they could not be
accessed as columns (though their scalar subfields – e.g. "x" and "y"
for ``Point`` – could be). In version 0, we used periods to separate
both words and namespace elements in field names, but converted periods
to underscores and back when writing to FITS. These schemas were mostly
produced by the old measurement framework in ``meas_algorithms``'
``SourceMeasurementTask``, which was removed in the 10.1 release.

In the new ("version 1") approach, compound objects are simply stored in
catalogs as their constituent scalars, with helper classes called `FunctorKeys
<http://lsst-web.ncsa.illinois.edu/doxygen/x_masterDoxyDoc/classlsst_1_1afw_1_1table_1_1_functor_key.html>`__
provided to pack and unpack them from ``Records`` (the ``FunctorKey``\ s that
replace the old compound fields are all in ``afw/table/aggregates.h``). Unlike
the original compound fields, there's no limit to how many types of
``FunctorKey`` we can have, or what package they can live in, making the system
much more extensible. By making the constituent scalar objects what the
``Schema`` object knows about, it will be much easier to map a ``Schema`` to
other table representations that don't know about LSST classes (e.g. SQL or
Pandas). Most ``FunctorKey``\ s can be used anywhere a regular ``Key`` can be
used. Also, in version 1, we use underscores as namespace separators, and
CamelCase to separate words, eliminating some ambiguity between word and
namespace boundaries. The new measurement framework in ``meas_base``'s
``SingleFrameMeasurementTask`` and ``ForcedMeasurementTask`` uses version
1 tables exclusively.

In previous releases of the pipeline, version 0 schemas were deprecated
but still supported. They have now been removed, but old catalogs saved
as version 0 will still be readable - they will be converted to version
1 on read, with period delimiters converted to underscores, and all
compound fields unpacked into scalar fields that can be used with a
corresponding ``FunctorKey``. This procedure obviously does not preserve
field names, but all slot definitions will be preserved, so code that
only relies on slot or minimal schema accessors (``getCoord()``,
``getCentroid()``, ``getPsfFlux()``, etc.) should not need to be
modified.
:jirab:`DM-1766`

Allow for use of Approximate (Chebyshev) model in background estimation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In previous releases, the only method for background estimation was to
use an interpolation scheme (constant, linear, or various splines).
These schemes tend to lead to over-subtraction of the background near
bright objects. The Approximate (Chebyshev) approach to background
estimation greatly improves the background subtraction around bright
objects. The relevant code to use this latter approach (including
persistence and backwards compatibility issues) is now in place.

While the intention is to eventually set the Approximate background
subtraction scheme as the default, there is some clean-up and
restructuring that needs to be done before resetting the defaults (which
may also require adjusting some defaults in the calibrate stage to be
more appropriate for the approximation, as opposed to interpolation,
scheme). Therefore, the default setting has not been changed (i.e. the
default is still to use an interpolation scheme for background
estimation). The Chebychev approximation can be selected for background
estimation through configuration parameters in the obs\_CAMERA packages,
i.e. useApprox=True and, optionally, approxOrderX (approximation order
in X for background Chebyshev), approxOrderX (approximation order in Y
for background Chebyshev: currently approxOrderY must be equal to
approxOrderX), weighting (if True, use inverse variance weighting in
calculation).
:jirab:`DM-2778`

Multi-band processing for coadds
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See the description of the multi-band coadd processing work performed in
S15 for details. In short, four new command-line Tasks have been added
for consistent multi-band coadd processing:

DetectCoaddSourcesTask
   Detect sources (generate Footprints for parent sources) and model
   background for a single band.
MergeDetectionsTask
   Merge Footprints and Peaks from all detection images into a single,
   consistent set of Footprints and Peaks.
MeasureMergedCoaddSourcesTask
   Deblend and measure on per-band coadds, starting from consistent
   Footprints and Peaks for parent objects.
MergeMeasurementsTask
   Combine separate measurements from different bands into a catalog
   suitable for driving forced photometry. Essentially, it must have a
   centroid, shape, and CModel fit for all objects, even for objects that
   were not detected on the canonical band. Will assume that all input
   catalogs already have consistent object lists.

:jirab:`DM-1945,DM-3139`

Enable use of deblended HeavyFootprints in coadd forced photometry
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Given the new multi-band processing for coadds (above), we now have a
reference catalog that is consistent across all bands. This catalog
allows the use of the source's HeavyFootprints to replace neighbors with
noise in forced photometry, thus providing deblended forced photometry
and consistent deblending across all bands. This provides much better
colors for blended objects as well as measurements for drop-out objects
that do not get detected in the canonical band. This functionality has
been enabled for forced coadd photometry.

See the description of the multi-band coadd processing work performed in
S15 for further motivation of this change.
:jirab:`DM-1954`

Limited the fractional number of masked pixels per source
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CModel has difficulties modelling backgrounds in vignetted regions of
the focal plane, leading to a performance bottleneck. To mitigate the
issue, if the fractional number of masked pixels in a particular source
exceeds a given threshold, that source will be skipped.
:jirab:`DM-2914`

Peak culling around large objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An excess of "junk" peaks may be observed around large objects. Given
the new multi-band processing architecture (above), these must be
consistently removed across bands. We therefore provide a method to
consistently "cull" this peaks at an earlier stage, immediately after
merging and sorting in ``MergeDetectionsTask``.
:jirab:`DM-2914`

Parent Footprints are the union of their children
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Parent ``Footprint``\ s are now trimmed so that they are strictly the
union of their children: any pixels which are not assigned to a child
are removed. This mitigates an issue whereby stray flux from the parent
was not correctly assigned to the children. Note that this has the
consequence that parent ``Footprint``\ s are not necessarily contiguous.
:jirab:`DM-2914`

Large Footprints may be skipped on initial processing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For practical processing purposes (specifically total processing time
and memory limits due to current hardware limitations), we have the
option to skip over objects with large ``Footprint``\ s during
large-scale processing, with the intention to return to these objects to
"reprocess" them using different hardware in future. The ability to
properly record which objects have been skipped and require further
processing has been implemented along with optimizations to the
deblender configuration for the maximum number of ``Peak``\ s per
``Footprint``, and the size and area of ``Footprint``\ s.
:jirab:`DM-2914`

Command line tasks for measurement transformation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The measurement transformation framework provides a generic mechanism
for transforming the outputs of measurement plugins in raw units, such
as pixel positions or flux, to calibrated, physical units, such as
celestial coordinates or magnitudes. Appropriate transformations are
defined on a per-measurement-plugin basis, and may make use of the
calibration information and WCS stored with the data.

This system is designed such that the transformation of a given catalog
is performed by a command line task. Different catalog types (such as
``src``, ``forced_src``, etc) make use of separate command line tasks.
In this release, we provide a variety of tasks to handle different
source types.

- `Documentation for generic transforms <https://lsst-web.ncsa.illinois.edu/doxygen/x_masterDoxyDoc/classlsst_1_1pipe_1_1tasks_1_1transform_measurement_1_1_transform_task.html#TransformTask_>`_.
- `Documentation for SrcTransformTask <https://lsst-web.ncsa.illinois.edu/doxygen/x_masterDoxyDoc/classlsst_1_1pipe_1_1tasks_1_1transform_measurement_1_1_src_transform_task.html#details>`_.
- `Documentation for ForcedSrcTransformTask <https://lsst-web.ncsa.illinois.edu/doxygen/x_masterDoxyDoc/classlsst_1_1pipe_1_1tasks_1_1transform_measurement_1_1_forced_src_transform_task.html#ForcedSrcTransformTask_>`_.
- `Documentation for CoaddSrcTransformTask <https://lsst-web.ncsa.illinois.edu/doxygen/x_masterDoxyDoc/classlsst_1_1pipe_1_1tasks_1_1transform_measurement_1_1_coadd_src_transform_task.html#CoaddSrcTransformTask_>`_.

(`DM-2191 <https://jira.lsstcorp.org/browse/DM-2191>`_,
`DM-3473 <https://jira.lsstcorp.org/browse/DM-3473>`_,
`DM-3483 <https://jira.lsstcorp.org/browse/DM-3483>`_)

Add ``NO_DATA`` mask plane
^^^^^^^^^^^^^^^^^^^^^^^^^^

Previously, we have used the ``EDGE`` mask plane to indicate *both*
pixels which are off-the-edge of the detector, and hence have no data
available, and pixels near the edge which cannot therefore be properly
searched for sources. Here, we introduce the ``NO_DATA`` plane to refer
to the former case and now use ``EDGE`` strictly for the latter.
:jirab:`DM-3136`

Add slot for flux used in photometric calibration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We define a new slot, ``CalibFlux``, on ``SourceRecord``\ s. This slot
is used to record the flux used for photometric calibration, rather than
hard-coding the name of a particular algorithm in the ``PhotoCal`` task.
This slot defaults to a 12 pixel circular aperture flux, the previous
default in ``PhotoCal``.
:jirab:`DM-3106,DM-3108`

Table field prefix for aperture flux measurements changed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Our aperture flux measurement algorithms take a list of radii, in
pixels, which define the radii over which measurements should be made.
Previously, the names of the table fields produced by the algorithm were
defined purely based on the position of the radius in that list (thus,
the first radius listed would produce a flux field named
``PluginName_0_flux``). This has been changed so that the fields are now
named after the radius, regardless of its position in the list. Thus, a
12.5 pixel aperture will result in a field named
``PluginName_12_5_flux``, regardless of its position in the list.
:jirab:`DM-3108`

Faster astrometry reference catalog loading
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The reference catalog loading was optimised by caching HEALpix
identifiers for the catalog files. This has been observed to speed up
loading times from 144 sec to 12 sec.

The cache is saved as ``andCache.fits`` in the astrometry catalog
directory. The use of the cache can be disabled through the
``andConfig.py`` file (or the ``AstrometryNetDataConfig``) by setting
``allowCache`` to ``False``. To prepare a cache,
``setup astrometry_net_data`` and use the ``generateANetCache.py``
script that now comes in ``meas_astrom``.
:jirab:`DM-3142`

Bad pixels tracked when coadding images
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When co-adding images, we now keep track of what fraction of the input
data for a given pixel was masked. If the total masked data exceeds some
user-configurable threshold, the mask is propagated to the coadd.
:jirab:`DM-3137`

Polygon masking in coadded PSFs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Polygonal masks are used to define the usable area of the focal plane;
they can be used to, for example, exclude vignetted areas from
coaddition. We now take account of these masks to determine which PSF
images to included when building co-added PSFs.
:jirab:`DM-3243,DM-3528`

Scale counts to reflect CCD-specific zero-points when warping to create coadd inputs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:jirab:`DM-2980`

Solving astrometry with distortions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The default astrometry matcher (``matchOptimisticB``) can now match
stars against a reference catalog when the stars are distorted (e.g., at
the outskirts of a wide field imager) if there is an estimate of the
distortion available.
:jirab:`DM-3492`

Rejection iterations in astrometry fitting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Astrometric fitting (``FitTanSipWcsTask``) now includes support for
iterative fitting with rejection.
:jirab:`DM-3492`

Inclusion of external package PSFEx as option for PSF determination
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PSFEx is currently the state of the art external package for PSF
determination, used in projects such as DES. LSST wrappers were created
such that PSFEx could be used as a plugin in place of the built in PSF
determiner. Tests with Hyper Supreme Camera data have shown that PSFEx
out performs the built-in PSF determiner.
:jirab:`DM-2961`

Improvements to CModel magnitude measurement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This release includes many miscellaneous improvements and fixes
resulting from testing on HSC data, including:

-  parameter tuning for computational performance improvement
-  correction to uncertainty estimation to account for extrapolation
   beyond the fit region
-  much more robust flagging of failure modes

Interface changes to forced measurement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The order of arguments to the forced measurement task was reversed, so
that it takes a source catalog followed by an ``Exposure``. This brings
it into line with the single frame measurement interface.
:jirab:`DM-3459`

N-way spatial matching
^^^^^^^^^^^^^^^^^^^^^^

A simple utility class for performing spatial matches between multiple
catalogs with identical has been added as
``lsst.afw.table.multiMatch.MultiMatch``. This is intended as a stop-gap
measure until more flexible and efficient functionality becomes
available, but is already usable.
:jirab:`DM-3490`

Display CCD data as laid out in the focal plane
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is now possible to use ``lsst.afw.cameraGeom.utils`` to display CCD
data laid out in the focal plane. `An
example <https://github.com/lsst/afw/blob/master/examples/Show%20Camera.ipynb>`_
of how this functionality works in practice is available as an IPython
notebook.
:jirab:`DM-2347`

.. _release-11-0-bug-fixes:

Bug Fixes
---------

The following fixes resolve problems visible to end users.

Doxygen documentation now correctly includes LaTeX formatting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Correctly referring to MathJax means that LaTeX markup in documentation
is nicely formatted.
:jirab:`DM-2545`

Performance regression in ``Footprint`` dilation resolved
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The previous release included improved algorithms for dilating
``Footprint``\ s. Unfortunately, in some circumstances (notably when
dealing with particularly large ``Footprint``\ s) this code could
actually perform more slowly than the previous implementation. This
could have significant performance implications for many image
processing operations. This regression has now been rectified, and the
new dilation operations are significantly faster than the old ones in
all circumstances tested.
:jirab:`DM-2787`

Footprint fixes
^^^^^^^^^^^^^^^

The following updates/fixes to Footprint handling have been made:

-  The default 32-bit heap space used to store FITS variable-length
   arrays isn't large enough to store some of our extremely large
   HeavyFootprints. This persistence issue has been fixed the by
   switching to 64-bit heap descriptors, which is now supported by FITS.
-  ``Footprint::transform`` is now properly copying peaks over to the new
   footprint.
-  ``Footprint::clipTo`` is now properly removing those peaks lying outside
   the desired region.
-  Several parts of the pipeline assume peaks are sorted from most
   positive to most negative. We now ensure the cross-band merge code
   maintains this ordering as much as possible (even though the sorting
   may not be consistent across different bands).
-  The merging of a parent and its children’s Footprints was failing in
   cases where one or more child Footprints were themselves
   noncontiguous. This has been fixed by adapting the mergeFootprints
   code in afw such that it combines all the Footprints in the
   FootprintSet it uses in its implementation (instead of requiring that
   the FootprintSet have only one Footprint).

:jirab:`DM-2606`

Fixed error in memory access in interpolation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An off-by-one error resulted in an attempt to read beyond the allocated
memory.
:jirab:`DM-3112`

Fixed truncated write of certain WCS information to FITS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:jirab:`DM-2931`

Use the correct weighting in photometric calibration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Previously, we were incorrectly weighting by errors, rather than inverse
errors.
:jirab:`DM-2423`

Remove non-positive variance pixels in coadd creation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When interpolating variance maps we can produce negative values. These
then cause failures when we try to take the square root. Ultimately, the
means of creating variance maps needs to be fixed (which is
:jira:`DM-3201`); as a temporary
workaround, we replace negative variance values with infinity.
:jirab:`DM-2980`

Task defaults are set correctly for difference imaging
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``DipoleMeasurementConfig.setDefaults`` method incorrectly contained
a ``return`` that was executed before the defaults were actually
applied. This has been corrected, and a number of tests updated to rely
on those defaults.
:jirab:`DM-3159`

.. _release-v11-0-internal-improvements:

Build and code improvements
---------------------------

These improvements should not usually be visible to end users. They may
be important for developers, however.

Backend-agnostic interface to displays
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The image display code no longer makes the assumption that display is
carried out using ds9. Rather, an API is available which is independent
of the the particular image viewer is in use. A backwards compatibility
layer ensures that display through ds9 is still supported, while other
backends will be added in future.

:jirab:`RFC-42,DM-2709,DM-2849,DM-2940,DM-3203,DM-3468`

Measurement framework compiler warnings resolved
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The measurement framework was refactored to avoid a series of warnings
produced by the clang compiler.
:jirab:`DM-2131`

Unsanctioned access to the display by tests suppressed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some unit tests were attempting to write to a display, even when no
display was available. On some systems, this directly caused test
failures; on others, it could obscure the true cause of failures when a
test did fail.
:jirab:`DM-2492,DM-2494`

Unused & obsolete code has been removed from the ``datarel`` package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This package is effectively obsolete, but is still used in documentation
generation which makes removing it entirely complex. For now, therefore,
it has simply been trimmed of all unused functionality; it may be
removed entirely following
:jira:`DM-2948`.
:jirab:`DM-2949`

Reduced verbosity of astrometry.net solver
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A correction to the way that astrometry.net logging was propagated to
the LSST logging system, together with reducing the priority of some
messages, leads to a substantial reduction in chatter from astrometry.
:jira:`DM-3141`

Ensure that slots are present before initializing algorithms that depend upon them
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When initializing an algorithm that refers to a particular slot, we
resolve the target of the slot and refer to that instead. That means
that if the slot definition is changed after measurement has been
performed, we are still pointing to the correct information. However, if
the algorithm is initialized before the slot it depends on, this
resolution could not take place and "circular" aliases could result. We
now explicitly check for and throw an error in this case.
:jirab:`DM-3400`

Visualizations for astrometry.net solver
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is now possible to display the source positions, distorted source
positions and reference positions to assist with debugging.
:jirab:`DM-3209`

Subaru support reinstated
^^^^^^^^^^^^^^^^^^^^^^^^^

The ``obs_subaru`` package, which provides packages and tasks specific
to the Subaru telescope, has been brought up to date with recent changes
to the LSST stack and improvements made during Hyper Suprime Cam
development.
:jirab:`DM-1794,DM-3403`

Refactor & document coadd construction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A number of minor changes and documentation improvements were made to
the ``CoaddBase``, ``AssembleCoadd``, ``CoaddInputRecorder`` and
``MakeCoaddTempExp`` tasks. These brought the structure of the code
better into line with the state-of-the-art development on Hyper Suprime
Cam.
:jirab:`DM-2980`

Properly handle masking NaN or saturated values in overscans
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Resolved an issue where, in certain circumstances, flags in the mask
plane for saturated and nan values in overscans were being improperly
propagated to all amplifiers in an image. These flags are now applied to
the amplifier where the bad values are seen.
:jirab:`DM-2923`

Deblender optimization
^^^^^^^^^^^^^^^^^^^^^^

Several performance optimizations to the (C++) algorithms used in the
deblender have been implemented, in particular those which identify
objects with significant amounts of their flux attributed to edge
pixels. In addition, memory usage was reduced by removing unused mask
planes left over from debugging, not storing masks for deblending
templates, and by clipping template images when their associated
``Footprint``\ s are clipped.
:jirab:`DM-2914`
