
# Developer guide: configuring and extending spil

*This page is work in progress.*

    - Configuring spil: existing pipeline / new pipeline
    - creating Finders, Getters, Writers


## Extending Spil

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