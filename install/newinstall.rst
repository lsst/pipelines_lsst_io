###########################################
Install with newinstall.sh and eups distrib
###########################################

This page guides you through installing the LSST Science Pipelines software.
This installation method is recommended for anyone who uses or develops the Pipelines software.

If you have installation issues, here are some ways to get help:

- Review the :ref:`known installation issues <installation-issues>`.
- Ask a question in the `LSST Community support forum <https://community.lsst.org/c/support>`_.

.. _newinstall-prereqs:

1. Prerequisites
================

You can install the LSST Science Pipelines on CentOS 7 (LSST's reference platform) as well as other Linux distributions and macOS (see the `LSST Stack Testing Status <https://ls.st/faq>`_ for information on the platforms we have tested with).

Before you begin, install prerequisite software for your platform:

- :doc:`macOS <prereqs/macos>`
- :doc:`Centos / RedHat <prereqs/centos>`
- :doc:`Debian / Ubuntu <prereqs/debian>`

..
  TK recommended memory, disk space, and build time.

.. _newinstall-source-dir:

2. Make an installation directory
=================================

First, choose where you want to install the LSST Science Pipelines.
Create and change into that directory:

.. code-block:: bash

   mkdir -p lsst_stack
   cd lsst_stack

If you are installing the software for multiple users (a shared stack), see :ref:`newinstall-shared-permissions`.

.. _newinstall-run:

3. Run newinstall.sh
====================

Open a new shell session for the installation (or ensure you haven't used LSST software in that shell before).
If you need to reuse a shell, see :ref:`newinstall-unset-variables`.

Next, run :command:`newinstall.sh` to set up the environment you'll install the LSST Science Pipelines into.
For most use cases we recommend downloading and running :command:`newinstall.sh` like this:

.. code-block:: bash

   curl -OL https://raw.githubusercontent.com/lsst/lsst/14.0/scripts/newinstall.sh
   bash newinstall.sh -ct

Always execute `newinstall.sh` with bash, as shown, regardless of what shell you are in.

We recommend that you opt into the provided Miniconda Python environment (see the links below for more information).

Then load this environment into your shell:

.. TODO Use sphinx-tabs here?

.. code-block:: bash

   source loadLSST.bash # for bash
   source loadLSST.csh  # for csh
   source loadLSST.ksh  # for ksh
   source loadLSST.zsh  # for zsh

.. note::

   Here are ways to customize the :command:`newinstall.sh` installation for specific needs:

   - The default Python environment is Python 3.5.
     **Python 2.7 users,** see :ref:`newinstall-py2`.
   - :ref:`newinstall-user-python`.
   - The recommended installation uses precompiled binary tarballs if available for your platform (and falls back to a source build).
     See :ref:`newinstall-binary-packages`.
     If you will be compiling and linking C++ code against this installation you'll need to ensure your compilers match the distribution's.
     **Developers should review** :ref:`newinstall-binary-compatibility`.

   For background information about :command:`newinstall.sh`, see:

   - :ref:`newinstall-background`.
   - :ref:`newinstall-miniconda`.
   - :ref:`newinstall-reference`.

.. _newinstall-install:

4. Install Science Pipelines packages
=====================================

Install the LSST Science Pipelines packages by running :command:`eups distrib install` for a top-level package and a tagged version.

This example installs the ``v14_0_rc1`` tagged version (current release) of the ``lsst_distrib`` top-level package:

.. code-block:: bash

   eups distrib install lsst_distrib -t v14_0_rc1 lsst_distrib
   curl -sSL https://raw.githubusercontent.com/lsst/shebangtron/master/shebangtron | python
   setup lsst_distrib

If pre-built binaries are available for your platform (and you ran :command:`newinstall.sh` with the :option:`-t <newinstall.sh -t>` argument) the installation should take roughly 10 minutes.
Otherwise, installation falls back to a source build which can take two hours, depending on the top-level package and your machine's performance.

The last command, :command:`setup`, activates the installed packages in your shell environment.
You'll need to run :command:`setup` in each shell session you'll use the LSST Science Pipelines in.
See :doc:`setup` for more information.

.. note::

   - ``lsst_distrib`` is a top-level package that brings-in most LSST Data Management pipelines software, but other top-level packages may be more applicable for your work, such as ``lsst_apps`` or ``lsst_sims``.
     See :doc:`top-level-packages` for more information.

   - ``v14_0_rc1`` is the current release.
     You can install other tagged versions of the LSST Science Pipelines, though.
     See :ref:`newinstall-other-tags`.

   - If you're curious about the shebangtron, see its repository at `github.com/lsst/shebrangtron <https://github.com/lsst/shebangtron>`_.

.. _newinstall-test:

5. Test your installation (optional)
====================================

Once the LSST Science Pipelines are installed, you can verify that it works by :doc:`running a demo pipeline <demo>`.
This demo processes a small amount of SDSS data and verifies that measurements match expected values.

See :doc:`demo` for instructions.

.. _newinstall-next-steps:

Next steps
==========

Add links to topics the reader should go to next.
Examples:

- A topic reminding a user to setup the stack in a new shell.
- Topic explaining top-level packages.
- Topic on compiling a package alongside an existing stack.

Advanced installation topics
============================

The above steps guided you through LSST's recommended installation.
These topics provide additional information about the installation and ways to customize it:

- :ref:`newinstall-shared-permissions`.
- :ref:`newinstall-unset-variables`.
- :ref:`newinstall-background`.
- :ref:`newinstall-miniconda`.
- :ref:`newinstall-py2`.
- :ref:`newinstall-user-python`.
- :ref:`newinstall-binary-packages`.
- :ref:`newinstall-binary-compatibility`.
- :ref:`newinstall-other-tags`.
- :ref:`newinstall-reference`.

.. _newinstall-shared-permissions:

Setting unix permissions for shared installations
-------------------------------------------------

You can make the LSST Science Pipelines installation accessible to multiple users on the same machine.

First, create a separate unix group (called ``lsst``, for example) with a ``umask`` of ``002`` (all access permissions for the group and allow other users to read/execute).

Then set the ownership of the installation directory to the ``lsst`` group, have the ``SGID`` (2000) bit set, and allow group read/write/execute (mode 2775).

.. _newinstall-unset-variables:

Running newinstall.sh in an already set-up shell
------------------------------------------------

If you've run the LSST Science Pipelines previously, you may have conflicting environment variables in your shell.
To be safe, run:

.. code-block:: bash

   unset LSST_HOME EUPS_PATH LSST_DEVEL EUPS_PKGROOT REPOSITORY_PATH

Then return to the instructions step :ref:`newinstall-run`.

.. _newinstall-background:

What newinstall.sh does
-----------------------

:command:`newinstall.sh` creates a self-contained environment on your machine where you can install, run, and develop the LSST Science Pipelines.
You activate this environment in a shell by sourcing the :command:`loadLSST` script in the installation directory (see :ref:`setup-howto`).

Here is how :command:`newinstall.sh` prepares the environment:

- Identifies your operating system and compilers to determine what EUPS binary packages should be installed (the EUPS package root, see :ref:`newinstall-binary-packages`).
- Installs a specific version of Python, through Miniconda, that is compatible with EUPS binary packages (see :ref:`newinstall-miniconda`).
- Installs Conda packages that the LSST Science Pipelines depends on (see :ref:`python-deps`).
- Checks for :command:`git` on your systems and offers to install it if necessary.
- Installs EUPS_, the package manager used by the LSST software stack.

For information about :command:`newinstall.sh`\ ’s arguments, see :ref:`newinstall-reference`.

.. _newinstall-miniconda:

About the Miniconda Python installed by newinstall.sh
-----------------------------------------------------

:command:`newinstall.sh` can install a dedicated Python environment for your LSST Science Pipelines installation.
This Python installation isn't required, but we recommend it.
See :ref:`newinstall-user-python` if required.

The Python environment installed by :command:`newinstall.sh` is Miniconda_, a minimal version of Anaconda_.
By default, :command:`newinstall.sh` installs Python 3.5.2.
If you need to work with your own Python 2.7-only packages, see :ref:`newinstall-py2`.

In this Miniconda environment, :command:`newinstall.sh` installs the Science Pipeline's Python prerequisites.
See :ref:`python-deps` for more information.

This Miniconda installation won't affect your other Python installations (like the system's Python, your own Anaconda or Miniconda, or virtual environments).
The LSST Miniconda environment is only active when you source the ``loadLSST`` script installed by :command:`newinstall.sh` (see :doc:`setup`).

If you install other Python packages in a shell where the LSST Miniconda is activated (with :command:`pip install` or :command:`conda install`) those packages are installed into the LSST Miniconda's :file:`site-packages`, not your system's.
The Python installed by :command:`newinstall.sh` works like an isolated Python environment dedicated to LSST Science Pipelines code and your own related modules---effectively like a `Conda environment <https://conda.io/docs/user-guide/concepts.html#conda-environments>`_ or Python `venv <https://docs.python.org/3/library/venv.html>`_.
This pattern is useful because it reduces the risk of having Python package version incompatibilities.

.. _newinstall-py2:

How to install a Python 2.7 environment with newinstall.sh
----------------------------------------------------------

LSST Science Pipelines is backwards compatible with Python 2.7.
If you need to run your own Python 2.7-only Python packages in conjunction with the Pipelines, you can have :command:`newinstall.sh` install a Python 2.7 environment for you instead of the default Python 3.5 environment.

To select Python 2.7, run :command:`newinstall.sh` with the :option:`-2 <newinstall.sh -2>` flag (in addition to other flags, like :option:`-t <newinstall.sh -t>`):

.. code-block:: bash

   bash newinstall.sh -2

Then follow the remaining instructions at :ref:`newinstall-run`.

See also: :ref:`newinstall-miniconda`.

.. _newinstall-user-python:

How to use your own Python with newinstall.sh
---------------------------------------------

:command:`newinstall.sh` creates a new Python environment by default (pre-configured with Python dependencies).
If necessary, you can use your own pre-existing Python environment.

To do so, run :command:`newinstall.sh` (see :command:`newinstall-run` for details and command arguments).
When :command:`newinstall-run` prompts you to install Miniconda, type ``no``.

Be aware of these caveats when using your own Python installation:

- You are responsible for installing Python package dependencies.
  See :ref:`python-deps`.

- Prebuilt binaries will not be available.
  :command:`eups distrib install` will always install from source.

.. _newinstall-binary-packages:

About EUPS tarball packages
---------------------------

EUPS distrib binary (tarball) packages significantly speed up your installation.
Rather than compiling the LSST Science Pipelines from source, EUPS tarballs are prebuilt packages made specifically for supported platforms.

Platforms are defined by four factors:

1. Operating system.
2. Compiler.
3. Miniconda_ (Python) version.
4. lsstsw_ version (Git ref).

EUPS distrib binary packages are currently being built for these platform combinations:

.. csv-table:: EUPS distrib binary flavors
   :header: "OS","Compiler","Python"

   "macOS ``osx/10.9``", "``clang-800.0.42.1``", "``miniconda3-4.2.12`` (Python 3)"
   "macOS ``osx/10.9``", "``clang-800.0.42.1``", "``miniconda2-4.2.12`` (Python 2)"
   "Redhat ``redhat/el7``", "``gcc-system``", "``miniconda3-4.2.12`` (Python 3)"
   "Redhat ``redhat/el7``", "``gcc-system``", "``miniconda2-4.2.12`` (Python 2)"
   "Redhat ``redhat/el6``", "``devtoolset-3``", "``miniconda2-4.2.12`` (Python 2)"

When you run :command:`newinstall.sh`, it looks at your system to identify your operating system and compiler.
The version of :command:`newinstall.sh` you run also determines the Miniconda_ version and the lsstsw_ build system versions.

Together, these four factors define the URL prefix (called an *EUPS package root*) that :command:`eups distrib install` looks for binary packages from.
If binary tarballs are unavailable for that EUPS package root, :command:`eups distrib install` automatically falls back to compiling LSST Science Pipelines packages from source.

You can see the active EUPS package roots on your system by running:

.. code-block:: bash

   eups distrib path

Here is an example of the output:

.. code-block:: text

   https://eups.lsst.codes/stack/osx/10.9/clang-800.0.42.1/miniconda3-4.2.12-7c8e67
   https://eups.lsst.codes/stack/src

Based on this example, :command:`eups distrib install` will preferentially install EUPS distrib binary packages for the macOS 10.9 system, ``clang-800.0.42.1`` compiler, and ``miniconda3-4.2.12-7c8e67`` Python and lsstsw combination.
If :command:`eups distrib install` cannot find packages at that EUPS package root it will look in the second EUPS package root (https://eups.lsst.codes/stack/src), which provides source packages.

.. _newinstall-binary-compatibility:

EUPS tarball packages and compiler compatibility
------------------------------------------------

EUPS binary tarball packages are prebuilt on LSST's continuous integration servers for a specific combination of operating system, compilers, Python, and Python dependencies.
If you are developing packages alongside this installation, you might encounter application binary interface (ABI) incompatibilities if are using a different compiler version or a different Python environment.

In this case, the more reliable solution is to revert to a source installation.
To do this, repeat the installation but run :command:`newinstall.sh` *without* the :option:`-t <newinstall.sh -t>` argument:

.. code-block:: bash

   bash newinstall.sh -c

Without the :option:`-t <newinstall.sh -t>` argument to :command:`newinstall.sh`, :command:`eups distrib install` will always build and install packages from source, ensuring ABI compatibility.

.. _newinstall-other-tags:

Installing other releases (including daily and weekly tags)
-----------------------------------------------------------

The instructions on this page guide you through installing the current release of the LSST Science Pipelines corresponding to this documentation.
You can, however, install other releases by running :command:`eups distrib install` with a different tag.

The common types of tags are:

- **Major releases,** tagged as ``v<MAJOR>_<MINOR>`` (for example, ``v14_0``).
- **Weekly builds,** tagged as ``w_<YEAR>_<N>`` (for example, ``w_2017_33`` is the 33rd weekly build in 2017).
- **Daily builds,** tagged as ``d_<YEAR>_<MONTH>_<DAY>`` (for example, ``d_2017_09_01`` is the daily build for September 1, 2017).

There are also tags pointing to the most recent releases:

- **Current major release,** tagged as ``current``.
- **Current weekly build,** tagged as ``w_latest``.
- **Current daily build,** tagged as ``d_latest``.

You can see all available tags at https://eups.lsst.codes/stack/src/tags (each tag has a ``.list`` file).

.. note::

   Binary installations may not be available for all tags.
   From https://eups.lsst.codes/stack, browse subdirectories corresponding to your platform and look for ``.list`` files of available tags.
   :command:`eups distrib install` automatically falls back to a source build if binaries are not available.

.. warning::

   You need to ensure that the Python environment created by :command:`newinstall.sh` (see step :ref:`newinstall-run`) is compatible with the tagged software.

   For example, if you are installing a recent weekly you may need to download and run :command:`newinstall.sh` from master:

   .. code-block:: bash

      curl -OL https://raw.githubusercontent.com/lsst/lsst/master/scripts/newinstall.sh
      bash newinstall.sh -ct

   See https://github.com/lsst/lsst/tags for available tagged versions of :command:`newinstall.sh`.

.. _newinstall-reference:

newinstall.sh argument reference
--------------------------------

.. program:: newinstall.sh

.. code-block:: text

   usage: newinstall.sh [-b] [-f] [-h] [-n] [-3|-2] [-t|-T] [-s|-S] [-P <path-to-python>]

.. option:: -b

   Run in batch mode. Don't ask any questions and install all extra packages.

.. option:: -c

   Attempt to continue a previously failed install.

.. option:: -n

   No-op. Go through the motions but echo commands instead of running them.

.. option:: -P <PATH_TO_PYTHON>

   Use a specific python interpreter for EUPS.

.. option:: -2

   Use Python 2 if the script is installing its own Python.

.. option:: -3

   Use Python 3 if the script is installing its own Python. (**default**)

.. option:: -t

   Use pre-compiled EUPS "tarball" packages, if available.

.. option:: -T

   **Do not** use pre-compiled EUPS "tarball" packages. (**default**)

.. option:: -s

   Use EUPS source "eupspkg" packages, if available (compile from source).

.. option:: -S

   **Do not** use EUPS source "eupspkg" packages (do not compile from source).

.. option:: -h

   Display this help message.


.. _Miniconda: https://conda.io/miniconda.html
.. _Anaconda: https://docs.anaconda.com
.. _lsstsw: https://github.com/lsst/lsstsw
.. _EUPS: https://github.com/RobertLuptonTheGood/eups
