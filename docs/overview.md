# Spil, the Simple Pipeline lib.

[![Spil, the simple pipeline lib.](img/spil-logo.png)](https://github.com/MichaelHaussmann/spil)

Spil provides a simple, human-readable, unique, and path-like identifier for every entity or file of a CG production pipeline.    
An intuitive API is built around this identifier, including glob-like query, CRUD data access and path resolving.  

## Overview

### Unique Hierarchical Identifier

This identifier is called the "**Sid**" - for "Scene Identifier".

Examples : 

- Sid of sequence 30 shot 10 in the project "Hamlet":
```
"hamlet/s/sq030/sh0010"
```

- Sid for the maya mb file of character Ophelia's modeling, published version v002:
```
"hamlet/a/chars/ophelia/modeling/v002/p/mb" 
```

### Data Dictionary with a Type 

Once resolved, the Sid is a dictionary associated to a type.

Some examples:

- type `shot__task` :
```
{ 
  'project': 'hamlet', 
  'type': 's', 
  'sequence': 'sq030', 
  'shot': 'sh0010',
  'task': 'animation' 
}
```
- type `shot__sequence` :
```
{ 
  'project': 'hamlet', 
  'type': 's', 
  'sequence': 'sq020' 
}
```
- type `asset__version` :
```
{ 
  'project': 'hamlet', 
  'type': 'a', 
  'cat': 'props', 
  'name': 'skull',
  'task': 'modeling',
  'version': 'v008' 
}
```

### Intuitive API

Sid creation and manipulation

```python
from spil import Sid

# create a Sid from scratch
task = Sid("hamlet/s/sq030/sh0010/render")      # a task sid: hamlet/s/sq030/sh0010/render

# create a Sid by changing values
anim_task = task.get_with(task="anim")          # task sid: hamlet/s/sq030/sh0010/anim 

# create a Sid from a Sids hierarchy 
sequence = task.get_as('sequence')              # sequence sid: hamlet/s/sq030

# another way
shot = task.parent                              # shot sid: hamlet/s/sq030/sh0010 
```

Data can be accessed in multiple ways: by keys, as a complete dictionary, as string or URI.
```python
from spil import Sid 
shot = Sid("hamlet/s/sq030/sh0010")

# get a field of the sid by key
shot.get("sequence")   # sq030

# as a dictionary
shot.fields            #  { 'project': 'hamlet', 'type': 's', 'sequence': 'sq030', 'shot': 'sh0010' }

# as a URI
shot.as_uri()          # "project=hamlet&type=s&seq=sq030&shot=sh0010"

# "fullstring": type and string
shot.fullstring        # "shot__shot:hamlet/s/sq030/sh0010" 
```

### Path Resolver

The Sid can be resolved to and from paths.  
Multiple configurations can co-exist.  
For example "local", "server", "linux", etc. paths.    

```python
from spil import Sid

# creating a Sid from path
scene = Sid(path="/projects/hamlet/chars/ophelia/modeling/v002/publish/ophelia_model.mb")

print(scene)            # "hamlet/a/chars/ophelia/modeling/v002/p/mb"

# returning default path
path = scene.path()     # "/projects/hamlet/chars/ophelia/modeling/v002/publish/ophelia_model.mb"

# returning path from "server" configuration
path = scene.path("server")     # "/server/projects/hamlet/chars/ophelia/modeling/v002/publish/ophelia_model.mb"
```

Example in maya, with an opened scene file:
```python
import maya.cmds as cmds
from spil import Sid

# Get the current scene's path
scene_path = cmds.file(query=True, sceneName=True)

# build the Sid
scene = Sid(path=scene_path)

# use the Sid
scene.get('version')                # "v002"
```

### Data access and Pipeline workflows

Sid wraps access to common requests, that are internally delegated to configurable data sources (Getters and Writers).

```python
from spil import Sid
task_sid = Sid("hamlet/s/sq030/sh0010/layout") 

task_sid.exists()                 # True
task_sid.get_last('version')      # "hamlet/s/sq030/sh0010/layout/v003"
```

Sids API can intuitively express common pipeline workflows. 
```python
from spil import Sid
task_sid = Sid("hamlet/s/sq030/sh0010/layout") 

if task_sid.exists():
  print( task_sid.get_last('version').get_attr('comment') )     # "Changed camera angle."

# match() is handy for hooks and action overrides
if task_sid.match('hamlet/s/*/*/layout/**/maya'):  
    # do something specific for hamlet maya layouts
    ... 
```

## Finding Sids: simple glob-like Search Syntax  

Considering the Sid as a middleware and data abstraction layer, Spil proposes an intuitive glob-like search syntax.
 
It is string based, and uses operators:
- \*   : star search
- **  : recursive star search
- \>   : last
- \,   : "or"  
Also supports configurable aliases (eg. "movie" is an alias for "mov,avi,mp4")
  
### Search Examples

- "All the Shots of sequence sq030" ?
```
"hamlet/s/sq030/*"
```

- "All the published maya files of Ophelias modeling" ?
```
"hamlet/a/chars/ophelia/model/*/p/maya"
```
- "Last published maya files of Ophelias rigging or surfacing" ?
```
"hamlet/a/chars/ophelia/rig,surface/>/p/maya"
```

- "Last published render Movie files for the project hamlet" ?
```
"hamlet/s/**/render/>/p/movie"
```

- "All cache files for hamlet's sequence 30, shot 10" ?
```
"hamlet/s/sq030/sh010/**/cache"
```

### URI in search 

URI Syntax can be used to add search filters on yet untyped searches

- "All published Movie files for hamlet's sequence 30" ?
```
"hamlet/s/sq030/**/movie?state=p"
```

- "All published hip files for hamlet's sequence 30, animation or layout" ?
```
"hamlet/s/sq030/**/hip?state=p&task=animation,layout"
```

  
### Finders

To launch queries, Spil implements `Finder` classes that access different data sources.  

- **FindInPaths**: to search the file system
- **FindInList**: to search a list
- **FindInCache**: to search a cache
- **FindInFinders**: to search other Finders, depending on a configuration

All Finders implement `find()`, `find_one()` and `exists()`.

```python
# Look up the last published versions for given shot, on the File System 
from spil import FindInPaths as Finder
for sid in Finder().find("hamlet/s/sq010/sh0010/**/>/p/movie"):
  print(sid)

# "hamlet/s/sq010/sh0010/layout/v012/p/mov"
# "hamlet/s/sq010/sh0010/animation/v003/p/avi"
# "hamlet/s/sq010/sh0010/render/v001/p/mov"
# ...
```
  
A `FindInShotgrid` is also included, as an example Finder implementation.     
It may need to be adapted, depending on the production's Shotgrid usage.    

It is planned to implement other Finders, for example for MongoDB and CGWire kitsu.    

 
## UI
 
Spil can be used with the spil_ui.browser.  

[![Spil Qt UI](img/spil_ui.png)](https://github.com/MichaelHaussmann/spil_ui)
  
Spil_UI is a Qt browser UI, built on top of Qt.py.   
Navigating through the columns builds a "Search Sid" and calls a Finder.    
It is possible to run actions on the currently selected Sid.  
 
spil_ui is a separate repository (in the process of being open sourced and released).   


## Flexible and configurable

Spil is a library, not a framework.  
It adopts your naming conventions, and can easily integrate and connect onto existing pipelines.    

The Sid is based on the [Lucidity](https://gitlab.com/4degrees/lucidity/) resolver, and is configurable.  

Sid config example:
```
'asset__file':            '{project}/{type:a}/{assettype}/{asset}/{task}/{version}/{state}/{ext:scenes}',
'shot__file':             '{project}/{type:s}/{sequence}/{shot}/{task}/{version}/{state}/{ext:scenes}',
'shot__movie_file':       '{project}/{type:s}/{sequence}/{shot}/{task}/{version}/{state}/{ext:movies}',
```

Paths config example:
```
'asset__file':             '{@project_root}/{project}/PROD/{type:ASSETS}/{assettype}/{asset}/{task}/{version}/{assettype}_{asset}_{task}_{state}_{version}.{ext:scenes}',
'shot__file':              '{@project_root}/{project}/PROD/{type:SHOTS}/{sequence}/{sequence}_{shot}/{task}/{version}/{sequence}_{shot}_{task}_{state}_{version}.{ext:scenes}',
'shot__movie_file':        '{@project_root}/{project}/PROD/{type:SHOTS}/{sequence}/{sequence}_{shot}/{task}/{version}/EXPORT/{sequence}_{shot}_{task}_{state}_{version}.{ext:movies}',   
```

The Data Source is configurable depending on the given Sid or Sid type.
```
get_data_source(sid)  # may return a SidCache or FS() (File system Search), or custom
get_attribute_source(sid, attribute)  # returns custom callables 
```

Spil works in Python 3.7+


## Performance

Spil thrives to be used interactively. 
It's performance depends on the data sources that are used.

- Spil ships with a configurable FindInCache to handle data that changes rarely (projects, sequences, asset types). 
- String / Sid Resolves are internally stored in a lru_cache
- searches use generators


## Concepts  

The Sid builds upon general concepts, as well as production proven CG pipeline concepts.  

### General concepts

- Unique Identifier - Human readable Identifier - "Natural Key"  
  [dzone.com/articles/7-strategies-for-assigning-ids-to-microservices](https://dzone.com/articles/7-strategies-for-assigning-ids-to-microservices)  
  [medium.com/blue-sky-tech-blog/a-rose-by-any-other-name-4b569309b575](https://medium.com/blue-sky-tech-blog/a-rose-by-any-other-name-4b569309b575)
  
- Python File sytem path  
  [www.python.org/dev/peps/pep-0428](https://www.python.org/dev/peps/pep-0428)
  
- Query by Example  
  A query technique where "example" entities, with search values, are used to retrieve "matching" results.  
  QBE is typically an abstraction layer on top of a database system query, like SQL or ORM (object-relational mapping).
  [en.wikipedia.org/wiki/Query_by_Example](https://en.wikipedia.org/wiki/Query_by_Example#As_a_general_technique)
  
- URI / URL  
  [en.wikipedia.org/wiki/Uniform_Resource_Identifier](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier)
  
- Node tree & hierarchy


### Pipeline concepts

- Unique Identifier & Resource Locator  
  Examples: "SPREF" (Sony Pictures), or the "Pipeline Resource Identifier - PRI" (Blue Sky)  
  [medium.com/blue-sky-tech-blog/conduit-pipeline-resource-identifiers](https://medium.com/blue-sky-tech-blog/conduit-pipeline-resource-identifiers-4432776da6ab)
  Also OpenAssetIO's [Entity Reference](https://openassetio.github.io/OpenAssetIO/glossary.html#entity_reference)
  
- Resource description and "Context" (Shotgrid Toolkit)  
  [developer.shotgridsoftware.com/tk-core/core.html#context](https://developer.shotgridsoftware.com/tk-core/core.html#context)
  
- the "TypedContext", an entity for hierarchical types in Ftrack
  
- Template based path resolving  
  As implemented in Shotgrid Toolkit:  
  [github.com/shotgunsoftware/tk-config-default/blob/master/core/templates.yml](https://github.com/shotgunsoftware/tk-config-default/blob/master/core/templates.yml) 
  Or by CGWire's kitsu [zou.cg-wire.com/file_trees](https://zou.cg-wire.com/file_trees)  
  Or by Lucidity : [Lucidity](https://gitlab.com/4degrees/lucidity)
  
- Middleware between Asset consumers or producers  
  [OpenAssetIO](https://github.com/OpenAssetIO/OpenAssetIO)  
  [Katana Asset API](https://learn.foundry.com/katana/4.0/Content/tg/asset_management_system_plugin_api/concepts.html)

- Asset Resolution - ArResolver - in USD    
  [graphics.pixar.com/usd/release/wp_ar2.html](https://graphics.pixar.com/usd/release/wp_ar2.html) 
  
- The Sid itself    
  The Sid has been used in general and fx pipelines for over 10 years, in various implementations and at various degrees.  

## Philosophy

Spil aims to be : flexible, pragmatic, simple - and reliable.   
  
- flexible  
Spil is a library, and not a framework.  
It can be plugged to existing pipelines. It easily blends in, to be used only where it is needed.  
It can also be planned at a pipelines core - and be a central part of it.    
<br>  
- pragmatic    
It all starts as files. So does Spil.  
YAGNI meets WYSIWYG.  
<br>  
- simple    
Complexity costs money, at all levels of a pipeline, from artist to core developer.    
Spil aims at simplicity, even at the cost of some universality or adaptability.  
Once the configuration is done, the complexity is hidden. Usage is intuitive.  
For example, it is obvious that `hamlet/a/char` is an asset category, and `hamlet/a/chars/ophelia/modeling` is a modeling task.    
Producers have an overview, artists see clearly, TDs are empowered.   
That is the goal of Spil.     
<br>
- reliable  
This part is yet to prove.  
"In the face of ambiguity, refuse the temptation to guess."    
But who are you to have read this far anyway?  

## Main limitations

- The configuration is tricky  
For complex projects, creating the config is not simple, and is lacking tools to help.  
Complex configurations may not work out of the box    
  
- Beta stage  
The core concepts have been around for a while, and different versions of the Sid are and have been used in production pipelines for some time now.    
But this version of "Spil" is a complete rewrite. It is currently used in production, but is still young.  
It lacks automated code testing, CI/CD, and profiling.  
  
- Needs optimisation  
Core parts, like the resolver, will need a C++ implementation.    
Searches returning big result sets can be relatively slow.  
File sequence support (eg. image sequences using fileseq) is still very slow.   

  
## Plans and ongoing development

The priority is to make the current feature set more robust and efficient.  
Adding tests, documentation and quickstart.

Then, implement some important core features and enhancements
- tools to help create and verify the configuration files
- adding a C++ implementation to make the resolve faster

To take profit from the Sids universality, we plan on building reusable open source bricks and pipeline tools.

For example:
- connectors to Shotgrid, CGWire, Ftrack and Relational Databases
- using the sid as a USD Asset Resolver / In a USD pipeline
- protocol for pipeline actions, for example `sid://play?hamlet/s/sq030/**/>/p/movie`
- GraphQL and/or rest API  
- file system style navigation and context handling    
For example `cd hamlet/s/sq010`

Yeah, and we need a quickstart video... 


## Interested ?

We'd love to hear from you.  
We are interested in any kind of feedback or questions.  

Spil is released under Lesser GPL and is usable in closed source commercial applications.  

Don't hesitate to contact us : [spil@xeo.info](mailto:spil@xeo.info).  
We will be happy to respond.  
<br>
  
![python](https://img.shields.io/badge/PYTHON-blue?style=for-the-badge&logo=Python&logoColor=white)
![code formatter](https://img.shields.io/badge/Formatter-BLACK-black?style=for-the-badge)
![type checker](https://img.shields.io/badge/Type%20checker-MYPY-dodgerblue?style=for-the-badge&labelColor=abcdef)
![gitHub release](https://img.shields.io/github/v/release/MichaelHaussmann/spil?style=for-the-badge&color=orange&labelColor=sandybrown)
