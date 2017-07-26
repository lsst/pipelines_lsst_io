#############
Prerequisites
#############

This page lists software needed to install and use the LSST Science Pipelines.

.. _system-prereqs:

System prerequisites
====================

.. toctree::
   :maxdepth: 1

   macos
   debian
   centos

.. _python-deps:

Python dependencies
===================

You can use your own Python 2.7.\* install or let :command:`newinstall.sh` install `Miniconda <https://www.continuum.io/downloads>`__ in your local directory.

If you opt to use your own Python, you can re-create the default Python environment made by :command:`newinstall.sh` and ``lsstsw`` with these Conda environments:

- `macOS and Python 2.7 <https://github.com/lsst/lsstsw/blob/master/etc/conda2_packages-osx-64.txt>`_.
- `macOS and Python 3.5+ <https://github.com/lsst/lsstsw/blob/master/etc/conda3_packages-osx-64.txt>`_.
- `Linux and Python 2.7 <https://github.com/lsst/lsstsw/blob/master/etc/conda2_packages-linux-64.txt>`_.
- `Linux and Python 3.5+ <https://github.com/lsst/lsstsw/blob/master/etc/conda3_packages-linux-64.txt>`_.

.. _optional-deps:

Optional dependencies
=====================

We use `SAOImage DS9 <http://ds9.si.edu/site/Home.html>`_ to display images for debugging.
