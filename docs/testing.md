# Testing

There are currently no automated tests.
*(They are planned and next on the todo list).*

There are tools to assist manual / exploratory testing.

## Unittest-like low level tests

- Low level functions have (or should have) a working `doctest`. 
- Modules usually have a `__main__` section with unittest-like code that log results.

## Configuration related tests

Most tools help test the configuration, and with it, Spil's functionality.

### Test tools

- `spil_tests/prep` contain modules to prepare test data
- `spil_tests/utils` contain modules for usage checks.
- `spil_tests/config_checks` contain configuration checks

### Tests in the configuration folder

Testing is closely related to the configuration.
The demo configuration contains test scripts, using `spil_tests` modules.

#### Prepare data

- Recreate or adapt the `hamlet_conf/scripts/example_sids.py` script, which generates correctly formatted test Sids.
- Run `hamlet_conf/scripts/save_examples_to_mock_fs.py`: this will create dummy project files and folders on disk (using the test Sids).

#### Checking the config

First, run basic config conformity checks.
- `spil_tests/config_checks/check_01_sid_config.py`: prints the processed **Sid** templates and checks for duplicates.
- `spil_tests/config_checks/check_02_path_config.py`: prints the processed **Path** templates and checks for duplicates.
  Also checks if sid templates and path templates match.

### Testing the Sids and Finders

If the checks pass, you can continue to usage tests.
Complete tests are found in `hamlet_conf/tests`.

- `hamlet_conf/tests/core_tests.py`: tests given Sids for **core attributes** (types, fields, parent(), etc.)
- `hamlet_conf/tests/path_tests.py`: tests given Sids **path resolving and path related attributes** (path())
- `hamlet_conf/tests/data_tests.py`: tests given Sids **data access attributes** (exists(), children(), get_last(), etc.)
- `hamlet_conf/tests/finder_tests.py`: uses given Sids to build random search Sids, and **tests Finders**.  
  Do not hesitate to adapt this test file, depending on the finders you will use.  
  *(Note that you could also manually create a python script with example / test searches)*.
- `hamlet_conf/tests/quicktest.py`: sandbox-like file to quickly test various things.



*This documentation is work in progress. Do not hesitate to get in touch if you are interested in using Spil.*

