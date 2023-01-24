
# Developer guide

This guide is for pipeline TDs and core developers who want to modify Spil.  

The guide to *use* Spil is here: [user guide](user_guide.md).    
See also the [glossay](glossary.md).

## Introduction

Before continuing, it is useful to read the [user guide](user_guide.md) and [glossay](glossary.md) for an optimal understanding of Spil.

Spil is still in Beta, and this documentation is work in progress.
If you are interested in using and modifying Spil, please drop us a line at [spil@xeo.info](mailto:spil@xeo.info).
We will be happy to assist you.


*This page is work in progress.*

    - Configuring spil: existing pipeline / new pipeline
    - creating Finders, Getters, Writers


## Spil class hierarchy

The Sid class (`spil.sid.sid`) is the final class in a hierarchy.

The Sids parents are, sorted by specialisation: 
- `BaseSid`: implements the factory mechanism
- `StringSid`: String and base attributes
- `TypedSid`: types and the `field` dictionary
- `PathSid`: path resolving 
- `DataSid`: delegation to data access (`Finder`)

Sid object creation is done by a configurable factory method.
The goal is to be able to extend the Sid, and to adapt the factory. 

### Sid object creation

*The implementation and factory mechanism is not yet final.  
It might change, without affecting the usage of the API.* 

`BaseSid.__new__` calls a factory as per `_factory` class attribute.   
This factory `spil.sid.core.sid_factory.sid_factory()` delegates to functions (`sid_to_sid`, `path_to_sid`, `dict_to_sid`), depending on the input parameters.
The function returns a Sid object, that is returned by the factory to `BaseSid.__new__`.

`BaseSid.__init__` is empty to avoid initialisation for already initialised instances.


*This page is work in progress.*

## Finders

All "Finder" classes extend `Finder`.
They are typically named "FindIn*".
- **FindInPaths**: to search the file system
- **FindInList**: to search a list
- **FindInCache**: to search a cache
- **FindInConstant**: to search a list of constants for a given type
- **FindInGlob**: parent class for the glob style searches (Path, List, Cache)
- **FindInAll**: to search other Finders, depending on a configuration
- **FindInShotgrid**: to search Shotgrid

Finders implement the methods `find()`, `do_find()`, `find_one()`, and `exists()`.

### Search process

The global search process is as follows.

1. `find()` is called with a search sid (string or Sid object). 
  The search sid is most of the times untyped. For example `hamlet/a/**` matches multiple types.
  The search sid it **"unfolded"**, transformed into a list of possible typed search Sids.

  Examples of unfolding:
  ```
    "hamlet/*/**" is unfolded to: 
    [Sid("asset__file:hamlet/a/*/*/*/*/*/*"),
     Sid("shot__file:hamlet/s/*/*/*/*/*/*"),
     Sid("shot__cache_node_file:hamlet/s/*/*/*/*/*/*/*"),
     ...]

    "hamlet/*/**/maya" is unfolded to:
        [Sid("asset__file:hamlet/a/*/*/*/*/*/ma"),
         Sid("asset__file:hamlet/a/*/*/*/*/*/mb"),
         Sid("shot__file:hamlet/s/*/*/*/*/*/ma"),
         Sid("shot__file:hamlet/s/*/*/*/*/*/mb"),
         ...]
  ```

2. `do_find()` is called with a list of search sids.
  It runs the actual search on each typed search sid, and yields the result.
  (the results are kept in an internal set() to avoid yielded one twice)

Note: `find_one()` and `exists()` call `find()` by default. 

### Implementing a search

You can implement a Finder to access a data source in your pipeline.
Finders are organised in a class hierarchy, and you can override the features as needed.

Not all APIs or data sources are easy to wrap, due to Sids / Finders hierarchical nature.

#### FindInShotgrid 

Have a look at `spil_plugins.sg.FindInShotgrid` to see how the Shotgrid API is wrapped by a finder.

The powerful design of the Shotgrid API makes it possible to query most types in one single request.
The technique is called “field hopping” [https://developer.shotgridsoftware.com/python-api/usage_tips.html](https://developer.shotgridsoftware.com/python-api/usage_tips.html).

For a relational database, it means querying table joints, or create denormalized views.

*This page is work in progress.*

