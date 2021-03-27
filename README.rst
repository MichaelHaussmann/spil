spil
====

The Simple Pipeline Lib

A Simple library for CG Pipelines, built around the "**Sid**\ ".

The goal of SPIL is to provide a simple, universal, hierarchical,
human-readable and unique identifier for every entity or file of a CG
production pipeline.

This identifier is called the "**Sid**\ " - for "Scene Identifier", or
simply "String ID".

Unique Identifier
~~~~~~~~~~~~~~~~~

SPIL considers entities of a CG pipeline as being nodes of a hierarchy.
Each node has a unique path, which is the entitie's unique identifier,
the "Sid".

Examples :

-  Sid of sequence 30 shot 10 in the project "Hamlet":

    "hamlet/s/sq030/sh0010"

-  Sid for the maya mb file of character Ophelia's modeling, published
   version v002:

    "hamlet/a/chars/ophelia/modeling/v002/p/mb"

A Dictionary with a type
------------------------

As it's core, the Sid is simply a dictionary associated to a type.

Some examples:

- type ``shot__task`` :

    {   'project': 'hamlet', 'type': 's', 'sequence': 'sq030', 'shot': 'sh0010', 'task': 'animation' }

-  type ``shot__sequence`` :

   { 'project': 'hamlet', 'type': 's', 'sequence': 'sq020' }

-  type ``asset__version`` :

   { 'project': 'hamlet', 'type': 'a', 'cat': 'props', 'name': 'skull', 'task': 'modeling', 'version': 'v008' }


Simple API
~~~~~~~~~~

Spil offers a simple API to work with Sids.

::

    current_shot = Sid("hamlet/s/sq030/sh0010") 
    current_shot.get("project")                 # "hamlet" 
    current_shot.get_as("sequence")             # "hamlet/s/sq030" 
    current_shot.get_with(task="animation")     # "hamlet/s/sq030/sh0010/animation"  
    current_shot.data                           #  { 'project': 'hamlet', 'type': 's', 'sequence': 'sq030', 'shot': 'sh0010' }

| Since the types make sense in a pipeline, Sids can be sorted.
| For example, "animation" comes before "render", and "v002" before "v005".

    "hamlet/s/sq030/sh0010/animation" < "hamlet/s/sq030/sh0010/render" < "hamlet/s/sq030/sh0010/comp"


Resolver to and from datasources - versatile middleware
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Sid can be translated to and from different data sources.

-  For example a file system:

   ::

       current_file = Sid(path="/projects/hamlet/chars/ophelia/modeling/v002/publish/ophelia_model.mb")
       print( current_file )       # "hamlet/a/chars/ophelia/modeling/v002/p/mb"
       current_file.path           # "/projects/hamlet/chars/ophelia/modeling/v002/publish/ophelia_model.mb"

-  Example in a maya scene file:

   ::

       current = Sid(path=pm.sceneName())
       current.get('version')                # "v002"


-  The Sid could be resolved from an ftrack "link" string, or a cgwire
   json, or any datasource, after implementation of a mapping or
   translation.

This makes the Sid a versatile data source abstraction layer.


Database Identifier
~~~~~~~~~~~~~~~~~~~

If the Sid is planned into the pipeline, it is a handy database field.

-  SQL Query example

   ::

       SELECT * FROM Entities WHERE sid = "hamlet/a/chars/ophelia"

-  Shotgun query example

   ::

       sg.find('Shot', 
               ['sg_sid', 'is', 'hamlet/s/sq030/sh0010'],
               ['code', 'sg_sid', 'sg_cut_in', 'sg_cut_out', 'sg_ep_in',
               'sg_ep_out', 'sg_editing_status'])

Intuitive Search Syntax
~~~~~~~~~~~~~~~~~~~~~~~

Building on top of these ideas, and considering the Sid as a middleware,
it can be used as a simple, intuitive, and unified search syntax.

-  "All the Shots of sequence sq030" ?

   ::

       "hamlet/s/sq030/*"

   Finds:

   ::

       "hamlet/s/sq030/sh0010"
       "hamlet/s/sq030/sh0020"
       "hamlet/s/sq030/sh0030"

-  "All the published maya files of Ophelias modeling" ?

   ::

       "hamlet/a/chars/ophelia/modeling/*/p/mb"

   Finds:

   ::

       "hamlet/a/chars/ophelia/modeling/v001/p/mb"
       "hamlet/a/chars/ophelia/modeling/v004/p/mb"

Flexible and configurable
~~~~~~~~~~~~~~~~~~~~~~~~~

| The Sid is based on the `Lucidity <https://gitlab.com/4degrees/lucidity/>`__ resolver, and isconfigurable.
| It can easily integrate and connect onto existing pipelines.

Sid config example:

::

    ('asset__file',            '{project}/{type:a}/{cat}/{name}/{variant}/{task}/{version}/{state}/{ext:scenes}'),
    ('asset__movie_file',      '{project}/{type:a}/{cat}/{name}/{variant}/{task}/{version}/{state}/{ext:movies}'),

File config example:

::

    ('asset__file',             r'{@project_root}/scenes/{type:01_assets}/{cat_long}/{name}/{variant}/{task}/{state}_{version}/{name}.{ext:scenes}'),
    ('asset__movie_file',       r'{@project_root}/movies/{type:01_assets}/{cat_long}/{name}/{variant}/{task}/{state}_{version}/{name}.{ext:movies}'),

Tested in Python 2.7 and 3.6

Concepts
~~~~~~~~

The Sid builds upon general concepts, as well as production proven CG
pipeline concepts.

General concepts

-  | Unique Identifier - Human readable Identifier - "Natural Key"
   | https://dzone.com/articles/7-strategies-for-assigning-ids-to-microservices
   | https://medium.com/blue-sky-tech-blog/a-rose-by-any-other-name-4b569309b575

-  | File sytem path
   | https://www.python.org/dev/peps/pep-0428

-  URI / URL
-  Node tree & hierarchy

Pipeline concepts

-  | Unique Identifier & Resource Locator
   | Examples: SPREF (Sony Pictures), or the Pipeline Resource Identifier - PRI (Blue Sky)
   | https://medium.com/blue-sky-tech-blog/conduit-pipeline-resource-identifiers-4432776da6ab

-  | Resource description and "Context" (Shotgun Toolkit)
   | https://developer.shotgunsoftware.com/tk-core/core.html#context

-  | Template based path resolving
   | As implemented in Shotgun Toolkit:
   | https://github.com/shotgunsoftware/tk-config-default/blob/master/core/templates.yml
   | Or in Ftrack: https://gitlab.com/4degrees/lucidity/

-  | Asset Resolution - ArResolver - in USD
   | https://graphics.pixar.com/usd/docs/668045551.html#AssetResolution(Ar)2.0-AddURIResolvers

-  | The Sid itself
   | The Sid has been used in general and fx pipelines for over 10 years, in various forms and at various degrees.

Philosophy
~~~~~~~~~~

Spil aims to be : flexible, pragmatic, simple - and reliable.

-  | flexible
   | Spil can be plugged to existing pipelines. It easily blends in, to be used only where it is needed.
   | It can also be planned at a pipelines core - and be a central part of it.

-  | pragmatic
   | It all starts as files. So does Spil.
   | YAGNI meets WYSIWYG.

-  | simple
   | One of the ideas of Spil is to build upon implicit information, to simplify how we see our datas.
   | For example, it is obvious that "hamlet/a/chars" is an asset category, and "hamlet/a/chars/ophelia/modeling" is a modeling task.
   | The Sid's string representation is a dictionary where the keys are implicit. Intuitive for the human user.

-  | reliable
   | This part is yet to prove.
   | "In the face of ambiguity, refuse the temptation to guess."
   | But who are you to have read this far anyway?

Main limitations
~~~~~~~~~~~~~~~~

-  | Alpha stage
   | The core concepts have been around for a while, and different versions of the Sid are and have been used in production pipelines for some time now.
   | But this version of "Spil" is a complete rewrite, which is still in Alpha stage.
   | Rollouts in production are planned, but many parts of this code are still Proof-of-Concept stage.
   | It lacks basic code testing and profiling tools.

-  | The configuration is tricky
   | For complex projects, creating the config is not simple, and is lacking tools to help. Sometimes, the configuration can create overlapping types, and errors that can go undetected and are hard to find.

-  Complex configurations do not work out of the box

-  | Needs optimisation
   | Core parts will need a C++ implementation.

Plans and ongoing development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| The priority is to make the current feature set more robust and efficient.
| Adding tests and documentation. Optimization through generators, caches, better algorithms.

Then, implement some important but missing core features and
enhancements - add support for file sequences (integration of pyseq or
fileseq, or similar) - allow optional fields in the config (as the
bracket syntax in SGTK yaml) - move the config to a universal format
(yaml) - adding a C++ implementation to make the resolve faster - tools
to help create and verify the configuration files

To take profit from the Sids universality, we then plan on building
reusable open source bricks and pipeline tools.

| For example: - simple and universal file browser UI - connectors to Shotgun and Relational Databases - using the sid as a USD Asset Resolver - protocol for pipeline actions
| For example ``sid://play?hamlet/s/sq030/*/^/^/p/movie`` - file system style navigation and context handling
| For example ``cd hamlet/s/sq010``

Yeah, and we need a logo and a quickstart video...

Interested ?
~~~~~~~~~~~~

We'd love to hear from you.
