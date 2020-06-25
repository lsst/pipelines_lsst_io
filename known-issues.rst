..
  Keep these known issues updated to the current state of the software.
  
  Maintain the existing headers in Installation Issues and simply report "None"
  if there are no issues at the moment.

############
Known Issues
############

.. _installation-issues:

Binary installation issues
==========================

Cross Platform
--------------

- Detailed numerical results may be sensitive to the exact versions of third party numerical libraries.
  If you are not using the :ref:`standard Conda environment <system-prereqs>` you may encounter issues when running the :doc:`validation demo </install/demo>`.

CentOS (and related) specific
-----------------------------

- The DM codebase is not compatible with the Intel Math Kernel Library (MKL).
  Attempting to use MKL may generate incorrect numerical results.

  If you have installed using your own Conda, you should install the ``nomkl`` package, and remove ``mkl`` and ``mkl service``.
  :jirab:`DM-5105`

.. _src-installation-issues:

Source installation issues
==========================

.. _installation-issues-cross-platform:

Cross Platform
--------------

- Compiling some packages---in particular ``afw``\ ---require large amounts of RAM to compile.
  This is compounded as the system will automatically attempt to parallelize the build, and can cause the build to run extremely slowly or fail altogether.
  On machines with less than 8 GB of RAM, disable parallelization by setting ``EUPSPKG_NJOBS=1`` in your environment before running ``eups distrib``.

- Detailed numerical results may be sensitive to the exact versions of third party numerical libraries.
  If you are not using the :ref:`standard Conda environment <system-prereqs>` you may encounter issues when running the :doc:`validation demo </install/demo>`.

.. _installation-issues-centos:

CentOS (and related) specific
-----------------------------

- The DM codebase is not compatible with the Intel Math Kernel Library (MKL).
  Attempting to use MKL will cause the test suite to fail, automatically aborting the installation. :jirab:`DM-5105`

.. _installation-issues-macos:

macOS specific
--------------

- Some old installations of Xcode on Macs create a :file:`/Developer` directory which can interfere with installation.

.. _other-issues:

Other issues
============

Many versions of the DS9 image viewer software incorrectly read mask planes in Science Pipelines image files as all zeros.
