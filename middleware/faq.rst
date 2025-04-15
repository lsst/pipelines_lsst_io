##########################
Frequently asked questions
##########################

.. py:currentmodule:: lsst.daf.butler

This page contains answers to common questions about the data access and pipeline middleware, such as the `Butler` and `~lsst.pipe.base.PipelineTask` classes.
The :ref:`lsst.daf.butler` package documentation includes a number of overview documentation pages (especially :ref:`daf_butler_organizing_datasets`) that provide an introduction to many of the concepts referenced here.

.. _middleware_faq_query_methods:

When should I use each of the query methods/commands?
=====================================================

The `Butler` Python class and :any:`butler <lsst.daf.butler-scripts>` command-line tool support five major query operations that can be used to inspect a data repository:

.. list-table:: Major query operations
   :header-rows: 1

   * - Command-line tool
     - Python API
   * - ``butler query-collections``
     - `Butler.collections.query_info <lsst.daf.butler.ButlerCollections.query_info>`
   * - ``butler query-dataset-types``
     - `Butler.registry.queryDatasetTypes <lsst.daf.butler.Registry.queryDatasetTypes>`
   * - ``butler query-dimension-records``
     - `Butler.query_dimension_records`
   * - ``butler query-datasets``
     - `Butler.query_datasets`
   * - ``butler query-data-ids``
     - `Butler.query_data_ids`

These operations share :ref:`many optional arguments <daf_butler_queries>` that constrain what is returned, but their return types each reflect a different aspect of :ref:`how datasets are organized <daf_butler_organizing_datasets>`).

.. _middleware_faq_query_methods_collections:

Collections
-----------

From the command-line, ``butler query-collections`` generally provides the best high-level view of the contents of a data repository, with the ``--chains=tree`` format.
For all but the smallest repos, it's best to start with some kind of guess at what you're looking for, or the results will still be overwhelming large.

.. code-block:: sh

    $ butler query-collections /repo/main HSC/runs/RC2/* --chains=tree
                     Name                      Type
    -------------------------------------- -----------
    HSC/runs/RC2/w_2021_02/DM-28282/sfm    RUN
    HSC/runs/RC2/w_2021_02/DM-28282/rest   RUN
    HSC/runs/RC2/w_2021_06/DM-28654        CHAINED
      HSC/runs/RC2/w_2021_06/DM-28654/rest RUN
      HSC/runs/RC2/w_2021_06/DM-28654/sfm  RUN
      HSC/raw/RC2/9615                     TAGGED
      HSC/raw/RC2/9697                     TAGGED
      HSC/raw/RC2/9813                     TAGGED
      HSC/calib/gen2/20180117              CALIBRATION
      HSC/calib/DM-28636                   CALIBRATION
      HSC/calib/gen2/20180117/unbounded    RUN
      HSC/calib/DM-28636/unbounded         RUN
      HSC/masks/s18a                       RUN
      skymaps                              RUN
      refcats/DM-28636                     RUN
    HSC/runs/RC2/w_2021_02/DM-28282        CHAINED
      HSC/runs/RC2/w_2021_02/DM-28282/rest RUN
      HSC/runs/RC2/w_2021_02/DM-28282/sfm  RUN
      HSC/raw/RC2/9615                     TAGGED
      HSC/raw/RC2/9697                     TAGGED
      HSC/raw/RC2/9813                     TAGGED
      HSC/calib/gen2/20180117              CALIBRATION
      HSC/calib/DM-28636                   CALIBRATION
      HSC/calib/gen2/20180117/unbounded    RUN
      HSC/calib/DM-28636/unbounded         RUN
      HSC/masks/s18a                       RUN
      skymaps                              RUN
      refcats/DM-28636                     RUN
    HSC/runs/RC2/w_2021_06/DM-28654/sfm    RUN
    HSC/runs/RC2/w_2021_06/DM-28654/rest   RUN

Note that some collections appear multiple times here - once as a top-level collection, and again later as some child of a `~CollectionType.CHAINED` collection (that's what the indentation means here).
In the future we may be able to remove some of this duplication.

Similar functionality can be accessed from Python using `Butler.collections.query_info <lsst.daf.butler.ButlerCollections.query_info>`.

Dataset Types
-------------

`Registry.queryDatasetTypes` reports the :ref:`dataset types <daf_butler_dataset_types>` that have been registered with a data repository, even if there aren't any datasets of that type actually present.
That makes it less useful for exploring a data repository generically, but it's an important tool when you know the name of the dataset type already and want to see how it's defined.

Dimension Records
-----------------

`Butler.query_dimension_records` is the best way to inspect the metadata records associated with data ID keys (:ref:`"dimensions" <lsst.daf.butler-dimensions_overview>`).
Those metadata tables include observations (the ``exposure`` and ``visit`` dimensions), instruments (``instrument``, ``physical_filter``, ``detector``), and regions on the sky (``skymap``, ``tract``, ``patch``, ``htm7``).
That isn't an exhaustive list of dimension tables (actually pseudo-tables in some cases), but you can get one in Python with::

    >>> print(butler.dimensions.getStaticDimensions())

And while `~Butler.query_dimension_records` shows you the schema of those tables with each record it returns, you can also get it without querying for any data with (e.g.)

.. code-block:: python

    >>> print(butler.dimensions["exposure"].schema)
    exposure:
      instrument: string
      id: int
      physical_filter: string
      obs_id: string
      exposure_time: float
          Duration of the exposure with shutter open (seconds).
      dark_time: float
          Duration of the exposure with shutter closed (seconds).
      observation_type: string
          The observation type of this exposure (e.g. dark, bias, science).
      observation_reason: string
          The reason this observation was taken. (e.g. science, filter scan,
          unknown).
      day_obs: int
          Day of observation as defined by the observatory (YYYYMMDD
          format).
      seq_num: int
          Counter for the observation within a larger sequence. Context of
          the sequence number is observatory specific. Can be a global
          counter or counter within day_obs.
      group_name: string
          String group identifier associated with this exposure by the
          acquisition system.
      group_id: int
          Integer group identifier associated with this exposure by the
          acquisition system.
      target_name: string
          Object of interest for this observation or survey field name.
      science_program: string
          Observing program (survey, proposal, engineering project)
          identifier.
      tracking_ra: float
          Tracking ICRS Right Ascension of boresight in degrees. Can be NULL
          for observations that are not on sky.
      tracking_dec: float
          Tracking ICRS Declination of boresight in degrees. Can be NULL for
          observations that are not on sky.
      sky_angle: float
          Angle of the instrument focal plane on the sky in degrees. Can be
          NULL for observations that are not on sky, or for observations
          where the sky angle changes during the observation.
      zenith_angle: float
          Angle in degrees from the zenith at the start of the exposure.
      timespan: timespan

For most dimensions and most data repositories, the number of records is quite large, so you'll almost always want a very constraining ``where`` argument to control what's returned, e.g.:

.. code-block:: sh

    $ butler query-dimension-records /repo/main detector \
        --where "instrument='HSC' AND detector.id IN (6..8)"
    instrument  id full_name name_in_raft raft purpose
    ---------- --- --------- ------------ ---- -------
           HSC   6      1_44           44    1 SCIENCE
           HSC   7      1_45           45    1 SCIENCE
           HSC   8      1_46           46    1 SCIENCE

When working with repositories of transient, cached datasets, note that dimension values may be retained in the registry for datasets that no longer exist (e.g. for provenance purposes) and may sometimes be present for datasets that do not yet exist.

Datasets
--------

`Butler.query_datasets` is used to query for `DatasetRef` objects - handles that point directly to something at least approximately like a file on disk.
These correspond directly to what can be retrieved with `Butler.get`.

Because there are usually many datasets in a data repository (even in a single collection), this also isn't a great tool for general exploration; it's perhaps most useful as a way to explore things *like* the thing you're looking for (perhaps because a call to `Butler.get` unexpectedly failed), by looking with similar collections, dataset types, or data IDs.

`~Butler.query_datasets` usually *isn't* what you want if you're looking for raw-image metadata (use `~Butler.query_dimension_records` instead); it's easy to confuse the dimensions that represent observations with instances of the ``raw`` dataset type, because they are always ingested into the data repository together.

Data Ids
--------

`Butler.query_data_ids` is used to query for combinations of dimension values that *could* be used to identify datasets.

The most important thing to know about `~Butler.query_data_ids` is when *not* to use it:

- It's usually not what you want if you're looking for datasets that already exist (use `~Butler.query_datasets` instead).

- It's usually not what you want if you're looking for metadata associated with those data ID values (use `~Butler.query_dimension_records`).
  While `~Butler.query_data_ids` can do that, too (via the ``with_dimension_records`` parameter), it's overkill if you're looking for metadata that corresponds to a single dimension rather than all of them.

`~Butler.query_data_ids` is most useful when you want to query for future datasets that *could* exist, such as when :ref:`debugging empty QuantumGraphs <middleware_faq_empty_quantum_graphs>`.

.. _middleware_faq_cli_docs:

Where can I find documentation for command-line butler queries?
===============================================================

The ``butler`` command line tool uses a plugin system to allow packages downstream of ``daf_butler`` to define their own ``butler`` subcommands.
Unfortunately, this means there's no single documentation page that lists all subcommands; each package has its own page documenting the subcommands it provides.
The :ref:`daf_butler <lsst.daf.butler-scripts>` and :ref:`obs_base <lsst.obs.base-cli>` pages contain most subcommands, but the best way to find them all is to use ``--help`` on the command-line.

The :any:`pipetask <lsst.ctrl.mpexec-script>` tool is implemented entirely within ``ctrl_mpexec``.

.. _middleware_faq_duplicate_results:

Why do queries using `Registry` methods return duplicate results?
=================================================================

.. note::

    Modern Butler query methods (`Butler.query_datasets`, `Butler.query_data_ids`, and `Butler.query_dimension_records`) no longer return duplicate results.
    The information in this section only applies when using the old `Registry` interface.

The `Registry.queryDataIds`, `~Registry.queryDatasets`, and `~Registry.queryDimensionRecords` methods can sometimes return true duplicate values, simply because the SQL queries used to implement them do.
You can always remove those duplicates by wrapping the calls in ``set()``; the `DataCoordinate`, `DatasetRef`, and `DimensionRecord` objects in the returned iterables are all hashable.
This is a conscious design choice; these methods return lazy iterables in order to handle large results efficiently, and that rules out removing duplicates inside the methods themselves.
We similarly don't want to *always* remove duplicates in SQL via ``SELECT DISTINCT``, because that can be much less efficient than deduplication in Python, but in the future we may have a way to turn this on explicitly (and may even make it the default).
We do already remove these duplicates automatically in the :any:`butler <lsst.daf.butler-scripts>` command-line interface.

It is also possible for `~Registry.queryDatasets` (and the :any:`butler query-datasets <lsst.daf.butler-scripts>` command) to return datasets that have the same dataset type and data ID from different collections,
This can happen even if the users passes only collection to search, if that collection is a `~CollectionType.CHAINED` collection (because this evaluates to searching one or more child collections).
These results are not true duplicates, and will not be removed by wrapping the results in ``set()``.
They are best removed by passing ``findFirst=True`` (or ``--find-first``), which will return - for each data ID and dataset type - the dataset from the first collection with a match.
For example, from the command-line, this command returns one ``calexp`` from each of the given collections:

..
    Can't use prompt:: directive here instead because it can't handle program output.

.. code-block:: sh

    $ butler query-datasets /repo/main calexp \
        --collections HSC/runs/RC2/w_2021_06/DM-28654 \
        --collections HSC/runs/RC2/w_2021_02/DM-28282 \
        --where "instrument='HSC' AND visit=1228 AND detector=40"

     type                  run                    id   band instrument detector physical_filter visit_system visit
    ------ ----------------------------------- ------- ---- ---------- -------- --------------- ------------ -----
    calexp HSC/runs/RC2/w_2021_02/DM-28282/sfm 5928697    i        HSC       40           HSC-I            0  1228
    calexp HSC/runs/RC2/w_2021_06/DM-28654/sfm 5329565    i        HSC       40           HSC-I            0  1228

(with no guaranteed order!) while adding ``--find-first`` yields only the ``calexp`` found in the first collection:

.. code-block:: sh

    $ butler query-datasets /repo/main calexp --find-first \
        --collections HSC/runs/RC2/w_2021_06/DM-28654 \
        --collections HSC/runs/RC2/w_2021_02/DM-28282 \
        --where "instrument='HSC' AND visit=1228 AND detector=40"

    type                  run                    id   band instrument detector physical_filter visit_system visit
    ------ ----------------------------------- ------- ---- ---------- -------- --------------- ------------ -----
    calexp HSC/runs/RC2/w_2021_06/DM-28654/sfm 5329565    i        HSC       40           HSC-I            0  1228

Passing ``findFirst=True`` or ``--find-first`` requires the list of collections to be clearly ordered, however, ruling out wildcards like ``...`` ("all collections"), globs, and regular expressions.
Single-dataset search methods like `Butler.get` and `Butler.find_dataset` always use the find-first logic (and hence always require ordered collections).

.. _middleware_faq_data_id_missing_keys:

Why are some keys (usually filters) sometimes missing from data IDs?
====================================================================

While most butler methods accept regular dictionaries as data IDs, internally we standardize them into instances of the `DataCoordinate` class, and that's also what will be returned by `Butler` and `Registry` methods.
How much information a `DataCoordinate` has about a data ID depends on how it was obtained:

- A minimal `DataCoordinate` has only the *required values* for the data ID - values for the dimensions in `DimensionGroup.required`, which are sufficent and necessary to look up any other implied dimenions.

- A `DataCoordinate` can also have the *full values* for the data ID, i.e. all dimensions in its `DimensionGroup`, which includes those whose values are
*implied* by the required values, recursively.
  For example, if ``visit`` is in the required dimensions, ``physical_filter`` will be in the full dimensions because a ``visit`` implies a ``physical_filter`` (there is exactly one ``physical_filter`` for a particular ``visit``).
  And because ``physical_filter`` implies ``band``, ``band`` will also be in the full values.
  `DataCoordinate` objects obtained from the butler query system almost always have full values.

- A `DataCoordinate` with full values can also have a mapping of `DimensionRecord` objects with metadata about all of the dimension elements it identifies.
  Dimension *elements* are a generalization of dimensions that also includes tables that hold metadata or relationships keyed on multiple dimensions, like
  ``visit_detector_region``.
  These are sometimes called "expanded" data IDs, and they can be obtained by using the ``.expanded`` (in the old `Registry` query system) and ``.with_dimension_records`` (in the new query system) query modifier methods, or by calling `Registry.expandDataId`.

The amount of information in a `DataCoordinate` does not affect its equality comparisons or hash value, which is usually the behavior users expect, but it has two somewhat surprising implications:

- `DataCoordinate` is not a `collections.abc.Mapping`.
  It does behave in many ways like a `dict`, but it intentionally does not have a `~collections.abc.Mapping.keys` method or support direct iteration over its keys.
  This is because `~collections.abc.Mapping` defines equality differently: two mappings are equal if they have the same keys and the same values for those keys, while two `DataCoordinate` instances can be equal even if they have different keys (if one has only the required dimension values and the other has full values, but the required values are the same).
  Instead of `keys`, use `DataCoordinate.dimensions` to iterate explicitly over the required or full dimensions, or use `DataCoordinate.mapping` to get a `dict` of all of the values the `DataCoordinate` knows (but be careful not to use that `dict` for equality comparisons).

- `DataCoordinate` can behave a little strangely when it is itself used as the key in a `dict` or `set`: if you put a minimal data ID in such a container, and then test whether a different, expanded `DataCoordinate` (for the same data ID) is in the container, the container will report that it is, even though that extra information from the expanded `DataCoordinate` isn't present.

.. note::

    Prior to the implementation of :jira:`RFC-834` in v27, `DataCoordinate` *was* a `collections.abc.Mapping` but its `~collections.abc.Mapping.keys` method only ever returned the required dimensions (even if it held values for the implied dimensions), which was even more confusing.

.. _middleware_faq_data_id_mapping:

How do I make a `dict` from a `DataCoordinate`?
===============================================

If you want a dictionary to use for comparison or minimal serialization, use::

    dict(data_coordinate.required)

This has just the required values of the data coordinate (see :ref:`middleware_faq_data_id_missing_keys`), not the implied ones.

If you want a dictionary to print for humans to read, use::

    dict(data_coordinate.mapping)

This has all of the values this `DataCoordinate` knows.
The `DataCoordinate` itself can of course be printed, but since it elides the quotes around dimension names (often better for conciseness) it can't be copy-pasted back into Python like the correspond `dict` can.

The `DataCoordinate.required` and `DataCoordinate.mapping` properties return true `collections.abc.Mapping` instances, so they can be used in many contexts where a `dict` would be accepted, but they are custom view types, not true `dict` objects.

.. _middleware_faq_calibration_query_errors:

How do I avoid errors involving queries for calibration datasets?
=================================================================

.. note::

    The modern `Butler.query_datasets` method is able to search in calibration collections.
    The information in this section only applies when using the old `Registry` interface.

`Registry.queryDatasets` currently has a major limitation in that it can't query for datasets within a `~CollectionType.CALIBRATION` collection; the error message looks like this::

    NotImplementedError: Query for dataset type 'flat' in CALIBRATION-type collection 'HSC/calib' is not yet supported.

We do expect to fix this limitation in the future, but it may take a while.
In the meantime, there are a few ways to work around this problem.

First, if you don't actually want to search for calibrations at all, but this exception is still getting in your way, you can make your query more specific.
If you use a dataset type list or pattern (a shell-style glob on the command line, or `re.compile` in the Python interface) that doesn't match any calibration datasets, this error should not occur.

Similarly, if you can use a list of collections or a collection pattern that doesn't include any `~CollectionType.CALIBRATION` collections, that will avoid the problem as well - but this is harder, because `~CollectionType.CHAINED` collections that include `~CollectionType.CALIBRATION` collections are quite common.
For example, both processing-output collections with names like "HSC/runs/w_2025_06/DM-50000" and per-instrument default collections like "HSC/defaults" include a `~CollectionType.CALIBRATION` child collection.
You can recursively expand a collection list and filter out any child `~CollectionType.CALIBRATION` collections from it with this snippet::

    expanded = list(
        butler.registry.queryCollections(
            original,
            flattenChains=True,
            collectionTypes=(CollectionType.all - {CollectionType.CALIBRATION}),
        )
    )

where ``original`` is the original, unexpanded list of collections to search.

The equivalent command-line invocation is:

.. code-block:: sh

    $ butler query-collections /repo/main --chains=flatten \
            --collection-type RUN \
            --collection-type CHAINED \
            --collection-type TAGGED \
            HSC/defaults
        Name               Type
    --------------------------------- ----
    HSC/raw/all                       RUN
    HSC/calib/gen2/20180117/unbounded RUN
    HSC/calib/DM-28636/unbounded      RUN
    HSC/masks/s18a                    RUN
    refcats/DM-28636                  RUN
    skymaps                           RUN

Another possible workaround is to make the query much more general - passing ``collections=...`` to search *all* collections in the repository will avoid this limitation even for calibration datasets, because it will take advantage of the fact that all datasets are in exactly one `~CollectionType.RUN` collection (even if they can also be in one or more other kinds of collection) by searching only all of the `~CollectionType.RUN` collections.

That same feature of `~CollectionType.RUN` collections can also be used with `Registry.queryCollections` (and our naming conventions) to find calibration datasets that *might* belong to particular `~CollectionType.CALIBRATION` collections.
For example, if "HSC/calib" is a `~CollectionType.CALIBRATION` collection (or a pointer to one), the datasets in it will usually also be present in `~CollectionType.RUN` collections that start with "HSC/calib/", so logic like this might be useful::

    run_collections = list(
        butler.registry.queryCollections(
            re.compile("HSC/calib/.+"),
            collectionTypes={CollectionTypes.RUN},
        )
    )

Or, from the command-line,

.. code-block:: sh

    $ butler query-collections /repo/main --collection-type RUN \
            HSC/calib/gen2/20200115/*
                    Name                   Type
    ---------------------------------------- ----
    HSC/calib/gen2/20200115/20170821T000000Z RUN
    HSC/calib/gen2/20200115/20160518T000000Z RUN
    HSC/calib/gen2/20200115/20170625T000000Z RUN
    HSC/calib/gen2/20200115/20150417T000000Z RUN
    HSC/calib/gen2/20200115/20181207T000000Z RUN
    HSC/calib/gen2/20200115/20190407T000000Z RUN
    HSC/calib/gen2/20200115/20150407T000000Z RUN
    HSC/calib/gen2/20200115/20160114T000000Z RUN
    HSC/calib/gen2/20200115/20170326T000000Z RUN
    ...

The problem with this approach is that it may return many datasets that aren't in "HSC/calib", including datasets that were not certified, and (like all of the previous workarounds) it doesn't tell you anything about the validity ranges of the datasets that it returns.

If you just want to load the calibration dataset appropriate for a particular ``raw`` (and you have the data ID for that ``raw`` in hand), the right solution is to use `Butler.get` with that raw data ID, which takes care of everything for you::

    flat = butler.get(
        "flat",
        instrument="HSC", exposure=903334, detector=0,
        collections="HSC/calib"
    )

The lower-level `Butler.find_dataset` method can also perform this search without actually reading the dataset, but you'll need to be explicit about how to do the temporal lookup::

    raw_data_id = butler.registry.expandDataId(
        instrument="HSC",
        exposure=903334,
        detector=0,
    )
    ref = butler.find_dataset(
        "flat",
        raw_data_id,
        timespan=raw_data_id.timespan,
    )

It's worth noting that `~Butler.find_dataset` doesn't need or use the ``exposure`` key in the ``raw_data_id`` argument that is passed to it - a master flat isn't associated with an exposure - but it's happy to ignore it, and we *do* need it (or something else temporal) in order to get a data ID with a timespan for the last argument.

Finally, if you need to query for calibration datasets *and* their validity ranges, and don't have a point in time you're starting from, the only option is `Registry.queryDatasetAssociations`.
That's a bit less user-friendly - it only accepts one dataset type at a time, and doesn't let you restrict the data IDs at all - but it *can* query `~CollectionType.CALIBRATION` collections and it returns the associated validity ranges as well.
It actually only exists as a workaround for the fact that `~Registry.queryDatasets` can't do those things, and it will probably be removed sometime after those limitations are lifted.

.. _middleware_faq_empty_quantum_graphs:

How do I fix an empty QuantumGraph?
===================================

.. py:currentmodule:: lsst.pipe.base

The :any:`pipetask <lsst.ctrl.mpexec-script>` tool attempts to predict all of the processing a pipeline will perform in advance, representing the results as a `QuantumGraph` object that can be saved or directly executed.
When that graph is empty, it means it thinks there's no work to be done, and unfortunately this is both a common and hard-to-diagnose problem.

The `QuantumGraph` generation algorithm begins with a large SQL query (a complicated invocation of `Registry.queryDataIds`, actually), where the result rows are essentially data IDs and the result columns are all of the dimensions referenced by any task or dataset type in the pipeline.
Queries for all `"regular input" <connectionTypes.Input>` datasets (i.e. not `PrerequisiteInputs <connectionTypes.PrerequisiteInput>`") are included as subqueries, spatial and temporal joins are automatically included, and the user-provided query expression is translated into an equivalent SQL ``WHERE`` clause.
That means there are many ways to get no result rows - and hence an empty graph.

Sometimes we can tell what will go wrong even before the query is executed - the butler maintains a summary of which dataset types are present each each collection, so if the input collections don't have any datasets of a needed type at all, a warning log message will be generated stating the problem.
This will also catch most cases where a pipeline is misconfigured such that what should be an intermediate dataset isn't actually being produced in the pipeline, because it will appear instead as an overall input that (usually) won't be present in those input collections.

We also perform some follow-up queries after generating an empty `QuantumGraph`, to see if any needed dimensions are lacking records entirely (the most common example of this case is forgetting to define visits after ingesting raws in a new data repository).

If you get an empty `QuantumGraph` without any clear explanations in the  warning logs, it means something more complicated went wrong in that initial query, such as the input datasets, available dimensions, and boolean expression being mutually inconsistent (e.g. not having any bands in common, or tracts and visits not overlapping spatially).
In this case, the arguments to `~Registry.queryDataIds` will be logged again as warnings, and the next step in debugging is to try that call manually with slight adjustments.

To guide this process, it can be very helpful to first use :any:`pipetask build --show pipeline-graph <lsst.ctrl.mpexec-script>` to create a diagram of the pipeline graph - a simpler directed acyclic graph that relates tasks to dataset types, without any data IDs:

.. code:: sh

    $ pipetask build ... --show pipeline-graph
                      ○          camera
                      │
                    ○ │          raw
                    │ │
                  ◍ │ │          yBackground, transmission_sensor, transmi...[1]
                  ├─┼─┤
                  ■ │ │          isr
                  │ │ │
                  ○ │ │          postISRCCD
                  │ │ │
                  ■ │ │          characterizeImage
                  │ │ │
                  ◍ │ │          icSrc, icExpBackground, icExp
                  │ │ │
                ○ │ │ │          ps1_pv3_3pi_20170110
                ├─┤ │ │
                │ ■ │ │          calibrate
    (...)

The ``--pipeline-dot`` argument can also be used to create a version of this graph in the `GraphViz dot language`_, and you can use the ubiquitous ``dot`` command-line tool to transform that into a PNG, SVG, or other graphical format file:

.. code:: sh

    $ pipetask build ... --pipeline-dot pipeline.dot
    $ dot pipeline.dot -Tsvg > pipeline.svg

That ``...`` should be replaced by most of the arguments you'd pass to :any:`pipetask <lsst.ctrl.mpexec-script>` that describe *what* to run (which tasks, pipelines, configuration, etc.), but not the ones that describe how, or what to use as inputs (no collection options).
See ``pipetask build --help`` for details.

For a modern, web-friendly alternative, the ``--pipeline-mermaid`` argument can be used to generate the same graph in `Mermaid.js`_ format:

.. code:: sh

    $ pipetask build ... --pipeline-mermaid pipeline.mmd
    $ mmdc -i pipeline.mmd -o pipeline.svg

The ``mmdc`` command is part of the `Mermaid CLI`_, which can render Mermaid definition files into PNG, SVG, or PDF files. Alternatively, the resulting ``.mmd`` file can be rendered with tools like the `Mermaid Live Editor`_ or Markdown platforms supporting Mermaid syntax such as GitHub. This format is particularly useful for creating interactive, easily shareable pipeline graphs.

The visualized graph will often reveal some unexpected input dataset types, tasks, or relationships between the two that make it obvious what's wrong.

Another useful approach is to try to simplify the pipeline, ideally removing all but the first task; if that works, you can generally rule it out as the cause of the problem, add the next task in, and repeat.

Because the big initial query only involves regular inputs, it can also be helpful to change regular `~connectionTypes.Input` connections into `~connectionTypes.PrerequisiteInput` connections - when a prerequisite input is missing, :any:`pipetask <lsst.ctrl.mpexec-script>` should provide more useful diagnostics.
This is only possible when the dataset type is already in your input collections, rather than something to be produced by another task within the same pipeline.
But if you work through your pipeline task-by-task, and run each single-task pipeline as well as produce a `QuantumGraph` for it, this should be true each step of the way as well.

.. _GraphViz dot language: https://graphviz.org/
.. _Mermaid.js: https://mermaid-js.github.io/mermaid/
.. _Mermaid CLI: https://github.com/mermaid-js/mermaid-cli/
.. _Mermaid Live Editor: https://mermaid-js.github.io/mermaid-live-editor/

.. _middleware_faq_long_qg_generation:

How can I make QuantumGraph generation faster?
==============================================

`QuantumGraph` generation can be slow in several different ways for different pipelines and datasets, and the first step in speeding it up is to look at the logs to see where it's spending its time.
We strongly recommend passing ``--long-log`` to include timestamps in all logging, and passing ``--log-level lsst.pipe.base.quantum_graph_builder=VERBOSE`` can provide more information about `QuantumGraph` generation in particular.
If you're running BPS, logs for this step are written to ``quantumGraphGeneration.out`` in the submit directory.

Here's what's going on after a few important log messages (all ``INFO`` level):

- ``Processing pipeline subgraph X of Y with N task(s).``: we're running the "big initial query" for all of the data IDs that might appear in the graph.
  This step is usually quite fast (seconds or minutes for large graphs, not hours), but occasionally catastrophically slow (days) when the database's query optimizer chooses a bad plan, so it's the step most amenable to big speedups (more on this below).

- ``Iterating over query results to associate quanta with datasets.``: we're processing the result rows of that big query, each of which will correspond to an edge or a set of similar edges in the graph.
  This step is pure Python (no database queries), and the only way to make it faster is to shrink the size of the problem by splitting it up.
  Splitting the task into steps may help more than splitting up data when this is the bottleneck, but only slightly.

- ``Initial bipartite graph has 290189 quanta, 1073224 dataset nodes, and 3591767 edges from 234155 query row(s).``: the preliminary graph is built, and now we're performing many smaller database queries to look for input datasets (or outputs that may be in the way, in some cases), and asking each task if each of its quanta should be kept or pruned out.
  This step is usually very close to linear in the number of quanta and is typically dominated by Python logic, but it does involve some database queries.
  The ``VERBOSE`` logging can provide information about exactly which dataset it's querying for, and if any of these seem to be unusually slow, please report it to the middleware team (with logs and a link to the pipeline you're running).
  There's not much a user can do about slowdowns here (aside from splitting up the problem).

- When the graph has been built, ``pipetask`` will print a table with the number of quanta for each task.  If it pauses a long time after this, it's probably spending a long time writing the graph to disk.
  This takes longer than it should (this is a known issue we have plans to fix, but it'll require some deep changes), but it should be linear in the number of quanta in the graph.

When the "big initial query" is catastrophically slow, it's almost always because the query is complex enough that the database's query optimizer chose to execute it in a way that didn't take advantage of the right index, and our goal is to give it an equivalent or nearly-equivalent query that's simpler.
By default, the query includes both the ``--data-query`` expression provided by the user and joins to a subqueries for each regular input dataset in the pipeline (but not prerequisites).

The best way to simplify the query is to eliminate as many of those dataset subqueries as you can via the ``--dataset-query-constraint`` option, which provides direct control over the dataset types to join against.
If you can easily write a ``--data-query`` argument that includes all of the data IDs you want to process and almost no data IDs you don't want to process (like an explicit ``tract`` or ``visit`` range), pass ``--dataset-query-constraint off`` to get rid of all of the dataset subqueries.

When that's not easy, try to identify one input dataset type whose existence strongly implies the others (perhaps because they're all produced together by some previous processing), and pass that as the argument to ``--dataset-query-constraint``.
Visualizing the pipeline as a graph (see e.g. ``pipetask build --show pipeline-graph``, as described in :ref:`middleware_faq_empty_quantum_graphs`) is the best way to do this.
Dataset types with data IDs that are more similar to the data IDs of the quanta are probably best, and dataset types with coarser data IDs are probably better choices than those with finer data IDs (e.g. prefer ``tract`` over ``patch``, ``visit`` over ``{visit, detector}``), but this is based on intuition, not experience, and the most important thing is to reduce the number of dataset types down to zero or one.

In most cases, a complex ``--data-query`` argument is preferable to even one input dataset constraint, but there are exceptions:

- If the ``--data-query`` references a dimension that is completely irrelevant to the graph (e.g. putting an ``exposure`` constraint into a graph that only uses ``{tract, patch}`` data IDs), it can really slow things down, because it still gets included in the query and the number of result rows is multiplied by the number of matching irrelevant-dimension values (e.g. the number ``exposures``).
  The fact that the ``exposure`` dimension is not spatial (but ``visit`` is) interacts with this in a particularly dramatic way: while it's fine to add a constraint on ``tract`` or ``patch`` to spatially control the a ``visit``-based pipeline, if you do this on a pipeline that only references ``exposure``, not ``visit`` (like ISR alone), the query system will not recognize that it needs to use ``visit`` to mediate between ``exposure`` and ``tract/patch``, and a disastrously huge query will be the result.

- If the ``--data-query`` references dimension metadata fields rather than primary key values (e.g. ``visit.exposure_time`` rather than just ``visit``), we may not have indexes in place to make those selections fast.
  Note that this includes the ``seqnum`` field of ``visit`` and ``exposure``, and - until the repositories are migrated to the latest dimension universe - ``day_obs`` as well.
  We haven't actually observed this ever leading to catastrophic query performance, so it's not worth worrying about unless you're trying to fix a graph-generation problem that you know is slow, and if you do think this is a problem for you, please report it so we can add indexes in the future.

Finally, while we haven't seen this problem in the wild (perhaps because ``--dataset-query-constraint`` is underused), if the combination of the ``--data-query`` and ``--dataset-query-constraint`` arguments leave the query underconstrained, it might run quickly but return many more result rows than we need.
For example, if one passes ``--dataset-query-constraint off`` and the ``--data-query`` matches 1000 visits while only 10 of those have inputs, the initial query will return a factor of 100 more result rows than it might need - and while the initial query may still be fast enough to avoid being the bottleneck, this will result in a preliminary graph that is too big and needs to be pruned considerably by the follow-up queries for input datasets, making later steps of the process 100x slower.

.. _middleware_faq_recovery_qgs

How do I recover from a small number of failed quanta in a big graph?
=====================================================================

When one quantum in a quantum graph fails (e.g. by raising an exception), executors typically block all downstream quanta, even those that might be able to proceed with the outputs of the failed quantum.
It's also possible for a quantum to nominally succeed while doing the wrong thing, which would allow downstream quanta to run but might also cause them to do the wrong thing.

These situations are usually best addressed by building a new quantum graph that includes only the quanta that were affected by the problem.
In some cases it may be possible to run this with the same output `~lsst.daf.butler.CollectionType.RUN` collection, but it is always possible and less error-prone to just create a new output `~lsst.daf.butler.CollectionType.RUN` in the same `~lsst.daf.butler.CollectionType.CHAINED` collection (which is what ``pipetask`` and ``bps`` do by default when an output collection is reused).
The primary tools here are the ``--skip-existing-in`` and ``--select-tasks`` options to ``pipetask qgraph`` (or equivalently, the BPS ``extraQgraphOptions`` setting).
The former is given a collection that is queried for existing outputs, and any quanta that already have a metadata dataset present in that collection are considered done and dropped from the new graph.
The latter takes a :ref:`pipeline graph subset expression <pipeline-graph-subset-expressions>` that can be used to easily identify the tasks that were affected by a failure.

There are a few different scenarios to consider.

Accepting failures
------------------

If a task with label ``unfixable`` fails in one or more quanta, and you just want to move on without its outputs, modify the original quantum-graph build command with:

.. code:: sh

    --skip-existing-in <output> --select-tasks '> unfixable'

This will only attempt to run tasks that are strictly downstream of ``unfixable``, and it will skip any quanta that already ran (i.e. because they didn't have upstream failures).

Fixing failures
---------------

If a task with label ``fixable`` fails in one or more quanta, but you have fixed the problem and now expect it to succeed at least some of the time, use:

.. code:: sh

    --skip-existing-in <output> --select-tasks '>= fixable'

This will run both the problematic task and everything downstream of it, again skipping any quanta that already ran successfully.
In this case ``-skip-existing-in <output>`` is actually all you need for correctness, but using ``--select-tasks`` should speed up the quantum graph build.

Fixing non-failures
-------------------

- If a task with label ``regrettable`` doesn't actually fail, but it's produced bad outputs (or an improvement is available that you want to try), use

.. code:: sh

    --select-tasks '>= regrettable'

to re-run that task and all downstream tasks regardless of whether they succeeded before.
This is also the right approach to take with quanta that incorrectly raised `NoWorkFound` or otherwise wrote no outputs without formally failing and blocking downstream quanta; these are considered "successes with caveats", not failures.

Data ID constraints
-------------------

When the data IDs of the problems are known in any of these cases, it may be possible to further limit the set of quanta re-run using the ``--data-query`` and/or ``--data-id-table`` options.
These data ID constraints act on *all* downstream quanta and datasets (often via spatial joins), not just the failures, and can even trim out inputs that were successfully produced on a previous run.
For example, consider the case where one detector in a visit failed while others succeeded, and a downstream task gathers multiple detectors from that visit as an input.
If the re-run attempt is constrained to only the failed detector, only that detector will be passed to the downstream gather task.
This can mostly be avoided by constraining only full visits or tracts, but it's important to be aware of the downstream task dimensions, as in rare cases even those coarse constraints can generate incorrect graphs.

.. _middleware_faq_long_query:

What do I do if a query method/command is slow?
===============================================

Adding the ``--log-level sqlalchemy.engine=DEBUG`` option to the :any:`butler <lsst.daf.butler-scripts>` or :any:`pipetask <lsst.ctrl.mpexec-script>` command will allow the SQL queries issued by the command to be inspected.
Similarly, for a slow query method, adding ``logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)`` can help.
The resulting query logs can be useful for developers and database administrators to determine what, if anything, is going wrong.

.. _middleware_faq_pipetask_report:

How can I get a report on all failures and missing datasets in a run?
=====================================================================

The :any:`pipetask report <lsst.ctrl.mpexec-pipetask#report>` tool can be used to analyze executed quantum graphs, troubleshoot, diagnose failures, and confirm that fail-and-recovery attempts (such as when using ``--skip-existing-in``) are effective.
It can also be used to categorize the "caveats" on certain successes, like the `lsst.pipe.base.NoWorkFound` exception.

When analyzing multiple graphs with ``pipetask report``, all graphs should be attempts to execute the same pipeline with the same dataquery.

The recommended usage is

.. code:: sh

      pipetask report --full-output-filename <path/to/output_file>.json --force-v2 REPO QGRAPHS


- The ``--full-output-filename <path/to/output_file>.json`` option provides the path to a file where the output of the full summary information can be stored
- The ``--force-v2`` option makes sure that the most recent version of the tool is used even when the user passes only one graph
- The ``REPO`` argument is the `Butler` repo where the output from the processing is stored
- The ``QGRAPHS`` argument is a sequence of quantum graphs to be analyzed, separated by spaces and passed in order of first to last executed

.. note::

    If the ``--full-output-filename`` argument is not provided, information on the error messages and data IDs for all failed quanta will be output to the command line, which can be overwhelming in the case of many failures.
    If you do not need error information, consider the ``--brief`` option, which prints the same tables to the command line as ``--full-output-filename``, but does not save additional information to a file.

This will print two ``bps report``-style tables, one for quanta and one for output datasets.

In the output JSON file will be

- A summary under every task with:

  * Every failed data ID and corresponding error message
  * Every qualified-success data ID and a set of "caveat flags"
  * Every run containing failing data IDs, and their status
  * A list of data IDs which have been "recovered"; i.e., successes from fail-and-recovery attempts
- A list of the data IDs associated with every missing dataset
- A field called ``producer`` connecting each ``datasetType`` for each data ID to the task which produced it
- Counts of quanta and datasets in all possible states.

Currently, the ``--force-v2`` option is the suggested usage until version 1 of pipetask report (using the `QuantumGraphExecutionReport` instead of the `QuantumProvenanceGraph`) is deprecated.

With that, we'll go into how to read the output of ``pipetask report``.

The Quanta Table
----------------

The table for Quanta from the ``w_2024_28`` DC2 test-med-1 reprocessing run, before recoveries, looked like:

.. code:: sh
             Task          Unknown Successful Blocked Failed Wonky TOTAL EXPECTED
    ---------------------- ------- ---------- ------- ------ ----- ----- --------
                  makeWarp       0       6596       0      0     0  6596     6596
     selectDeepCoaddVisits       0        294       0      0     0   294      294
    selectGoodSeeingVisits       0        294       0      0     0   294      294
               templateGen       0        288       0      6     0   294      294
             assembleCoadd       0        280       0     14     0   294      294
                 detection       0        280      14      0     0   294      294
    healSparsePropertyMaps       0          1       5      0     0     6        6
           mergeDetections       0         36      13      0     0    49       49
                   deblend       0         36      13      0     0    49       49
                   measure       0        216      78      0     0   294      294
         mergeMeasurements       0         36      13      0     0    49       49
           forcedPhotCoadd       0        216      78      0     0   294      294
          writeObjectTable       0         36      13      0     0    49       49
      transformObjectTable       0         36      13      0     0    49       49
    consolidateObjectTable       0          0       1      0     0     1        1
        matchObjectToTruth       0          0       1      0     0     1        1
      compareObjectToTruth       0          0       1      0     0     1        1


which indicates that there are 6 failed ``templateGen`` quanta, 14 failed ``assembleCoadd`` quanta, 14 blocked ``detection`` quanta, and so on.

These totals are all determined by examining the status of each task run on each data ID from run to run.

Status Definitions for Task Quanta
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Unknown
"""""""
The ``Unknown`` category could mean one of two things.
Being the default value for the status of a task run on a particular data ID, it could technically mean that no attempt has been made to execute this part of the graph.
However, in a table that does not look empty, it much more likely denotes that the task's metadata is missing for that data ID.
This makes it impossible for us to tell whether the task succeeded or failed, but does point to possible infrastructure problems.

Successful
""""""""""
This status is the trademark of a successful quantum.
The specific path to being marked as successful by the `QuantumProvenanceGraph` is that metadata and log datasets exist for the task for the data ID in question.

Successful quanta can still have caveats, and it's entirely possible that a pipeline bugs could cause what should be a failure to be misclassified as a success with caveats.
The flags that characterize success caveats are documented in the `lsst.pipe.base.QuantumSuccessCaveats` enumeration.

Blocked
"""""""
Blocked quanta are the successors of unsuccesful quanta which cannot be executed because their inputs are not present.
They do not represent failure per se, but since they could not execute, they also do not produce output data products.
The way that the `QuantumProvenanceGraph` identifies a ``Blocked`` quantum is that it has no metadata and no logs (so it did not start or finish execution) **and** that the task run on that particular data ID is a successor (according to the quantum graph) of a ``Failed`` quantum.

Failed
""""""
There are log datasets but no metadata datasets for this task and data ID, indicating that the task started but did not finish execution.

Wonky
"""""
A Wonky quantum is the result of infrastructure problems or concerning middleware mismatches.
The category is intended to halt processing and require human intervention to proceed. As such, when a task is marked as ``Wonky`` for a particular data ID, no further successes (or any other statuses, for that matter) will change the overall status out of ``Wonky``.
A quantum can only exit a ``Wonky`` state via human intervention. Currently, there are three paths to the ``Wonky`` state for a quantum:

- A quantum which was marked as ``Successful`` on a previous processing attempt (run) has a more recent attempt (run) which the `QuantumProvenanceGraph` identifies as unsuccessful (i.e., Graph 1 says task *a* ran successfully on data ID *x*, but Graph 2 says task *a*'s attempt at data ID *x* was ``Failed``, ``Blocked``, or ``Unknown``)
- Logs are missing for at least one of the attempts to run this task on this data ID
- ``Registry.queryDatasets`` for the output datasets of this quantum return outputs from multiple different processing attempts (runs)

The outputs of ``Registry.queryDatasets`` are important because they are the datasets which will be used as inputs to downstream tasks. If the inputs to a downstream task are from different processing attempts, the Butler cannot ensure that they have been processed in the same way, with the same inputs, dataqueries, etc.

Total
"""""
The sum of all the previous categories.

Expected
""""""""
The expected number of quanta, according to the quantum graphs.


The Dataset Table
-----------------
The (abbreviated because there are many datasets) table for the output datasets from the same ``w_2024_38`` DC2 test-med-1 run, before recoveries, looked like

.. code:: sh

                      Dataset                    Visible Shadowed Predicted Only Unsuccessful Cursed TOTAL EXPECTED
    -------------------------------------------- ------- -------- -------------- ------------ ------ ----- --------
                            deepCoadd_directWarp    6384        0            457            0      0  6841     6841
                        deepCoadd_psfMatchedWarp    6369        0            472            0      0  6841     6841
                               makeWarp_metadata    6841        0              0            0      0  6841     6841
                                    makeWarp_log    6841        0              0            0      0  6841     6841
                                 deepCoaddVisits     294        0              0            0      0   294      294
                  selectDeepCoaddVisits_metadata     294        0              0            0      0   294      294
                       selectDeepCoaddVisits_log     294        0              0            0      0   294      294
                                goodSeeingVisits     294        0              0            0      0   294      294
                 selectGoodSeeingVisits_metadata     294        0              0            0      0   294      294
                      selectGoodSeeingVisits_log     294        0              0            0      0   294      294
                                 goodSeeingCoadd     288        0              0            6      0   294      294
                          goodSeeingCoadd_nImage     288        0              0            6      0   294      294
                            templateGen_metadata     288        0              0            6      0   294      294
                                 templateGen_log     288        0              0            6      0   294      294
                                       deepCoadd     280        0              0           14      0   294      294
                              deepCoadd_inputMap     280        0              0           14      0   294      294
                                deepCoadd_nImage     280        0              0           14      0   294      294
                          assembleCoadd_metadata     280        0              0           14      0   294      294
                               assembleCoadd_log     280        0              0           14      0   294      294
                                   deepCoadd_det     280        0              0           14      0   294      294
                                deepCoadd_calexp     280        0              0           14      0   294      294
                     deepCoadd_calexp_background     280        0              0           14      0   294      294
                     ...

which shows ``Unsuccessful`` datasets for all the outputs of the failed ``getTemplate`` and ``assembleCoadd`` tasks, as well as the outputs of their (``Blocked``) successors. It also shows ``Predicted Only`` for some ``deepCoadd_directWarp`` and ``deepCoadd_psfMatchedWarp`` datasets, which is a result of these outputs being predicted when the `QuantumGraph` was built, but found to be unnecessary by the Science Pipelines during execution.

Status Definitions for Datasets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The statuses for datasets all pertain to whether a ``datasetType`` associated with a certain data ID exists in the `Butler`, and whether it could be used as an input to downstream tasks.

Visible
"""""""
The dataset exists, and comes up in a find-first search (``Registry.queryDatasets``). This means it will be used as an input for downstream tasks.

Shadowed
""""""""
The dataset exists in the `Butler`, but does not come up in a find-first search (``Registry.queryDatasets``). Therefore, we don't have to worry about it being used as an input.

Predicted Only
""""""""""""""
This status occurs when the graph predicts an output dataset that ultimately is not produced by the Science Pipelines because it was deemed unnecessary when the graph was executed. These are commonly referred to as "NoWorkFound cases" because their output messages say "No work found for task" (and hence said task does not produce output datasets).

Unsuccessful
""""""""""""
An unsuccessful status for a dataset just means it does not exist in the `Butler`. ``Unsuccessful`` datasets are the results of ``Failed`` and ``Blocked`` quanta.

Cursed
""""""
A ``Cursed`` dataset is the result of an unsuccessful quantum which would otherwise be marked as ``Visible``. This means that if any datasets which were produced by non-``Successful`` quanta (this includes ``Unknown``, ``Failed``, ``Blocked`` and ``Wonky`` quanta) come up in a ``Registry.queryDatasets`` find-first search, we flag them as ``Cursed`` in order to halt processing, start investigation, and prevent them from being used as inputs later. Ideally ``Cursed`` datasets should be removed before processing continues.

Total
"""""
The sum of all the previous categories.

Expected
""""""""
The expected number of datasets, according to the quantum graphs.

.. note::

    The number in ``Total`` should always match the number in ``Expected``.
    If it does not, this is a problem with this algorithm and should be reported to the developers.

Combining group-level pipetask report summaries into a step-level rollup
------------------------------------------------------------------------

`pipetask report` works on the group-level (on attempts to execute the same pipeline with the same data-query). However, it is possible to collate the JSON output from multiple groups into one file. This is intended for combining group-level summaries into summaries over processing steps, and answering questions like "What are all the errors that occurred in step 1?" or "How many quanta were blocked in step 5?"

Recommended usage is

.. code::

    pipetask aggregate-reports --full-output-filename <path/to/combined/output_file>.json <path/to/group/file/1.json> <path/to/group/file/2.json>...


where the argument to ``--full-output-filename`` is a filepath to store the combined `QuantumProvenanceGraph` summary.
If no argument is passed, the combined summary will be printed to the screen.


.. _middleware_faq_clean_up_runs:

How do I clean up processing runs I don't need anymore?
=======================================================

.. py:currentmodule:: lsst.daf.butler

Because a data repository stores information on both a filesystem or object store and a SQL database, deleting datasets completely requires using butler commands, even if you know where the associated files are stored on disk.

For processing runs that follow our usual conventions (following them is automatic if you use ``--output`` and don't override ``--output-run`` when running :any:`pipetask <lsst.ctrl.mpexec-script>`), two different collections are created:

- a `~CollectionType.RUN` collection that directly holds your outputs
- a `~CollectionType.CHAINED` collection that points to that RUN collection as well as all of your input collections.

If you perform multiple processing runs with the same ``--output``, you'll get multiple `~CollectionType.RUN` collections in the same `~CollectionType.CHAINED` collection.
The `~CollectionType.CHAINED` collection will have the name you passed to ``--output``, and the RUN collections will start with that and end with a timestamp.
You can see this structure for your own collections with a command like this one:

.. code:: sh

    $ butler query-collections /repo/main --chains=tree u/jbosch/*
    u/jbosch/DM-30649                                    CHAINED
      u/jbosch/DM-30649/20210614T191615Z                 RUN
      HSC/raw/RC2/9813                                   TAGGED
      HSC/calib/gen2/20180117                            CALIBRATION
      HSC/calib/DM-28636                                 CALIBRATION
      HSC/calib/gen2/20180117/unbounded                  RUN
      HSC/calib/DM-28636/unbounded                       RUN
      HSC/masks/s18a                                     RUN
      HSC/fgcmcal/lut/RC2/DM-28636                       RUN
      refcats/DM-28636                                   RUN
      skymaps                                            RUN
    u/jbosch/DM-30649/20210614T191615Z                   RUN

The `~CollectionType.RUN` collections that directly hold the datasets are what we want to remove in order to free up space, but these need to be removed from the `~CollectionType.CHAINED` before this is possible.
And we definitely don't want to delete the *input* collections.

.. note::

    If you delete files from the filesystem before using butler commands to remove entries from the database, the commands for cleaning up the database are actually exactly the same.
    The butler won't know that the files are gone until you try to use or delete them, but when you try to delete them, it will just log this at debug level.

The Easy Way: deleting everything
---------------------------------

If you want to delete an entire processing run - all of the output  `~CollectionType.RUN` collections and the `~CollectionType.CHAINED` collection, but (of course) not any of the input collections, just use ``pipetask purge``:

.. code:: sh

    $ pipetask purge -b /repo/main u/jbosch/DM-30649

This relies entirely on collection name prefixes (it assumes output `~CollectionType.RUN` collections start with the `~CollectionType.CHAINED` collection name), so it works just fine with collections created by BPS.
With the ``--recursive`` it would *probably* work with collections created by Campaign Management tooling, depending on how it was configured.
But it won't work if you've run with ``--outpun-run`` overridden to something else.

The Easy Way: delete a bad output runs
--------------------------------------

If you want to keep most of an output collection set but have a few bad `~CollectionType.RUN` collections that you can identify, start by reomving them from the `~CollectionType.CHAINED` collection:

.. code:: sh

    $ butler collection-chain /repo/main --remove u/jbosch/DM-30649 u/jbosch/DM-20210614T191615Z

You can also pass ``--replace-run`` to ``pipetask run`` if you know the previous run was bad and want to kick it out of the chain.
Note that neither of these approaches actually deletes the bad `~CollectionType.RUN` collection, but they do keep the datasets in it from being used as inputs in further processing with the chain.

To actually delete all `~CollectionType.RUN` collections that are no longer members of a particular chain, use ``pipetask cleanup``:

.. code:: sh

    $ pipetask purge -b /repo/main u/jbosch/DM-30649

Once again this just uses the assumption that the `~CollectionType.CHAINED` collection name is the prefix for all associated `~CollectionType.RUN` collections, so it works with any way of creating collections that maintains that relationship.

Deleting only some datasets
---------------------------

If you don't want to delete the full RUN collection, just some datasets within it, you can generally use the ``prune-datasets`` subcommand:

.. code:: sh

    $ butler prune-datasets /repo/main --purge u/jbosch/DM-29776/singleFrame/20210426T161854Z --datasets postISRCCD u/jbosch/DM-29776/singleFrame/20210426T161854Z
    The following datasets will be removed:

    type                         run                                        id                  band instrument detector physical_filter exposure
    ---------- ---------------------------------------------- ------------------------------------ ---- ---------- -------- --------------- --------
    postISRCCD u/jbosch/DM-29776/singleFrame/20210426T161854Z c45a177f-24e8-4dc9-9268-5895decb7989    y        HSC        0           HSC-Y      318
    postISRCCD u/jbosch/DM-29776/singleFrame/20210426T161854Z 461d0293-3c80-45ea-9f06-21a90525c185    y        HSC        1           HSC-Y      318
    postISRCCD u/jbosch/DM-29776/singleFrame/20210426T161854Z 1572dd02-c959-4d23-ba03-91cf235e1291    y        HSC        2           HSC-Y      318
    postISRCCD u/jbosch/DM-29776/singleFrame/20210426T161854Z b38afec9-1970-478d-80d8-4f61c5a992d0    y        HSC        3           HSC-Y      318
    postISRCCD u/jbosch/DM-29776/singleFrame/20210426T161854Z 769bb9ce-9267-4e57-812f-82fee3fd0afa    y        HSC        4           HSC-Y      318
    (...)
    Continue? [y/N]: y
    The datasets were removed.

Note that here you have to know the exact `~CollectionType.RUN` collection that holds the datasets, and specify it twice (the argument to ``--purge`` is the collection to delete from, while the positional argument is the collection to query within - the latter could be some other kind of collection, but it's rare for that to be useful).

The Python `Butler.pruneDatasets` method can be used for even greater control of what you want to delete, as it accepts an arbitrary `DatasetRef` iterable indicating what to delete.

.. _middleware_faq_clean_up_directories:

Removing `~CollectionType.RUN` collections always removes the files within them, but it does not remove the directory structure, because in the presence of arbitrary path templates (including any that may have been used in the past) and possible concurrent writes, it's difficult for the butler to recognize efficiently when a directory will end up empty.
You're welcome to delete empty directories on your own after using ``remove-runs``; they're typically in subdirectories of the main repository directory named after the collection (it's possible to configure the butler such that this isn't the case, but rare).
It's also completely fine to just leave them.
