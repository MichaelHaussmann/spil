# Installation

## Prerequisites
- python 3.7+

## pip

```shell
# Install latest release
$ pip install spil

# Or install latest version
$ pip install git+https://github.com/MichaelHaussmann/spil.git
```
This installs `spil`, `spil_tests`, `spil_plugins`, and `hamlet_conf`, the demo configuration.

### Default configuration

To be able to use Spil, the configuration must be added to the python path.  
Spil ships with an example configuration folder named `hamlet_conf`.
If no configuration is found, the `hamlet_conf` folder is added to the python path during spil import.

Learn more at the [configuration documentation](configuration.md).

## rez package

Installation using rez pip: 
```shell
# Install latest release
$ rez pip -i spil

# Or install latest version
$ rez pip -i git+https://github.com/MichaelHaussmann/spil.git
```

It is recommended to create a distinct rez package for the configuration files, to be able to create evolving and potentially project dependent configurations.  
The config package could be versioned by current year, for example 2023.0.1

## Testing the install

Spil works out of the box with the shipped demo config `hamlet_conf`.

In python, type:
```python
from spil import Sid

sid = Sid("hamlet/a/char/ophelia/model/v001/w/ma")
print(sid)   # should print "hamlet/a/char/ophelia/model/v001/w/ma"
print(sid.type)
print(sid.path())
print(sid.as_uri())
```

### Test with FindInPaths

To play with the Finder and Sid paths, files need to exist on the file system.

To generate test files, run `hamlet_conf/scripts/save_examples_to_mock_fs.py`.
This will create dummy project files and folders on disk, inside the `hamlet_conf/data` folder.

From the installation folder type:
```shell
$ python hamlet_conf/scripts/save_examples_to_mock_fs.py 
```
*If you didn't configure Spil, it prints the location of the `hamlet_conf` path when you use it. For example when you `import spil`.*
*Make sure `spil` is in your python path, which should be the case after installation.*


Now in python try:
```python
from spil import FindInPaths as Finder

for sid in Finder().find('hamlet/a/char/*'):
    print(f"Found: {sid}")
```
This should print
```
Found: hamlet/a/char/polonius
Found: hamlet/a/char/horatio
Found: hamlet/a/char/claudius
Found: hamlet/a/char/hamlet
Found: hamlet/a/char/ophelia
Found: hamlet/a/char/ghost
Found: hamlet/a/char/gertrude
```

You are all set, and can experiment with Spil.

