.. _source-install-redhat-prereqs:

####################################
RedHat / CentOS system prerequisites
####################################

First install the packages required to build the distribution products:

.. code-block:: bash

   yum install bison curl blas bzip2-devel bzip2 flex fontconfig \
       freetype-devel gcc-c++ gcc-gfortran git libuuid-devel \
       libXext libXrender libXt-devel make openssl-devel patch perl \
       readline-devel tar zlib-devel ncurses-devel cmake glib2-devel \
       java-1.8.0-openjdk gettext perl-ExtUtils-MakeMaker \
       mesa-libGL

.. from https://github.com/lsst-sqre/puppet-lsststack/blob/master/manifests/params.pp

Prefix the :command:`yum` command with :command:`sudo` if necessary.

Then install the CentOS Linux Software Collections release file:

.. code-block:: bash

   yum install centos-release-scl 

And finally the latest compiler packages:

.. code-block:: bash

   yum install devtoolset-6-gcc-gfortran centos-release-scl devtoolset-6-gcc devtoolset-6-gcc-c++


Activate the compiler provided by devtoolset-6 as follows:

.. code-block:: bash

   scl enable devtoolset-6 bash

Check that the :command:`gcc` compiler is *version 6.3 or later*.

Now you are ready to proceed with the installation.

.. note::

   **New since 15.0**: The gcc compiler to be used must support **C++ 14**. The gcc compiler version used in both Red Hat / CentOS 6 and 7 to verify the LSST Science Pipelines 15.0 distribution is **gcc 6.3.1**, provided by devtoolset-6.
