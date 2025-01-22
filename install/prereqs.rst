#############
Prerequisites
#############

This page lists software needed to install and use the LSST Science Pipelines.

.. _prereq-platforms:

Platform compatibility
======================

The LSST Data Management reference platform is AlmaLinux 9.
This is the platform we officially develop, test, and operate with.

Besides the reference platform, the Pipelines can run on a variety of other Linux distributions like Ubuntu, and various versions of macOS.

.. _system-prereqs:

System prerequisites
====================

The Science Pipelines are developed and built using a standard `Conda`_ environment.
This provides (almost; see below) all necessary tools and libraries for building and running the Pipelines.
On installation, you will be given the option of automatically installing that environment.
If you decline, your system must have all of the prerequisites listed below available:

.. jinja:: default

   - `macOS <https://github.com/lsst/scipipe_conda_env/blob/{{ scipipe_conda_ref }}/etc/conda3_packages-osx-64.yml>`_.
   - `Linux <https://github.com/lsst/scipipe_conda_env/blob/{{ scipipe_conda_ref }}/etc/conda3_packages-linux-64.yml>`_.

In addition to the Conda environment, the following packages must be installed on the host system.

.. _Conda: https://conda.io

AlmaLinux 9
-----------

On AlmaLinux 9 patch needs to be installed.

.. code-block:: bash

   sudo dnf install patch

If you wish to follow the instructions for :doc:`lsstsw` (recommended for some developers, but not necessary for most users), you will also need to install git:

.. code-block:: bash

   sudo dnf install git

Debian/Ubuntu
-------------

On Debian and Ubuntu systems, curl and patch are required.
These may be installed as follows:

.. code-block:: bash

   sudo apt-get update && sudo apt-get install curl patch

If you wish to follow the instructions for :doc:`lsstsw` (recommended for some developers, but not necessary for most users), you will also need to install git:

.. code-block:: bash

   sudo apt-get update && sudo apt-get install git

Tip: installing ``xpa-tools`` with this specific statement might be necessary, in some cases,
in order to avoid `xpa`-related errors when displaying images in DS9:

.. code-block:: bash

   sudo apt install xpa-tools; xpans


macOS
-----

On macOS systems, please install the Xcode Command Line Tools:

.. code-block:: bash

   xcode-select --install
   

.. _filesystem-prereqs:

Filesystem prerequisites
========================

Filesystems used for compiling the Stack and hosting output data repositories must support the ``flock`` system call for file locking.
Local filesystems virtually always have this support.
Network filesystems are sometimes mounted without such support to improve performance; the output of the :command:`mount` command may show the ``nolock`` or ``noflock`` option in those cases.

.. _optional-deps:

Optional dependencies
=====================

Some pipeline components use `SAOImage DS9 <http://ds9.si.edu/site/Home.html>`_, if available, for image display purposes.
