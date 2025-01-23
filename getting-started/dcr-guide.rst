######################################
Generating DCR Coadds with LSST ComCam
######################################

A walkthrough for building differential chromatic refraction (DCR) coadds by running the
`dcrAssembleCoaddTask` on an example set of ComCam image data. Prior to generating DCR coadds, you must
have image templates.

.. note::

   This guide assumes the user has access to a shared Butler repository containing data from LSST ComCam via
   the `US Data Facility (USDF) <https://developer.lsst.io/usdf/storage.html>`__. This guide further assumes
   the user has a recently-built version of ``lsst.distrib`` from the `LSST Science Pipelines
   <https://developer.lsst.io/usdf/stack.html>`__ (circa ``w_2022_30`` or later).

Generating AP Templates
=======================
For detailed instructions on generating AP Templates, please see the `Building good seeing templates
<https://pipelines.lsst.io/getting-started/dc2-guide.html>`__ guide for details.


Assembling DCR Coadds
=====================
To generate DCR coadds, you must use the `dcrAssembleCoaddTask` found in the `drp_tasks` package. This will
require image templates. Note: You will need to register your DCR subfilters prior to creating DCR coadds by
using the following code:

.. code-block:: python
    butler register-dcr-subfilters /repo/main 3 'g'


Creating Your DCR Assemble Coadd Pipeline
-----------------------------------------
The first step in generating DCR coadds is to make a pipeline that runs the `dcrAssembleCoaddTask` from the
LSST 'drp_tasks' package. A sample `dcrAssembleCoadd` pipeline is shown below.

.. code-block:: python

    :name: dcrAssembleCoadd.yaml

    description: The DCR assemble coadd pipeline for LSSTComCam

    parameters:
      coaddName: dcr
    tasks:
      DcrAssembleCoaddTask:
        class: lsst.drp.tasks.dcr_assemble_coadd.DcrAssembleCoaddTask
        config:
          effectiveWavelength: 478.5
          bandwidth: 147.0

To visualize your pipeline, you may wish to use `pipetask build` e.g.,

.. code-block:: shell
    pipetask build -p $AP_PIPE_DIR/pipelines/LSSTComCam/dcrAssembleCoadd.yaml --pipeline-dot dcrCoadd.dot
    dot dcrCoadd.dot -Tpng > dcrCoadd.png


Run `dcrAssembleCoadd` Pipeline
-------------------------------
To run this task and generate coadds, make up an appropriate output collection name
(u/USERNAME/OUTPUT-COLLECTION in the example below), and run

.. code-block:: shell
    pipetask run -j 4 -b /repo/main -d "skymap='lsst_cells_v1' AND visit in (2024112800132,2024112900230)
    AND detector in (0,1) AND band='g'" -i path/to/your/templates,LSSTComCam/defaults
    -o u/USERNAME/OUTPUT-COLLECTION -p path/to/your/dcrAssembleCoadd.yaml

To tell the process to run in the background and write output to a logfile, you may wish to prepend pipetask
run with nohup and postpend the command with > OUTFILENAME &. Once complete, you should have generated DCR
coadds from your templates.


Assembling DCR Coadds with BPS
------------------------------
To assemble DCR coadds using the Batch Processing System (BPS) you will need to create a BPS submission file
that runs the `dcrAssembleCoadd` pipeline file you created above (this will be you `pipelineYaml` input). A
sample BPS submit file is shown below:

.. code-block:: python

    :name: bps_submit_dcrAssembleCoadd.yaml

    dmnum: '34910'
    weekly: 'w_2025_05'

    pipelineYaml: '/path/to/your/dcrAssembleCoaddTask.yaml'

    project: ApPipe-ComCam
    campaign: DM-{dmnum}

    payload:
      payloadName: DM-{dmnum}/{weekly}/ComCam-dcr-assembleCoadd
      butlerConfig: /sdf/group/rubin/repo/main/butler.yaml
      inCollection: path/to/your/templates,LSSTComCam/defaults
      dataQuery: "instrument='LSSTComCam' and visit in (2024112800132,2024112900230) and detector in (0,1) and skymap='lsst_cells_v1' and band='g'"

    extraQgraphOptions: "--dataset-query-constraint off"

    provisionResources: true
    provisioning:
      provisioningMaxWallTime: 1-00:00:00
