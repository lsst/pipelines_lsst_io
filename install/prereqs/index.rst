#############
Prerequisites
#############

This page lists software needed to install and use the LSST Science Pipelines.

.. _prereq-platforms:

Platform compatibility
======================

The LSST Data Management reference platform is CentOS 7-1611.
This is the platform we officially develop, test, and operate with.

Besides the reference platform, we generally expect the Pipelines to also compile and run under CentOS 6, Debian Linux (including Ubuntu), and macOS.
See `LSST Stack Testing Status <https://ls.st/faq>`_ reports of building LSST software on various platforms.

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

Both the :doc:`newinstall.sh <../newinstall>` and :doc:`lsstsw <../lsstsw>`\ -based installation methods provide dedicated Miniconda environments pre-loaded with Python dependencies.
If you opt to use your own Python, you can re-create the default Python environment made by :command:`newinstall.sh` and ``lsstsw`` with these Conda environments:

- `macOS and Python 2.7 <https://github.com/lsst/lsstsw/blob/master/etc/conda2_packages-osx-64.txt>`_.
- `macOS and Python 3.5+ <https://github.com/lsst/lsstsw/blob/master/etc/conda3_packages-osx-64.txt>`_.
- `Linux and Python 2.7 <https://github.com/lsst/lsstsw/blob/master/etc/conda2_packages-linux-64.txt>`_.
- `Linux and Python 3.5+ <https://github.com/lsst/lsstsw/blob/master/etc/conda3_packages-linux-64.txt>`_.

.. _optional-deps:

Optional dependencies
=====================

We use `SAOImage DS9 <http://ds9.si.edu/site/Home.html>`_ to display images for debugging.
