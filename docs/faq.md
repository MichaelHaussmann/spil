# FAQ

## What is Spil ?

Spil is a pure python library for CG and VFX pipelines. 
Spil provides a simple, human-readable, hierarchical, path-like unique identifier for every entity or file of a CG production pipeline.    
An intuitive API is built around this identifier, including glob-like query, CRUD data access and path resolving.  

## Can Spil be useful to me ?

If ...
- you work on a CG or VFX pipeline  
- the pipeline is using an unambiguous naming convention
- the pipeline is file system based, or uses multiple file system configurations
- there are multiple data sources (file system, database, asset management system, etc.)
- there is no data access api, or multiple apis, or an overcomplicated api

If you check two or three of these statements, Spil might be for you.

## Can I get it ? 

Spil is open source and can be used for free.  
It can be installed using `pip install spil` or forked from [github](https://github.com/MichaelHaussmann/spil).
See [installation](installation.md).

Spil is released under Lesser GPL and is usable in **closed source commercial applications**.  
(Only modifications to Spil itself must be open sourced).


## Why does Spil print the message "USING DEMO CONFIGURATION ...." ?

Spil needs configuration files in the pythonpath.
("spil_sid_conf.py" and others named "spil_*_conf.py") 

If none are found, Spil falls back to the shipped demo configuration.
It prints the message "USING DEMO CONFIGURATION... ".

You can adapt this demo configuration to your needs, or create a configuration on your own. 
Once you add your configuration folder (or the demo configuration folder) to the pythonpath, this message will disappear.

Please check the documentation for "Adapting the demo config" [configuration](configuration.md).

## The project name is hard coded in the configuration file ?

In the shipped default demo configuration, the project is hardcoded in the spil_sid_conf file.
This can be changed, to retrieve projects names by any other possible way.

The main idea is: the preciser the information in the configuration, the better the pattern matching works.    
Data that changes rarely (asset types, task types, and potentially project names) should find their way into the configuration.  
How this is done can vary, and getting the configuration from a database is absolutely possible.

## Use the name of an item as it's unique Id - really ? 

Human-readable Identifier ("Natural Key") vs Generated Unique ID (UUID).  
That is the (tough) question.

In Spil, the name of an item becomes its unique ID.  
`hamlet/s/sq010/sh0010/layout/v012/p/mov` instead of `74fbd636–4fc5–11e9–91a2-ecb1d74481b4`.  

While this has an obvious advantage on readability and simplicity, it comes at a price.  
The biggest disadvantage is the locking of names. It becomes difficult to rename things.  
*(Example: if the sid is stored in a database, it gets complicated to rename an asset category)*.  
But we still believe the advantage is worth the price.  

It actually can have a beneficial effect on naming and data understanding.  
It is "Wyniwyg": What you name is what you get.

Please see also the blue sky tech blog on the subject:  
[medium.com/blue-sky-tech-blog/a-rose-by-any-other-name-4b569309b575](https://medium.com/blue-sky-tech-blog/a-rose-by-any-other-name-4b569309b575)  

**Note:** 
If Spil is used as a pure data abstraction layer, it is only a transient, non-permanent, data source.
In that case, name locking is not a limitation.


## My pipeline doesn't look like any other, all the names are different than in the Spil example codes...

The naming is fully configurable.
We are all-in for the famous [ubiquitous language](https://www.lullabot.com/articles/naming-content-types-using-ubiquitous-language).

For example, if your pipeline has episodes that you name "EP", and sequences are named "SEQ", 
they are integers, and all is uppercase, then your code will more look like:

```python
from spil import Sid

sid = Sid("HAMLET/S/010/0020")
print(sid.get("EP"))  # print the episode
```


## Usage seems simple, but configuration is a nightmare.

*“Simple things should be simple, complex things should be possible.”*  
(Alan Kay)  

Spil should be intuitive and simple to use.  
Complexity is hidden - but it's still there.

Clearly, efforts need to be put in tools assisting the configuration process, better documentation, more examples. etc.
In the meantime, please do not hesitate to get in touch at [spil@xeo.info](mailto:spil@xeo.info).


## The UI looks like an ugly thing from the 90's 

For Spil, **"The API is the first UI".**

The Qt GUI is just one simple example on how to use Spil's query mechanism.
It proofed its usability and versatility in production, is easy to deploy, and works in all major DCCs.

But one can do way better. 
We will welcome any proposal, idea, pull request or rewrite from scratch to make it look and feel nicer! :)


## Naming is completely free in my pipeline, there are no rules. Will Spil work ?

A string Sid, eg. `hamlet/s/sq010/sh0010` uses positional information and string patterns to infer the type.

The resolver uses rules to make templates match data types.
The tighter the rules, the better it can do so.

Let's consider these naming options for a "sequence":
- `sq010`: very tight rule (word `sq` followed by 3 digits), easy to match.
- `010`: tight rule (3 digits), easy to match
- `hamlet_and_skull`: freely named sequence, no rule. Difficult to match. 
  Can be matched thanks to the context, eg `hamlet/s/hamlet_and_skull/sh010`.
  But what about this search: `hamlet/*/hamlet_and_skull`? It may be an asset (which would still work).
  
With loose rules, the configuration becomes tricky. Some cases may not work out of the box.


## Who makes Spil ?

The Sid concept goes back to Studio100Animation in 2011.  
History page in the making.  
It was rewritten and open sourced in 2019, by [Michael Haussmann](https://github.com/MichaelHaussmann), [spil@xeo.info](mailto:spil@xeo.info).

