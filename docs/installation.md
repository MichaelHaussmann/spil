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

You can test the installation with the shipped demo config `hamlet_conf`.

In python, type
```python
from spil import Sid

sid = Sid("hamlet/a/char/ophelia/model/v001/w/ma")
print(sid)   # should print "hamlet/a/char/ophelia/model/v001/w/ma"
print(sid.type)
print(sid.path())
print(sid.as_uri())
```

### Test with FindInPaths

To play with the Finder and Sid paths, run **hamlet_conf/scripts/save_examples_to_mock_fs.py**.
This will create dummy project files and folders on disk, inside the `hamlet_conf/data` folder.

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

From here you can experiment with Spil.

## Install Spil_ui

**Spil UI** is a Qt User interface to browse Sids and launch actions.

[![Spil Qt UI](img/spil_ui.png)](https://github.com/MichaelHaussmann/spil_ui)
 
spil_ui is a separate repository (in the process of being open sourced and released).   