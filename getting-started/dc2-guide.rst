########################################
Processing DC2 data with the Gen3 Butler
########################################

The data explored in this guide is simulated data, the same kind used for Rubin's Data Preview 0 (DP0).

.. note::

   This guide assumes the user has access to a shared "Gen3" Butler repository containing data from the Dark Energy Science Collaboration (DESC)'s Data Challenge 2 (DC2), most likely on the ``lsstdevl`` machines at NCSA.
   This guide further assumes the user has a recently-built version of :py:mod:`lsst.distrib` from the LSST Science Pipelines.
   The instructions in this guide were verified to work in July 2021 using ``rubin-env 0.6.0`` with the weekly tagged ``w_2021_30``.
   Finally, this guide assumes the user is interested in running the Alert Production (AP) pipeline on this data using good seeing templates.

What's in the Shared DC2 Butler Repository?
===========================================

* The instrument is called ``LSSTCam-imSim``
* The obs-package is ``obs_lsst``, i.e., :py:mod:`lsst.obs.lsst` (note ``imsim`` subdirectories within)
* The skymap is called ``DC2``
* Patches go from 0 to 48
* Detectors go from 0 to 188
* Available bands are ``ugrizy``
* Data exist for some tracts in the ~2553–5074 range, and as examples below show, commonly used tracts include 3828 and 3829
* One set of reference catalogs are called ``cal_ref_cat_2_2``, and have some filtermap definitions that must be specified
* On NCSA's ``lsstdevl`` in ``/repo/dc2``, tracts 3828 and 3829 are in the collection ``2.2i/defaults/test-med-1``
* A smaller CI dataset, just patch 24 in tract 3828, is in ``2.2i/defaults/ci_imsim`` and corresponds to the GitHub repo ``testdata_ci_imsim``

To see some collections, try, e.g.,

.. prompt:: bash

   butler query-collections /repo/dc2 --chains=tree "2.2i/*"
   butler query-collections /repo/dc2 --chains=tree "u/mrawls/*"

These commands should print a list of collections that meet the search criteria.
The "tree chain" view is a handy way to see the "chained" data products that are included with each collection, such as calibs, skymaps, refcats, etc.

To see some available datasets for processing, try, e.g.,

.. prompt:: bash

   butler query-data-ids /repo/dc2 tract patch visit --collections='2.2i/defaults/test-med-1' --where "skymap='DC2' AND band='g' AND tract=3828 AND patch=47 AND instrument='LSSTCam-imSim'" --datasets "raw"

This command should print a list of data IDs that meet the search criteria, along with their tract, patch, and visit number.
Certain arguments are required after the ``--where``, including ``skymap`` and ``instrument``, while most others are optional.

Processing Data
===============

Now it's time to process some data.
In this guide, we will start with raws, run "processCcd" (which includes :py:mod:`lsst.ip.isr.IsrTask`, :py:mod:`lsst.pipe.tasks.characterizeImage.CharacterizeImageTask`, and :py:mod:`lsst.pipe.tasks.calibrate.CalibrateTask`), and make good seeing coadd templates.

In a second pipeline, we will run difference imaging using the templates we just built and save the results in an Alert Production Database (APDB).

Building good seeing templates
------------------------------

Here is the pipeline we will use.
Note that multiple python configuration options can be used by typing a placeholder continuation character (e.g., ``|``) followed by one python config declaration per line.

.. prompt:: yaml

   description: An AP pipeline for building templates with LsstCam-imSim data

   instrument: lsst.obs.lsst.LsstCamImSim
   imports:
   - location: $AP_PIPE_DIR/pipelines/ApTemplate.yaml
   tasks:
     isr:
       class: lsst.ip.isr.IsrTask
       config:
         connections.newBFKernel: bfk
         doBrighterFatter: True
     calibrate:
       class: lsst.pipe.tasks.calibrate.CalibrateTask
       config:
         connections.astromRefCat: 'cal_ref_cat_2_2'
         connections.photoRefCat: 'cal_ref_cat_2_2'
         astromRefObjLoader.ref_dataset_name: 'cal_ref_cat_2_2'
         photoRefObjLoader.ref_dataset_name: 'cal_ref_cat_2_2'
         python: |
           config.astromRefObjLoader.filterMap = {band: 'lsst_%s_smeared' % (band) for band in 'ugrizy'};
           config.photoRefObjLoader.filterMap = {band: 'lsst_%s_smeared' % (band) for band in 'ugrizy'};
   subsets:
     singleFrameAp:
       subset:
         - isr
         - characterizeImage
         - calibrate
         - consolidateVisitSummary
       description: >
         Tasks to run for single frame processing that are necessary to use the good seeing selector to build coadds for use as difference imaging templates.

This example pipeline imports a pipeline from :py:mod:`lsst.ap.pipe` you may `view on GitHub <https://github.com/lsst/ap_pipe/blob/main/pipelines/ApTemplate.yaml>`__.
There are some special configurations concerning reference catalogs that must be set for this camera and/or dataset, so the example pipeline above lists the ``calibrate`` task explicitly to add custom configurations.

To run this example pipeline, save it as ``ApTemplate-DC2.yaml``, choose an appropriate output collection name (``u/USERNAME/OUTPUT-COLLECTION-1`` in the example below), and run

.. prompt:: bash

   pipetask run -j 12 -b /repo/dc2 -d "band='g' AND skymap='DC2' AND tract=3829" -i 2.2i/defaults/test-med-1 -o u/USERNAME/OUTPUT-COLLECTION-1 -p ApTemplate-DC2.yaml#singleFrameAp --register-dataset-types

This will take some time, but when it's done, you should have calibrated exposures and a visit summary table ready for making warps, selecting the best seeing visits, and assembling coadds for use as difference imaging templates.
To continue, run:

.. prompt:: bash

   pipetask run -j 12 -b /repo/dc2 -d "skymap='DC2' AND tract=3829 AND patch=47" -i u/USERNAME/OUTPUT-COLLECTION-1 -o u/USERNAME/OUTPUT-COLLECTION-2 -p ApTemplate-DC2.yaml#makeTemplate --register-dataset-types

This will also take some time.
When it is complete, you should have good seeing coadds covering the entirety of patch 47 in tract 3829 for multiple bands and be ready to run the rest of the AP Pipeline (namely difference imaging and source association).

Performing difference imaging to make an APDB
---------------------------------------------

This next step uses a second pipeline, which effectively includes :py:mod:`lsst.ip.diffim.subtractIamges.AlardLuptonSubtractTask`, :py:mod:`lsst.ip.diffim.detectAndMeasure.DetectAndMeasureTask`, :py:mod:`lsst.ap.association.TransformDiaSourceCatalogTask`, and :py:mod:`lsst.ap.association.DiaPipelineTask`.

.. prompt:: yaml

   description: An AP pipeline for difference imaging with LsstCam-imSim

   instrument: lsst.obs.lsst.LsstCamImSim
   imports:
   - location: ApTemplate-DC2.yaml
     exclude:  # These tasks are not necessary, as we already have templates
       - consolidateVisitSummary
       - selectGoodSeeingVisits
       - makeWarp
       - assembleCoadd
   - location: $AP_PIPE_DIR/pipelines/ApPipe.yaml
     exclude:  # These tasks come from the ApTemplate-DC2 pipeline instead
       - isr
       - characterizeImage
       - calibrate

This difference imaging pipeline uses the good seeing templates we built and treats all the DP0 defaults as input "science" images.

**This is a two-step process.**
First, create an empty sqlite APDB:

.. prompt:: bash

   make_apdb.py -c isolation_level=READ_UNCOMMITTED -c db_url="sqlite:////PATH-TO-DESIRED-APDB/ApPipeTest1.db"

Note that the APDB must be empty, and it is highly recommended to make a new one each time the AP Pipeline is rerun for any reason.

Second, run the pipeline:

.. prompt:: bash

   pipetask run -j 12 -b /repo/dc2 -d "skymap='DC2' AND tract=3829 AND patch=47" -i u/USERNAME/OUTPUT-COLLECTION-2,2.2i/defaults/test-med-1 -o u/USERNAME/OUTPUT-COLLECTION-3 -p ApPipe-DC2.yaml -c diaPipe:apdb.isolation_level=READ_UNCOMMITTED -c diaPipe:apdb.db_url="sqlite:////PATH-TO-DESIRED-APDB/ApPipeTest1.db" --register-dataset-types

When this pipeline completes, you should have difference images and an APDB with populated tables (``DiaSource``, ``DiaObject``, etc.) for multiple bands in patch 47 of tract 3829 of this dataset.

Processing Data with BPS
========================

The example data processing steps above assume a relatively small data volume (a single patch), so running from the command line and using an sqlite APDB is appropriate.
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

Ensure the ``pipelineYaml`` keyword points to ``ApTemplate-DC2.yaml`` and ``ApPipe-DC2.yaml`` in each configuration file, respectively, and that you specify appropriate values for ``inCollection``, ``outCollection``, and ``dataQuery`` like before on the command line with ``pipetask run`` and the ``-i``, ``-o``, and ``-d`` arguments.

For example, to make good seeing templates using all available patches and bands, you may wish to use a less restrictive data query like ``instrument='LSSTCam-imSim' and tract in (3828, 3829) and skymap='DC2'``.

When you are ready to submit your first BPS run to build templates, follow the documentation to `submit a run <https://pipelines.lsst.io/v/weekly/modules/lsst.ctrl.bps/quickstart.html#submitting-a-run>`__, e.g.,

.. prompt:: bash

   bps submit ApTemplate-DC2-bps.yaml

Once the templates are built, the second BPS configuration file will need to have two input collections: the output collection from the first run and a collection with raw science images (such as ``2.2i/defaults/test-med-1``).
To submit the second BPS run and perform difference imaging and populate the PostgreSQL APDB, run, e.g.,

.. prompt:: bash

   bps submit ApPipe-DC2-bps.yaml

