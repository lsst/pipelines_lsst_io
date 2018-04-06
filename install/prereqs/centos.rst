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

   yum install devtoolset-6-gcc-gfortran devtoolset-6-gcc devtoolset-6-gcc-c++

Activate the compiler provided by devtoolset-6 as follows:

.. code-block:: bash

   scl enable devtoolset-6 bash

Check that the :command:`gcc` compiler is *version 6.3 or later*.

.. code-block:: bash

   gcc -v

Now you are ready to proceed with the installation.

.. note::

   **New since 15.0**: The gcc compiler to be used must support **C++ 14**. The gcc compiler version used in both Red Hat / CentOS 6 and 7 to verify the LSST Science Pipelines 15.0 distribution is **gcc 6.3.1**, provided by devtoolset-6.
