######################################################
Testing the Science Pipelines Installation with a Demo
######################################################

This demo will allow you to quickly test your LSST Science Pipelines installation, :doc:`regardless of your installation method <index>`.

1. Activate the LSST Science Pipelines
======================================

Remember to first load the LSST Science Pipelines into your shell's environment.
The method depends on how the Science Pipelines were installed:

- :ref:`Conda <conda-install-activate>`
- :ref:`newinstall.sh <install-from-source-loadlsst>`
- :ref:`lsstsw <lsstsw-setup>`

2. Download the Demo Project
============================

Choose a directory to install demo data into.
We'll call this directory :file:`$DEMO_DATA`.
Then run:

.. code-block:: bash

   mkdir -p $DEMO_DATA
   cd $DEMO_DATA
   curl -L https://github.com/lsst/lsst_dm_stack_demo/archive/12.0.tar.gz | tar xvzf -
   cd lsst_dm_stack_demo-12.0

The demo repository consumes roughly 41 MB, contains input images, reference data, and configuration files.
The demo script will process SDSS images from two fields in Stripe 82, as shown in the following table:

==== ====== ===== =========
run  camcol field filters
==== ====== ===== =========
4192 4      300   *(ur)giz*
6377 4      399   *(gz)uri*
==== ====== ===== =========

*Filters in parentheses are not processed if run with the* ``--small`` *option, see below*

3. Run the Demo
===============

Now setup the processing package and run the demo:

.. code-block:: bash

   setup obs_sdss
   ./bin/demo.sh # --small to process a subset of images

For each input image the script performs the following operations:

* generate a subset of basic image characterization (e.g., determine photometric zero-point, detect sources, and measures positions, shapes, brightness with a variety of techniques),
* creates a :command:`./output` subdirectory containing subdirectories of configuration files, processing metadata, calibrated images, FITS tables of detected sources. These "raw" outputs are readable by other parts of the LSST pipeline, and
* generates a master comparison catalog in the working directory from the band-specific source catalogs in the ``output/sci-results/`` subdirectories.

4. Check the Demo Results
=========================

The demo will take a minute or two to execute (depending upon your machine), and will generate a large number of status messages.
Upon successful completion, the top-level directory will contain an output ASCII table that can be compared to the expected results from a reference run.
This table is for convenience only, and would not ordinarily be produced by the production LSST pipelines.  

=============== ========================== ===================================
Demo Invocation Demo Output                Reference output
=============== ========================== ===================================
demo.sh         detected-sources.txt       detected-sources.txt.expected
demo.sh --small detected-sources_small.txt detected-sources_small.txt.expected
=============== ========================== ===================================

The demo output may not be identical to the reference output due to minor variation in numerical routines between operating systems (see :jira:`DM-1086` for details).
The :command:`bin/compare` script will check whether the output matches the reference to within expected tolerances:

.. code-block:: bash

   bin/compare detected-sources.txt.expected detected-sources.txt

The script will print "``Ok``" if the demo ran correctly.

For more information about the processing done by the demo, refer to `its README on GitHub <https://github.com/lsst/lsst_dm_stack_demo>`_.
