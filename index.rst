##########################
The LSST Science Pipelines
##########################

The LSST Science Pipelines enable optical and near-infrared astronomy in the big data era.
We are building the Science Pipelines for the `Large Synoptic Survey Telescope (LSST) <http://lsst.org>`_, but our command line task and Python API can be extended for any optical or near-infrared dataset.

The latest release is |current-release|: :doc:`learn what's new <releases/index>`.
  
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
- `CernVM FS <https://github.com/airnandez/lsst-cvmfs>`_ (contributed by IN2P3)

To install the LSST Simulation software, such as MAF, follow the `LSST Simulations documentation <https://confluence.lsstcorp.org/display/SIM/Catalogs+and+MAF>`_.

.. This toctree is hidden to let us curate the section above, but still add the install/ pages to the Sphinx toctree

.. toctree::
   :hidden:
   :caption: Installation

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

More info
=========

- Join us on the `LSST Community forum, community.lsst.org <http://community.lsst.org>`_.
- Fork our code on GitHub at https://github.com/lsst.
- Report issues in `JIRA <https://jira.lsstcorp.org/projects/DM/issues/>`_.
- API documentation is currently published with `Doxygen <http://doxygen.lsst.codes/stack/doxygen/x_masterDoxyDoc/>`_.
- DM Developer guidance is at https://developer.lsst.io.
- Learn more about LSST Data Management by visiting http://dm.lsst.org.
- Contribute to our documentation. This guide is on GitHub at `lsst/pipelines_lsst_io <https://github.com/lsst/pipelines_lsst_io>`_.
