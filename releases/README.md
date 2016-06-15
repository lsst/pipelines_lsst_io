# How to document releases

## Release notes

Release notes are published through `release-notes.rst`, however, source for individual releases' notes is contained in individual files in `note-source/`.

To start release notes for a new release

1. Create a new notes file in `note-source/` based on the template below
2. Add an include line for that file in `note-source/` in `release-notes.rst` (follow existing pattern)
3. Add a ref link in `release-notes.rst` (follow existing pattern). Change the release marked 'current'

### Template for release notes

```
.. _release-vNN-N:

Cycle 20XY Release (vNN_N)
==========================

+---------------------------------------------+------------+
| Source                                      | Identifier |
+=============================================+============+
| Git tag                                     | NN.N       |
+---------------------------------------------+------------+
| :doc:`EUPS distrib <../install/newinstall>` | vNN\_N     |
+---------------------------------------------+------------+

- :ref:`release-vNN-N-major-changes`
- :ref:`release-vNN-N-bug-fixes`
- :ref:`release-vNN-N-internal-improvements`

*See also:*

- :doc:`Installation instructions <../install/index>`
- :doc:`Known issues <known-issues>`
- :doc:`Measurements & Characterization <metrics/vNN_N/index>`

.. _release-vNN-N-major-changes:

Major Functionality and Interface Changes
-----------------------------------------

.. Insert list of :ref:`..` to individual items

.. Add items here

.. _release-vNN-N-bug-fixes:

Bug Fixes
---------

.. Insert list of :ref:`..` to individual items

.. Add items here

.. _release-vNN-N-internal-improvements:

Build and Code Improvements
---------------------------

.. Insert list of :ref:`..` to individual items

.. Add items here
```

Release note items have headers at the `^` symbol level.

Use the

```
:jirab:`DM-NNNN`
```

role at the of release note items to indicate and link to the corresponding link tickets and RFCs.
If the item is a single paragraph, the JIRA link should occur at the end of the paragraph.
If the item has several paragraphs, the JIRA link should occur in its own paragraph at the end of the release note item.
