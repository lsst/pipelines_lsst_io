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

- `ap\_verify <https://github.com/lsst/ap_verify>`_
- `atmospec <https://github.com/lsst/atmospec>`_
- `cbp <https://github.com/lsst/cbp>`_
- `cp\_pipe <https://github.com/lsst/cp_pipe>`_
- `cp\_verify <https://github.com/lsst/cp_verify>`_
- `ctrl\_bps <https://github.com/lsst/ctrl_bps>`_
- `ctrl\_mpexec <https://github.com/lsst/ctrl_mpexec>`_
- `display\_astrowidgets <https://github.com/lsst/display_astrowidgets>`_
- `display\_firefly <https://github.com/lsst/display_firefly>`_
- `display\_matplotlib <https://github.com/lsst/display_matplotlib>`_
- `drp\_pipe <https://github.com/lsst/drp_pipe>`_
- `faro <https://github.com/lsst/faro>`_
- `fgcmcal <https://github.com/lsst/fgcmcal>`_
- `jointcal <https://github.com/lsst/jointcal>`_
- `lsst\_bps_plugins <https://github.com/lsst/lsst_bps_plugins>`_ (contains supported BPS plugins)
- `lsst\_obs <https://github.com/lsst/lsst_obs>`_ (contains supported "obs" packages)
- `meas\_extensions_convolved <https://github.com/lsst/meas_extensions_convolved>`_
- `meas\_extensions_gaap <https://github.com/lsst/meas_extensions_gaap>`_
- `meas\_extensions_photometryKron <https://github.com/lsst/meas_extensions_photometryKron>`_
- `meas\_extensions_scarlet <https://github.com/lsst/meas_extensions_scarlet>`_
- `meas\_extensions_shapeHSM <https://github.com/lsst/meas_extensions_shapeHSM>`_
- `meas\_extensions_trailedSources <https://github.com/lsst/meas_extensions_trailedSources>`_
- `sdm\_schemas <https://github.com/lsst/sdm_schemas>`_
- `verify <https://github.com/lsst/verify>`_

Example installation (:ref:`more info <newinstall-install>`):

.. code-block:: bash

   eups distrib install lsst_distrib -t <tag>
   setup lsst_distrib

.. _EUPS: https://github.com/RobertLuptonTheGood/eups
