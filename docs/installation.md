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
This installs `spil`, and `spil_hamlet_conf`, the demo configuration.

The `spil_plugins` folder is currently only available when cloning the repository.
It is not production ready, and not shipped with the release.


### Default configuration

To be able to use Spil, the configuration must be added to the python path.  
Spil ships with an example configuration folder named `spil_hamlet_conf`.
If no configuration is found, the `spil_hamlet_conf` folder is added to the python path during spil import.

*If you didn't configure Spil, it prints the message "USING DEMO CONFIGURATION... ".*
*Once you add your configuration folder (or the demo configuration folder) to the pythonpath, this message will disappear.*

Learn more at the [configuration documentation](configuration.md).

## Testing the install

Spil works out of the box with the shipped demo config `spil_hamlet_conf`.

In python, type:
```python
from spil import Sid

sid = Sid("hamlet/a/char/ophelia/model/v001/w/ma")
print(sid)   # should print "hamlet/a/char/ophelia/model/v001/w/ma"
print(sid.type)
print(sid.path())
print(sid.as_query())
```

### Test with FindInPaths

To play with the Finder and Sid paths, files need to exist on the file system.

To generate test files, in python:
```python
import spil  # adds spil_hamlet_conf to the python path
import hamlet_scripts.save_examples_to_mock_fs as mfs
mfs.run()
```
This will create dummy project files and folders on disk, inside the `spil_hamlet_conf/data/testing` folder.

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

