.. _docker:

###################
Running with Docker
###################

LSST provides versioned Docker images containing the Science Pipelines software.
With Docker, you can quickly install, download, and run the LSST Science Pipelines on any platform without compiling from source.
Docker is an effective and reliable alternative to the :doc:`lsstinstall <lsstinstall>` and :doc:`lsstsw <lsstsw>`\ -based methods that install LSST software directly on your system.

If you have issues using the LSST Docker images, reach out on the `LSST Community support forum <https://community.lsst.org/c/support>`_.

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

This command downloads a current version of the LSST Science Pipelines Docker image (see also :ref:`docker-tags`), starts a container, and opens a prompt:

.. jinja:: default

   .. code-block:: bash

      docker run -ti lsstsqre/centos:7-stack-lsst_distrib-{{ release_eups_tag }}

Then in the container's shell, load the LSST environment and activate the ``lsst_distrib`` top-level package:

.. code-block:: bash

   source /opt/lsst/software/stack/loadLSST.bash
   setup lsst_distrib

This step is equivalent to the :doc:`set up instructions <setup>` for a :doc:`lsstinstall <lsstinstall>`\ -based installation.
In fact, the images are internally based on :command:`lsstinstall`.

When you're done with the container, exit from the container's shell:

.. code-block:: bash

   exit

This returns you to the original shell on your host system.

Next, learn more with these topics:

- :ref:`docker-mount`
- :ref:`docker-detached`
- :ref:`docker-develop`
- :ref:`docker-tags`

.. _docker-mount:

How to mount a host directory into a container
==============================================

When you run a Docker container, you're working inside a system that is isolated from your host machine.
The container's filesystem is distinct from your host machine's.

You can mount a host directory into the container, however.
When you mount a host directory to a container, the data and code that resides on your host filesystem is accessible to the container's filesystem.
This is useful for processing data with the LSST Science Pipelines and even developing packages for the Science Pipelines.

To mount a local directory, add a ``-v <host directory>/<mount directory>`` argument to the :command:`docker run` command.
For example:

.. jinja:: default

   .. code-block:: bash

      docker run -it -v `pwd`:/home/lsst/mnt lsstsqre/centos:7-stack-lsst_distrib-{{ release_eups_tag }}

The example mounts the current working directory (```pwd```) to the ``/home/lsst/mnt`` directory in the container.

If you run :command:`ls` from the container's prompt you should see all files in the current working directory of the host filesystem:

.. code-block:: bash

   ls mnt

As usual with interactive mode (``docker run -it``), you can ``exit`` from the container's shell to stop the container and return to the host shell:

.. code-block:: bash

   exit

.. _docker-detached:

How to run a container in the background and attach to it
=========================================================

The :ref:`docker-quick-start` showed you how to run a container in interactive mode.
In this mode, Docker immediately opens a shell in the new container.
When you ``exit`` from the shell, the container stops.

An alternative is to run a container in a detached state.
With a detached container, the container won't stop until you specify it.

To get started, run the container with the ``-d`` flag (**detached**):

.. jinja:: default

   .. code-block:: bash

      docker run -itd --name lsst lsstsqre/centos:7-stack-lsst_distrib-{{ release_eups_tag }}

You still use the ``-it`` arguments to put the container in interactive mode, even though Docker doesn't immediately open a container prompt for you.

The ``--name lsst`` argument gives the new container a name.
You can choose whatever name makes sense for your work.
This example uses the name "``lsst``."

Next, from a shell on your host system (the same shell as before, or even a new shell) open a shell in the container with the :command:`docker exec` command:

.. code-block:: bash

   docker exec -it lsst /bin/bash

Your prompt is now a prompt in the container.

You can repeat this process, attaching to the container multiple times, to open multiple container shells.

To close a container shell, type ``exit``.

Finally, to stop the container entirely, run this command from your host's shell:

.. code-block:: bash

   docker stop lsst

And delete the container:

.. code-block:: bash

   docker rm lsst

.. _docker-develop:

How to develop packages inside Docker containers
================================================

You can develop code, including LSST Science Pipelines packages, with the LSST Science Pipelines Docker images.
This section summarizes the containerized development workflow.
Refer to :doc:`package-development` for general information.

Basic set up
------------

These steps show how to run a container and build a LSST Science Pipelines package in it:

1. **From the host shell,** clone packages into the current working directory.
   For example:

   .. code-block:: bash

      git clone https://github.com/lsst/pipe_tasks

   Any datasets you're working with should be in the current working directory as well.

2. **From the host shell,** start the container with the current working directory mounted:

   .. jinja:: default

      .. code-block:: bash

         docker run -itd -v `pwd`:/home/lsst/mnt --name lsst lsstsqre/centos:7-stack-lsst_distrib-{{ release_eups_tag }}

   This starts the container in a detached mode so you can open and exit multiple container shells.
   Follow the steps in :ref:`docker-detached` to open a shell in the container.

3. **From the container's shell,** activate the LSST environment and setup the top-level package:

   .. code-block:: bash

      source /opt/lsst/software/stack/loadLSST.bash
      setup lsst_distrib

4. **From the container's shell,** change into the directory of the package you cloned and set it up.
   For example:

   .. code-block:: bash

      cd mnt/pipe_tasks
      setup -r .

   .. note::

      Compared to the :ref:`typical development work <package-dev-setup>`, the :command:`setup` command shown here does not include the ``-t $USER`` argument to tag the development package.
      This is because the Docker container doesn't have a ``$USER`` environment variable set by default.
      You can still set up and develop the package this way, it just won't be tagged by EUPS.

5. **From the container's shell,** build the package.
   For example:

   .. code-block:: bash

      scons -Q -j 6 opt=3

The containerized development workflow
--------------------------------------

To develop packages with Docker containers you will use a combination of shells and applications on both the host system and inside the Docker container.

**On the host system** you will run your own code editors and :command:`git` to develop the package.
This way you don't have to configure an editor of :command:`git` inside the container.
This is why we mount a local directory  with the code and data in it.

**In container shells** you run commands to set up packages (:command:`setup`), compile code (:command:`scons`), test code (:command:`pytest`), and run the Pipelines on data (:command:`processCcd.py`, for example).
Use :command:`docker exec` to open multiple shells in the container (see :ref:`docker-detached`).

Cleaning up the development container
-------------------------------------

You can stop and delete the container at any time:

.. code-block:: bash

   docker stop <container name>
   docker rm <container name>

In this example, the container is named ``lsst``.

Stopping and deleting a container doesn't affect the data in the local directory you mounted into that container.

.. _docker-tags:

Finding images for different LSST Science Pipelines releases
============================================================

LSST Science Pipelines Docker images are published as `lsstsqre/centos`_ on Docker Hub.
These images are based on a CentOS_ base image.

Docker images are versioned with tags, allowing you to run any release of the LSST Science Pipelines software.
The schema of these tags is:

.. code-block:: text

   <centos major version>-stack-<EUPS product>-<EUPS distrib tag>

For example:

.. jinja:: default

   .. code-block:: text

      7-stack-lsst_distrib-{{ release_eups_tag }}

   This tag corresponds to:

   - CentOS 7 operating system.
   - ``lsst_distrib`` :doc:`top-level package <top-level-packages>`.
   - ``{{ release_eups_tag }}`` EUPS tag. See :ref:`lsstinstall-other-tags` for an overview of LSST's EUPS tag schema.

You can see what tags are available by browsing `lsstsqre/centos on Docker Hub <https://hub.docker.com/r/lsstsqre/centos/tags/>`_.

.. seealso::

   See :ref:`lsstinstall-other-tags` for information on the different types of EUPS tags.

.. _`lsstsqre/centos`: https://hub.docker.com/r/lsstsqre/centos/
.. _CentOS: https://www.centos.org
