.. _docker:

###################
Running with Docker
###################

LSST provides versioned Docker images containing the Science Pipelines software.
With Docker, you can quickly install download and run the LSST Science Pipelines on any platform without compiling from source.

If you have issues, reach out on the `LSST Community support forum <https://community.lsst.org/c/support>`_.

.. _docker-prereqs:

Prerequisites
=============

To download Docker images and run containers, you need Docker's software.
The `Docker Community Edition <https://store.docker.com>`_ is freely available for most platforms, including macOS, Linux, and Windows.

If you haven't used Docker before, you might want to learn more about Docker, images, and containers.
Docker's `Getting Started <https://docs.docker.com/get-started/>`_ documentation is a good resource.

.. _docker-quick-start:

Quick start
===========

This command downloads a weekly build of the LSST Science Pipelines, starts a container, and opens a prompt:

.. code-block:: bash

   docker run -ti lsstsqre/centos:7-stack-lsst_distrib-w_2017_35

Then in the container's shell, load the LSST environment and set up a :doc:`top-level package <top-level-packages>` (``lsst_distrib`` in this case):

.. code-block:: bash

   source /opt/lsst/software/stack/loadLSST.bash
   setup lsst_distrib

This step is equivalent to the :doc:`setup instructions <setup>` for a :doc:`newinstall.sh <newinstall>`\ -based installation.
In fact, the images are internally based on :command:`newinstall.sh`.

Next, learn more with these topics:

- :ref:`docker-tags`

.. _docker-tags:

Finding images for different LSST Science Pipelines releases
============================================================

LSST Science Pipelines Docker images are published as `lsstsqre/centos`_ on Docker Hub.
These images are based on the CentOS base image.

Docker images are versioned with tags, allowing you to run any release of the LSST Science Pipelines software.
The schema of these tags is:

.. code-block:: text

   <centos major version>-stack-<EUPS product>-<EUPS distrib tag>

For example:

.. code-block:: text

   7-stack-lsst_distrib-w_2017_35

This tag corresponds to:

- CentOS 7 operating system.
- ``lsst_distrib`` :doc:`top-level package <top-level-packages>`.
- ``w_2017_35`` EUPS tag. See :ref:`newinstall-other-tags` for an overview of LSST's EUPS tag schema.

You can see what tags are available by browsing `lsstsqre/centos on Docker Hub <https://hub.docker.com/r/lsstsqre/centos/tags/>`_.

.. _`lsstsqre/centos`: https://hub.docker.com/r/lsstsqre/centos/
