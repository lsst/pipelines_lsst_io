###############################################
Development Tutorial with lsstsw and lsst-build
###############################################

The page :doc:`/install/index` describes how to obtain a released version of the Science Pipelines.
However, developers will want to work and build directly against the Pipelines's Git repositories.
This page describes how to develop the Science Pipelines using the ``lsstsw`` build tool.

1. :ref:`lsstsw-workflow-obtaining-lsstsw-stack`
2. :ref:`lsstsw-workflow-working-ticket`
3. :ref:`lsstsw-workflow-jenkins`
4. :ref:`lsstsw-workflow-pr`
5. :ref:`lsstsw-workflow-reset`
6. :ref:`lsstsw-workflow-ext`

Developers should consult the `LSST DM Developer Guide <http://developer.lsst.io>`_, which comprehensively covers DM coding standards and development workflows.

.. _lsstsw-workflow-prerequisites:

Prerequisites
=============

Before embarking on Science Pipelines development, ensure you have all software dependencies installed on your system.
These dependencies are listed in the :doc:`guide to installing the stack from source </install/index>`.

For ``lsstsw``-based development you will need to work in a bash shell.

Additionally, consult the `Development Workflow page of the Developer Guide <http://developer.lsst.io/en/latest/processes/workflow.html>`_ for guidance setting up Git and Git LFS for DM development and our policies on JIRA ticketing, Git branching, testing with Jenkins, code review and merging.
We'll link to relevant sections of the `Development Workflow <http://developer.lsst.io/en/latest/processes/workflow.html>`_ throughout this tutorial.

.. _lsstsw-workflow-obtaining-lsstsw-stack:

Obtaining a Development Stack with lsstsw
=========================================

Code for the LSST Stack is distributed across many Git repositories (see `github.com/lsst <https://github.com/lsst>`_).
`lsstsw <https://github.com/lsst/lsstsw>`_ is a tool that helps you manage the codebase by automating the process of cloning all of these repositories and building that development Stack for testing.

.. _lsstsw-workflow-obtaining-lsstw-stack-get:

Step 1. Get lsstsw
------------------

Begin by choosing a work directory, then clone ``lsstsw`` into it:

.. prompt:: bash

   git clone https://github.com/lsst/lsstsw.git
   cd lsstsw

.. _lsstsw-workflow-obtaining-lsstw-stack-deploy:

Step 2. Deploy lsstsw
---------------------

Prepare the development environment by running two commands in the :file:`lsstsw/` directory:

.. prompt:: bash

   ./bin/deploy
   . bin/setup.sh

The ``deploy`` script automates several things for you:

1. installs a miniconda_ Python environment specific to this lsstsw workspace,
2. installs EUPS_ in :file:`eups/current/`,
3. clones `lsst-build`_, which will run the build process for us,
4. clones versiondb_, a robot-made Git repository of package dependency information, and
5. creates an empty Stack *installation* directory, :file:`stack/`.

By default, ``lsstsw`` `clones repositories using HTTPS <https://github.com/lsst/lsstsw/blob/master/etc/repos.yaml>`_.
Our guide to `Setting up a Git credential helper <http://developer.lsst.io/en/latest/tools/git_lfs.html>`_ will allow you to push new commits up to GitHub without repeatedly entering your GitHub credentials.

The ``setup.sh`` step enables EUPS_, the package manager used by LSST.
**Whenever you open a new terminal session, you need to run '. bin/setup.sh' to activate your lsstsw environment.**

.. _lsst-build: https://github.com/lsst/lsst_build
.. _versiondb: https://github.com/lsst/versiondb
.. _EUPS: https://github.com/RobertLuptonTheGood/eups
.. _miniconda: http://conda.pydata.org/miniconda.html

.. _lsstsw-workflow-obtaining-lsstw-stack-rebuild:

Step 3. Download and build the stack
------------------------------------

Run

.. prompt:: bash

   rebuild lsst_apps

Initially this will ``git clone`` all of the Stack repositories.
A high-bandwidth connection is helpful since the stack contains a non-trivial amount of code and test data.

.. TODO suggest keeping a separate clone of afwdata and linking it when necessary (put in git recipes page)

Next, ``rebuild`` will run our Scons-based build process to compile C++, make Swig bindings, and ultimately create the ``lsst`` Python package.
The Stack is built and installed into the :file:`stack/` directory inside your :file:`lsstsw/` work directory.

Note that we ran ``rebuild lsst_apps`` since `lsst_apps`_ is a meta package that depends on the entire Stack, thus ensuring you have a complete Stack to develop on.

.. _lsst_apps: https://github.com/lsst/lsst_apps

.. _lsstsw-workflow-obtaining-lsstw-stack-current:

Step 4. Tag the current build
-----------------------------

Once the ``rebuild`` step finishes, take note of the build number printed on screen.
It is formatted as "``bNNNN``."
Tell EUPS this is the current build by making a clone of the build's EUPS tag and calling it "``current``:"

.. prompt:: bash

   eups tags --clone bNNNN current

*Note:* this command will print ``eups tags: local variable 'tagNames' referenced before assignment``; this is a known EUPS bug that doesn't affect functionality.

You now have a working Stack, ready for development.

.. _lsstsw-workflow-working-ticket:

Working on a Ticket
===================

At LSST Data Management, we use `tickets on JIRA to track work <http://developer.lsst.io/en/latest/processes/workflow.html#workflow-jira>`_.
You might be assigned an existing ticket, or you might create a new ticket to work on.
These tickets are named "``DM-MMMMM``."

.. _JIRA: https://jira.lsstcorp.org

When beginning any Stack development work, ensure lsstsw is setup in your terminal sessions.
From the ``lsstsw/`` directory:

.. prompt:: bash

   . bin/setup.sh

.. _lsstsw-workflow-working-ticket-branch:

Step 1. Create ticket branches for repositories in development
--------------------------------------------------------------

Make a `ticket branch <http://developer.lsst.io/en/latest/processes/workflow.html#git-branch-ticket>`_ for each repository involved in your ticket work.
From a package's repository in ``lsstsw/build``:

.. prompt:: bash

   git checkout -b tickets/DM-MMMM

*(repeat for other packages in development)*

Note that you can do local work on arbitrarily-named branches, but all commits that you intend to make a pull request for must be in ``tickets/DM-MMMM`` branches.
If you want to push non-ticket work up an LSST repository on GitHub you can prefix your branch's name with ``u/{{username}}/`` (as in, your GitHub username).
`Our developer workflow page explains DM's Git branch policy. <http://developer.lsst.io/en/latest/processes/workflow.html#git-branching>`_

Next, create this branch on the GitHub remote.
From a package's repository in ``lsstsw/build``:

.. prompt:: bash

   git push -u

*(repeat for other packages in development)*

This initial push will create a remote branch ``origin/tickets/DM-MMMM`` and *track* it so that you can simply ``git push`` and ``git pull`` without arguments between the ticket branch on the ``origin`` remote and your local clone.

.. _lsstsw-workflow-working-ticket-declare:

Step 2. Declare these repositories to EUPS
------------------------------------------

We need to tell EUPS_ about these development repositories (with ``eups declare``) and set them up for building (with ``setup``).
From a package's repository in ``lsstsw/build``:

.. prompt:: bash

   eups declare -r . -t $USER {{package_name}} git
   setup -r . -t $USER

*(repeat for other packages in development)*

Unpacking the ``eups declare`` arguments:

- ``-r .`` is the path to the package's repository, which is the current working directory.
  You don't *need* to be in the repository's directory if you provide the path appropriately.
- ``-t $USER`` sets the EUPS *tag*.
  We use this because your username (``$USER``) is an allowed EUPS tag.
- ``git`` is used as an EUPS *version*.
  Semantically we default to calling the version "``git``" to indicate this package's version is the HEAD of a Git development branch.

In the above ``eups declare`` command we associated the package version "``git``" with the tag "``$USER``."
In running ``setup``, we told EUPS to setup the package *and its dependencies* with the version associated to the ``$USER`` tag.
If the ``$USER`` tag isn't found for dependencies, EUPS will revert to using versions of dependencies linked to the ``current`` tag.
This is why we initially declared the entire lsstsw repository to have the version ``current``.

.. why not setup -j? Means setup *just* this package, no dependencies

.. _lsstsw-workflow-working-ticket-scons:

Step 3. Compile and test with SCons
-----------------------------------

Develop the package(s) as you normally would.
To build the Stack with the newly-developed package, run SCons from the repository of a package being developed:

.. prompt:: bash

   scons -Q -j 6 opt=3 

These flags tell SCons to build with flags:

- ``-Q``: reduce logging to the terminal,
- ``-j 6``: build in parallel (e.g., with '6' CPUs),
- ``opt=3``: build with level 3 optimization.

This ``scons`` command will run several targets by default, in sequence:

1. ``lib``: build the C++ code and SWIG interface layer
2. ``python``: install the Python code
3. ``tests``: run the test suite
4. ``example``: compile the examples,
5. ``doc``: compile Doxygen-based documentation, and
6. ``shebang``: convert the ``#!/usr/bin/env`` line in scripts for OS X compatibility (see `DMTN-001 <http://dmtn-001.lsst.io>`_).

You can build a subset of these targets by specifying one explicitly.
To simply compile C++, SWIG, build the Python package and run tests:

.. prompt:: bash

   scons -q -j 6 opt=3 tests

If you are developing multiple packages simultaneously on the same ticket branch, you can compile and test all of them with the ``rebuild`` command from :file:`lsstsw/`:

.. prompt:: bash

   rebuild -r tickets/DM-MMMM lsst_apps

This will build all Stack repositories within the ``lsst_apps`` umbrella using the ``tickets/DM-MMMM`` ticket branch if available (falling back to the ``master`` branch).

.. _lsstsw-workflow-jenkins:

Continuous Integration with Jenkins
===================================

We use a Jenkins instance to run continuous integration tests on the LSST Stack.
Jenkins tests the Stack against multiple environments, ensuring that your code is robust.

Step 1. Ensure the code is pushed
---------------------------------

``git push`` all commits in development branches of packages to the remote development branches on GitHub.

Step 2. Log into ci.lsst.codes
------------------------------

Open https://ci.lsst.codes/job/stack-os-matrix/build?delay=0sec in a browser and setup an account if you have not already done so.
Once logged in you will see the Jenkins job submission page.
On that page:

1. Enter the name(s) of development branches to include in the build in the **BRANCHES** field.
2. Click the **Submit** button and wait.

You can monitor builds in the `"Bot: Jenkins" HipChat room <https://lsst.hipchat.com/rooms/show/1648522>`_.
If your build is shown to have failed, you can click on the 'Console' link in the HipChat message to see a build log.

.. _lsstsw-workflow-pr:

Making a Pull Request and Merging
=================================

Once your code is passing tests, it's ready to be packaged, sent for review, and ultimately merged.

Our `DM Development Guide <http://developer.lsst.io/en/latest/processes/workflow.html>`_ has a comprehensive section on `DM's code review process <http://developer.lsst.io/en/latest/processes/workflow.html#workflow-code-review>`_.
Please review that document thoroughly to learn about the nuances of DM's development workflow; here we outline the basic steps:

1. `Rebase your commit history against the latest master branch <http://developer.lsst.io/en/latest/processes/workflow.html#workflow-pushing>`_ (or other integration branch) and update your development branch on GitHub.

2. `Create a GitHub pull request <http://developer.lsst.io/en/latest/processes/workflow.html#workflow-pr>`_.

3. `Assign a reviewer <http://developer.lsst.io/en/latest/processes/workflow.html#workflow-review-assign>`_.

4. `Discuss the code on the GitHub pull request page <http://developer.lsst.io/en/latest/processes/workflow.html#workflow-code-review-process>`_.

5. `Merge the ticket branch <http://developer.lsst.io/en/latest/processes/workflow.html#workflow-code-review-merge>`_ and mark the ticket as done.

.. _lsstsw-workflow-reset:

Resetting your lsstsw development stack
=======================================

.. _lsstsw-workflow-pr-undeclare:

Removing Eups username tags
---------------------------

Once your work is merged into master, Eups no longer needs to track the ``git`` development version; instead we can use the default ``current`` tag to refer to the latest build.

To remove your Eups username tag, run this command from each package repository involved in your previous development:

.. prompt:: bash

   eups undeclare -t $USER {{package_name}} git

Replace the version name as needed if you didn't use the default EUPS version 'git'
(from :ref:`Step 2 <lsstsw-workflow-working-ticket-declare>` of *Working on a Ticket*).

.. _lsstsw-workflow-rebuild:

Rebuilding your lsstsw development stack
----------------------------------------

Finally, you can also update your entire development stack.
This involves pulling ``master`` branches for all Stack repositories and recompiling the Stack from source.
``lsstsw`` automates this with the ``rebuild`` command.
Before rebuilding, ensure that any work in any Git repository has been pushed to GitHub.
``rebuild`` wipes the existing repositories.
Unpushed work will be deleted.

From the ``lsstsw/`` directory:

.. prompt:: bash

   rebuild lsst_apps

Then re-tag the build as ``current`` (see :ref:`above <lsstsw-workflow-obtaining-lsstw-stack-current>`).

.. _lsstsw-workflow-ext:

Extending the lsstsw Workflow
=============================

The above workflow described an idealized case of working on a single ticket.
This section describes how to extend the basic workflow for more complex cases.

.. _lsstsw-workflow-ext-rebuild:

Refreshing the master for the entire stack
------------------------------------------

If the ticket is taking an extended time to develop, you may need to update the master branches of the entire Stack to reliably test and merge your ticket branch.
The most robust way to do this is by rebuilding the lsstsw environment completely (:ref:`see above <lsstsw-workflow-rebuild>`).

Before doing, ensure that all work is pushed to branches on GitHub.

After the rebuild, you will need to EUPS tag the current Stack, following :ref:`the instructions above <lsstsw-workflow-obtaining-lsstw-stack-current>`.

Finally, checkout your work branches from the GitHub remote and :ref:`declare these work repositories to EUPS following <lsstsw-workflow-working-ticket-declare>`.

..
  Working on Multiple Tickets in lsstsw
  -------------------------------------
  
  TODO
  
  - undeclare
  - declare
  - setup
