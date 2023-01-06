#############################
Top-level packages to install
#############################

The LSST Science Pipelines are part of LSST's EUPS_ package stack.
This means that the Science Pipelines software is actually a collection of packages that you install and set up together.
By specifying different **top-level packages** to the :ref:`eups distrib install <newinstall-install>` and :doc:`setup <setup>` commands, you can control the size of the software installation or add new capabilities.

This page describes the common top-level packages that make up the LSST Science Pipelines and related EUPS stacks.

lsst\_apps
==========

This package provides the only core frameworks and algorithmic code that we expect to be of interest to most users.
It may be convenient when space is at a premium.

Example installation (:ref:`more info <newinstall-install>`):

.. code-block:: bash

   eups distrib install lsst_apps -t <tag>
   setup lsst_apps

lsst\_distrib
=============

This package provides all of the core Science Pipelines functionality, together with additional measurement algorithms, support for a wider variety of instrumentation, and process execution middleware designed for running pipelines on a cluster.
In addition to the contents of ``lsst_apps``, it provides the following packages:

- `ap_verify <https://github.com/lsst/ap_verify>`_
- `cbp <https://github.com/lsst/cbp>`_
- `cp\_pipe <https://github.com/lsst/cp_pipe>`_
- `ctrl\_mpexec <https://github.com/lsst/ctrl_mpexec>`_
- `display\_firefly <https://github.com/lsst/display_firefly>`_
- `display\_matplotlib <https://github.com/lsst/display_matplotlib>`_
- `eigen <https://github.com/lsst/eigen>`_ (Eigen is also installed through our :ref:`Conda environment <system-prereqs>`; this version is only necessary to support Jointcal)
- `fgcm <https://github.com/lsst/fgcm>`_
- `fgcmcal <https://github.com/lsst/fgcmcal>`_
- `jointcal <https://github.com/lsst/jointcal>`_
- `jointcal\_cholmod <https://github.com/lsst/jointcal_cholmod>`_
- `lsst_obs <https://github.com/lsst/lsst_obs>`_
- `meas\_extensions_convolved <https://github.com/lsst/meas_extensions_convolved>`_
- `meas\_extensions_photometryKron <https://github.com/lsst/meas_extensions_photometryKron>`_
- `meas\_extensions_shapeHSM <https://github.com/lsst/meas_extensions_shapeHSM>`_
- `obs\_cfht <https://github.com/lsst/obs_cfht>`_
- `obs\_decam <https://github.com/lsst/obs_decam>`_
- `obs\_decam_data <https://github.com/lsst/obs_decam_data>`_
- `obs\_lsst <https://github.com/lsst/obs_lsst>`_
- `obs\_lsst_data <https://github.com/lsst/obs_lsst_data>`_
- `obs\_subaru <https://github.com/lsst/obs_subaru>`_
- `obs\_subaru\_data <https://github.com/lsst/obs_subaru_data>`_
- `synpipe <https://github.com/lsst/synpipe>`_

Example installation (:ref:`more info <newinstall-install>`):

.. code-block:: bash

   eups distrib install lsst_distrib -t <tag>
   setup lsst_distrib

.. _EUPS: https://github.com/RobertLuptonTheGood/eups
