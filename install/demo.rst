######################################################
Testing the Science Pipelines installation with a demo
######################################################

This demo will allow you to quickly test your LSST Science Pipelines installation, :doc:`regardless of your installation method <index>`.

1. Activate the LSST Science Pipelines
======================================

Remember to first load the LSST Science Pipelines into your shell's environment.
The method depends on how the Science Pipelines were installed:

- :doc:`newinstall.sh <setup>`
- :ref:`lsstsw <lsstsw-setup>`

2. Download the demo project
============================

Choose a directory to run the demo in.
For example:

.. code-block:: bash

   mkdir -p demo_data
   cd demo_data

Then download the demo's data (if you aren't running the current stable release, see the note below):

.. jinja:: default

   .. code-block:: bash

      curl -L https://github.com/lsst/pipelines_check/archive/{{ pipelines_demo_ref }}.tar.gz | tar xvzf -
      cd pipelines_check-{{ pipelines_demo_ref }}

.. caution::

   The demo's version should match your LSST Science Pipelines installed software.
   If you installed from source (with :doc:`lsstsw <lsstsw>`) or with a :ref:`newer tag <newinstall-other-tags>`, you'll likely need to run the latest version of the demo (``main`` branch):

   .. code-block:: bash

      curl -L https://github.com/lsst/pipelines_check/archive/main.tar.gz | tar xvzf -
      cd pipelines_check-main

3. Run the demo
===============

Now setup the processing package and run the demo:

.. code-block:: bash

   setup -r .
   ./bin/run_demo.sh


Check that no errors are printed out during the execution.

The script creates a new Butler data repository in the `DATA_REPO` subdirectory containing the raw and calibration data found in the `input_data` directory.
It then processes the data using the `pipetask` command to execute the `ProcessCcd` pipeline.
The outputs from processing are written to the `demo_collection` collection.
The input data is a single raw image from Hyper Suprime-Cam, detector 10 of visit 903342.
