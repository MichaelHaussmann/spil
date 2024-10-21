# Background

## Concepts  

Spil builds upon general concepts, as well as production proven CG pipeline concepts.  

### General concepts

- Unique Identifier - Human readable Identifier - "Natural Key"  
  [dzone.com/articles/7-strategies-for-assigning-ids-to-microservices](https://dzone.com/articles/7-strategies-for-assigning-ids-to-microservices)  
  [medium.com/blue-sky-tech-blog/a-rose-by-any-other-name-4b569309b575](https://medium.com/blue-sky-tech-blog/a-rose-by-any-other-name-4b569309b575)
  
- Python File system path  
  [www.python.org/dev/peps/pep-0428](https://www.python.org/dev/peps/pep-0428)
  
- Query by Example  
  A query technique where "example" entities, with search values, are used to retrieve "matching" results.  
  [en.wikipedia.org/wiki/Query_by_Example](https://en.wikipedia.org/wiki/Query_by_Example#As_a_general_technique)
  
- URI / URL  
  [en.wikipedia.org/wiki/Uniform_Resource_Identifier](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier)
  
- Node tree & hierarchy


### Pipeline concepts

- Unique Identifier & Resource Locator, as seen in:  
  - Blue Sky's ["Pipeline Resource Identifier (PRI)"](https://medium.com/blue-sky-tech-blog/conduit-pipeline-resource-identifiers-4432776da6ab)
  - Sony Pictures "SPREF"
  - Animal Logic [USD Asset Resolver URIs](https://github.com/DigitalProductionExampleLibrary/ALab/blob/main/docs/src/pages/alSpecific.md#uris--relative-filepaths)
  - Also OpenAssetIO's [Entity Reference](https://openassetio.github.io/OpenAssetIO/glossary.html#entity_reference)  
  
- Resource description and "Context" (Shotgrid Toolkit)  
  [developer.shotgridsoftware.com/tk-core/core.html#context](https://developer.shotgridsoftware.com/tk-core/core.html#context)  
  
- the "TypedContext", an entity for hierarchical types in Ftrack
  
- Template based path resolving  
  As implemented in Shotgrid Toolkit:  
  [github.com/shotgunsoftware/tk-config-default/blob/master/core/templates.yml](https://github.com/shotgunsoftware/tk-config-default/blob/master/core/templates.yml)   
  By CGWire's kitsu [zou.cg-wire.com/file_trees](https://zou.cg-wire.com/file_trees)   
  By [Lucidity](https://gitlab.com/4degrees/lucidity) or [resolva](https://github.com/MichaelHaussmann/resolva)
  
- Middleware between Asset consumers or producers  
  [OpenAssetIO](https://github.com/OpenAssetIO/OpenAssetIO)  
  [Katana Asset API](https://learn.foundry.com/katana/4.0/Content/tg/asset_management_system_plugin_api/concepts.html)  

- Asset Resolution - ArResolver - in USD    
  [https://openusd.org/release/api/ar_page_front.html](https://openusd.org/release/api/ar_page_front.html)  
  
- The Sid itself    
  The Sid has been used in general and fx pipelines since 2011, in various implementations and at various degrees.    

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
  Complexity costs money, at all levels of a pipeline.    
  Spil aims at simplicity, even at the price of some universality or adaptability.  
  Usage is intuitive: it is obvious that `hamlet/a/char` is an asset category, 
  and `hamlet/a/char/ophelia/modeling` is a modeling task.      
  Producers have an overview, artists see clearly, TDs are empowered.   
  That is the goal of Spil.     
  <br>
- reliable  
  This part is yet to prove.  
  "In the face of ambiguity, refuse the temptation to guess."    
  But who are you to have read this far anyway?  

## Limitations

- The configuration is tricky  
  For complex projects, creating the config is not simple, and is lacking tools to help.  
  Complex configurations may not work out of the box    
  
- Beta stage  
  The core concepts have been around for a while, and different versions of the Sid are and have been used in production pipelines for some time now.    
  But this version of "Spil" is a rewrite. It is currently used in production, but is still young.
  
- Needs optimisation  
  The resolver is fast (using caches and memoization), but would benefit from a faster rust implementation.       
  File sequence support (eg. image sequences using fileseq) is still very slow.     

## Performance

Spil thrives to be used interactively.  
It's performance depends on the data sources that are used.

- Spil uses a `FindInConstants` class to handle configurable data that mostly doesn't change (types, asset types)
- Spil ships with a configurable `FindInCache` class to handle data that changes rarely (projects, sequences, assets, etc.).
  (not production ready in current release)
- Pattern regex-compiles are instance cached
- String Resolves are internally stored in a custom lru_cache
- `Finders` use generators

## Plans and ongoing development

The priority is to make the current feature set more robust, efficient, and easy to deploy.
- tools to help create and verify the configuration files
- more testing and profiling
- rust implementation of [resolva](https://github.com/MichaelHaussmann/resolva)

To take profit from the Sids universality, we plan on building reusable open source bricks and pipeline tools.

For example:
- protocol for pipeline actions, for example `sid://play?hamlet/s/sq030/**/>/p/movie`
- connectors to Shotgrid, CGWire Kitsu, Ftrack and Databases
- using the sid as a USD Asset Resolver / In a USD pipeline
- GraphQL and/or rest API  
- file system style navigation and context handling    
For example `cd hamlet/s/sq010`


<br/>
