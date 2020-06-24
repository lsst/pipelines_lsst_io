##########################
The LSST Science Pipelines
##########################

The LSST Science Pipelines enable optical and near-infrared astronomy in the big data era.
We are building the Science Pipelines for the `Rubin Observatory Legacy Survey of Space and Time (Rubin’s LSST) <https://lsst.org/>`_, but our command-line task and Python API can be extended for any optical or near-infrared dataset.

This documentation covers version |eups-tag-bold|.
:doc:`Learn what's new <releases/index>`.
You can also find documentation for `other versions <https://pipelines.lsst.io/v>`__.

.. _part-getting-started:

Getting started
===============

If you're new to the LSST Science Pipelines, these step-by-step data processing tutorials will get you up and running:

- Data processing tutorial series: Part 1 :doc:`Data repositories <getting-started/data-setup>` · Part 2 :doc:`Single frame processing <getting-started/processccd>` · Part 3 :doc:`Image and catalog display <getting-started/display>` · Part 4 :doc:`Image coaddition <getting-started/coaddition>` · Part 5 :doc:`Source measurement <getting-started/photometry>` · Part 6 :doc:`Multi-band catalog analysis <getting-started/multiband-analysis>`.

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

.. _part-modules:

Python modules
==============

.. module-toctree::

Additional C++ API reference documentation is currently available at the `doxygen.lsst.codes <http://doxygen.lsst.codes/stack/doxygen/x_masterDoxyDoc/namespaces.html>`__ site.

.. _part-packages:

Packages
========

.. package-toctree::

.. _part-release-details:

Release details
===============

-  :doc:`releases/notes`
-  :doc:`known-issues`
-  :doc:`metrics`

.. toctree::
   :hidden:

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
- Report issues in `JIRA <https://jira.lsstcorp.org/projects/DM/issues/>`_.
- Some API documentation, particularly for C++, is currently published separately on a `Doxygen site <http://doxygen.lsst.codes/stack/doxygen/x_masterDoxyDoc/>`_.
- DM Developer guidance is at https://developer.lsst.io.
- Learn more about LSST Data Management by visiting http://lsst.org/about/dm.
- Contribute to our documentation. This guide is on GitHub at `lsst/pipelines_lsst_io <https://github.com/lsst/pipelines_lsst_io>`_.
