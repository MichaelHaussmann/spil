# Configuration

## Warning about the configuration

The configuration can be tricky, especially for complex cases.
There is currently a lack of documentation and tools to assist and ease the configuration.
Some complex use cases may not be achieved out of the box without augmenting Spil itself.

**If you read this and are considering the use of Spil, please don't hesitate to contact us at [spil@xeo.info](mailto:spil@xeo.info).  
We will be glad to help.** 

*This documentation is work in progress.* 

## Configuration

Configuration is the tricky part of using Spil.

Best way to get started:

1. Use an existing configuration as a base.
2. Get in touch, we help you out.

## Included Demo configuration

To be able to use Spil, the configuration must be added to the python path.  
Spil ships with an example configuration folder named `hamlet_conf`, for a hypothetical *"hamlet"* project.

If no configuration is found, the `hamlet_conf` folder is added to the python path during spil import.

### Adapting the demo config 

The easiest way to start, is to adapt the existing config to your needs.

- Copy or move the `hamlet_conf` folder to a location of your choice, and add it to your python path.
- You can rename it. 
- The configuration files inside the folder, `spil_*_conf.py`,  must keep the same naming.

### Included config files

4 configuration files are included

- `spil_sid_conf`: 
  Contains the Sid templates. They are used to resolve the Sid string to the dictionary.
  Various configuration dictionaries are used to augment the initial templates.

- `spil_fs_conf`: containing 
  Contains the path templates. They are used to resolve the path string to the dictionary.
  Various dictionaries map between the Sid and the Path representation.

- `spil_fs_server_conf.py`: 
  An alternative path template configuration. 
  This file only shows how one can override an existing config.

- `spil_data_conf`: 
  Mappings for the "data access". 
  Used to define and configure Finders, Getters, Writers.
  (Not fully formalised).
  
### Included script files

3 script files are included

- `example_sids.py`
  This script generates Sids that are compatible with the configuration.
  Adapt the script to your configuration.

- `save_examples_to_file.py`
  Uses the generated example sids and writes them to a file.

- `save_examples_to_mock_fs.py`
  Uses the generated example sids and writes empty asset and shot files to disk.
  
### Included test files

Under `hamlet_conf/tests` are tests scripts, that test the functions of the Sid and the configuration.
While adapting the configuration, running the tests help detect problems.

See below, [Testing the configuration](configuration.md).

## Fundamentals

There are 3 main configuration files
- `spil_sid_conf`: containing the Sid templates
- `spil_fs_conf`: containing the path templates
- `spil_data_conf`: mappings for the "data access", configuring Finders, Getters, Writers.  

`spil_sid_conf` and `spil_data_conf` must be named as is, and be in the python path.

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

**Note that these keys are configurable and can be changed.**

Note: the "leaf types" will be automatically "extrapolated" to the intermediate types.

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
It configures Finders (FindInCaches, FindInAll), Getters, and Writers.

*This chapter is work in progress. If you consider using Spil, get in touch, we help with the config.* 


## Testing the configuration

- Recreate or adapt the `hamlet_conf/scripts/example_sids.py` script, which generates correctly formatted test Sids.
- Run `hamlet_conf/scripts/save_examples_to_mock_fs.py`: this will create dummy project files and folders on disk

### Checking the config

First, run basic config conformity checks.
- `spil_tests/config_checks/check_01_sid_config.py`: prints the processed Sid templates and checks for duplicates.
- `spil_tests/config_checks/check_02_path_config.py`: prints the processed Path templates and checks for duplicates.
  Also checks if sid templates and path templates match.

### Testing the Sids

If the checks pass, you can continue to usage tests.

For a first test, in python, type:
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

Complete tests are found in `hamlet_conf/tests`.

Read more here: [testing](testing.md).

*This documentation is work in progress. Do not hesitate to get in touch if you are interested in using Spil.*

