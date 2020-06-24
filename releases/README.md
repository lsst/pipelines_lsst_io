# How to document releases

## Release notes

Release notes are published through the `releases/vXX_Y_Z.rst` files; one per each release
In addition, the `releases/tickets/vXX_Y_Z.rst` file lists all the tickets closed in the corresponding release.

To start release notes for a new release:

1. Create a new file in `releases/` based on the template below
2. Create a new file in `releases/tickets` listing all the tickets closed in this release
3. Remove the `release-latest` label from the previous latest release
4. Add an entry for `vXX_Y_Z` to `releases/index.rst`

### Template for release notes

```
.. _release-latest:
.. _release-vNN-N:

#####################################
LSST Science Pipelines XX.Y.Z Release
#####################################

.. toctree::
   :hidden:

   tickets/vXX_Y_Z

+-------------------------------------------+------------+
| Source                                    | Identifier |
+===========================================+============+
| Git tag                                   | XX.Y.Z     |
+-------------------------------------------+------------+
| :doc:`EUPS distrib </install/newinstall>` | vXX\_Y\_Z  |
+-------------------------------------------+------------+

This release is based on the ``w_YYYY_NN`` weekly build.

These release notes highlight significant changes to the Science Pipelines codebase which are likely to be of wide interest.
For a complete list of changes made, see :doc:`tickets/vXX_Y_Z`.

- :ref:`release-vXX-Y-Z-functionality`
- :ref:`release-vXX-Y-Z-interface`
- :ref:`release-vXX-Y-Z-pending-deprecations`
- :ref:`release-vXX-Y-Z-deprecations`

*See also:*

.. todo::

   Insert link to the CMR when it is available.

.. todo::

   Insert link to Doxygen documentation when the release is frozen.

- :doc:`Installation instructions </install/index>`
- :doc:`Known issues </known-issues>`
- `Characterization Metric Report (DMTR-NNN) <https://ls.st/DMTR-NNN>`_
- `Doxygen Documentation`__

__ http://doxygen.lsst.codes/stack/doxygen/xlink_master_XXXX/


.. _release-vXX-Y-Z-functionality:

Major New Features
==================

.. Insert list of :ref:`..` to individual items

.. Add items here

.. _release-vXX-Y-Z-interface:

Significant Interface Changes
=============================

.. Insert list of :ref:`..` to individual items

.. Add items here

.. _release-vXX-Y-Z-pending-deprecations:

Pending Deprecations
====================

.. That is, items that we anticipate deprecating in the next release
.. Insert list of :ref:`..` to individual items

.. Add items here

.. _release-vXX-Y-Z-deprecations:

Deprecations
============

.. That is, items that are deprecated in this releas
.. Insert list of :ref:`..` to individual items

.. Add items here


```

Release note items have headers at the `-` symbol level.

Use the

```
:jirab:`DM-NNNN`
```

role at the of release note items to indicate and link to the corresponding link tickets and RFCs.
If the item is a single paragraph, the JIRA link should occur at the end of the paragraph.
If the item has several paragraphs, the JIRA link should occur in its own paragraph at the end of the release note item.
