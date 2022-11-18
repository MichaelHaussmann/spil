
[![Spil, the simple pipeline lib.](docs/img/spil-logo.png)](https://github.com/MichaelHaussmann/spil)


# spil  
The Simple Pipeline Lib.  
A Simple library for CG Pipelines, built around the "**Sid**".   
<br/>
The goal of SPIL is to provide a simple, universal, hierarchical, human-readable and unique identifier for every entity or file of a CG production pipeline.   

This identifier is called the "**Sid**" - for "Scene Identifier", or simply "String ID".

# 
## Unique Identifier

SPIL considers entities of a CG pipeline as being nodes of a hierarchy.
Each node has a unique path, which is the entitie's unique identifier, the "Sid".

Examples : 

- Sid of sequence 30 shot 10 in the project "Hamlet":
```
"hamlet/s/sq030/sh0010"
```

- Sid for the maya mb file of character Ophelia's modeling, published version v002:
```
"hamlet/a/chars/ophelia/modeling/v002/p/mb" 
```

#
## A Dictionary with a type
As it's core, the Sid is simply a dictionary associated to a type.

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

#
## Simple API

Spil offers a simple API to work with Sids.  

```
current_shot = Sid("hamlet/s/sq030/sh0010") 
current_shot.get("project")           # "hamlet" 
current_shot.get_as("sequence")       # "hamlet/s/sq030" 
current_shot.get_with(task="render")  # "hamlet/s/sq030/sh0010/render"  
```

Data can be accessed in multiple ways, dictionary, string or URI
```
current_shot = Sid("hamlet/s/sq030/sh0010") 
current_shot.data            #  { 'project': 'hamlet', 'type': 's', 'sequence': 'sq030', 'shot': 'sh0010' }
current_shot.get_uri()       # "project=hamlet&type=s&seq=sq030&shot=sh0010"
current_shot.fullstring      # "shot__shot:hamlet/s/sq030/sh0010" 
```

#
## Resolver to and from datasources - versatile middleware 
The Sid can be translated to and from different data sources.

- For example a file system:
```
current_file = Sid(path="/projects/hamlet/chars/ophelia/modeling/v002/publish/ophelia_model.mb")

print( current_file )       # "hamlet/a/chars/ophelia/modeling/v002/p/mb"
current_file.path           # "/projects/hamlet/chars/ophelia/modeling/v002/publish/ophelia_model.mb"
```

- Example in a maya scene file:
```
current = Sid(path=pm.sceneName())
current.get('version')                # "v002"
```

- The Sid could be resolved from an ftrack "link" string, or a cgwire json, or any datasource, after implementation of a mapping or translation.

Common requests are delegated from the Sid to a configurable Data Source
```
task_sid = Sid("hamlet/s/sq030/sh0010/layout") 

task_sid.exists()                 # True
task_sid.get_last('version')      # "hamlet/s/sq030/sh0010/layout/v003"
```

Sids can be chained to easily express common pipeline needs 
```
task_sid = Sid("hamlet/s/sq030/sh0010/layout") 

if task_sid.exists():
  print( task_sid.get_last('version').get_attr('comment') )     # "Changed camera angle."
```

This all makes the Sid a versatile and lightweight data source abstraction layer.

#
## Intuitive Search Syntax  

Building on top of these ideas, and considering the Sid as a middleware, 
it can be used as a simple, intuitive, and unified search syntax.

The search syntax is string based, and uses operators:
- \*   : star search
- **  : recursive star search
- \>   : last
- \,   : or
  
### Search Examples
- "All the Shots of sequence sq030" ?
```
"hamlet/s/sq030/*"
```

- "All the published maya files of Ophelias modeling" ?
```
"hamlet/a/chars/ophelia/modeling/*/p/maya"
```
- "Last published maya file of Ophelias modeling" ?
```
"hamlet/a/chars/ophelia/modeling/>/p/maya"
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

  
### Implementation

This search syntax is currently implemented:
- to search the file system
- to search in a list of Sids, for example a list of cached query results

It is possible (and planned) to implement this search as a front to other query methods.
For example to translate to an SQL, Shotgrid or Ftrack query. 

A CGWire kitsu connector is under development.

# 
## UI

Spil can be used with the spil_ui.browser.

The browser allows to run sid searches, navigate through the results and select Sids.
spil_ui is a separate repository.


# 
## Flexible and configurable

Spil is a library, and not a framework.  
It can easily integrate and connect onto existing pipelines.

The Sid is based on the [Lucidity](https://gitlab.com/4degrees/lucidity/) resolver, and is configurable.  

Sid config example:
```
('asset__file',            '{project}/{type:a}/{cat}/{name}/{variant}/{task}/{version}/{state}/{ext:scenes}'),
('asset__movie_file',      '{project}/{type:a}/{cat}/{name}/{variant}/{task}/{version}/{state}/{ext:movies}'),
```

File config example:
```
('asset__file',             r'{@project_root}/scenes/{type:01_assets}/{cat_long}/{name}/{variant}/{task}/{state}_{version}/{name}.{ext:scenes}'),
('asset__movie_file',       r'{@project_root}/movies/{type:01_assets}/{cat_long}/{name}/{variant}/{task}/{state}_{version}/{name}.{ext:movies}'),
```

The Data Source is configurable depending on the given Sid or Sid type.
```
get_data_source(sid)  # may return a SidCache or FS() (File system Search), or custom
get_attribute_source(sid, attribute)  # returns custom callables 
```

Spil works in Python 2.7 and 3.7


#
### Database Identifier

If the Sid is planned into the pipeline, it is a handy database field.

- SQL Query example
```
SELECT * FROM Entities WHERE sid = "hamlet/a/chars/ophelia"
```

- Shotgrid query example 
```
sg.find('Shot', 
        ['sg_sid', 'is', 'hamlet/s/sq030/sh0010'],
        ['code', 'sg_sid', 'sg_cut_in', 'sg_cut_out', 'sg_ep_in',
        'sg_ep_out', 'sg_editing_status'])
```

# 
## Performance

Spil thrives to be used interactively. 
It's performance depends on the data sources that are used.

- Spil ships with a configurable SidCache to handle data that changes rarely (projects, sequences, asset categories). 
- String / Sid Resolves are internally stored in a lru_cache
- searches use generators
- Python 3 is globally faster that python 2


#
## Concepts  

The Sid builds upon general concepts, as well as production proven CG pipeline concepts.  

### General concepts

- Unique Identifier - Human readable Identifier - "Natural Key"  
https://dzone.com/articles/7-strategies-for-assigning-ids-to-microservices  
https://medium.com/blue-sky-tech-blog/a-rose-by-any-other-name-4b569309b575
####
- File sytem path  
https://www.python.org/dev/peps/pep-0428
####
- Query by Example  
  A query technique where "example" entities, with search values, are used to retrieve "matching" results.  
  QBE is typically an abstraction layer on top of a database system query, like SQL or ORM (object-relational mapping).
  https://en.wikipedia.org/wiki/Query_by_Example#As_a_general_technique
####
- URI / URL  
  https://en.wikipedia.org/wiki/Uniform_Resource_Identifier
####
- Node tree & hierarchy


### Pipeline concepts

- Unique Identifier & Resource Locator  
Examples: "SPREF" (Sony Pictures), or the "Pipeline Resource Identifier - PRI" (Blue Sky)  
https://medium.com/blue-sky-tech-blog/conduit-pipeline-resource-identifiers-4432776da6ab
####
- Resource description and "Context" (Shotgrid Toolkit)  
  https://developer.shotgridsoftware.com/tk-core/core.html#context
####
- the "TypedContext", an entity for hierarchical types in Ftrack
####
- Template based path resolving  
  As implemented in Shotgrid Toolkit:  
  https://github.com/shotgunsoftware/tk-config-default/blob/master/core/templates.yml  
  Or by CGWire's kitsu https://zou.cg-wire.com/file_trees  
  Or by Lucidity : https://gitlab.com/4degrees/lucidity
####
- Middleware between Asset consumers or producers  
  [OpenAssetIO](https://github.com/OpenAssetIO/OpenAssetIO)  
  [Katana Asset API](https://learn.foundry.com/katana/4.0/Content/tg/asset_management_system_plugin_api/concepts.html)  
####
- Asset Resolution - ArResolver - in USD    
  https://graphics.pixar.com/usd/release/wp_ar2.html  
####
- The Sid itself    
  The Sid has been used in general and fx pipelines for over 10 years, in various implementations and at various degrees.  
 
#
## Philosophy

Spil aims to be : flexible, pragmatic, simple - and reliable. 
####
- flexible  
Spil is a library, and not a framework.  
It can be plugged to existing pipelines. It easily blends in, to be used only where it is needed.
It can also be planned at a pipelines core - and be a central part of it.
####
- pragmatic  
It all starts as files. So does Spil.  
YAGNI meets WYSIWYG.  
####
- simple  
One of the ideas of Spil is to build upon implicit information, to simplify how we see our datas.  
For example, it is obvious that "hamlet/a/chars" is an asset category, and "hamlet/a/chars/ophelia/modeling" is a modeling task.  
The Sid's string representation is a dictionary where the keys are implicit. Intuitive for the human user. 
####
- reliable  
This part is yet to prove.  
"In the face of ambiguity, refuse the temptation to guess."  
But who are you to have read this far anyway?  

# 
## Discussion

- Human readable Identifier ("Natural Key") vs Generated Unique ID (UUID)  
Using the Sid implies that the name of the item becomes its unique ID.  
While this has a huge advantage on readability and simplicity, it comes at a price.
The biggest disadvantage is the locking of names. It becomes difficult to rename things.  
*(Example: if the sid is stored in a database, and I would like to rename an asset category.
Either I need to update all the asset sids, or use a sid name mapping for types).*  
We still believe the advantage is worth the price. 
Please see also the blue sky tech blog on the subject:
https://medium.com/blue-sky-tech-blog/a-rose-by-any-other-name-4b569309b575


# 
## Main limitations

- The configuration is tricky  
For complex projects, creating the config is not simple, and is lacking tools to help.
Complex configurations do not work out of the box
####
- Beta stage  
The core concepts have been around for a while, and different versions of the Sid are and have been used in production pipelines for some time now.  
But this version of "Spil" is a complete rewrite. It is currently used in production, but is still young.
It lacks automated code testing and profiling.
####
- Needs optimisation  
Core parts will need a C++ implementation.
Searches returning big result sets can be relatively slow.  
File sequence support (eg. image sequences using fileseq) is still very slow. 


# 
## Plans and ongoing development

The priority is to make the current feature set more robust and efficient.  
Adding tests, documentation and quickstart.

Then, implement some important core features and enhancements
- tools to help create and verify the configuration files
- simplify the Sid's core implementation and make it extendable
- adding a C++ implementation to make the resolve faster

To take profit from the Sids universality, we plan on building reusable open source bricks and pipeline tools.

For example:
- connectors to Shotgrid, CGWire, Ftrack and Relational Databases
- using the sid as a USD Asset Resolver / In a USD pipeline
- protocol for pipeline actions  
For example `sid://play?hamlet/s/sq030/**/>/p/movie`
- REST API
- GraphQL API  
- file system style navigation and context handling    
For example `cd hamlet/s/sq010`
  
Some under the hood development is under evaluation
- faster support for file sequences (fileseq)
- allow optional fields in the config (as the bracket syntax in SGTK yaml)
- move the config to a universal format (yaml) 


Yeah, and we need a quickstart video... 

# 
## Interested ?

We'd love to hear from you.

