######################################
Source Installation with newinstall.sh
######################################

This page will guide you through installing the LSST Science Pipelines from source with :command:`newinstall.sh` (internally based on :command:`eups distrib`).

The reference platform for the LSST Science Pipelines is CentOS 7 however individual developers compile on `a variety of Linux and macOS operating systems <https://ls.st/faq>`_ so if you are on a similar platform you should be able to build from source successfully.

:doc:`We also offer Conda binaries and Docker images <index>` if you do not wish to install the Science Pipelines from source.

If you have difficulty installing LSST software:

- review the :ref:`known installation issues for your platform <installation-issues>`.
- reach out on the `Support forum at community.lsst.org <https://community.lsst.org/c/support>`_.

.. _source-install-prereqs:

1. Install prerequisites
========================

- Install prerequisites for your platform: :doc:`macOS <prereqs/macos>`, :doc:`Debian / Ubuntu <prereqs/debian>`, or :doc:`Centos / RedHat <prereqs/centos>`.
- If you opt not to use :command:`newinstall` \’s default Python environment you need to :ref:`install these Python dependencies <python-deps>`.

.. _install-from-source-dir:

2. Choose an installation directory
===================================

First, choose where you want to install the LSST Science Pipelines.
We'll use :file:`$HOME/lsst_stack` in this example.
Create and change into that directory:

.. code-block:: bash

   mkdir -p $HOME/lsst_stack
   cd $HOME/lsst_stack

.. tip::

   **Permissions for multi-user installations**
   
   Those in a system administration role, who are installing a writable stack for multiple users, will likely want to establish a separate group (perhaps lsst) with a umask of 002 (all access permissions for the group; allow other users to read+execute).
   The installation directory must be owned by the group, have the SGID (2000) bit set, and allow group read/write/execute: that is, mode 2775.
   Individual users who install a personal Stack on their own machine need not worry about this.

.. _install-from-source-envvar:

3. Unset environment variables
==============================

If you've run the LSST Science Pipelines previously, you may have conflicting environment variables setup.
To be safe, run:

.. code-block:: bash

   unset LSST_HOME EUPS_PATH LSST_DEVEL EUPS_PKGROOT REPOSITORY_PATH

.. _install-from-source-setup:

4. Installation set-up
======================

Download and run the `installation setup script from GitHub <https://raw.githubusercontent.com/lsst/lsst/13.0/scripts/newinstall.sh>`__, which installs the basic packages required to install other packages:

.. code-block:: bash

   curl -OL https://raw.githubusercontent.com/lsst/lsst/13.0/scripts/newinstall.sh
   bash newinstall.sh

This installs the :command:`loadLSST.*` scripts, which you should source to ensure that LSST tools (e.g., the :command:`eups` command) are included in your path.

The install script will check your system to ensure that appropriate versions of critical packages are installed on your system, to enable bootstrapping the Science Pipelines, including :command:`git`, and :command:`python`.
If these packages are not available, the script will offer to install them for you (using the Anaconda Python distribution for the latter packages). 

Allowing the installation of these core packages will not replace or modify any other version of these packages that may be installed on your system.
If you do not choose the Anaconda Python install, and subsequent package build steps fail, you can do one of two things:

* Report the problem to `community.lsst.org <https://community.lsst.org>`_. Include your OS, a description of the problem, plus any error messages. Community members will provide assistance.
* Consider removing all contents of the install directory and start from scratch, and accepting the Anaconda Python installation option.

Once :command:`newinstall.sh` has finished, source the LSST environment to continue the installation by running the appropriate command for your shell:

.. code-block:: bash

   source $LSST_HOME/loadLSST.bash # for bash users
   source $LSST_HOME/loadLSST.csh  # for csh users
   source $LSST_HOME/loadLSST.ksh  # for ksh users
   source $LSST_HOME/loadLSST.zsh  # for zsh users

where :file:`$LSST_HOME` is expanded to your installation directory.

.. _install-from-source-packages:

5. Install lsst_distrib
=======================

Finally, install components of the LSST Science Pipelines that are relevant for your work.
A simple way to ensure that you have a fairly complete set of packages for this need is to install ``lsst_distrib``:

.. code-block:: bash

   eups distrib install -t v13_0 lsst_distrib
   setup lsst_distrib

After this initial setup, it is a good idea to test the installation.
See :ref:`source-install-testing-your-installation`.

.. _install-from-source-loadlsst:

6. Source the LSST environment in each shell session
====================================================

Whenever you want to run the installed LSST Science Pipelines in a new terminal session, be sure to :command:`source` the appropriate :file:`loadLSST.bash`, :file:`loadLSST.csh`, :file:`loadLSST.ksh` or :file:`loadLSST.zsh}` script.

Then setup the EUPS packages you need, typically:

.. code-block:: bash

   setup lsst_distrib

.. _source-install-testing-your-installation:

7. Testing Your Installation
============================

Once the LSST Science Pipelines are installed, you can verify that it works by :doc:`running a demo project <demo>`.
This demo processes a small amount of SDSS data.
