.. _source-install-debian-prereqs:

####################################
Debian / Ubuntu system prerequisites
####################################

Debian or Ubuntu systems require the following packages:

.. code-block:: bash

   apt-get install \
       bison \
       ca-certificates \
       cmake \
       curl \
       default-jre \
       flex \
       gettext \
       git \
       libbz2-dev \
       libcurl4-openssl-dev \
       libfontconfig1 \
       libglib2.0-dev \
       libncurses5-dev \
       libreadline6-dev \
       libx11-dev \
       libxrender1 \
       libxt-dev \
       m4 \
       make \
       perl-modules \
       rsync \
       zlib1g-dev

.. from https://github.com/lsst-sqre/puppet-lsststack/blob/master/manifests/params.pp

Prefix the :command:`apt-get` command with :command:`sudo` if necessary.

.. tip::

   If you get an error, run:

   .. code-block:: bash

      apt-get update --fix-missing

   Then re-run the :command:`apt-get install` command, above.

.. note::

   **New since 17.0**: The gcc compiler to be used shall fully support **C++ 14**. The gcc version used to compile the LSST Science Pipelines shall be at least **gcc 6.1**.

Additional installation steps for Ubuntu 16
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are deploying ``lsst_distrib`` in an Ubuntu 16.04 operating system, the :command:`gcc` compiler version installed using the above steps is the **5.4**. In order to get a :command:`gcc` version compatible with **C++ 14**, following steps have to be completed in addition at the above ones.

.. code-block:: bash

   sudo apt-get update
   sudo apt-get install build-essential software-properties-common
   sudo add-apt-repository ppa:ubuntu-toolchain-r/test 
   sudo apt-get update
   sudo apt-get install gcc-6 g++-6
   sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-6 60 --slave /usr/bin/g++ g++ /usr/bin/g++-6

.. warning::

   The command, above, modifies system-wide configuration and will impact other users on the machine.

