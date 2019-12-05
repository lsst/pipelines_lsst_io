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

.. note::

   **since 19.0.0**: ubuntu 16 is not supported anymore. Note also that due to compiler or Glibc changes, the demo execution on ubuntu 19.04 and 19.10 will produce slight numeric differences. See :jirab:`DM-22377` jira issue.

Additional installation steps for Ubuntu 19.10
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are deploying ``lsst_distrib`` in an Ubuntu 19.10 operating system, the :command:`gcc` compiler version installed using the above steps is the **8.3.0**. The compiler provided by default with the Ubuntu 19.10 distribution is 9.2.1 and needs to be downgraded. This can be done using the following steps, in addition at the above ones.

.. code-block:: bash

   sudo apt-get install gcc-8 g++-8
   sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 800 --slave /usr/bin/g++ g++ /usr/bin/g++-8

.. warning::

   The command, above, modifies system-wide configuration and will impact other users on the machine.

