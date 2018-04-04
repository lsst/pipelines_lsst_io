.. _source-install-redhat-prereqs:

####################################
RedHat / CentOS system prerequisites
####################################

..   yum install bison curl blas bzip2-devel bzip2 flex fontconfig \
       freetype-devel gcc-c++ gcc-gfortran git libuuid-devel \
       libXext libXrender libXt-devel make openssl-devel patch perl \
       readline-devel tar zlib-devel ncurses-devel cmake glib2-devel \
       java-1.8.0-openjdk gettext perl-ExtUtils-MakeMaker \
       centos-release-scl devtoolset-6-gcc devtoolset-6-gcc-c++ \
       devtoolset-6-gcc-gfortran mesa-libGL-devel

First install the packages required to build the ditribution products:

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

and finally the latest compiler packages:

.. code-block:: bash

   yum install devtoolset-6-gcc-gfortran centos-release-scl devtoolset-6-gcc devtoolset-6-gcc-c++


Activate the compiler provided by devtoolset-6 as follows:

.. code-block:: bash

   scl enable devtoolset-6 bash

Check with the command:


.. code-block:: bash

   gcc -v

that the version of your compiler is at least **6.3**.

Now you are ready to proceed with the installation.

.. note::

   **New since 15.0**: The gcc compiler to be used shall support **C++ 14**. The gcc version used in both RedHat / centOS 6 and 7 to compile the LSST Science Pipelines is **gcc 6.3**, provided by devtoolset-6.
