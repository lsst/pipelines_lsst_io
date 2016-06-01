#####################################
Installing the LSST Science Pipelines
#####################################

.. toctree::
   :hidden:
   
   conda
   eups-distrib
   lsstsw

We offer a few ways of installing the LSST Science Pipelines.
Choose an option below to get started.

:doc:`Conda installation <conda>`
   Install the Pipelines as an `Anaconda/Miniconda <https://www.continuum.io/why-anaconda>`__ binary package.
   This is the easiest installation option since no source compilation is required.

:doc:`Source installation (eups distrib) <eups-distrib>`
   ``eups distrib`` allows you to build and install the LSST Science Pipelines from source.
   You can use your existing Python 2.7, or opt to use a built-in `Miniconda <http://conda.pydata.org/docs/>`__.

`CernVM FS (external link) <https://github.com/airnandez/lsst-cvmfs>`__
   CernVM FS is a virtual machine that makes it easy to run the LSST Science Pipelines without compiling code.
   This distribution is supported by Fabio Hernandez of IN2P3.

`Docker and Amazon Machine Images <https://sqr-002.lsst.io>`__
   These images are convenient for using the LSST Science Pipelines in distributed or cloud-based computing workflows.
   The `SQR-002: Binary Science Pipeline Software Distribution <https://sqr-002.lsst.io>`__ technote describes how to obtain and use these images.

:doc:`lsstsw installation <lsstsw>`
   ``lsstsw`` (and ``lsst-build``) are the tools we use internally to build and test the LSST Science Pipelines.
   Use this installation option if you're interested in developing the Science Pipelines since ``lsstsw`` presents the Pipelines as a directory of cloned repositories from `github.com/lsst <https://github.com/lsst>`__.

If you have difficulty installing LSST software, reach out on the `Support forum at community.lsst.org <community.lsst.org/c/support>`_.
