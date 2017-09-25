#############################
Top-level packages to install
#############################

The LSST Science Pipelines are part of LSST's EUPS_ package stack.
This means that the Science Pipelines software is actually a collection of packages that you install and set up together.
By specifying different **top-level packages** to the :ref:`eups distrib install <newinstall-install>` and :doc:`setup <setup>` commands, you can control the size of the software installation or add new capabilities.

This page describes the common top-level packages that make up the LSST Science Pipelines and related EUPS stacks.

lsst\_apps
==========

``lsst_apps`` provides the core packages that LSST will use in operations.

Example installation (:ref:`more info <newinstall-install>`):

.. code-block:: bash

   eups distrib install lsst_apps -t <tag>
   setup lsst_apps

lsst\_distrib
=============

``lsst_distrib`` provides all the packages from ``lsst_apps`` along with these additional ones:

.. https://github.com/lsst/lsst_distrib/blob/master/ups/lsst_distrib.table

- `ctrl\_execute <https://github.com/lsst/ctrl_execute>`_
- `ctrl\_platform_lsstvc <https://github.com/lsst/ctrl_platform_lsstvc>`_
- `datarel <https://github.com/lsst/datarel>`_
- `meas\_extensions_convolved <https://github.com/lsst/meas_extensions_convolved>`_
- `meas\_extensions_shapeHSM <https://github.com/lsst/meas_extensions_shapeHSM>`_
- `meas\_extensions_photometryKron <https://github.com/lsst/meas_extensions_photometryKron>`_
- `pipe\_drivers <https://github.com/lsst/pipe_drivers>`_
- `lsst\_obs <https://github.com/lsst/lsst_obs>`_
- `jointcal <https://github.com/lsst/jointcal>`_
- `verify <https://github.com/lsst/verify>`_

Example installation (:ref:`more info <newinstall-install>`):

.. code-block:: bash

   eups distrib install lsst_distrib -t <tag>
   setup lsst_distrib

.. _EUPS: https://github.com/RobertLuptonTheGood/eups
