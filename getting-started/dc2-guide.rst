#########################################
Processing DC2 data with the AP Pipelines
#########################################

A walkthrough for running the Alert Production (AP) pipeline on an example set of image data. The data used in this guide is simulated data, the same kind used for Rubin's Data Preview 0 (DP0).

.. note::

   This guide assumes the user has access to a shared Butler repository containing data from the Dark Energy Science Collaboration (DESC)'s Data Challenge 2 (DC2) via the `US Data Facility (USDF) <https://developer.lsst.io/usdf/storage.html>`__.
   This guide further assumes the user has a recently-built version of ``lsst.distrib`` from the `LSST Science Pipelines <https://developer.lsst.io/usdf/stack.html>`__ (circa ``w_2022_30`` or later).

What does existing DC2 data look like?
======================================

* The instrument is called ``LSSTCam-imSim``
* The obs-package is ``obs_lsst``, i.e., :ref:`lsst.obs.lsst` (note ``imsim`` subdirectories within)
* The skymap is called ``DC2``
* Patches go from 0 to 48
* Detectors go from 0 to 188
* Available bands are ``ugrizy``
* Data exist for some tracts in the ~2553–5074 range, and commonly reprocessed tracts include 3828, 3829, and 4431
* One set of reference catalogs are called ``cal_ref_cat_2_2``, and have some filtermap definitions that must be specified

The Shared DC2 Butler Repository at the USDF
--------------------------------------------

* The Butler repository is located at ``/sdf/group/rubin/repo/dc2``, which the Butler also recognizes via the alias ``/repo/dc2``
* All raw data are available in the collection ``2.2i/raw/all``
* All raw data with ancillary processing inputs (e.g., calibs, skymaps, refcats) are available in the collection ``2.2i/defaults``; this collection includes ``2.2i/raw/all``, and several other collections, inside it
* Tracts 3828 and 3829 only are in the collection ``2.2i/defaults/test-med-1``
* A smaller CI dataset, just patch 24 in tract 3828, is in ``2.2i/defaults/ci_imsim`` and corresponds to the GitHub repo ``testdata_ci_imsim``
* Tract 4431 has a 10-year simulated depth, and was processed in the collection ``u/kherner/2.2i/runs/tract4431-w40``
* Visits that fully overlap four adjacent patches (9, 10, 16, and 17) in tract 4431 are in the collection ``u/mrawls/DM-34827/defaults/4patch_4431`` (this guide will use this collection!)

Using the Butler to explore collections and datasets
----------------------------------------------------

To explore these and other collections, try, e.g.,

.. prompt:: bash

   butler query-collections /repo/dc2 "2.2i/defaults"
   butler query-collections /repo/dc2 "u/mrawls/DM-34827*"

These commands should print a list of collections that meet the search criteria.

To see some available datasets for processing, try, e.g.,

.. prompt:: bash

   butler query-data-ids /repo/dc2 tract patch visit --collections='u/mrawls/DM-34827/defaults/4patch_4431' --where "skymap='DC2' AND band='g' AND instrument='LSSTCam-imSim'" --datasets "raw"

This command should print a list of data IDs that meet the search criteria, along with their tract, patch, and visit number.
Certain arguments are required after the ``--where``, including ``skymap`` and ``instrument``, while most others are optional, and may include ``band``, ``tract``, ``patch``, etc.

Processing Data with the AP Pipelines
=====================================

Now it's time to process some data.
In this guide, we will run a template-building pipeline, ``ApTemplate.yaml``, first.
This pipeline starts with raw images and runs standard single frame processing (which includes :py:class:`lsst.ip.isr.isrTask.IsrTask`, :py:class:`lsst.pipe.tasks.characterizeImage.CharacterizeImageTask`, and :py:class:`lsst.pipe.tasks.calibrate.CalibrateTask`).
From here, it is possible to run :py:class:`lsst.pipe.tasks.postprocess.ConsolidateVisitSummaryTask`, :py:class:`lsst.pipe.tasks.makeCoaddTempExp.MakeWarpTask`, :py:class:`lsst.pipe.tasks.selectImages.BestSeeingQuantileSelectVisitsTask`, and :py:class:`lsst.pipe.tasks.assembleCoadd.CompareWarpAssemblecoaddTask`.
The final result is good seeing coadd templates.

In a second pipeline, ``ApPipe.yaml``, we will run difference imaging using the templates we just built.
This pipeline also starts with single frame processing on raw images, followed by :py:class:`lsst.ip.diffim.subtractImages.AlardLuptonSubtractTask`, :py:class:`lsst.ip.diffim.detectAndMeasure.DetectAndMeasureTask`, :py:class:`lsst.ap.association.transformDiaSourceCatalog.TransformDiaSourceCatalogTask`, and :py:class:`lsst.ap.association.diaPipe.DiaPipelineTask`.
The final results include difference images, some output catalogs, and an Alert Production Database (APDB).

Building good seeing templates
------------------------------

The pipeline we will use lives in the ``ap_pipe`` package, and is the camera-specific ``ApTemplate.yaml`` pipeline.
To see it, either navigate to the `pipeline on GitHub <https://github.com/lsst/ap_pipe/blob/main/pipelines/LsstCamImSim/ApTemplate.yaml>`__ or display the pipeline on via the command line, e.g.,

.. prompt:: bash

   cat $AP_PIPE_DIR/pipelines/LsstCamImSim/ApTemplate.yaml

Note that this camera-specific pipeline imports both a camera-specific single-frame processing pipeline (sometimes called "processCcd") and a more generic AP Template building pipeline.

To visualize this pipeline, you may wish to use ``pipetask build``, e.g.,

.. prompt:: bash

   pipetask build -p $AP_PIPE_DIR/pipelines/LsstCamImSim/ApTemplate.yaml --pipeline-dot ApTemplate.dot
   dot ApTemplate.dot -Tpng > ApTemplate.png

Alternately, navigate to `this website that serves visualizations of all the AP and DRP pipelines <https://tigress-web.princeton.edu/~lkelvin/pipelines/current>`__.
Click through to ``ap_pipe``, then ``LsstCamImSim``, and finally ``ApTemplate`` to find a PDF visualizing all the pipeline inputs, outputs, and intermediate data products.
This PDF is auto-generated each week using the same ``pipetask build`` command as shown above.

To run this pipeline, make up an appropriate output collection name (``u/USERNAME/OUTPUT-COLLECTION-1`` in the example below), and run

.. prompt:: bash

   pipetask run -j 4 -b /repo/dc2 -d "skymap='DC2' AND tract=4431 AND patch IN (9, 10, 16, 17) AND band='g'" -i 2.2i/defaults -o u/USERNAME/OUTPUT-COLLECTION-1 -p $AP_PIPE_DIR/pipelines/LsstCamImSim/ApTemplate.yaml

To tell the process to run in the background and write output to a logfile, you may wish to prepend ``pipetask run`` with ``nohup`` and postpend the command with ``> OUTFILENAME &``.
This will take some time, but when it's done, you should have calibrated exposures and a visit summary table, warps, and assembled good seeing coadds for use as templates.
We are now ready to run the rest of the AP Pipeline (namely difference imaging and source association).

Performing difference imaging and making an APDB
------------------------------------------------

This next step uses a second pipeline, which begins once again with single frame processing.
If you choose to reuse some or all of the same input raw exposures, all previously-run steps will automatically be skipped and pre-existing outputs used.
Afterwards, it performs difference imaging and saves the results in an Alert Production Database (APDB).

The pipeline we will use also lives in the ``ap_pipe`` package, and is the camera-specific ``ApPipe.yaml`` pipeline. To see it, either navigate to the `pipeline on GitHub <https://github.com/lsst/ap_pipe/blob/main/pipelines/LsstCamImSim/ApPipe.yaml>`__ or display the pipeline on via the command line, e.g.,

.. prompt:: bash

   cat $AP_PIPE_DIR/pipelines/LsstCamImSim/ApPipe.yaml

This difference imaging pipeline requires coadds as inputs for use as templates, and treats all input raws as "science" images.

Unlike before, however, we need to create an empty APDB for the final step of the pipeline to connect and write to.
The simplest option, which works fine for relatively small processing runs, is to create an empty sqlite database in your working directory.
Larger runs will require using, e.g., PostgreSQL, which is beyond the scope of this guide.
To create an empty sqlite APDB:

.. prompt:: bash

   make_apdb.py -c db_url="PATH-TO-YOUR-APDB-HERE"

**The APDB must exist and be empty before you run the AP Pipeline.**
It is highly recommended to make a new APDB each time the AP Pipeline is rerun for any reason.
A typical ``db_url`` is, e.g., ``sqlite:////path/to/my-working-directory/run1.db``.

The configs you set when making the APDB must match those you give the AP Pipeline at runtime.

As before, to visualize the AP Pipeline, you may navigate to `the website with visualizations of all the AP and DRP pipelines <https://tigress-web.princeton.edu/~lkelvin/pipelines/current>`__.
Click through to ``ap_pipe``, then ``LsstCamImSim``, and finally ``ApPipe`` to find a PDF visualizing all the pipeline inputs, outputs, and intermediate data products.
This PDF is auto-generated each week using an analogous ``pipetask build`` command as shown above for ``ApTemplate.yaml``.

You are now ready to run the AP Pipeline!
You will need to substitute appropriate values for your input collections, your desired new output collection, and your APDB URL in order to run

.. prompt:: bash

   pipetask run -j 4 -b /repo/dc2 -d "skymap='DC2' AND band='g'" -i u/USERNAME/OUTPUT-COLLECTION-1,u/mrawls/DM-34827/defaults/4patch_4431 -o u/USERNAME/OUTPUT-COLLECTION-2 -p $AP_PIPE_DIR/pipelines/LsstCamImSim/ApPipe.yaml -c diaPipe:apdb.db_url="PATH-TO-YOUR-APDB-HERE"

What are the output data products?
==================================

When the AP Pipeline completes, you will have difference images, difference image source tables, and an APDB with populated tables (``DiaSource``, ``DiaObject``, etc.) for ``g`` band visits that fully overlap four patches of tract 4431.

A few analysis and plotting tools exist to explore the APDB and other AP Pipeline outputs.
These live in `analysis_ap <https://github.com/lsst/analysis_ap>`__.
One output from the AP Pipeline are DIA (Difference Image Analysis) Source Tables, which the Butler can retrieve via ``goodSeeingDiff_diaSrcTable``.

To see what DIA Source Tables exist, query, e.g.,

.. prompt:: bash

   butler query-data-ids /repo/dc2 visit detector --collections="u/USERNAME/OUTPUT-COLLECTION-2" --where "skymap='DC2' AND band='g' AND instrument='LSSTCam-imSim'" --datasets "goodSeeingDiff_diaSrcTable"

The APDB also contains several tables with information about DIA Sources, DIA Objects, and Solar System Objects.
Objects represent real astrophysical things, and are created by spatially associating per-visit Sources.
The DIA prefix indicates we are talking about Sources and Objects in difference images.
More information about the APDB schema is available in `sdm_schemas <https://github.com/lsst/sdm_schemas/blob/main/yml/apdb.yaml?>`__.

.. note::

   None of the following is a formally supported APDB user interface.
   It one way to load a table from the APDB into memory in python and make a quick plot to see where the associated DIA Objects fall on the sky.
   It also includes an example of how to load a ``goodSeeingDiff_diaSrcTable`` with the Butler for further analysis.
   
   Future plans include support for visualizing some AP Pipeline outputs via :ref:`lsst.analysis.tools` and/or :ref:`lsst.analysis.ap`.

Give this a try in a Jupyter notebook:

.. code-block:: python
   :name: apdb-simple-example

   %matplotlib notebook
   import sqlite3
   import pandas as pd
   import matplotlib.pyplot as plt
   import lsst.daf.butler as dafButler

   # Define the data we are exploring, and instantiate a Butler
   repo = '/repo/dc2'
   collections = 'u/USERNAME/OUTPUT-COLLECTION-2'
   instrument='LSSTCam-imSim'
   skymap='DC2'
   butler = dafButler.Butler(repo, collections=collections, instrument=instrument, skymap=skymap)

   # Load a diaSrcTable from the Butler for one (visit, detector)
   diaSrcTable_example = butler.get('goodSeeingDiff_diaSrcTable', visit=960220, detector=33)

   # Take a look at it
   diaSrcTable_example.head()

   # Connect to the APDB and load all DiaObjects from the whole run
   connection = sqlite3.connect('/path/to/my-working-directory/run1.db')
   objTable = pd.read_sql_query('select "diaObjectId", "ra", "decl", \
                              "nDiaSources", "gPSFluxMean", "validityEnd" \
                              from '"DiaObject"' where "validityEnd" is NULL;', connection)

   # Take a look at it
   objTable

   # Plot DIA Objects on the sky
   fig = plt.figure(figsize=(6,6))
   ax = fig.add_subplot(111)
   ax.scatter(objTable.ra, objTable.decl, s=objTable.nDiaSources*2, marker='o', alpha=0.4)
   ax.set_xlabel('RA (deg)')
   ax.set_ylabel('Dec (deg)')
   ax.set_title('DIA Objects on the sky')



Processing Data with BPS
========================

The example data processing steps above assume a relatively small data volume, so running from the command line and using an sqlite APDB is appropriate.
However, if you want to process larger data volumes, you'll need to use the Batch Processing System (BPS, :py:mod:`lsst.ctrl.bps`) and a PostgreSQL APDB.

Describing how to set up a PostgreSQL APDB from scratch is beyond the scope of this guide.
One key difference between using an sqlite APDB versus a PostgreSQL APDB is that the former is a file on disk created from scratch when running ``make_apdb.py``.
The latter requires a database to already exist, and ``make_apdb.py`` turns the specified schema (via the ``namespace`` config option) in an existing PostgreSQL database into an empty APDB.
As before, you will still need to run, e.g.,

.. prompt:: bash

   make_apdb.py -c db_url="postgresql://USER@DB_ADDRESS/DB_NAME" -c namespace='DESIRED_POSTGRES_SCHEMA_NAME'

(being sure to replace ``USER``, ``DB_ADDRESS``, and ``DB_NAME`` with appropriate values).
Next, use the documentation for :py:mod:`lsst.ctrl.bps` to `define a submission <https://pipelines.lsst.io/v/weekly/modules/lsst.ctrl.bps/quickstart.html#defining-a-submission>`__ by creating two BPS configuration files --- one for the template-building step and one for the difference-imaging step.
Save these BPS configuration files as ``ApTemplate-DC2-bps.yaml`` and ``ApPipe-DC2-bps.yaml``.

.. note::

   The :py:mod:`lsst.ctrl.bps` module is well-documented, but at the time of this writing, best practices for running BPS at the USDF are still in development.
   Refer to the `USDF documentation pages <https://developer.lsst.io/usdf/batch.html>`__ for the latest recommendations.
   There is likely a set of default configurations users must import or place directly in their BPS configuration file that pertain to the underlying architecture for batch job submissions.

Ensure the ``pipelineYaml`` keyword points to the appropriate ApTemplate and ApPipe pipelines in each BPS configuration file, and that you specify appropriate values for ``butlerConfig``, ``inCollection``, ``outCollection`` (or ``payloadName``, which may be used to construct ``outCollection``), and ``dataQuery``.
These values mirror those on the command line via ``pipetask run`` and the ``-b``, ``-i``, ``-o``, and ``-d`` arguments, respectively.

For example, to make good seeing templates using all available patches and bands in two entire tracts, you may wish to use a data query like ``instrument='LSSTCam-imSim' and tract in (3828, 3829) and skymap='DC2'``.

When you are ready to submit your first BPS run to build templates, follow the documentation to `submit a run <https://pipelines.lsst.io/v/weekly/modules/lsst.ctrl.bps/quickstart.html#submitting-a-run>`__, e.g.,

.. prompt:: bash

   bps submit ApTemplate-DC2-bps.yaml

Once the templates are built, the second BPS configuration file will typically need to have two input collections: the output collection from the first run and a collection with raw science images.

As before, you will need to run ``make_apdb.py`` prior to running the second pipeline.
To configure the APDB in a BPS configuration file that runs ``ApPipe.yaml``, add a line like this for a PostgreSQL APDB:

.. prompt:: bash

   extraQgraphOptions: "-c diaPipe:apdb.db_url='postgresql://USER@DB_ADDRESS/DB_NAME' -c diaPipe:apdb.namespace='DESIRED_POSTGRES_SCHEMA_NAME'"

Finally, to submit the second BPS run and perform difference imaging and populate the APDB, run, e.g.,

.. prompt:: bash

   bps submit ApPipe-DC2-bps.yaml
