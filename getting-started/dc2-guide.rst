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
* The skymap is called ``DC2_cells_v1``
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

   butler query-data-ids /repo/dc2 tract patch visit --collections='u/mrawls/DM-34827/defaults/4patch_4431' --where "skymap='DC2_cells_v1' AND band='r' AND instrument='LSSTCam-imSim'" --datasets "raw"

This command should print a list of data IDs that meet the search criteria, along with their tract, patch, and visit number.
Certain arguments are required after the ``--where``, including ``skymap`` and ``instrument``, while most others are optional, and may include ``band``, ``tract``, ``patch``, etc.

Processing Data with the AP Pipelines
=====================================

Now it's time to process some data.
The pipeline ``ApPipe.yaml`` will be used to run difference imaging using a set of template files.
In this guide, good seeing templates are assumed to have already been constructed using the :py:class:`~lsst.pipe.tasks.selectImages.BestSeeingQuantileSelectVisitsTask` and the :py:class:`~lsst.drp.tasks.assemble_coadd.CompareWarpAssembleCoaddTask`.

The ``ApPipe.yaml`` pipeline starts with single frame processing on raw images, followed by :py:class:`~lsst.ip.diffim.subtractImages.AlardLuptonSubtractTask`, :py:class:`~lsst.ip.diffim.detectAndMeasure.DetectAndMeasureTask`, :py:class:`~lsst.ap.association.transformDiaSourceCatalog.TransformDiaSourceCatalogTask`, and :py:class:`~lsst.ap.association.diaPipe.DiaPipelineTask`.
The final results include difference images, some output catalogs, and an Alert Production Database (APDB).

Importing good seeing templates
-------------------------------

As mentioned above, a series of good seeing templates are assumed to have been generated already.
For convenience, a templates import script is available in the `ap_verify_ci_dc2` repository which assists with this process: `import_templates.py <https://github.com/lsst/ap_verify_ci_dc2/blob/main/scripts/import_templates.py>`__.

An example usage of this script is:

.. code-block:: shell

    import_templates.py \
    -b /repo/dc2 \
    -t $MY_COLLECTION \
    -w "skymap='DC2_cells_v1' and tract=4431 and patch IN (9,10,16,17) and band='r'"

*where*

    `$MY_COLLECTION`
        The collection containing the templates to import.

We are now ready to run the AP Pipeline (namely difference imaging and source association).

Visualizing a pipeline
----------------------

To visualize a pipeline, you may wish to use ``pipetask build``, e.g.,

.. code-block:: shell

    pipetask build \
    -p $AP_PIPE_DIR/pipelines/LSSTCam-imSim/ApPipe.yaml \
    -c  parameters:apdb_config=foo \
    --pipeline-dot ApPipe.dot

    dot ApPipe.dot -Tpng > ApPipe.png

Alternately, navigate to `this website that serves visualizations of all the AP and DRP pipelines <https://tigress-web.princeton.edu/~lkelvin/pipelines/current>`__.
Click through to ``ap_pipe``, then ``LSSTCam-imSim``, and finally ``ApPipe`` to find a PDF visualizing all the pipeline inputs, outputs, and intermediate data products.
This PDF is auto-generated each week using the same ``pipetask build`` command as shown above.

Performing difference imaging and making an APDB
------------------------------------------------

This next step uses a second pipeline, which begins once again with single frame processing.
If you choose to reuse some or all of the same input raw exposures, all previously-run steps will automatically be skipped and pre-existing outputs used.
Afterwards, it performs difference imaging and saves the results in an Alert Production Database (APDB).

The pipeline we will use also lives in the ``ap_pipe`` package, and is the camera-specific ``ApPipe.yaml`` pipeline. To see it, either navigate to the `pipeline on GitHub <https://github.com/lsst/ap_pipe/blob/main/pipelines/LSSTCam-imSim/ApPipe.yaml>`__ or display the pipeline on via the command line, e.g.,

.. prompt:: bash

   cat $AP_PIPE_DIR/pipelines/LSSTCam-imSim/ApPipe.yaml

This difference imaging pipeline requires coadds as inputs for use as templates, and treats all input raws as "science" images.

Unlike before, however, we need to create an empty APDB for the final step of the pipeline to connect and write to.
If the APDB is not empty, you can pass ``--drop`` in the ``apdb-cli create-sql`` command to drop the existing tables.
The simplest option, which works fine for relatively small processing runs, is to create an empty sqlite database in your working directory.
Larger runs will require using, e.g., PostgreSQL.
To create an empty sqlite APDB:

.. prompt:: bash

   apdb-cli create-sql sqlite:////path/to/my/database/apdb.sqlite3 apdb_config.py
   apdb-cli metadata set apdb_config.py instrument LSSTCam-imSim

**The APDB must exist and be empty before you run the AP Pipeline.**
It is highly recommended to make a new APDB each time the AP Pipeline is rerun for any reason.

The configs you set when making the APDB must match those you give the AP Pipeline at runtime.

As before, to visualize the AP Pipeline, you may navigate to `the website with visualizations of all the AP and DRP pipelines <https://tigress-web.princeton.edu/~lkelvin/pipelines/current>`__.
Click through to ``ap_pipe``, then ``LSSTCam-imSim``, and finally ``ApPipe`` to find a PDF visualizing all the pipeline inputs, outputs, and intermediate data products.
This PDF is auto-generated each week using an analogous ``pipetask build`` command as shown above for ``ApPipe.yaml``.

You are now ready to run the AP Pipeline!
You will need to substitute appropriate values for your input collections, your desired new output collection, and your APDB URL in order to run

.. prompt:: bash

   pipetask run -j 4 -b /repo/dc2 -d "skymap='DC2_cells_v1' AND band='r'" -i u/USERNAME/OUTPUT-COLLECTION-1,u/mrawls/DM-34827/defaults/4patch_4431 -o u/USERNAME/OUTPUT-COLLECTION-2 -p $AP_PIPE_DIR/pipelines/LSSTCam-imSim/ApPipe.yaml -c parameters:apdb_config=apdb_config.py

What are the output data products?
==================================

When the AP Pipeline completes, you will have difference images, difference image source tables, and an APDB with populated tables (``DiaSource``, ``DiaObject``, etc.) for ``r`` band visits that fully overlap four patches of tract 4431.

A few analysis and plotting tools exist to explore the APDB and other AP Pipeline outputs.
These live in `analysis_ap <https://github.com/lsst/analysis_ap>`__.
One output from the AP Pipeline are DIA (Difference Image Analysis) Source Tables, which the Butler can retrieve via ``goodSeeingDiff_diaSrcTable``.

To see what DIA Source Tables exist, query, e.g.,

.. prompt:: bash

   butler query-data-ids /repo/dc2 visit detector --collections="u/USERNAME/OUTPUT-COLLECTION-2" --where "skymap='DC2_cells_v1' AND band='r' AND instrument='LSSTCam-imSim'" --datasets "goodSeeingDiff_diaSrcTable"

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
   skymap='DC2_cells_v1'
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
One key difference between using an sqlite APDB versus a PostgreSQL APDB is that the former is a file on disk created from scratch when running ``apdb-cli create-sql``.
The latter requires a database to already exist and creation of the database is beyond the scope of this guide.

As before, to create an empty sqlite APDB you will still need to run, e.g.,

.. prompt:: bash

   apdb-cli create-sql sqlite:////path/to/my/database/apdb.sqlite3 apdb_config.py
   apdb-cli metadata set apdb_config.py instrument LSSTCam-imSim

When working with a central PostgreSQL database (APDB), ``apdb-cli create-sql`` turns the specified schema (via the ``namespace`` config option) in an existing PostgreSQL database into an empty APDB. 
If the APDB is not empty, you can pass ``--drop`` in the ``apdb-cli create-sql`` command to drop the existing tables.
To create a PostgreSQL APDB for a BPS configuration file that runs ``ApPipe.yaml``, these arguments are instead required to be passed into ``apdb-cli``:

.. prompt:: bash

   apdb-cli create-sql --namespace DESIRED_POSTGRES_SCHEMA_NAME postgresql://rubin@usdf-prompt-processing-dev.slac.stanford.edu/lsst-devl apdb_config.py
   apdb-cli metadata set apdb_config.py instrument LSSTCam-imSim

.. note::

    This examples uses the ``usdf-prompt-processing-dev`` server which only works in the development environment at the USDF.
    Please replace it with your postgres server address if you are running it elsewhere.

Next, use the documentation for :py:mod:`lsst.ctrl.bps` to `define a submission <https://pipelines.lsst.io/v/weekly/modules/lsst.ctrl.bps/quickstart.html#defining-a-submission>`__ by creating a BPS configuration file to perform difference-imaging.
Save the BPS configuration file as ``ApPipe-DC2-bps.yaml``.

.. note::

   The :py:mod:`lsst.ctrl.bps` module is well-documented, but at the time of this writing, best practices for running BPS at the USDF are still in development.
   Refer to the `USDF documentation pages <https://developer.lsst.io/usdf/batch.html>`__ for the latest recommendations.
   There is likely a set of default configurations users must import or place directly in their BPS configuration file that pertain to the underlying architecture for batch job submissions.

Ensure the ``pipelineYaml`` keyword points to the appropriate ApPipe pipeline in the BPS configuration file, and that you specify appropriate values for ``butlerConfig``, ``inCollection``, ``outCollection`` (or ``payloadName``, which may be used to construct ``outCollection``), and ``dataQuery``.
These values mirror those on the command line via ``pipetask run`` and the ``-b``, ``-i``, ``-o``, and ``-d`` arguments, respectively.

For example, to generate difference imaging outputs using all available patches and bands in two entire tracts, you may wish to use a data query like ``instrument='LSSTCam-imSim' and tract in (3828, 3829) and skymap='DC2_cells_v1'``.

When you are ready to submit your BPS run, follow the documentation to `submit a run <https://pipelines.lsst.io/v/weekly/modules/lsst.ctrl.bps/quickstart.html#submitting-a-run>`__, e.g.,

.. prompt:: bash

   bps submit ApPipe-DC2-bps.yaml

This BPS configuration file may need to have more than one input collection, for example, the output collection containing the templates and a collection with raw science images.
Additionally, depending on the size of the run, you may wish to utilize ``nohup`` or ``screen`` to have it run in the background.
