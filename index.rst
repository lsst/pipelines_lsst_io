##########################
The LSST Science Pipelines
##########################

The LSST Science Pipelines are designed to enable optical and near-infrared astronomy in the “big data” era.
While they are being developed to process the data for the `Rubin Observatory Legacy Survey of Space and Time (Rubin’s LSST) <https://lsst.org/>`_, our command line and programming interfaces can be extended to address any optical or near-infrared dataset.

This documentation covers version |eups-tag-bold|.
:ref:`Learn what's new <release-latest>`.
You can also find documentation for `other versions <https://pipelines.lsst.io/v>`__.

.. _part-getting-started:

Getting started
===============

If you're new to the LSST Science Pipelines, these step-by-step data processing tutorials will get you up and running.

Data processing tutorial series (these were developed using the ``w_2021_33`` version of the science pipelines):

- Part 1 :doc:`Data repositories <getting-started/data-setup>`
- Part 2 :doc:`Single frame processing <getting-started/singleframe>`
- Part 3 :doc:`Image and catalog display <getting-started/display>`
- Part 4 :doc:`Global calibration <getting-started/uber-cal>`
- Part 5 :doc:`Image coaddition <getting-started/coaddition>`
- Part 6 :doc:`Source measurement <getting-started/photometry>`
- Part 7 :doc:`Multi-band catalog analysis <getting-started/multiband-analysis>`.

Guide for processing DESC DC2 data in a shared repository using the Alert Production pipeline (this was developed using the ``w_2021_30`` version of the science pipelines):

- :doc:`Processing DESC DC2 data with the Alert Production pipeline <getting-started/dc2-guide>`.

Join us on the `LSST Community forum <https://community.lsst.org>`_ to get help and share ideas.

.. toctree::
   :hidden:
   :caption: Getting Started

   getting-started/index

.. _part-installation:

Installation
============

Recommended installation path:

- :doc:`Installing with newinstall.sh <install/newinstall>`
- :doc:`install/setup`
- :doc:`install/top-level-packages`

Alternative distributions and installation methods:

- :doc:`install/docker`
- :doc:`Installing from source with lsstsw <install/lsstsw>`
- `CernVM FS <https://sw.lsst.eu>`_ (contributed by CC-IN2P3)

Related topics:

- :doc:`Configuring Git LFS for data packages <install/git-lfs>`
- :doc:`install/package-development`

To install the LSST Simulation software, such as MAF, please follow the `LSST Simulations documentation <https://confluence.lsstcorp.org/display/SIM/Catalogs+and+MAF>`_.

.. This toctree is hidden to let us curate the section above, but still add the install/ pages to the Sphinx toctree

.. toctree::
   :hidden:
   :caption: Installation

   install/index

Frameworks
==========

.. toctree::
   :maxdepth: 2

   middleware/index

.. _part-modules:

Python modules
==============

.. module-toctree::

Additional C++ API reference documentation is currently available at the `doxygen.lsst.codes <http://doxygen.lsst.codes/stack/doxygen/x_mainDoxyDoc/namespaces.html>`__ site.

.. _part-packages:

Packages
========

.. package-toctree::

.. _part-release-details:

Release details
===============

.. toctree::
   :maxdepth: 2

   releases/index
   known-issues
   metrics

.. _part-indices:

Indices
=======

.. toctree::
   :maxdepth: 1
   :hidden:

   Tasks <tasks>

- :doc:`Tasks <tasks>`
- :ref:`genindex`
- :ref:`Search <search>`

More info
=========

- Join us on the `LSST Community forum, community.lsst.org <http://community.lsst.org>`_.
- Fork our code on GitHub at https://github.com/lsst.
- Report issues in `Jira <https://jira.lsstcorp.org/projects/DM/issues/>`_.
- Some API documentation, particularly for C++, is currently published separately on a `Doxygen site <http://doxygen.lsst.codes/stack/doxygen/x_mainDoxyDoc/>`_.
- Our `Developer Guide <https://developer.lsst.io>`_ describes the procedures and standards followed by the DM team.
- Learn more about Rubin Observatory Data Management by visiting http://lsst.org/about/dm.
- Contribute to our documentation. This guide is on GitHub at `lsst/pipelines_lsst_io <https://github.com/lsst/pipelines_lsst_io>`_.
