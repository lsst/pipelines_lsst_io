######################################################
Configuring Git LFS for downloading LSST data packages
######################################################

LSST uses `Git LFS`_ to efficiently store large files in Git repositories.
Typical Science Pipelines installations, like ``lsst_distrib``, *do not* require Git LFS.
However, some tutorials might require Git LFS to clone a specific Git repository that does use Git LFS.
The `testdata_ci_hsc`_ package is one example.
This page describes how to configure Git LFS to work with LSST's servers.

.. note::

   LSST staff and contributors should follow the `instructions in the Developer Guide`_ for configuring Git LFS with authenticated (push) access.

.. _git-lfs-installation:

Getting Git LFS
===============

Git LFS comes with your LSST Science Pipelines installation.
To check that it's available, run:

.. code-block:: bash

   git-lfs version

You can also install Git LFS independently of the LSST Science Pipelines.
Follow the instructions on the `Git LFS homepage`_ to install Git LFS onto your system.
**LSST requires Git LFS 2.3.4 or later.**

.. Generally our stated Git LFS version requirements should track what's used in CI:
.. https://github.com/lsst/lsstsw/blob/master/bin/deploy

.. _git-lfs-config:

Configuring Git LFS for LSST
============================

Since LSST uses its own data servers, rather than GitHub's, you'll need to add some extra configurations beyond a regular installation.

Create or edit the :file:`~/.gitconfig` file to add these new lines:

.. code-block:: text

   # Cache anonymous access to LSST Git LFS S3 servers
   [credential "https://lsst-sqre-prod-git-lfs.s3-us-west-2.amazonaws.com"]
       helper = store
   [credential "https://s3.lsst.codes"]
       helper = store

Also create or edit the :file:`~/.git-credentials` file to add these new lines:

.. code-block:: text

   https://:@lsst-sqre-prod-git-lfs.s3-us-west-2.amazonaws.com
   https://:@s3.lsst.codes

.. _git-lfs-test:

Try it out
==========

Trying cloning the `testdata_decam`_ Git repository to test your configuration:

.. code-block:: bash

   git clone https://github.com/lsst/testdata_decam.git

.. note::

   LSST contributors need to follow some extra steps to authenticate commands that push to the upstream repository on GitHub.
   See the `Developer Guide for details`.

.. _`Git LFS homepage`:
.. _Git LFS: https://git-lfs.github.com/
.. _`Developer Guide for details`:
.. _`instructions in the Developer Guide`: https://developer.lsst.io/git/git-lfs.html
.. _`testdata_decam`: https://github.com/lsst/testdata_decam
.. _`testdata_ci_hsc`: https://github.com/lsst/testdata_ci_hsc
