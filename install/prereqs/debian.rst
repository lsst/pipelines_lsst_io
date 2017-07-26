.. _source-install-debian-prereqs:

####################################
Debian / Ubuntu system prerequisites
####################################

Debian or Ubuntu systems require the following packages:

.. code-block:: bash

   apt-get install bison ca-certificates \
           cmake flex g++ gettext git libbz2-dev \
           libfontconfig1 libglib2.0-dev libncurses5-dev \
           libreadline6-dev libssl-dev libx11-dev libxrender1 \
           libxt-dev m4 openjdk-8-jre \
           perl-modules zlib1g-dev \

.. from https://github.com/lsst-sqre/puppet-lsststack/blob/master/manifests/params.pp

Prefix the :command:`apt-get` command with :command:`sudo` if necessary.

.. note::

   **New since 11.0**: The minimum gcc version required to compile the LSST Science Pipelines is **gcc 4.8.**
