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

.. note::

  **New since 14.0**: The minimum :command:`cmake` version required to compile the Stack is **2.8.12**.

.. _filesystem-prereqs:

Filesystem prerequisites
========================

Filesystems used for compiling the Stack and hosting output data repositories must support the ``flock`` system call for file locking.
Local filesystems virtually always have this support.
Network filesystems are sometimes mounted without such support to improve performance; the output of the :command:`mount` command may show the ``nolock`` or ``noflock`` option in those cases.

.. _python-deps:

Python dependencies
===================

The LSST Science Pipelines require Python 3.6 or newer.

Both the :doc:`newinstall.sh <../newinstall>` and :doc:`lsstsw <../lsstsw>`\ -based installation methods provide dedicated Miniconda environments pre-loaded with Python dependencies.
If you opt to use your own Python, you can re-create the default Python environment made by :command:`newinstall.sh` and ``lsstsw`` with these Conda environments:

- `macOS <https://github.com/lsst/lsstsw/blob/master/etc/conda3_packages-osx-64.txt>`_.
- `Linux <https://github.com/lsst/lsstsw/blob/master/etc/conda3_packages-linux-64.txt>`_.

.. _optional-deps:

Optional dependencies
=====================

We use `SAOImage DS9 <http://ds9.si.edu/site/Home.html>`_ to display images for debugging.
