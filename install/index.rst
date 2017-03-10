#####################################
Installing the LSST Science Pipelines
#####################################

.. toctree::
   :hidden:
   
   conda
   newinstall
   lsstsw
   demo

We offer a few ways of installing the LSST Science Pipelines.
Choose an option below to get started.

.. note::

   To install the LSST Simulation software, such as MAF, please follow the `LSST Simulations documentation <https://confluence.lsstcorp.org/display/SIM/Catalogs+and+MAF>`_ instead of these guides.

:doc:`Conda installation <conda>`
   Install the Pipelines as an `Anaconda/Miniconda <https://www.continuum.io/why-anaconda>`__ binary package.
   This is the easiest installation option since no source compilation is required.

:doc:`Source installation (newinstall.sh) <newinstall>`
   ``newinstall.sh`` allows you to build and install the LSST Science Pipelines from source.
   You can use your existing Python 2.7, or opt to use a built-in `Miniconda <http://conda.pydata.org/docs/>`__.

`CernVM FS (external link) <https://github.com/airnandez/lsst-cvmfs>`__
   CernVM FS is a virtual machine that makes it easy to run the LSST Science Pipelines without compiling code.
   This distribution is supported by Fabio Hernandez of IN2P3.

`Docker Containers (external link) <https://hub.docker.com/r/lsstsqre/centos/>`__
   These images are convenient for using the LSST Science Pipelines in distributed or cloud-based computing workflows, or for one-off installations without modifying your environment. You can get them from our `DockerHub repo <https://hub.docker.com/r/lsstsqre/centos/>`__

:doc:`lsstsw installation <lsstsw>`
   ``lsstsw`` (and ``lsst-build``) are the tools we use internally to build and test the LSST Science Pipelines.
   Use this installation option if you're interested in developing the Science Pipelines since ``lsstsw`` presents the Pipelines as a directory of cloned repositories from `github.com/lsst <https://github.com/lsst>`__.

Next, :doc:`try out your Science Pipelines installation by running a demo <demo>`.

If you have difficulty installing LSST software:

- review the :ref:`known installation issues for your platform <installation-issues>`.
- reach out on the `Support forum at community.lsst.org <https://community.lsst.org/c/support>`_.
