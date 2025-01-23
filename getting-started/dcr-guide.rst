######################################
Generating DCR Coadds with LSST ComCam
######################################

This article walks through the building of differential chromatic refraction (DCR) coadds by running the
``dcrAssembleCoaddTask`` on an example set of ComCam image data. Prior to generating DCR coadds, image
templates must already be imported.

.. note::

   This guide assumes the user has access to a shared Butler repository containing data from LSST ComCam via
   the `US Data Facility (USDF) <https://developer.lsst.io/usdf/storage.html>`__. This guide further assumes
   the user has a recently-built version of ``lsst.distrib`` from the `LSST Science Pipelines
   <https://developer.lsst.io/usdf/stack.html>`__ (circa ``w_2025_09`` or later).

Importing AP Templates
=======================
For detailed instructions on importing AP Templates, see the `importing good seeing templates
<https://pipelines.lsst.io/getting-started/dc2-guide.html>`__ guide for details.


Assembling DCR Coadds
=====================
To generate DCR coadds, use the ``dcrAssembleCoaddTask`` found in the ``drp_tasks`` package. This requires
image templates. The DCR subfilters must be registered prior to creating DCR coadds by following the
`register-dcr-subfilters guide <https://pipelines.lsst.io/modules/lsst.daf.butler/scripts/butler.html#butler-register-dcr-subfilters>`__. The ``dcrNumSubfilters`` in the config must match the number
of subfilters specified when running ``register-dcr-subfilters``.


Creating Your DCR Assemble Coadd Pipeline
-----------------------------------------
The first step in generating DCR coadds is to make a pipeline that runs the ``dcrAssembleCoaddTask`` from the
LSST ``drp_tasks`` package. A sample ``dcrAssembleCoadd`` pipeline is shown below.

.. code-block:: yaml

    description: A DCR assemble coadd pipeline for LSSTComCam.
    instrument: lsst.obs.lsst.LsstComCam

    parameters:
      coaddName: dcr
    tasks:
      DcrAssembleCoaddTask:
        class: lsst.drp.tasks.dcr_assemble_coadd.DcrAssembleCoaddTask
        config:
          effectiveWavelength: 478.5 # in nm
          bandwidth: 147.0 # in nm

Save the pipeline file as ``dcrAssembleCoadd.yaml``. To visualize the pipeline, consider using
``pipetask build``. For example,

.. code-block:: bash

    pipetask build -p path/to/your/dcrAssembleCoadd.yaml --pipeline-dot dcrCoadd.dot
    dot dcrCoadd.dot -Tpng > dcrCoadd.png


Assembling DCR Coadds with ``pipetask run``
-------------------------------------------
To generate DCR coadds using ``pipetask run``, make an appropriate output collection name
(``u/USERNAME/OUTPUT-COLLECTION`` in the example below), and then use the following code.

.. code-block:: bash

    pipetask run -j 4 -b /repo/main -d "skymap='lsst_cells_v1' AND visit in (2024112800132,2024112900230)
    AND detector in (0,1) AND band='g'" -i path/to/your/templates,LSSTComCam/defaults
    -o u/USERNAME/OUTPUT-COLLECTION -p path/to/your/dcrAssembleCoadd.yaml

To tell the process to run in the background and write output to a logfile, consider prepending pipetask
run with ``nohup`` and postpend the command with ``> OUTFILENAME &``. Once complete, the DCR coadds from
your templates should have generated.


Assembling DCR Coadds with BPS
------------------------------
To assemble DCR coadds using the `Batch Processing System (BPS) <https://github.com/lsst/ctrl_bps/blob/417d56d35c7585def97b602fca1fa377d7ccc49e/doc/lsst.ctrl.bps/quickstart.rst>`__, create a BPS submission file
that runs the ``dcrAssembleCoadd`` pipeline file created above (this is the ``pipelineYaml`` input).
Below is a sample BPS submit file.

.. code-block:: yaml

    pipelineYaml: '/path/to/your/dcrAssembleCoaddTask.yaml'

    project: ComCam-DCRCoadds
    campaign: ComCam-dcr-assembleCoadd

    payload:
      payloadName: ComCam-dcr-assembleCoadd
      butlerConfig: /sdf/group/rubin/repo/main/butler.yaml
      inCollection: path/to/your/templates,LSSTComCam/defaults
      dataQuery: "instrument='LSSTComCam' and visit in (2024112800132,2024112900230) and detector in (0,1) and skymap='lsst_cells_v1' and band='g'"

    extraQgraphOptions: "--dataset-query-constraint off"

    provisionResources: true
    provisioning:
      provisioningMaxWallTime: 1-00:00:00

Save the file as ``bps_submit_dcrAssembleCoadd.yaml``.
