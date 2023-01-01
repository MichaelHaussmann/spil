# FAQ

## What is Spil ?

Spil is a pure python library for CG and VFX pipelines. 
Spil provides a simple, human-readable, hierarchical, path-like unique identifier for every entity or file of a CG production pipeline.    
An intuitive API is built around this identifier, including glob-like query, CRUD data access and path resolving.  

## Can Spil be useful to me ?

If ...
- you work on a CG or VFX pipeline 
- the pipeline is file system based, or uses multiple file system configurations
- there are multiple data sources (file system, database, asset management system, etc.)
- there is no data access api, or multiple apis, or an overcomplicated api

If you check two or three of these statements, Spil may be for you.

## Can I get it ? 

Spil is open source and can be used for free.  
It can be installed using `pip install spil` or forked from [github](https://github.com/MichaelHaussmann/spil)
See [installation](installation.md).

Spil is released under Lesser GPL and is usable in **closed source commercial applications**.  
(Only modifications to Spil itself must be open sourced).

## Use the name of an item as it's unique Id - really ? 

Human-readable Identifier ("Natural Key") vs Generated Unique ID (UUID).  
That is the (tough) question.

For the Sid, the name of an item becomes its unique ID.  
`hamlet/s/sq010/sh0010/layout/v012/p/mov` instead of `74fbd636–4fc5–11e9–91a2-ecb1d74481b4`.  

While this has an obvious advantage on readability and simplicity, it comes at a price.  
The biggest disadvantage is the locking of names. It becomes difficult to rename things.  
*(Example: if the sid is stored in a database, it gets complicated to rename an asset category)*.  
But we still believe the advantage is worth the price.  

Please see also the blue sky tech blog on the subject:  
[medium.com/blue-sky-tech-blog/a-rose-by-any-other-name-4b569309b575](https://medium.com/blue-sky-tech-blog/a-rose-by-any-other-name-4b569309b575)  

**Note:** 
If Spil is used as a pure data abstraction layer, it is only a transient, non-permanent, data source.
In that case, the name locking is not a limitation anymore.


## Usage seems simple, but configuration is a nightmare.

*“Simple things should be simple, complex things should be possible.”*  
(Alan Kay)  

Spil should be intuitive and simple to use.  
Complexity is hidden - but it's still there.

Clearly, efforts need to be put in tools assisting the configuration process, better documentation, more examples. etc.
In the meantime, please do not hesitate to get in touch at [spil@xeo.info](mailto:spil@xeo.info).

## Who makes Spil ?

The Sid concept goes back to Studio100Animation in 2011.  
History page in the making.  
It was rewritten and open sourced in 2019, by [Michael Haussmann](https://github.com/MichaelHaussmann), [spil@xeo.info](mailto:spil@xeo.info).

