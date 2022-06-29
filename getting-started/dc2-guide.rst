########################################
Processing DC2 data with the Gen3 Butler
########################################

A walkthrough for running the Alert Production (AP) pipeline on an example set of image data. The data used in this guide is simulated data, the same kind used for Rubin's Data Preview 0 (DP0).

.. note::

   This guide assumes the user has access to a shared "Gen3" Butler repository containing data from the Dark Energy Science Collaboration (DESC)'s Data Challenge 2 (DC2) via the ``lsst-devl`` machines at NCSA.
   This guide further assumes the user has a recently-built version of :py:mod:`lsst.distrib` from the LSST Science Pipelines.

What does existing DC2 data look like?
======================================

* The instrument is called ``LSSTCam-imSim``
* The obs-package is ``obs_lsst``, i.e., :py:mod:`lsst.obs.lsst` (note ``imsim`` subdirectories within)
* The skymap is called ``DC2``
* Patches go from 0 to 48
* Detectors go from 0 to 188
* Available bands are ``ugrizy``
* Data exist for some tracts in the ~2553–5074 range, and commonly reprocessed tracts include 3828, 3829, and 4431
* One set of reference catalogs are called ``cal_ref_cat_2_2``, and have some filtermap definitions that must be specified

Some specifics about the Shared DC2 Butler Repository at NCSA
-------------------------------------------------------------

* The repository is called ``/repo/dc2``
* All raw data are available in the collection ``2.2i/raw/all``
* All raw data with ancillary processing inputs (e.g., calibs, skymaps, refcats) are available in the collection ``2.2i/defaults``
* Tracts 3828 and 3829 only are in the collection ``2.2i/defaults/test-med-1``
* A smaller CI dataset, just patch 24 in tract 3828, is in ``2.2i/defaults/ci_imsim`` and corresponds to the GitHub repo ``testdata_ci_imsim``
* Tract 4431 has a 10-year simulated depth, and was processed in the collection ``u/kherner/2.2i/runs/tract4431-w40``
* Visits that fully overlap four adjacent patches (9, 10, 16, and 17) in tract 4431 are in the collection ``u/mrawls/DM-34827/defaults/4patch_4431`` (this guide will use this collection!)

Using the Butler to explore collections and datasets
----------------------------------------------------

To explore these and other collections, try, e.g.,

.. prompt:: bash

   butler query-collections /repo/dc2 --chains=tree "2.2i/defaults"
   butler query-collections /repo/dc2 --chains=tree "u/mrawls/*"

These commands should print a list of collections that meet the search criteria.
The "tree chain" view is a handy way to see the "chained" data products that are included with each collection, such as calibs, skymaps, refcats, etc.

To see some available datasets for processing, try, e.g.,

.. prompt:: bash

   butler query-data-ids /repo/dc2 tract patch visit --collections='u/mrawls/DM-34827/defaults/4patch_4431' --where "skymap='DC2' AND band='g' AND instrument='LSSTCam-imSim'" --datasets "raw"

This command should print a list of data IDs that meet the search criteria, along with their tract, patch, and visit number.
Certain arguments are required after the ``--where``, including ``skymap`` and ``instrument``, while most others are optional, and may include ``band``, ``tract``, ``patch``, etc.

Processing Data with the AP Pipelines
=====================================

Now it's time to process some data.
In this guide, we will start with raws, run standard single frame processing (which includes :py:mod:`lsst.ip.isr.IsrTask`, :py:mod:`lsst.pipe.tasks.characterizeImage.CharacterizeImageTask`, and :py:mod:`lsst.pipe.tasks.calibrate.CalibrateTask`), and make good seeing coadd templates.

In a second pipeline, we will run difference imaging using the templates we just built and save the results in an Alert Production Database (APDB).

Building good seeing templates
------------------------------

The pipeline we will use lives in the ``ap_pipe`` package, and is the camera-specific ``ApTemplate.yaml`` pipeline.
To see it, either navigate to the `pipeline on GitHub <https://github.com/lsst/ap_pipe/blob/main/pipelines/LsstCamImSim/ApTemplate.yaml>`__ or display the pipeline on via the command line, e.g.,

.. prompt:: bash

   cat $AP_PIPE_DIR/pipelines/LsstCamImSim/ApTemplate.yaml

Note that this camera-specific ``ApTemplate.yaml`` pipeline imports both a camera-specific single-frame processing pipeline (sometimes called "processCcd") and a more generic AP Template building pipeline.

To visualize this pipeline, use ``pipetask build``, e.g.,

.. prompt:: bash

   pipetask build -p $AP_PIPE_DIR/pipelines/LsstCamImSim/ApTemplate.yaml --pipeline-dot ApTemplate.dot
   dot ApTemplate.dot -Tpng > ApTemplate.png

To run this pipeline, make up an appropriate output collection name (``u/USERNAME/OUTPUT-COLLECTION-1`` in the example below), and run

.. prompt:: bash

   pipetask run -j 4 -b /repo/dc2 -d "skymap='DC2' AND tract=4431 AND patch IN (9, 10, 16, 17) AND band='g'" -i 2.2i/defaults -o u/USERNAME/OUTPUT-COLLECTION-1 -p $AP_PIPE_DIR/pipelines/LsstCamImSim/ApTemplate.yaml --register-dataset-types

To tell the process to run in the background and write output to a logfile, you may wish to prepend ``pipetask run`` with ``nohup`` and postpend the command with ``> OUTFILENAME &``.
This will take some time, but when it's done, you should have calibrated exposures and a visit summary table, warps, and assembled good seeing coadds for use as templates.
We are now ready to run the rest of the AP Pipeline (namely difference imaging and source association).

Performing difference imaging and making an APDB
------------------------------------------------

This next step uses a second pipeline, which effectively includes :py:mod:`lsst.ip.diffim.subtractIamges.AlardLuptonSubtractTask`, :py:mod:`lsst.ip.diffim.detectAndMeasure.DetectAndMeasureTask`, :py:mod:`lsst.ap.association.TransformDiaSourceCatalogTask`, and :py:mod:`lsst.ap.association.DiaPipelineTask`.

The pipeline we will use also lives in the ``ap_pipe`` package, and is the camera-specific ``ApPipe.yaml`` pipeline. To see it, either navigate to the `pipeline on GitHub <https://github.com/lsst/ap_pipe/blob/main/pipelines/LsstCamImSim/ApPipe.yaml>`__ or display the pipeline on via the command line, e.g.,

.. prompt:: bash

   cat $AP_PIPE_DIR/pipelines/LsstCamImSim/ApPipe.yaml

This difference imaging pipeline requires coadds as inputs for use as templates, and treats all input raws as "science" images.

Unlike before, however, we need to make our own pipeline that imports this pipeline so we can configure the APDB URL. Create and save this pipeline yaml file as, e.g., ``My-DC2-ApPipe.yaml`` in your working directory:

.. prompt:: yaml

   description: My very own AP pipeline for LsstCam-imSim

   instrument: lsst.obs.lsst.LsstCamImSim
   imports:
   - location: $AP_PIPE_DIR/pipelines/LsstCamImSim/ApPipe.yaml

   tasks:
     diaPipe:
       class: lsst.ap.association.DiaPipelineTask
       config:
         apdb.isolation_level: READ_UNCOMMITTED
         apdb.db_url: 'PATH-TO-YOUR-APDB-HERE'

What to put for the ``apdb.db_url``? The simplest option, which works fine for relatively small processing runs, is to create an empty sqlite database in your working directory.
Larger runs will require using, e.g., postgres, which is beyond the scope of this guide.
To create an empty sqlite APDB:

.. prompt:: bash

   make_apdb.py -c isolation_level=READ_UNCOMMITTED -c db_url="PATH-TO-YOUR-APDB-HERE"

**The APDB must exist and be empty before you run the AP Pipeline.**
Note that sqlite APDBs require the ``isolation_level`` to be set to ``READ_UNCOMMITTED``, while postgres APDBs do not.
It is highly recommended to make a new APDB each time the AP Pipeline is rerun for any reason.
A typical ``apdb.db_url`` is, e.g., ``sqlite:////project/mrawls/my-working-directory/run1.db``.

Next, edit your pipeline file to have the same configs used with ``make_apdb.py`` --- the configs you set when making the APDB must match those in your AP Pipeline.

As before, to visualize the AP Pipeline, you may run, e.g.,

.. prompt:: bash

   pipetask build -p My-DC2-ApPipe.yaml --pipeline-dot My-DC2-ApPipe.dot
   dot My-DC2-ApPipe.dot -Tpng > My-DC2-ApPipe.png

You are now ready to run the AP Pipeline!
Notice you will need to substitute appropriate values for your input collection with templates and your desired new output collection name:

.. prompt:: bash

   pipetask run -j 4 -b /repo/dc2 -d "skymap='DC2' AND band='g'" -i u/USERNAME/OUTPUT-COLLECTION-1,u/mrawls/DM-34827/defaults/4patch_4431 -o u/USERNAME/OUTPUT-COLLECTION-2 -p My-DC2-ApPipe.yaml --register-dataset-types

What are the output data products?
==================================

When the AP Pipeline completes, you will have difference images, difference image source tables, and an APDB with populated tables (``DiaSource``, ``DiaObject``, etc.) for ``g`` band visits that fully overlap four patches of tract 4431.

A few analysis and plotting tools exist to explore the APDB and other AP Pipeline outputs.
In the future, these will live in `analysis_ap <https://github.com/lsst/analysis_ap>`__, but in the interim, many have a temporary home in `ap_pipe-notebooks <https://github.com/lsst-dm/ap_pipe-notebooks>`__, which is not formally part of the Science Pipelines.
One output from the AP Pipeline are are DIA (Difference Image Analysis) Source Tables, which but Butler can retrieve via ``goodSeeingDiff_diaSrcTable``.

To see what DIA Source Tables exist, query, e.g.,

.. prompt:: bash

   butler query-data-ids /repo/dc2 visit detector --collections="u/USERNAME/OUTPUT-COLLECTION-2" --where "skymap='DC2' AND band='g' AND instrument='LSSTCam-imSim'" --datasets "goodSeeingDiff_diaSrcTable"

The APDB also contains several tables with information about DIA Sources, DIA Objects, and Solar System Objects.
Recall that Objects represent real astrophysical things, and are created by spatially associating per-visit Sources.
The DIA prefix indicates we are talking about Sources and Objects in difference images.
More information about the APDB schema is available in `dax_apdb <https://github.com/lsst/dax_apdb/blob/main/python/lsst/dax/apdb/apdbSchema.py>`__.

.. note::

   None of the following is a formally supported APDB user interface.
   It one way to load a table from the APDB into memory in python and make a quick plot to see where the associated DIA Objects fall on the sky.
   It also includes an example of how to load a ``goodSeeingDiff_diaSrcTable`` with the Butler for further analysis.

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
   connection = sqlite3.connect('PATH-TO-YOUR-APDB-HERE')
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

Describing how to set up a PostgreSQL APDB is beyond the scope of this guide.
Members of the Data Management Team may wish to reference `this non-public guide <https://community.lsst.org/t/using-postgresql-at-ncsa-for-an-apdb/4603>`__ for how to use an existing NCSA PostgreSQL database as an APDB.
One key difference between using an sqlite APDB versus a PostgreSQL APDB is that the former is a file on disk created from scratch when running ``make_apdb.py``.
The latter requires a database to already exist, and ``make_apdb.py`` turns the PostgreSQL database's default schema into an empty APDB.
As before, you will still need to run, e.g.,

.. prompt:: bash

   make_apdb.py -c db_url="postgresql://USER@DB_ADDRESS/DB_NAME"

(being sure to replace ``USER``, ``DB_ADDRESS``, and ``DB_NAME`` with the correct values).
Next, use the documentation for :py:mod:`lsst.ctrl.bps` to `define a submission <https://pipelines.lsst.io/v/weekly/modules/lsst.ctrl.bps/quickstart.html#defining-a-submission>`__ by creating two BPS configuration files --- one for the template-building step and one for the difference-imaging step.
Save these BPS configuration files as ``ApTemplate-DC2-bps.yaml`` and ``ApPipe-DC2-bps.yaml``.

.. note::

   The :py:mod:`lsst.ctrl.bps` module is well-documented, and is the first place to look for how to submit a batch processing run on the lsst-devl machines.

Ensure the ``pipelineYaml`` keyword points to the appropriate ApTemplate and ApPipe pipelines in each BPS configuration file, and that you specify appropriate values for ``inCollection``, ``outCollection``, and ``dataQuery`` like before on the command line with ``pipetask run`` and the ``-i``, ``-o``, and ``-d`` arguments.

For example, to make good seeing templates using all available patches and bands in two entire tracts, you may wish to use a data query like ``instrument='LSSTCam-imSim' and tract in (3828, 3829) and skymap='DC2'``.

When you are ready to submit your first BPS run to build templates, follow the documentation to `submit a run <https://pipelines.lsst.io/v/weekly/modules/lsst.ctrl.bps/quickstart.html#submitting-a-run>`__, e.g.,

.. prompt:: bash

   bps submit ApTemplate-DC2-bps.yaml

Once the templates are built, the second BPS configuration file will need to have two input collections: the output collection from the first run and a collection with raw science images (such as ``2.2i/defaults/test-med-1``).
To submit the second BPS run and perform difference imaging and populate the PostgreSQL APDB, run, e.g.,

.. prompt:: bash

   bps submit ApPipe-DC2-bps.yaml
