##########################
Frequently asked questions
##########################

This page contains answer to common questions about the data access and pipeline middleware, such as the Butler and pipeline tasks.

Why do queries return duplicate results?
========================================

.. py:currentmodule:: lsst.daf.butler

The `Registry.queryDataIds`, `~Registry.queryDatasets`, and `~Registry.queryDimensionRecords` methods can sometimes return true duplicate values, simply because the SQL queries used to implement them do.
You can always remove those duplicates by wrapping the calls in ``set()``; the `DataCoordinate`, `DatasetRef`, and `DimensionRecord` objects in the returned iterables are all hashable.
This is a conscious design choice; these methods return lazy iterables in order to handle large results efficiently, and that rules out removing duplicates inside the methods themselves.
We similarly don't want to *always* remove duplicates in SQL via ``SELECT DISTINCT``, because that can be much less efficient than deduplication in Python, but in the future we may have a way to turn this on explicitly (and may even make it the default).
We do already remove these duplicates automatically in the :program:`butler` command-line interface.

It is also possible for `~Registry.queryDatasets` (and the :program:`butler query-datasets` command) to return datasets that have the same dataset type and data ID from different collections,
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

Passing ``findFirst=True``/``--find-first`` requires the list of collections to be clearly ordered, however, ruling out wildcards like ``...`` ("all collections"), globs, and regular expressions.
Single-dataset search methods like `Butler.get` and `Registry.findDataset` always use the find-first logic (and hence require ordered collections).

Why are some keys (usually filters) sometimes missing from data IDs?
====================================================================

While most butler methods accept regular dictionaries as data IDs, internally we standardize them into instances of the `DataCoordinate` class, and that's also what will be returned by `Butler` and `Registry` methods.
Printing a `DataCoordinate` can sometimes yield results with a confusing ``...`` in it::

    >>> dataId = butler.registry.expandDataId(instrument="HSC", exposure=903334)
    >>> print(dataId)
    {instrument: 'HSC', exposure: 903334, ...}

And similarly asking for its ``keys`` doesn't show everything you'd expect (same for ``values`` or ``items``); in particular, there are no ``physical_filter`` or ``band`` keys here, either::

    >>> print(dataId.keys())
    {instrument, exposure}

The quick solution to these problems is to use `DataCoordinate.full`, which is another more straightforward `~collections.abc.Mapping` that contains all of those keys:

    >>> print(dataId.full)
    {band: 'r', instrument: 'HSC', physical_filter: 'HSC-R', exposure: 903334}

You can also still use expressions like ``dataId["band"]``, even though those keys *seem* to be missing:

    >>> print(dataId["band"])
    r

The catch is these solutions only work if `DataCoordinate.hasFull` returns `True`; when it doesn't, accessing `DataCoordinate.full` will raise `AttributeError`, essentially saying that the `DataCoordinate` doesn't know what the filter values are, even though it knows other values (i.e. the ``exposure`` ID) that could be used to fetch them.
The terminology we use for this is that ``{instrument, exposure}`` are the *required* dimensions for this data ID and ``{physical_filter, band}`` are *implied* dimensions::

    >>> dataId.graph.required
    {instrument, exposure}
    >>> dataId.graph.implied
    {band, physical_filter}

The good news is that any `DataCoordinate` returned by the `Registry` query methods will always have `~DataCoordinate.hasFull` return `True`, and you can use `Registry.expandDataId` to transform any other `DataCoordinate` or `dict` data ID into one that contains everything the database knows about those values.

The obvious follow-up question is why `DataCoordinate.keys` and stringification don't just report all of they key-value pairs the object actually knows, instead of hiding them.
The answer is that `DataCoordinate` is trying to satisfy a conflicting set of demands on it:

- We want it to be a `collections.abc.Mapping`, so it behaves much like the `dict` objects often used informally for data IDs.
- We want a `DataCoordinate` that *only* knows the value for required dimensions to compare as equal to any data ID with the same values for those dimensions, regardless of whether those other data IDs also have values for implied dimensions.
- `collections.abc.Mapping` defines equality to be equivalent to equality over ``items()``, so if one mapping includes more keys than the other, they can't be equal.

Our solution was to make it so `DataCoordinate` is always a `~collections.abc.Mapping` over just its required keys, with ``full`` available sometimes as a `~collections.abc.Mapping` over all of them.
And because the `~Mapping` interface doesn't prohibit us from allowing ``__getitem__`` to succeed even when the given value isn't in ``keys``, we support that for implied dimensions as well.
It's possible it would have been better to just not make it a `~collections.abc.Mapping` at all (i.e. remove ``keys``, ``values``, and ``items`` in favor of other ways to access those things).
`DataCoordinate` :ref:`has already been through a number of revisions<lsst.daf.butler-dev_data_coordinate>`, though, and it's not clear it's worth yet another try.

How do I avoid exceptions involving queries for calibration datasets?
=====================================================================

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

You can also make the query much more general - passing ``collections=...`` to search *all* collections in the repository will avoid this limitation even for calibration datasets, because it will take advantage of the fact that all datasets are in exactly one `~CollectionType.RUN` collection (even if they can also be in one or more other kinds of collection) by searching only all of the `~CollectionType.RUN` collections.

That same feature of `~CollectionType.RUN` collections can also be used with `Registry.queryCollections` (and our naming conventions) to find calibration datasets that *might* belong to particular `~CollectionType.CALIBRATION` collections.
For example, if "HSC/calib" is a `~CollectionType.CALIBRATION` collection (or a pointer to one), the datasets in it will usually also be present in `~CollectionType.RUN` collections that start with "HSC/calib/", so logic like this might be useful::

    run_collections = list(
        butler.registry.queryCollections(re.compile("HSC/calib/.+"),
        collectionTypes={CollectionTypes.RUN},
    )

The problem with this approach is that it may return many datasets that aren't in "HSC/calib", including datasets that were not certified, and (like all of the previous workarounds) it doesn't tell you anything about the validity ranges of the datasets that it returns.

If you just want to load the calibration dataset appropriate for a particular ``raw`` (and you have the data ID for that ``raw`` in hand), the right solution is to use `Butler.get` with that raw data ID, which takes care of everything for you::

    flat = butler.get(
        "flat",
        instrument="HSC", exposure=903334, detector=0,
        collections="HSC/calib"
    )

The lower-level `Registry.findDataset` method can also perform this search without actually reading the dataset, but you'll need to be explicit about how to do the temporal lookup::

    raw_data_id = butler.registry.expandDataId(
        instrument="HSC",
        exposure=903334,
        detector=0,
    )
    ref = butler.registry.findDataset(
        "flat",
        raw_data_id,
        timespan=raw_data_id.timespan,
    )

It's worth noting that `~Registry.findDataset` doesn't need or use the ``exposure`` key in the ``raw_data_id`` argument that is passed to it - a master flat isn't associated with an exposure - but it's happy to ignore it, and we *do* need it (or something else temporal) in order to get a data ID with a timespan for the last argument.

Finally, if you need to query for calibration datasets *and* their validity ranges, and don't have a point in time you're starting from, the only option is `Registry.queryDatasetAssociations`.
That's a bit less user-friendly - it only accepts one dataset type at a time, and doesn't let you restrict the data IDs at all - but it *can* query `~CollectionType.CALIBRATION` collections and it returns the associated validity ranges as well.
It actually only exists as a workaround for the fact that `~Registry.queryDatasets` can't do those things, and it will probably be removed sometime after those limitations are lifted.

