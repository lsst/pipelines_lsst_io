.. _source-install-debian-prereqs:

####################################
Debian / Ubuntu system prerequisites
####################################

Debian or Ubuntu systems require the following packages:

.. code-block:: bash

   apt-get install bison ca-certificates cmake flex gettext\
           git libbz2-dev libfontconfig1 libglib2.0-dev \
           libncurses5-dev libreadline6-dev \
           libcurl4-openssl-dev libx11-dev libxrender1 \
           libxt-dev m4 default-jre perl-modules zlib1g-dev \
           curl git libbz2-dev make

.. from https://github.com/lsst-sqre/puppet-lsststack/blob/master/manifests/params.pp

Prefix the :command:`apt-get` command with :command:`sudo` if necessary.

If you get an error run:

.. code-block:: bash

   apt-get update --fix-missing

Then re-run the :command:`apt-get install` command, above.

.. note::

   **New since 15.0**: The gcc compiler to be used shall support **C++ 14**. The gcc version used in Ubuntu 16 to compile the LSST Science Pipelines is **gcc 5.4**.

Additional installation steps for Ubuntu 14
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the case you are deploying ``lsst_distrib`` in an Ubuntu 14.04 operating system, the :command:`gcc` compiler installed using the above steps is the **4.8**. In order to get :command:`gcc` version **5.4**, following steps have to be completed in addition at the above ones.

.. code-block:: bash

   sudo apt-get update
   sudo apt-get install build-essential software-properties-common
   sudo add-apt-repository ppa:ubuntu-toolchain-r/test 
   sudo apt-get update
   sudo apt-get install gcc-5 g++-5
   sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5 60 --slave /usr/bin/g++ g++ /usr/bin/g++-5

.. warning::

   The command, above, modifies system-wide configuration and will impact other users on the machine.

