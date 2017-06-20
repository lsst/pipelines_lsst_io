##########################
The LSST Science Pipelines
##########################

The LSST Science Pipelines enable optical and near-infrared astronomy in the big data era.
We are building the Science Pipelines for the `Large Synoptic Survey Telescope (LSST) <http://lsst.org>`_, but our command line task and Python API can be extended for any optical or near-infrared dataset.

The latest release is |current-release|: :doc:`learn what's new <releases/index>`.
  
.. .. toctree::
  ..  :hidden:

  ..  releases/index

.. _part-getting-started:

Getting started
===============

If you're new to the LSST Science Pipelines, these tutorials will get you up and running with step-by-step installation and processing tutorials.

- :doc:`Installation tutorial <getting-started/installation>`
- :doc:`Data processing tutorial <getting-started/data-setup>`: Part 1 :doc:`Data repositories <getting-started/data-setup>` · Part 2 :doc:`Single frame processing <getting-started/processccd>` · Part 3 :doc:`Image coaddition <getting-started/coaddition>` · Part 4 :doc:`Source measurement <getting-started/photometry>`.

Join us on the `LSST Community forum <https://community.lsst.org>`_ to get help and share ideas.

.. toctree::
   :hidden:
   :caption: Getting Started

   getting-started/index

.. _part-installation:

Installation
============

- :doc:`Overview of installation methods <install/index>`
- :doc:`Installing with newinstall.sh <install/newinstall>` (recommended)
- :doc:`Installing from source with lsstsw <install/lsstsw>` (for developers)

.. toctree::
   :hidden:
   :caption: Installation in-depth

   install/index

.. _part-release-details:

.. toctree::
   :maxdepth: 1
   :caption: Release details

   releases/notes
   known-issues
   metrics/index

.. toctree::
   :hidden:

   releases/index

Links
=====

- Contribute to this guide on GitHub at `lsst/pipelines_lsst_io <https://github.com/lsst/pipelines_lsst_io>`_.
- Fork our code on GitHub at https://github.com/lsst.
- API documentation is currently published with `Doxygen <http://doxygen.lsst.codes/stack/doxygen/x_masterDoxyDoc/>`_.
- DM Developer guidance is at https://developer.lsst.io.
- Learn more about LSST Data Management by visiting http://dm.lsst.org.
