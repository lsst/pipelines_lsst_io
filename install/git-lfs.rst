######################################################
Configuring Git LFS for downloading LSST data packages
######################################################

LSST uses `Git LFS`_ to efficiently store large files in Git repositories.
Typical Science Pipelines installations, like ``lsst_distrib``, *do not* require Git LFS.
However, some tutorials might require Git LFS to clone a specific Git repository that does use Git LFS.
The `testdata_ci_hsc`_ package is one example.
This page describes how to configure Git LFS to work with LSST's servers.

.. note::

   LSST staff and contributors should follow the `instructions in the Developer Guide`_, specifically `Authenticating for push access`_,for configuring Git LFS with authenticated (push) access.

.. _git-lfs-installation:

Getting Git LFS
===============

Git LFS may have been installed with your LSST Science Pipelines installation.

To check that it's available, run:

.. code-block:: bash

   git-lfs version

If it is not installed, or if you want to use it You can also install Git LFS independently of the LSST Science Pipelines.

Follow the instructions on the `Git LFS homepage`_ to install Git LFS onto your system, and then the first bullet point in "Getting Started."

If all you will need to do is to use files that have been stored in Git LFS, and will not need to read them,

.. code-block:: bash

   git-lfs install

is all you need to do after installing the git lfs binaries.  This must be done on each machine from which you will be accessing repositories with Git LFS-stored artifacts.

If all you need is read-only access to LFS-stored files, you're done.  The ``.gitattributes`` file will already have been created appropriately in each LFS-using repository.

.. _git-lfs-test:

Try it out
==========

Trying cloning the `testdata_decam`_ Git repository to test your configuration:

.. code-block:: bash

   git clone https://github.com/lsst/testdata_decam.git

.. note::

Push access
===========

   LSST contributors need to follow some extra steps to authenticate commands that push to the upstream repository on GitHub.
   See `Authenticating for push access`_.

.. _`Git LFS homepage`:
.. _Git LFS: https://git-lfs.github.com/
.. _`Developer Guide for details`:
.. _`instructions in the Developer Guide`: https://developer.lsst.io/git/git-lfs.html
.. _`Authenticating for push access`: https://developer.lsst.io/git/git-lfs.html#git-lfs-auth
.. _`testdata_decam`: https://github.com/lsst/testdata_decam
.. _`testdata_ci_hsc`: https://github.com/lsst/testdata_ci_hsc
