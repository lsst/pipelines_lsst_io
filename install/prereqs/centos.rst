.. _source-install-redhat-prereqs:

####################################
RedHat / CentOS system prerequisites
####################################

.. code-block:: bash

   yum install bison curl blas bzip2-devel bzip2 flex fontconfig \
       freetype-devel gcc-c++ gcc-gfortran git libuuid-devel \
       libXext libXrender libXt-devel make openssl-devel patch perl \
       readline-devel tar zlib-devel ncurses-devel cmake glib2-devel \
       java-1.8.0-openjdk gettext perl-ExtUtils-MakeMaker

.. from https://github.com/lsst-sqre/puppet-lsststack/blob/master/manifests/params.pp

Prefix the :command:`yum` command with :command:`sudo` if necessary.

.. note::

   **New since 11.0**: The minimum gcc version required to compile the LSST Science Pipelines is **gcc 4.8.**
   If you are using our previous factory platform, RedHat/CentOS 6, and you are unable to upgrade to version 7 (which comes with gcc 4.8 as default) consult :ref:`the section below on upgrading compilers in legacy Linux <source-install-redhat-legacy>`.

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
