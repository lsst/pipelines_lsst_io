.. _source-install-mac-prereqs:

##########################
macOS system prerequisites
##########################

To build LSST software, macOS systems need:

1. :ref:`Xcode <source-install-mac-prereqs-xcode>`, or command line tools.
2. :ref:`cmake <source-install-mac-prereqs-cmake>`.

.. note::

   macOS versions 10.9 and earlier have not been tested recently and may not work.

.. _source-install-mac-prereqs-xcode:

Xcode
=====

You will need to install developer tools, which we recommend you obtain with Apple's Xcode command line tools package.
To do this, run from the command line (e.g. ``Terminal.app`` or similar):

.. code-block:: bash

   xcode-select --install

You can verify where the tools are installed by running:

.. code-block:: bash

   xcode-select -p

.. _source-install-mac-prereqs-cmake:

cmake
=====

``cmake`` can be installed through a package manager like `Homebrew <https://brew.sh>`_:

.. code-block:: bash

   brew install cmake

**Alternatively,** `Anaconda <https://www.continuum.io/downloads>`_ users can install ``cmake`` with :command:`conda`:

.. code-block:: bash

   conda install cmake
