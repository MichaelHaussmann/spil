# Configuration

## Warning about the configuration

The configuration can be tricky, especially for complex cases.
There is currently a lack of documentation and tools to assist and ease the configuration.
Some complex use cases may not be achieved out of the box without augmenting Spil itself.

**If you read this and are considering the use of Spil, please don't hesitate to contact us.  
We will be glad to help.** 

*This documentation is work in progress.* 

## Configuration

Configuration is the tricky part of using Spil.

Two ideas to help you:

1. Use an existing configuration as a base.
2. Get in touch, we help you out.

## Basics

There are 3 main configuration files
- `spil_sid_conf`: containing the Sid templates
- `spil_fs_conf`: containing the path templates
- `spil_data_conf`: mappings for the "data access", configuring Finders, Getters, Writers.  

`spil_sid_conf` and `spil_data_conf` must be named as is, and be in the python path.
(see [installation](installation.md))

*(since Spil is for tech users, and for practical reasons, config files are in python rather than yaml).*

### spil_sid_conf

This files contains the templates for the Sid.
The Sid is an abstract representation of your pipeline, it describes the data you manipulate at a high level.

The typical sid pattern looks like this: 
```
'asset__file':            '{project}/{type:a}/{assettype}/{asset}/{task}/{version}/{state}/{ext}',
'shot__file':             '{project}/{type:s}/{sequence}/{shot}/{task}/{version}/{state}/{ext}',
```

Keys: 
- **project**: short project name
- **type**: broad type, eg "asset", "shot", "render", abreviated, eg. "a", "s", "r".
- **task**: a task instance or a task type (see below)
- **state**: a version's "state", eg. "work", "publish". Sometimes called "branch".
- **ext**: a file extension

Note: these "leaf types" will be automatically "extrapolated" to the intermediate types.

For example `asset__file` will be extrapolated to `asset__state`, `asset__version`, `asset__task`, etc.  
The last pattern(s) cannot be extrapolated, and need to be explicitely configured, typically:
```
'project':                 '{project}'
```

Besides the templates, this configuration file contains mappings and values that are included in the templates at runtime.

### spil_fs_conf

This files contain the path templates. It name is defined in `spil_data_conf` in `path_configs`.

For all templates that exist in `spil_sid_conf` and that have a path representation.

Example:
```
'asset__file':             '{@project_root}/{project}/PROD/{type:ASSETS}/{assettype}/{asset}/{task}/{version}/{assettype}_{asset}_{task}_{state}_{version}.{ext:scenes}',
'shot__file':              '{@project_root}/{project}/PROD/{type:SHOTS}/{sequence}/{sequence}_{shot}/{task}/{version}/{sequence}_{shot}_{task}_{state}_{version}.{ext:scenes}',
```
Note:  the intermediate types cannot be "extrapolated" automatically, and should be defined, if they have a path representation.
Besides the templates, this configuration file contains mappings and values that are included in the templates at runtime.


It is possible to use multiple file configurations, and to declare them in `spil_data_conf` in `path_configs`.
For secondary path configurations, it is easy to use the main config, and to override some elements.
Example:
```python
from spil_fs_conf import *  # 

path_templates = path_templates.copy()
path_templates['project_root'] = r'/home/mh/Desktop/SPIL_PROJECTS/SERVER/PRJ'  # only overriding this key 
```

### spil_data_conf

This files contains mappings and other configuration or the data access.
It configures Finders (FindInCaches, FindInFinders), Getters, and Writers.

*This chapter is work in progress. If you consider using Spil, get in touch, we help with the config.* 


## Start configuring

To start with, there are two options: 
- you configure Spil for usage in an existing pipeline 
- you create a pipeline from scratch

### Configuration for an existing pipeline

Don't forget these ideas to keep your life simple:
1. Use an existing configuration as a base.
2. Get in touch, we help you out.  

1. spil_sid_conf

This files contains the templates for the Sid.
The Sid is an abstract representation of your pipeline, it describes the data you manipulate at a high level.

The typical sid pattern looks like this: 
```
'asset__file':            '{project}/{type:a}/{assettype}/{asset}/{task}/{version}/{state}/{ext}',
'shot__file':             '{project}/{type:s}/{sequence}/{shot}/{task}/{version}/{state}/{ext}',
```

#### Some tips/questions to guide your configuration decisions:

- use the naming convention of your existing pipeline, eg `tasktype` or `step`? `asset_type` or `category`?
- use abbreviations if your naming convention contains some, eg `seq` for `sequence`
- by default use short, industry adopted, naming, eg "asset", "shot".
- keep one case for all, preferably lowercase (unless all significant data is uppercase)
- stick to singular (`prop` vs `props`) unless your naming convention states otherwise.  
- match the hierarchy of the filesystem (given the filesystem plays an important role in your system).
  Is `{version}` above `{state}` or vice-versa? Eg. `animation/work/v002` or `animation/v002/work`?
  (The latter is the typical cgwire config)
- Keep the sid config simple, but complete. 
  Do not cut out what you may need, but don't carry around invaluable fields. 
  Eg. Do you use `tasktype` (aka `step`) **and** `task`, or **only** `task`?
  Or `task` with **optional** `subtask`? (see the "kumquat" config example)
  Do you need an asset `variant` (for clothes, lods, etc.) or is it included in the asset name ?
- where possible use enforceable patterns.
  Examples: `sq010`, `v002` are easier to resolve than named sequences or just numbers.

2. spil_fs_conf

This files contain the path templates.
For all templates that exist in `spil_sid_conf` and that have a path representation.

### Testing the configuration with an existing file system
- Use **parse_sids_from_fs.py** to parse existing sids, and check if they get correctly parsed

## Configuration for a new pipeline

So, you are about to create a new pipeline ? :)

### Some tips/questions to guide your configuration decisions:
- build a strong naming convention with short, industry proven terms.
  Eg. use Shotgrid terminology, check out the [spil glossary](glossary.md#industry-naming-standards)
- define the data you need, and structure it in a hierarchy

        - new pipeline - choices
            - overall hierarchy definition and glossary
            - episodes or not ?
            - step / tasktype
            - named or numbered shots and sequences
            - state over version (cgwire)
            - publish/work version matching
            - push or pull updates (publish permalinks or explicit dependent version update)

(See also questions for an existing pipeline)


### Testing the configuration

- Create a **example_sids.py** script (as found in `hamlet_conf/scripts`) which generates correctly formatted test Sids.
- Run **save_examples_to_mock_fs.py**: this will create dummy project files and folders on disk


Don't forget, to keep your life simple:
1. Use an existing configuration as a base.
2. Get in touch, we help you out.  

## Creating a new type

### Create a new Config entry.

- First, we define the data in the `spil_sid_conf`.
- Then, we define it in `spil_fs_conf`.

### Testing a new config entry

- Checking the config
- Testing the Sids
- Testing the Finders

## Testing the configuration

### Checking the config

First, run basic config conformity checks.
- **spil_tests/config_checks/check_01_sid_config.py**: print the final sid templates and check for duplicates
- **spil_tests/config_checks/check_02_path_config.py**: print the final path templates and check for duplicates.
  Also checks if sid templates and path templates match.

### Testing the Sids

If the checks pass, you can continue to usage tests.

Complete tests are found in `hamlet_conf/tests`.

These tests use dummy Sids generated by `hamlet_conf/scripts/example_sids.py`
Create your own `example_sids`.
You may also use your parsed Sids.

#### Test scripts:
- **core_tests**: tests given Sids for core attributes (types, fields, parent(), etc.)
- **path_tests**: tests given Sids path resolving and path related attributes (path())


### Testing Data Access: DataSids, Finders, Getters, Writers

Basic Finder test to see if the path search works.
```python
from spil import FindInPaths as Finder

for sid in Finder().find('hamlet/a/char/*'):  # Use your own naming
    print(f"Found: {sid}")
```
This should print something like:
```
Found: hamlet/a/char/polonius
Found: hamlet/a/char/horatio
Found: hamlet/a/char/claudius
Found: hamlet/a/char/hamlet
Found: hamlet/a/char/ophelia
Found: hamlet/a/char/ghost
Found: hamlet/a/char/gertrude
```

#### Test scripts:
- **data_tests**: tests given Sids data access attributes (exists(), children(), get_last(), etc.)
- **finder_tests**: uses given Sids to build random search Sids, and tests Finders.
  Note that you could also create a python script with example / test searches.


## Advanced

The configuration files are loaded via `*_conf_load` modules in the `spil.conf` package.


### Pytest and your custom Spil Configuration

Pytest uses its own python path.
The `demo_conf` is added to the python path (sys.path) inside of `tests/test_00_init.py`.

If you want to test your own configuration package, and if it is not in the pytest python path, you must edit the 
`SPIL_CONF_PATH` variable inside of `tests/test_00_init.py`.

Subsequent tests use `test_00_init`, so the path only needs to be set there.


*This documentation is work in progress. Do not hesitate to get in touch if you are interested in using Spil.*