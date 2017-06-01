:orphan: True

.. _release-v13-0-sui:

Fall 2016 Science User Interface Highlights
===========================================

- PDAC v1 was deployed at NCSA.
  It provides data query and display of SDSS Stripe 82 data processed with the LSST pipeline stack in 2013.
  Please see `the PDAC v1 guide <https://confluence.lsstcorp.org/display/DM/Guide+to+PDAC+version+1>`_ for details and an access guide.

- Finished the Firefly client side code rewrite in JavaScript using React/Redux framework.
  The binary release is available from https://github.com/Caltech-IPAC/firefly/releases.

- Major visualization feature improvements:

  - Firefly JavaScript API and Python API improvements, providing more controls using Firefly visualization components and features. Python API firefly_client is pip and eups installable.
  - Phase folding capabilities for time series data, and light curve plots.
  - Overlay layer on images:
  
          - LSST mask overlay
	  - User can change overlay symbol shape, size, and color.
	  
  - Charts redesign and expansion of capabilities:

	  - Multiple charts of different columns from the same data sets. Display XY 2D plot and histogram at the same time
	  - XY 2D plots with error bars

  - afw.display firefly_display improvement using firefly_client.
  - Developed two Jupyter widgets for Firefly.

