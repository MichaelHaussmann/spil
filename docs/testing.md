# Testing

## Automated tests

Spil uses pytest.

The *Auto Test* (auto_test.yml) github action runs all tests, including doc-tests, on windows and ubuntu.

Pytest is configured in `pyproject.toml` and a `conftest.py` file.
On session start, Pytest runs test file creations (inside the `spil_hamlet_conf/data/testing` folder).

The Action is triggered by push or pull-request on main branch.


## Unit Tests

Most of the low level functions have `doctest` unittests.  

Modules usually have a `__main__` section with unittest-like code that log results.   
These modules can be run directly from a code editor.

## Integration Tests - Data tests

Most tests work in conjunction with the configuration.
Per default, they use the shipped demo configuration `spil_hamlet_conf`.

On session start, Pytest runs file creations (inside the `spil_hamlet_conf/data/testing` folder).
These files are used by the tests (including doctests).

When creating a new configuration for a pipeline, it is recommended to implement related tests.
The best is to reuse the tests shipped with the example configuration.

### Checking the config

When creating a new config, these basic config conformity checks are useful: 
- `spil/tests/config_checks/check_01_sid_config.py`: prints the processed **Sid** templates and checks for duplicates.
- `spil/tests/config_checks/check_02_path_config.py`: prints the processed **Path** templates and checks for duplicates.  
  Also checks if sid templates and path templates match.


### Test data preparation

For in-depth tests and greater test coverage, it is useful to prepare static data for repeatable tests.
 
- Recreate or adapt the `spil_hamlet_conf/hamlet_scripts/generate_example_sids.py` script, which generates correctly formatted test Sids.
- Save the example sids into a file using `spil_hamlet_conf/hamlet_scripts/save_examples_to_file.py`
- Run `spil_hamlet_conf/hamlet_scripts/save_examples_to_mock_fs.py`: this will create dummy project files and folders on disk (using the test Sids).

In python:
```python
import spil  # adds spil_hamlet_conf to the python path
import hamlet_scripts.save_examples_to_mock_fs as mfs
mfs.run()
```

This is configured in `conftest.py` file.

### Testing the Sids and Finders

If the basic config checks pass, and there is testable data, we can continue to usage tests.  
Complete tests are found in `spil_hamlet_conf/hamlet_tests`.

- `spil_hamlet_conf/hamlet_tests/core_test.py`: tests given Sids for **core attributes** (types, fields, parent(), etc.)
- `spil_hamlet_conf/hamlet_tests/path_test.py`: tests given Sids **path resolving and path related attributes** (path())
- `spil_hamlet_conf/hamlet_tests/data_test.py`: tests given Sids **data access attributes** (exists(), children(), get_last(), etc.)
- `spil_hamlet_conf/hamlet_tests/finder_test.py`: uses given Sids to build random search Sids, and **tests Finders**.  
  Do not hesitate to adapt this test file, depending on the finders you will use.  
  *(Note that you could also manually create a python script with example / test searches)*.
- `spil_hamlet_conf/hamlet_tests/quicktest.py`: sandbox-like file to quickly test various things.

*(more tests work in progress)*

### Test tools

- `spil/tests/prep` contain modules to prepare test data
- `spil/tests/utils` contain modules for usage checks.
- `spil/tests/config_checks` contain configuration checks


*This documentation is work in progress. Do not hesitate to get in touch if you are interested in using Spil.*

