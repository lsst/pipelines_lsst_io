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

- This release may not work when installed without the Conda environments provided by the documented :doc:`newinstall.sh </install/newinstall>`, :doc:`lsstsw </install/lsstsw>`, or :doc:`Docker </install/docker>` installation methods.
  The :ref:`documented Python dependencies <python-deps>` may differ slightly from those in the release, causing issues with the :doc:`validation demo </install/demo>`.

Red Hat (and clones) specific
-----------------------------

- The DM codebase is not compatible with the Intel Math Kernel Library (MKL).
  Attempting to use MKL may generate incorrect numerical results.

  If you have installed using Conda, you should install the ``nomkl`` package,
  and remove ``mkl`` and ``mkl service``. :jirab:`DM-5105`

.. _src-installation-issues:

Source installation issues
==========================

.. _installation-issues-cross-platform:

Cross Platform
--------------

- Compiling some packages---in particular ``afw``\ ---require large amounts of
  RAM to compile. This is compounded as the system will automatically attempt
  to parallelize the build, and can cause the build to run extremely slowly or
  fail altogether. On machines with less than 8 GB of RAM, disable
  parallelization by setting ``EUPSPKG_NJOBS=1`` in your environment before
  running ``eups distrib``.

- The lsst_dm_stack_demo package may produce slightly different numeric results
  if executed on operating systems other than the officially supported versions
  of macOS and CentOS, or if using a different Python environment.

.. _installation-issues-redhat:

Red Hat (and clones) specific
-----------------------------

- The DM codebase is not compatible with the Intel Math Kernel Library (MKL).
  Attempting to use MKL will cause the test suite to fail, automatically
  aborting the installation. :jirab:`DM-5105`

- Ensure that the :command:`gcc` compiler version supports **C++14** as 
  specified in the :ref:`Pre-requisites <source-install-redhat-prereqs>`.

RHEL 7.*
^^^^^^^^

- No specific issues.

RHEL 6.*
^^^^^^^^

- curl looks for certificates in :file:`/etc/pki/tls/certs/ca-bundle.crt`
  rather than :file:`/etc/ssl/certs/ca-certificates.crt`. The solution is to
  copy :file:`ca-certificates.crt` to :file:`ca-bundle.crt`.

.. _installation-issues-macos:

macOS specific
--------------

- Macs must use the :command:`clang` compiler, not :command:`gcc`.
  :jirab:`DM-3405`

macOS 10.13 (Sierra) and OS X 10.11 (El Capitan)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `MPICH`_ version 3.2, as currently distributed with the stack, fails
  regularly and unpredictably with a segmentation fault on macOS systems.
  MPICH is used by the `ctrl_pool`_ task distribution framework, and hence the
  `pipe_drivers`_ top-level scripts package which provides the following
  executables:

  - :file:`coaddDriver.py`
  - :file:`constructBias.py`
  - :file:`constructDark.py`
  - :file:`constructFlat.py`
  - :file:`constructFringe.py`
  - :file:`multiBandDriver.py`
  - :file:`singleFrameDriver.py`

  It should be possible to run these commands by restricting them to a single
  CPU core (i.e., ``--batch-type=smp --cores=1``).

  This issue will be resolved by upgrading to version 3.3 of MPICH when it
  becomes available. :jirab:`DM-7588`

.. _MPICH: http://www.mpich.org/
.. _ctrl_pool: https://github.com/lsst/ctrl_pool
.. _pipe_drivers: https://github.com/lsst/pipe_drivers

Older systems
^^^^^^^^^^^^^

- Some old installations of XCode on Macs create a :file:`/Developer`
  directory.  This can interfere with installation.

.. _Macports: https://www.macports.org/index.php


.. _other-issues:

Other issues
============

Many versions of the DS9 image viewer software incorrectly read mask planes in Science Pipelines image files as all zeros.
