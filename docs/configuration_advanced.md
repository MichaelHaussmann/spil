# Advanced Configuration 

## Warning about the configuration

The configuration can be tricky, especially for complex cases.
There is currently a lack of documentation and tools to assist and ease the configuration.
Some complex use cases may not be achieved out of the box without augmenting Spil itself.

**If you read this and are considering the use of Spil, please don't hesitate to contact us at [spil@xeo.info](mailto:spil@xeo.info).  
We will be glad to help.** 

*This documentation is work in progress.* 

## Configuring from scratch

To start with, there are two options: 
- you configure Spil for usage in an existing pipeline 
- you create a new pipeline

### Configuration for an existing pipeline

1. spil_sid_conf

This files contains the templates for the Sid.
The Sid is an abstract representation of your pipeline, it describes the data you manipulate at a high level.

The typical sid pattern looks like this: 
```
'asset__file':            '{project}/{type:a}/{assettype}/{asset}/{task}/{version}/{state}/{ext}',
'shot__file':             '{project}/{type:s}/{sequence}/{shot}/{task}/{version}/{state}/{ext}',
```

#### Some tips/questions to guide your configuration decisions:

- use the naming convention of your existing pipeline, 
  eg `tasktype` or `step`? `asset_type` or `category`?  
- use abbreviations if your naming convention contains some, eg `seq` for `sequence`  
- by default use short, industry adopted, naming, eg "asset", "shot", "task", "version"
- keep one case for all, preferably lowercase
- stick to singular (`prop` vs `props`) unless your naming convention states otherwise.  
- match the hierarchy of the filesystem (given the filesystem plays an important role in your system).
  Is `{version}` above `{state}` or vice-versa? Eg. `animation/work/v002` or `animation/v002/work`?
  (The latter is the typical cgwire config)
- Keep the sid config simple, but complete. 
  Do not cut out what you may need, but don't carry around invaluable fields. 
  Eg. Do you use `tasktype` (aka `step`) **and** `task`, or **only** `task`?
  Or `task` with **optional** `subtask`? (see the "kumquat" config example)
  Do you need an asset `variant` (for clothes, lods, etc.) or is it included in the asset name ?
- whenever possible, use enforceable patterns.
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
  Eg. use Shotgrid terminology, check out the [spil glossary](glossary.md)
- define the data you need, and structure it in a hierarchy

        - new pipeline - choices
            - overall hierarchy definition and glossary
            - episodes or not ?
            - step / tasktype
            - named or numbered shots and sequences
            - state over version (cgwire)
            - publish/work version matching
            - push or pull updates ? (publish permalinks, eg. a "valid version" or explicit dependent version update)

(See also questions for an existing pipeline)


### Testing the configuration

- Create or adapt the **generate_example_sids.py** script (as found in `spil_hamlet_conf/hamlet_scripts`) which generates correctly formatted test Sids.
- Run **save_examples_to_mock_fs.py**: this will create dummy project files and folders on disk


## Creating a new type

### Create a new Config entry.

- First, we define the data in the `spil_sid_conf`.
- Then, we define it in `spil_fs_conf`.

### Testing a new config entry

- Checking the config
- Testing the Sids
- Testing the Finders

Check out: [Testing the configuration](testing.md). 

*This documentation is work in progress. Do not hesitate to get in touch if you are interested in using Spil.*