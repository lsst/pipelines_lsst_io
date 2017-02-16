######################################
Source Installation with newinstall.sh
######################################

This page will guide you through installing the LSST Science Pipelines from source with :command:`newinstall.sh` (internally based on :command:`eups distrib`).

The LSST Science Pipelines are officially tested against CentOS 7, however developers regularly use `a variety of Linux and macOS operating systems <https://ls.st/faq>`_.

:doc:`We also offer Conda binaries and Docker images <index>` if you do not wish to install the Science Pipelines from source.

If you have difficulty installing LSST software:

- review the :ref:`known installation issues for your platform <installation-issues>`.
- reach out on the `Support forum at community.lsst.org <https://community.lsst.org/c/support>`_.

.. _source-install-prereqs:

Prerequisites
=============

This section lists system prerequisites for :ref:`macOS <source-install-mac-prereqs>`, :ref:`Debian/Ubuntu <source-install-debian-prereqs>`, and :ref:`RedHat/CentOS <source-install-redhat-prereqs>` platforms.
All platforms also need :ref:`Python package dependencies <source-install-py-deps>` listed here.

.. note::

   **New since 11.0**: The minimum gcc version required to compile the Stack is **gcc 4.8.**
   If you using our previous factory platform, RedHat/CentOS 6, and you are unable to upgrade to version 7 (which comes with gcc 4.8 as default) consult :ref:`the section below on upgrading compilers in legacy Linux <source-install-redhat-legacy>`.

.. _source-install-mac-prereqs:

macOS
-----

To build LSST software, macOS systems need:

1. :ref:`Xcode <source-install-mac-prereqs-xcode>`, or command line tools.
2. :ref:`cmake <source-install-mac-prereqs-cmake>`.

Versions prior to OS X 10.9 and earlier have not been tested recently and may not work.

.. _source-install-mac-prereqs-xcode:

Xcode
^^^^^

You will need to install developer tools, which we recommend you obtain with Apple's Xcode command line tools package.
To do this, run from the command line (e.g. ``Terminal.app`` or similar):

.. code-block:: bash

   xcode-select --install

and follow the on-screen instructions.
You can verify where the tools are installed by running:

.. code-block:: bash

   xcode-select -p

.. _source-install-mac-prereqs-cmake:

cmake
^^^^^

``cmake`` can be `installed directly <https://cmake.org/download/>`__, or though a package manager like `Homebrew <https://brew.sh>`__.

.. _source-install-debian-prereqs:

Debian / Ubuntu
---------------

.. code-block:: bash

   apt-get install bison ca-certificates \
           cmake flex g++ gettext git libbz2-dev \
           libfontconfig1 libglib2.0-dev libncurses5-dev \
           libreadline6-dev libssl-dev libx11-dev libxrender1 \
           libxt-dev m4 openjdk-8-jre \
           perl-modules zlib1g-dev \


.. from https://github.com/lsst-sqre/puppet-lsststack/blob/master/manifests/params.pp

Prefix the :command:`apt-get` command with :command:`sudo` if necessary.

.. _source-install-redhat-prereqs:

RedHat / CentOS
---------------

.. code-block:: bash

   yum install bison curl blas bzip2-devel bzip2 flex fontconfig \
       freetype-devel gcc-c++ gcc-gfortran git libuuid-devel \
       libXext libXrender libXt-devel make openssl-devel patch perl \
       readline-devel tar zlib-devel ncurses-devel cmake glib2-devel \
       java-1.8.0-openjdk gettext perl-ExtUtils-MakeMaker

.. from https://github.com/lsst-sqre/puppet-lsststack/blob/master/manifests/params.pp

Prefix the :command:`yum` command with :command:`sudo` if necessary.

.. _source-install-redhat-legacy:

Upgrading compilers for legacy RedHat / CentOS 6
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The minimum gcc version required to compile the Stack is gcc 4.8.
This comes as standard in the LSST "factory" platform, Red Hat / CentOS 7.

On our previous factory platform, Red Hat / CentOS 6, you will need to use a more current version of gcc that what is available with your system.
If you can go to Red Hat 7, we recommend that you do; if you cannot, we recommend that you use a newer gcc version for the stack by using a Software Collection (SCL) with a different version of devtoolset.
This will enable you to safely use a different version of gcc (4.9) for the stack than that used by your operating system (4.4).

First, install ``devtoolset-3`` (after the :ref:`installing the standard pre-requisites (above) <source-install-redhat-prereqs>`):

.. code-block:: bash

   sudo yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
   sudo yum install -y https://www.softwarecollections.org/en/scls/rhscl/rh-java-common/epel-6-x86_64/download/rhscl-rh-java-common-epel-6-x86_64.noarch.rpm
   sudo yum install -y https://www.softwarecollections.org/en/scls/rhscl/devtoolset-3/epel-6-x86_64/download/rhscl-devtoolset-3-epel-6-x86_64.noarch.rpm
   sudo yum install -y scl-utils
   sudo yum install -y devtoolset-3

Then enable ``devtoolset-3`` by including this line in your :file:`~/.bash_profile`:

.. code-block:: bash

   scl enable devtoolset-3 bash

.. _source-install-py-deps:

Python dependencies
-------------------

You can use your own Python 2.7.\* install or let :command:`newinstall.sh` install `Miniconda <https://www.continuum.io/downloads>`__ in your local directory.

.. _source-install-optional-deps:

Optional dependencies
---------------------

Although not required, we recommend you install the `matplotlib <http://matplotlib.org>`_ and `scipy <http://scipy.org>`_ Python packages:

.. code-block:: bash

   pip install -U matplotlib scipy

.. FIXME

Note these are included by default in `Anaconda <https://store.continuum.io/cshop/anaconda/>`__, which :command:`newinstall.sh` *can* obtain for you.

We also use `SAOImage DS9 <http://ds9.si.edu/site/Home.html>`_ to display images for debugging.

.. _install-from-source:

Installing from Source with newinstall.sh
=========================================

This section will guide you through installing the *current* release of the LSST Science Pipelines from source given that prerequisites have been installed.

.. _install-from-source-dir:

1. Choose an installation directory
-----------------------------------

First, choose where you want to install the LSST Science Pipelines.
We'll use :file:`$HOME/lsst_stack` in this example.
Create and change into that directory:

.. code-block:: bash

   mkdir -p $HOME/lsst_stack
   cd $HOME/lsst_stack

Installation for groups
^^^^^^^^^^^^^^^^^^^^^^^
   
Those in a system administration role, who are installing a writable stack for multiple users, will likely want to establish a separate group (perhaps lsst) with a umask of 002 (all access permissions for the group; allow other users to read+execute).
The installation directory must be owned by the group, have the SGID (2000) bit set, and allow group read/write/execute: that is, mode 2775.
Individual users who install a personal Stack on their own machine need not worry about this.

.. _install-from-source-envvar:

2. Unset environment variables
------------------------------

If you've run the LSST Science Pipelines previously, you may have conflicting environment variables setup.
To be safe, run:

.. code-block:: bash

   unset LSST_HOME EUPS_PATH LSST_DEVEL EUPS_PKGROOT REPOSITORY_PATH

.. _install-from-source-setup:

3. Installation set-up
----------------------

Download and run the `installation setup script from GitHub <https://raw.githubusercontent.com/lsst/lsst/12.1/scripts/newinstall.sh>`__, which installs the basic packages required to install other packages:

.. code-block:: bash

   curl -OL https://raw.githubusercontent.com/lsst/lsst/12.1/scripts/newinstall.sh
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

   source $LSST_INSTALL_DIR/loadLSST.bash # for bash users
   source $LSST_INSTALL_DIR/loadLSST.csh  # for csh users
   source $LSST_INSTALL_DIR/loadLSST.ksh  # for ksh users
   source $LSST_INSTALL_DIR/loadLSST.zsh  # for zsh users

where :file:`$LSST_INSTALL_DIR` is expanded to your installation directory.

.. _install-from-source-packages:

4. Install packages
-------------------

Finally, build/install any other components of the LSST Science Pipelines that are relevant for your work.
A simple way to ensure that you have a fairly complete set of packages for this need is to install ``lsst_apps``.
The dependency tree for ``lsst_apps`` ensures that many other packages (about 70, including e.g., ``pipe_tasks``) are also installed. 

Installing ``lsst_apps`` may take a little while (about 1.2 hr on a 2014-era iMac with 32 GB of memory and 8 cores):

.. code-block:: bash

   eups distrib install -t v12_1 lsst_apps

After this initial setup, it is a good idea to test the installation.
See :ref:`source-install-testing-your-installation`.

.. _install-from-source-loadlsst:

5. Source the LSST environment in each shell session
----------------------------------------------------

Whenever you want to run the installed LSST Science Pipelines in a new terminal session, be sure to :command:`source` the appropriate :file:`loadLSST.{bash,csh,ksh,zsh}` script.

.. _source-install-testing-your-installation:

Testing Your Installation
=========================

Once the LSST Science Pipelines are installed, you can verify that it works by :doc:`running a demo project <demo>`.
This demo processes a small amount of SDSS data.
