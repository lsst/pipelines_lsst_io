.. _source-install-redhat-prereqs:

####################################
RedHat / CentOS system prerequisites
####################################

First install the packages required to build the distribution products:

.. code-block:: bash

    yum install \
        bison \
        blas \
        bzip2 \
        bzip2-devel \
        cmake \
        curl \
        flex \
        fontconfig \
        freetype-devel \
        gawk \
        gcc-c++ \
        gcc-gfortran \
        gettext \
        git \
        glib2-devel \
        java-1.8.0-openjdk \
        libcurl-devel \
        libuuid-devel \
        libXext \
        libXrender \
        libXt-devel \
        make \
        mesa-libGL \
        ncurses-devel \
        openssl-devel \
        patch \
        perl \
        perl-ExtUtils-MakeMaker \
        readline-devel \
        sed \
        tar \
        which \
        zlib-devel

.. from https://github.com/lsst-sqre/puppet-lsststack/blob/master/manifests/params.pp

Prefix the :command:`yum` command with :command:`sudo` if necessary.

Then install the CentOS Linux Software Collections release file:

.. code-block:: bash

   yum install centos-release-scl

And finally the latest compiler packages:

.. code-block:: bash

   yum install devtoolset-8-gcc-gfortran devtoolset-8-gcc devtoolset-8-gcc-c++

Activate the compiler provided by devtoolset-8 as follows:

.. code-block:: bash

   scl enable devtoolset-8 bash

Check that the :command:`gcc` compiler is *version 6.3 or later* by running:

.. code-block:: bash

   gcc -v

Now you are ready to proceed with the installation.

.. note::

   **New after 18.1**: The gcc compiler to be used must support **C++ 14**. The gcc compiler version used in both Red Hat / CentOS 6 and 7 to verify the LSST Science Pipelines distribution is **gcc 8.3.1**, provided by devtoolset-8.
