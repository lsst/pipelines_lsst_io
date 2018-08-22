#####################################
Documentation contribution guidelines
#####################################

External contributions
======================

This is an open source project and LSST welcomes contributions from the community.
Feel free to create a GitHub issue to report a problem or even submit a pull request.
Issues and pull requests are triaged into LSST's ticketing system, and we'll be able to resolve those issues or merge those pull requests for you.

Project contributors
====================

If you're a member of the LSST Project, and have push access to this repository, please follow `LSST DM's Development Workflow <https://developer.lsst.io/work/flow.html>`__, particularly including the branching conventions.

Content guidelines
==================

Most of this project's content is written in reStructuredText.
Please see the `DM ReStructuredText Style Guide <https://developer.lsst.io/restructuredtext/style.html>`__ for information on how to format things like headers, lists, tables, images, and code samples.

Please write one sentence per line (as opposed to hard-wrapping text to a specific line width).
This makes Git diffs and pull requests easier to use.

Use sentence case for headlines.

The `Stack section of the DM Developer Guide <https://developer.lsst.io/index.html#dm-stack>`__ has more information on how to create content for pipelines.lsst.io.

Building the documentation
==========================

`Documenteer <https://documenteer.lsst.io>`__ is the build tool for LSST's Sphinx-based documentation (like this project).
Depending on whether you're building pipelines.lsst.io as a whole, or just a single package, you can follow one of these tutorials to build and test your documentation changes:

- `Building single-package documentation locally <https://developer.lsst.io/stack/building-single-package-docs.html>`__.
- `Building the pipelines.lsst.io site locally <https://developer.lsst.io/stack/building-pipelines-lsst-io-locally.html>`__.
- `Building pipelines.lsst.io with Jenkins <https://developer.lsst.io/stack/building-pipelines-lsst-io-with-documenteer-job.html>`__.

Reference documentation for the build commands:

- `stack-docs <https://documenteer.lsst.io/pipelines/stack-docs-cli.html>`__: used to build https://pipelines.lsst.io from the `lsst/pipelines_lsst_io <https://github.com/lsst/pipelines_lsst_io>`__ repository itself.
- `package-docs <https://documenteer.lsst.io/pipelines/package-docs-cli.html>`__: used to build documentation for single packages from their ``doc/`` directories.

To get a sense of how all this all works, you can read the `Overview of the Stack documentation system <https://developer.lsst.io/stack/documentation-system-overview.html>`__.

Getting help with contributions
===============================

Whether you have general questions about contributing to pipelines.lsst.io, or need help with a specific piece of documentation that you're contributing, you can get help a couple different ways:

- Ask a question in `#dm-docs <https://lsstc.slack.com/archives/dm-docs>`__ on Slack.
- Ask a question in the `Data Management category <https://community.lsst.org/c/dm>`__ on the LSST Community forum.
