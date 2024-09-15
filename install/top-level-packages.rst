#############################
Top-level packages to install
#############################

The LSST Science Pipelines are part of LSST's EUPS_ package stack.
This means that the Science Pipelines software is actually a collection of packages that you install and set up together.
By specifying different **top-level packages** to the :ref:`eups distrib install <lsstinstall-install>` and :doc:`setup <setup>` commands, you can control the size of the software installation or add new capabilities.

This page describes the common top-level packages that make up the LSST Science Pipelines and related EUPS stacks.

lsst\_distrib
=============

This package provides all of the core Science Pipelines functionality, together with additional measurement algorithms, support for a wider variety of instrumentation, and process execution middleware designed for running pipelines on a cluster.

Example installation (:ref:`more info <lsstinstall-install>`):

.. code-block:: bash

   eups distrib install lsst_distrib -t <tag>
   setup lsst_distrib

.. _EUPS: https://github.com/RobertLuptonTheGood/eups

lsst\_apps
==========

This package provides the only core frameworks and algorithmic code.
It may be convenient when space is at a premium.

Example installation (:ref:`more info <lsstinstall-install>`):

.. code-block:: bash

   eups distrib install lsst_apps -t <tag>
   setup lsst_apps
