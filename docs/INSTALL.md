# Installation

Install via 
```
pip install spil
```


# Configuration

Spil needs a configuration.
An example configuration is shipped inside the `demo_conf` package.

There are 2 configuration files:

- `sid_conf.py`
Configures the sid itself. Maps the path-like Sid string to a data dictionary

- `fs_conf.py`
Configures the files. Maps the path to data dictionary. 


Once you start working with your own data, you will replace the demo_conf folder by a folder of your choice.
For SPIL to work, simply include this folder to your python path.

For a configuration to be recognized by Spil, both files must be in the python path, and named `sid_conf` and `fs_conf`.
*You can change these names by editing `spil/conf/sid_conf_load.py` and `spil/conf/fs_conf_load.py`*



#### Warning about the configuration

The configuration can be tricky, especially for complex cases.
There is currently a lack of documentation and tools to assist and ease the configuration.
Some complex use cases can probably not be achieved out of the box without changing Spil itself.

If ever you read this and are considering the use of Spil, please don't hesitate to contact us.
We will be glad to help. 


# Testing

Sid comes with a set of simple tests that can be run by pytest.

These tests are broad tests for the application, and are also useful to test the configuration.

Tests rely on 2 modules, that are part of the configuration
- `example_sids.py` 

A generator of dummy sids matching the configuration.

- `example_searches.py` 

A dictionary of searches to be tested.

When implementing your own configuration, it is advisable to also implement these test packages.
They allow testing your configuration.

**Note: The tests write folders and files to disk.**
 
 

#### Pytest and your custom Spil Configuration

Pytest uses its own python path.
The `demo_conf` is added to the python path (sys.path) inside of `tests/test_00_init.py`.

If you want to test your own configuration package, and if it is not in the pytest python path, you must edit the 
`SPIL_CONF_PATH` variable inside of `tests/test_00_init.py`.

Subsequent tests use `test_00_init`, so the path only needs to be set there.



