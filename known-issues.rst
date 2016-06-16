..
  Keep these known issues updated to the current state of the software.
  
  Maintain the existing headers in Installation Issues and simply report "None"
  if there are no issues at the moment.

############
Known Issues
############

.. _installation-issues:

Installation Issues
===================

.. _installation-issues-cross-platform:

Cross Platform
--------------

- Compiling some packages---in particular ``afw``\ ---require large amounts of
  RAM to compile. This is compounded as the system will automatically attempt
  to parallelize the build, and can cause the build to run extremely slowly or
  fail altogether. On machines with less than 8 GB of RAM, disable
  parallelization by setting ``EUPSPKG_NJOBS=1`` in your environment before
  running ``eups distrib``.

.. _installation-issues-redhat:

Red Hat (and clones) specific
-----------------------------

Older platforms
^^^^^^^^^^^^^^^

- If you have a problem building on **RHEL 6** check the :ref:`Pre-requisites
  <source-install-redhat-prereqs>` to make sure sure you are using a more
  recent version of :command:`gcc` (minimum required is 4.8)

- curl looks for certificates in :file:`/etc/pki/tls/certs/ca-bundle.crt`
  rather than :file:`/etc/ssl/certs/ca-certificates.crt`. The solution is to
  copy :file:`ca-certificates.crt` to :file:`ca-bundle.crt`.

.. _installation-issues-macos:

OS X specific
-------------

New versions
^^^^^^^^^^^^

- El Capitan came out after our testing period, and there are known issues
  :jirap:`DM-3200` that will be addressed in the next release.

Older platforms
^^^^^^^^^^^^^^^

- Some old installations of XCode on Macs create a :file:`/Developer`
  directory.  This can interfere with installation.

- Macs must use the :command:`clang` compiler, not :command:`gcc`.
  :jirab:`DM-3405`

  One version of this problem occurs when using Macports_, which, by
  default, will create a symlink from :file:`/opt/local/bin/c++` to its
  version of :command:`g++`. Try removing that, starting a new shell, and
  restarting :command:`eups distrib install`.

.. _Macports: https://www.macports.org/index.php
