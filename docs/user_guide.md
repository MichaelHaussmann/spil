
# User Guide

This guide is for TDs and technical artists who want to use Spil.  

The guide to modify spil is here [developer guide](dev_guide.md).  
See also the [glossay](glossary.md).

## Introduction to the Sid

The "**Sid**" - for "Scene Identifier" - is a human-readable, hierarchical, path-like unique identifier for every entity or file of a CG production pipeline.    
An intuitive API is built around this identifier, including glob-like query, CRUD data access and path resolving.  

In practice, it is an immutable string, looking like a path, and representing hierarchical data.

Examples (for a movie called "hamlet"):
```
"hamlet/s/sq030/sh0100/anim"
"hamlet/s/sq030/sh0100/render"
"hamlet/s/sq030/sh0100"
"hamlet/a/char/ophelia/model/v001/w/ma"
"hamlet/a/char"
"hamlet"
```

At creation time, the string is "resolved", matched against configurated templates.
(Resolving done by [resolva](https://github.com/MichaelHaussmann/resolva))

If the resolve succeeds, it defines the Sids type, and store its data in a dictionary.
Finally, a Sid contains 3 values.

1) A string
This is the bare minimum for a Sid to exist. By default it is an empty string.

2) A dictionary
If the string matches a defined pattern, the fields dictionary is filled.

3) A type
The matching pattern gives the Sid its type.
The type is of form basetype__keytype.

Examples:
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

For more about Sid types, please check out the [glossary](glossary.md).  

If the Sid contains search characters (eg. *, **, <, >) it is considered a "search Sid".  
A Search Sid can be typed or not, or can resolve to multiple types.
```
"hamlet/s/sq030/*"  # is typed: shot__shot
"hamlet/s/sq030/**"  # will resolve to multiple types, because of the recursive "**"
```
(See more on searches below).


## API Usage examples

Sid creation and manipulation

```python
from spil import Sid

# create a Sid from scratch
task = Sid("hamlet/s/sq030/sh0010/render")
# a task sid: hamlet/s/sq030/sh0010/render

# create a Sid by changing values
anim_task = task.get_with(task="anim")          
# task sid: hamlet/s/sq030/sh0010/anim 

# create a Sid from a Sids hierarchy 
sequence = task.get_as('sequence')              
# sequence sid: hamlet/s/sq030

# another way
shot = task.parent                              
# shot sid: hamlet/s/sq030/sh0010 
```

Parts of the Sid's API are inspired by the pathlib
https://www.python.org/dev/peps/pep-0428

```python
from spil import Sid
shot = Sid("hamlet") / "s" / "sq030" / "sh0010"
```

Creation with a Query or dictionary
```python
from spil import Sid
seq = Sid(query="project=hamlet&type=s&sequence=sq010")  # query        
seq = Sid(fields={'project': 'hamlet', 'type': 's', 'sequence': 'sq010'})  # dict
```

A Sid is immutable. Methods returning Sids support method chaining.
```python
from spil import Sid
s = (Sid()
     .get_with(project="hamlet", type="s")
     .get_with(query="sequence=sq010&shot=sh0010&task=anim")
     .get_as('project'))
print(s)  
```
*(Note that this chain doesn't make any sense, since the Sid is just "hamlet" in the end...)*


Access data about the Sid: by key, as a complete dictionary, as string or Query.
```python
from spil import Sid 
shot = Sid("hamlet/s/sq030/sh0010")

# get a field of the sid by key
shot.get("sequence")   
# sq030

# as a dictionary
shot.fields            
#  { 'project': 'hamlet', 'type': 's', 'sequence': 'sq030', 'shot': 'sh0010' }

# as a Query
shot.as_query()          
# "project=hamlet&type=s&seq=sq030&shot=sh0010"

# "uri": type and string
shot.uri        
# "shot__shot:hamlet/s/sq030/sh0010" 
```

### Path Resolver

The Sid can be resolved to and from paths.  
Multiple configurations can co-exist.  
For example "local", "server", "linux", etc. paths.    

```python
from spil import Sid

# creating a Sid from path
scene = Sid(path="/projects/hamlet/chars/ophelia/modeling/v002/publish/ophelia_model.mb")

print(scene)            
# "hamlet/a/chars/ophelia/modeling/v002/p/mb"

# returning default path
path = scene.path()     
# "/projects/hamlet/chars/ophelia/modeling/v002/publish/ophelia_model.mb"

# returning path from "server" configuration
path = scene.path("server")     
# "/server/projects/hamlet/chars/ophelia/modeling/v002/publish/ophelia_model.mb"
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
if scene:  # A sid that is not resolvable (not conform), has not type, and evaluates to False.
    print(scene.get('project'))  # hamlet
    print(scene.get('version'))  # "v002"
else:
    print("opened scene is not a pipeline scene")
```

### Data access and Pipeline workflows

Sid wraps common requests, that are internally delegated to configurable data sources (Getters and Writers).

```python
from spil import Sid
task_sid = Sid("hamlet/s/sq030/sh0010/layout") 

task_sid.exists()                 # True
version_sid = task_sid.get_last('version')      # "hamlet/s/sq030/sh0010/layout/v003"
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

## Finding Sids

It is possible to query Sids using a glob-like syntax.

Operators:
- \*   : star search
- **  : recursive star search
- \>   : last
- \,   : "or"  
- configurable aliases ("movie" -> "mov,avi,mp4", "maya" -> "ma,mb") 

### Search Examples

- "All the Shots of sequence sq030" ?
```
"hamlet/s/sq030/*"
```

- "All the published maya files of Ophelias modeling" ?
```
"hamlet/a/chars/ophelia/model/*/p/maya"
```

- "Last published render movies for the project hamlet" ?
```
"hamlet/s/**/render/>/p/movie"
```

- "All cache files for hamlet's sequence 30, shot 10" ?
```
"hamlet/s/sq030/sh010/**/cache"
```

### Query in search 

Query Syntax can be used to add search filters on yet untyped searches

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
- **FindInAll**: to search other Finders, depending on a configuration
- **FindInShotgrid**: to search Shotgrid

Finders implement `find()`, `do_find()` find_one()` and `exists()`.

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
  
The `FindInShotgrid` is an example Finder implementation.  
It may need to be adapted, depending on the production's Shotgrid usage.    

*This page is work in progress.* 
