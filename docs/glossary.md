# Spil Glossary

*This page is work in progress.*

## Sid

The Sid a structure containing:
- a string
- a type, if defined
- a dictionary, named `fields`, if type is defined

The string can be any string.

During instantiation, the Sid factory attempts to resolve the string, according to the `spil_sid_conf`.
If it succeeds, the Sid object receives a `type` property, and a `fields` dictionary.
If the string contains a `query`, it is applied.

If the string cannot be resolved, the Sid object only has a `string` property.

### Fields

Name of the Sid's data dictionary.

```python 
from spil import Sid
Sid('hamlet/s/sq030/sh0010').fields  # #  { 'project': 'hamlet', 'type': 's', 'sequence': 'sq030', 'shot': 'sh0010' }
```

### Types

When the Sid string is resolved, it becomes typed. 
- The `type` is the key of the mapping template.  
Examples: `shot__file`, `shot__task`, `asset__version`
- the `basetype` is the first part of the type 
Examples: `shot`, `asset`
- The keytype is the name of the last key of the Sid's `fields` data dictionary.
Examples: `task`, `version`

#### type
 
The type the unique key to the Sid template dictionary.

```python 
from spil import Sid
Sid('hamlet/s/sq030/sh0010/animation').type  # "shot__task"
```

#### basetype

First part of the type.
A Basetype defines sorted keys.

```python 
from spil import Sid
Sid('hamlet/s/sq030/sh0010/animation').basetype  # "shot"
```

#### keytype

last key of the Sid's data dictionary (`fields`)

Most of the time, the keytype is the second part of the type, for example:
`shot__task`, `asset__version`.

Sometimes it is not: 
type: `asset__file`, keytype: `ext`  

```python 
from spil import Sid
Sid('hamlet/s/sq030/sh0010/animation').keytype  # "task"
Sid('hamlet/a/char/ophelia/modeling/v002/p/mb').keytype  # "ext"
```
 
#### Examples:  

        Sid("hamlet/a/char/claudius/model/v001/w/blend")
        type: 'asset__file'
        basetype: 'asset'
        keytype: 'ext'
        
        Sid("hamlet/s")
        type: 'shot'
        basetype: 'shot'
        keytype: 'type'
        
        Sid("hamlet")
        type: 'project'
        basetype: 'project'
        keytype: 'project'


### query

A query is a key value representation of a Sid.  

`project=hamlet&type=a&assettype=props&asset=skull`

It can be used to complement a string:  
`project/a/props?asset=skull`

Or to update it:  
`project/a/props/dagger?asset=skull`

It is typically useful in search sids, because it allows to apply values to yet untyped Sids.

Example:  
`project/s/sq010/sh0010/**/ma?state=p`    
Search all maya files for shot 0010, that are published.

A Query can contain optional fields, that get applied only where they already exist
(fields are only updated, never added).  
Optional fields are prefixed with `~`.  

Example:  
`project/s/sq010/sh0010/anim/**/cache?node=~*`   
Search all caches for shot 0010, optionally with node.  

When a Sid is created with a Query, this Query is "applied" to the Sid.

```python
from spil import Sid

sid = Sid("hamlet/a/props/dagger?asset=skull")
print(sid.get("asset"))  # "skull"
```

The query apply works like this:
- the Sid's type is defined, which creates the data dictionary
- the query key/values update the dictionary

The query apply is designed to update an existing typed Sid.
If the Sid is not typed, or the apply changes the type, it is considered fail, and is not applied. 
If the query is not applied, it stays as a trailing part of the string.

### Extrapolate

From an iterable containing leaf node paths, extrapolates all the subnode paths.

This is useful when the data source quickly provides leaves only, but we want to find child data.

Example: 

The Sid 
```
"hamlet/a/chars/ophelia/modeling/v002/p/mb"
```  
will generate:
```
"hamlet/a/char/ophelia/modeling/v002/p/mb" 
"hamlet/a/char/ophelia/modeling/v002/p"
"hamlet/a/char/ophelia/modeling/v002"
"hamlet/a/char/ophelia/modeling"
"hamlet/a/char/ophelia/modeling"
"hamlet/a/char/ophelia"
"hamlet/a/char"
"hamlet/a"
"hamlet"
```

### Resolving

Globally, resolving means translating a string into meaningful data, in dictionary form.
Spil uses Lucidity as the resolver.

Spil uses resolving for 2 types of strings: 
- the Sid string, for example `hamlet/a/char/ophelia`.
- path strings

*Sid resolving*

Upon instantiation, the Sid factory attempts to resolve the Sid string, for example `hamlet/a/char/ophelia`.
It uses the `spil_sid_conf` configuration, containing a dictionary with all available Lucidity templates.
(The templates are "extrapolated" and augmented with configured mappings, prior to resolving, see configuration.)
If the resolve is a success, the Sids `type` becomes the template's name, and `fields` the resolved dictionary.

*Path resolving*

Sid instantiation using the `path` parameter triggers a path resolving.
The Lucidity resolver uses `spil_data_conf.path_configs` to find one or more path template configurations.
These templates are then used to resolve the given path string to the Sids dictionary.

Sid and Path templates should match (although some Sid types may not have a path counterpart). 

For more on the configuration, read the configuration guide.


### unfold

A single, potentially untyped, Search Sid string is "unfolded" into a list of typed search sids.


### expand

"Expand" means replacing a double wildcard "/**" by the possible amount of simple wildcards "/*", wherever possible.

This allows for simpler searches on multiple types.

Example:
    To find all movie files from a shot, we need to search for: hamlet/s/sq010/sh0020/*/*/*/mov
    hamlet/s/sq010/sh0020/**/mov is a simpler form.


### CRUD

Acronym for Create, Read, Update, Delete.  

Spil implements:
- **Finders** (find Sids), 
- **Getters** (get data for Sids) and 
- **Writers** (create, delete Sids, and update data).

These classes are open to extension by custom classes.  
They are designed to be combined, to aggregate and abstract data sources.  

#### Finders
#### Getters
#### Writers

### Caching

#### lru_cache

Spil implements a lightweight lru ("least recently used") cache decorator, which caches many functions that are often called and return the same result.
For example the resolver.

#### FindInCache

Implements a simple (simplistic) Memory and Disk cache holding a List of Sids.
See detailed API documentation.

*FindInCache is not yet production ready*.

## Industry naming standards

The core of spil is fully configurable, and will adopt your pipeline's naming convention and vocabulary.
In Spils example configs, we use naming conventions that we believe have become industry standards.
This vocabulary is included here, for reference.

### project
Name of a production.

### asset
### shot
### entity
### step / tasktype
### assettype
### version


*This page is work in progress.*