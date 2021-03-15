
# Features

## Must

#### Multiple root paths 

- Different path per project

Currently all projects need to be under the same root path.
Workaround / Solution: use **rez** or another configuration manager to load the config files as needed, per project.
Nevertheless this workaround makes it impossible to work with multiple projects at the same time.

- Multiple paths per project

Currently, a project has a unique root path.
To allow data mounted on different roots (typically images, caches), a projects needs to have muliple root paths.


#### Optional fields

Currently all fields for a given type are mandatory.
Optional fields are necessary.
For example for asset variants, subtsasks, frames. 
See braket notation in the see SGTK implementation.
https://github.com/shotgunsoftware/tk-config-default/blob/master/core/templates.yml


## Should

#### Per project config

Sid configs are identical for all projects. It would be great to have different configs on different projects.
Drawback would be inter-project data exchange.

Workaround / Solution: use **rez** or another configuration manager to load the config files as needed.  


#### C++ Core
#### Optional fields



## Could 

- Create the config files from parsing an existing file structure 
- More Path inspired methods, like `with_name()`
(https://docs.python.org/3/library/pathlib.html#pathlib.PurePosixPath)


## Won't
