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

- :doc:`Installing with lsstinstall <install/lsstinstall>`
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

.. _part-frameworks:

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

.. _part-citation:

Citing and acknowledging the LSST Science Pipelines
===================================================

If you use the science pipelines in a published work, we request that you cite *Vera C. Rubin Observatory Science Pipelines Developers*, 2025, `doi:10.71929/rubin/2570545 <https://doi.org/10.71929/rubin/2570545>`_:

.. code-block:: bibtex

   @TechReport{10.71929/rubin/2570545,
      author = "{Vera C. Rubin Observatory Science Pipelines Developers}",
      title = "{The LSST Science Pipelines Software: Optical Survey Pipeline Reduction and Analysis Environment}",
      institution = "{Vera C. Rubin Observatory}",
      year = "2025",
      month = "June",
      handle = "PSTN-019",
      type = "{Project Science Technical Note}",
      number = "PSTN-019",
      doi = "10.71929/rubin/2570545",
      url = "https://pstn-019.lsst.io/"
   }

This reference will be updated once we submit to to arXiv and AAS.
You are also welcome to cite older papers such as `Bosch et al. 2018 <https://ui.adsabs.harvard.edu/abs/2018PASJ...70S...5B/abstract>`_, `2019 <https://ui.adsabs.harvard.edu/abs/2019ASPC..523..521B/abstract>`_.
In addition, it is appropriate to include an acknowledgement of the form:

  This paper makes use of LSST Science Pipelines software developed by the `Vera C. Rubin Observatory <https://rubinobservatory.org/>`_.
  We thank the Rubin Observatory for making their code available as free software at `https://pipelines.lsst.io <https://pipelines.lsst.io/>`_.

For studies that make use of the Data Butler and pipeline execution system, we request that you additionally cite `Jenness et al. 2022 <https://ui.adsabs.harvard.edu/abs/2022SPIE12189E..11J/abstract>`_.
For studies that make use of the SCARLET source separation framework, we request that you additionally cite `Melchior et al. 2018 <https://ui.adsabs.harvard.edu/abs/2018A%26C....24..129M/abstract>`_.

As the Rubin Observatory is not funded to provide support for the LSST Science Pipelines outside of the project, any support provided by project members will come out of their own free or science time.
A fair way to acknowledge their help and good will may be to offer co-authorship on technical papers describing the derived software (e.g. pipelines).

.. _part-license:

License
=======

All LSST Science Pipelines code is `free software <http://www.gnu.org/philosophy/free-sw.html>`_, licensed under the terms of the `GNU General Public Licence, Version 3 <http://www.gnu.org/copyleft/gpl.html>`_.
You have the freedom to run, copy, distribute, study, change and improve the software as you see fit within the terms of the GPL v3 license.
Using, modifying or redistributing the LSST Science Pipelines does not make you subject to the LSST Project Publication Policy (`LPM-162 <https://ls.st/lpm-162>`_).
This documentation is licensed under the `Creative Commons Attribution Share Alike 4.0 International License (CC-BY-SA 4.0) <https://github.com/lsst/pipelines_lsst_io/blob/main/LICENSE>`_.

.. _part-more-info:

More info
=========

- Join us on the `LSST Community forum, community.lsst.org <http://community.lsst.org>`_.
- Fork our code on GitHub at https://github.com/lsst.
- Report issues in `Jira <https://ls.st/jira>`_.
- Some API documentation, particularly for C++, is currently published separately on a `Doxygen site <http://doxygen.lsst.codes/stack/doxygen/x_mainDoxyDoc/>`_.
- Our `Developer Guide <https://developer.lsst.io>`_ describes the procedures and standards followed by the DM team.
- Learn more about Rubin Observatory Data Management by visiting http://lsst.org/about/dm.
- Contribute to our documentation. This guide is on GitHub at `lsst/pipelines_lsst_io <https://github.com/lsst/pipelines_lsst_io>`_.
