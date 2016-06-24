:orphan: True

.. _release-v12-0-qserv-dax:

Winter 2016 & X2016 QServ and Data Access Release Notes
=======================================================

The 12.0 release of the LSST Science Pipelines includes Qserv release 2016_05.

- :ref:`release-v12-0-qserv-major-changes`
- :ref:`release-v12-0-qserv-bug-fixes`
- :ref:`release-v12-0-qserv-internal-improvements`

*See also:*

- `Qserv 2016_05 documentation <https://www.slac.stanford.edu/exp/lsst/qserv/2016_05/>`_

.. _release-v12-0-qserv-major-changes:

Major Functionality and Interface Changes
-----------------------------------------

- :ref:`release-v12-0-qserv-shared-scans`
- :ref:`release-v12-0-qserv-large-results`
- :ref:`release-v12-0-qserv-query-cancellation`
- :ref:`release-v12-0-qserv-query`
- :ref:`release-v12-0-qserv-logging`
- :ref:`release-v12-0-qserv-sqlalchemy`
- :ref:`release-v12-0-qserv-sql-css`
- :ref:`release-v12-0-qserv-multinode-docker`
- :ref:`release-v12-0-qserv-database-delete`
- :ref:`release-v12-0-qserv-mariadb`
- :ref:`release-v12-0-qserv-czar-in-proxy`
- :ref:`release-v12-0-qserv-docs`

.. _release-v12-0-qserv-shared-scans:

Shared scan performance improvements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Qserv's shared scan capability was extensively reworked, including a new scheduler and page-locking memory
support on the workers. Performance was greatly improved.
:jirab:`DM-3755,DM-4677,DM-4697,DM-4807,DM-4943,DM-5313,DM-5514`

.. _release-v12-0-qserv-large-results:

Robustness with large (multi-gigbyte) result sets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Qserv previously had an issue where dense and highly distributed queries could cause workers to "fire-hose"
the czar, causing it to lock up or fail due to memory and/or CPU exhaustion.  Threading and flow control
changes were made on the czar and workers to address this.  A memory management issue in the mysql proxy
LUA code was also addressed.
:jirab:`DM-5908,DM-5909,DM-5910,DM-6149`

.. _release-v12-0-qserv-query-cancellation:

Query cancellation
^^^^^^^^^^^^^^^^^^

Query cancellation improvements and rework begun in the W16 cycle were completed.  Queries in flight are
now canceled robustly on both czar and workers when a user types ^C to the mysql client.
:jirab:`DM-2699,DM-3562,DM-3564,DM-3946,DM-3945`

.. _release-v12-0-qserv-query:

Query coverage
^^^^^^^^^^^^^^

Qserv now correctly handles queries with "where objectId between", and "where objectId in".
:jirab:`DM-2873,DM-2887`

.. _release-v12-0-qserv-logging:

Logging improvements
^^^^^^^^^^^^^^^^^^^^

Qserv log messages now include user-friendly thread IDs and unique query IDs.  This improves consumability
of logs for both real users and automated tools.
:jirab:`DM-5314,DM-4755,DM-4756`

.. _release-v12-0-qserv-sqlalchemy:

SQLAlchemy client support
^^^^^^^^^^^^^^^^^^^^^^^^^
The SQlAlchemy client library makes a few probe queries on connect to assess Unicode support by the engine.
Some of these queries were problematic for the czar.  This was addressed and SQLAlchemy can now be used as
an alternative client for Qserv.
:jirab:`DM-4648`

.. _release-v12-0-qserv-sql-css:

SQL-based CSS implementation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Qserv's central shared-state (CSS) meta-data service implementation, formerly based on Zookeeper, was
replaced with a more robust and transactional SQL-based implementation. Dependencies on Zookeeper were
removed from the build.
:jirab:`DM-4003,DM-4138,DM-3192,DM-3574,DM-2733`

.. _release-v12-0-qserv-multinode-docker:

Multi-node integration tests via Docker
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A multi-node integration test suite was added, which may be run on a single host via Docker.  The multi-node
integration test is integrated with Travis CI, and now runs automatically on commits to all branches
of the LSST Qserv git repo on github.
:jirab:`DM-5218,DM-3985,DM-4295,DM-3910,DM-3922,DM-4395`

.. _release-v12-0-qserv-database-delete:

Distributed table and database deletion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Distributed table and database deletion were implemented.  Watcher process (wmgr) does deletion on workers,
and state is synchronized via CSS.
:jirab:`DM-2522,DM-2622,DM-2624,DM-4206,DM-2625`

.. _release-v12-0-qserv-mariadb:

Qserv stack now based on MariaDB
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Qserv and all associated services and libraries were ported from MySQL to MariaDB.  Dependencies on mysql and
mysqlclient were removed from the build.
:jirab:`DM-224,DM-5319,DM-5125,DM-5122,DM-4705,DM-3949,DM-5026`

.. _release-v12-0-qserv-czar-in-proxy:

Czar now in-process with mysqlproxy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The Qserv czar was previously wrapped with SWIG then hosted within a Python process which communicated with
mysqlproxy over an XMLRPC interface implemented in Twisted and LUA.  The czar has been reworked so it is
now directly wrapped to LUA and brought into the mysqlproxy process.  This allowed elimination of the XMLRPC
wire protocol and associated code, elimination of several external library dependencies, and removal of all
Python involvement from the proxy/czar process.
:jirab:`DM-4348,DM-5307`

.. _release-v12-0-qserv-docs:

Documentation updates
^^^^^^^^^^^^^^^^^^^^^

Qserv user and installation documentation
(`Qserv 2016_05 documentation <https://www.slac.stanford.edu/exp/lsst/qserv/2016_05/>`_)
was updated/corrected.
:jirab:`DM-5754,DM-4105`

.. _release-v12-0-qserv-bug-fixes:

Bug Fixes
---------

- :ref:`release-v12-0-qserv-service-timeout`
- :ref:`release-v12-0-qserv-testqdisp`
- :ref:`release-v12-0-qserv-match-tables`

.. _release-v12-0-qserv-service-timeout:

Service timeout failure fix
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Qserv services would crash in some instances if left running for several days.  The cause was tracked down
to a missing null handle check in a mysql wrapper library, which was provoked when server connections would
timeout.
:jirab:`DM-5594`

.. _release-v12-0-qserv-testqdisp:

Intermittent testQdisp unit test failure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This was tracked down to a problem with the Executive class mocks used by the unit test.  These mocks did
not handle threading during cancellation correctly.
:jirab:`DM-4928`

.. _release-v12-0-qserv-match-tables:

Data loader didn't work for match tables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The qserv-data-loader.py script was not invoking the correct partitioner for match tables, and was not
passing all required CSS parameters down to the CSS update code.
:jirab:`DM-3656`

.. _release-v12-0-qserv-internal-improvements:

Build and Code Improvements
---------------------------

- :ref:`release-v12-0-qserv-stream-logs`
- :ref:`release-v12-0-qserv-scons`
- :ref:`release-v12-0-qserv-compilers`
- :ref:`release-v12-0-qserv-style`
- :ref:`release-v12-0-qserv-lib-updates`
- :ref:`release-v12-0-qserv-dead-code`
- :ref:`release-v12-0-qserv-docker`
- :ref:`release-v12-0-qserv-integration-tests`
- :ref:`release-v12-0-qserv-futurize`
- :ref:`release-v12-0-qserv-worker-config`
- :ref:`release-v12-0-qserv-taskmsgfactory2`
- :ref:`release-v12-0-qserv-installation-files`

.. _release-v12-0-qserv-stream-logs:

Stream based logging macros
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Qserv was cut over to using stream based logging macros exclusively, and the boost format style logging
macros (considered harmful) were removed from the LSST log package.  A redundant logging wrapping layer
in qserv was also removed.
:jirab:`DM-4616,DM-5204,DM-5202,DM-3037`

.. _release-v12-0-qserv-scons:

Build improvements
^^^^^^^^^^^^^^^^^^

Overly verbose build output from scons was greatly reduced.  Scons files were reworked to treat shared
libraries consistently, and some latent incorrect shared lib linkages were corrected.  Scons files were also
adjusted to avoid unnecessary copying of the source tree into the build tree.
:jirab:`DM-3447,DM-2421,DM-4145,DM-3686,DM-3707`

.. _release-v12-0-qserv-compilers:

Compiler support
^^^^^^^^^^^^^^^^

Issues were addressed to ensure that qserv builds and passes all unit tests on Linux with gcc 4.8.5 - 5.3.1,
and on MacOSX with XCode 7.3.0.  Warnings were addressed wherever possible, and the builds are now largely
warning free except for some warnings produced by third-party library dependencies.  Warnings generated by
the Eclipse Neon C++ code analyzer were also addressed wherever possible.
:jirab:`DM-3584,DM-3663,DM-3803,DM-3772,DM-3779,DM-3915,DM-4398,DM-4470,DM-4529,DM-4704,DM-5788,DM-6292`

.. _release-v12-0-qserv-style:

C++ style and conformance
^^^^^^^^^^^^^^^^^^^^^^^^^

Various small systematic changes were made across the Qserv code base for style consistency.  Anonymous
namespaces were moved to top level of translation units. A single space was added after "if" before
the subsequent paren.  toString() functions were removed in favor of streaming operators.  Non-standard
uint type was replaced with unsigned int.
:jirab:`DM-4753,DM-3888,DM-2452,DM-3805`

.. _release-v12-0-qserv-lib-updates:

Library updates
^^^^^^^^^^^^^^^

Qserv was rolled forward to scisql 0.3.5, mysqlproxy 0.8.5, boost 1.60, and the latest changes from
XRootD were incorporated.  We also moved from using a forked version of the sphgeom library to following the
tip of the official LSST version.
:jirab:`DM-4938,DM-4786,DM-5394,DM-2178,DM-4092,DM-2334`

.. _release-v12-0-qserv-dead-code:

Dead code removal
^^^^^^^^^^^^^^^^^

Unused worker configuration templates and deprecated czar merging codes were removed.  Unused objectId
hinting code was removed from the proxy LUA miniParser.
:jirab:`DM-4440,DM-2320,DM-3952`

.. _release-v12-0-qserv-docker:

Docker improvements
^^^^^^^^^^^^^^^^^^^

Docker container build and deploy scripts continued to be extended, enhanced, and debugged.  Scripts are
currently based on shmux, and have been used for administration of multiple qserv clusters
at both NCSA and IN2P3.
:jirab:`DM-3199,DM-6130,DM-4438,DM-5187,DM-5402,DM-4523,DM-5336`

.. _release-v12-0-qserv-integration-tests:

Integration test improvements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Integration tests were added involving blobs and non-box spatial constraints.  Additionally, a facility to
reset the empty chunk list in the czar was added, which greatly streamlines the integration tests.
:jirab:`DM-991,DM-2900,DM-4383`

.. _release-v12-0-qserv-futurize:

Modernize python code in Qserv admin tools
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Python admin scripts were run through "futurize -1".  One print change was made to runQueries.py.
:jirab:`DM-6324`

.. _release-v12-0-qserv-worker-config:

Worker configuration files
^^^^^^^^^^^^^^^^^^^^^^^^^^

INI file style configuration support was added for the worker, in support of being able to configure
shared scans without resorting to environment variables.
:jirab:`DM-5209`

.. _release-v12-0-qserv-taskmsgfactory2:

Rename TaskMsgFactory2
^^^^^^^^^^^^^^^^^^^^^^

to TaskMsgFactory.  I can't believe we track this kind of nonsense.
:jirab:`DM-2060`

.. _release-v12-0-qserv-installation-files:

Clean up installation files
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Directories cfg/ and proxy/ in the qserv install tree were moved under share/ and lib/ for consistency.
:jirab:`DM-1355`
