# Installation

## Prerequisites
- python 3.7+

## Quick install Spil & Spil UI 

```shell
pip install spil_ui
```
This installs `spil_ui`, `spil`, and `spil_hamlet_conf`, the demo configuration.

A Qt package must be installed separately.  
Any [QtPy](https://github.com/spyder-ide/qtpy) compatible Qt version: PySide2, PySide6, PyQt5, or PyQt6.
```shell
pip install PySide2
```

To try it out, in python:
- generate test files inside `spil_hamlet_conf`
```python
import spil  # adds spil_hamlet_conf to the python path
import hamlet_scripts.save_examples_to_mock_fs as mfs
mfs.run()
```
- run  the UI
```python
from spil_ui import app
app()
```

### Running Spil UI inside a DCC 

From within a DCC, which is already running a QApplication Instance, run:
```python
from spil_ui import open_browser
open_browser()
```

## Install Spil without Spil UI

```shell
pip install spil
```
This installs `spil`, and `spil_hamlet_conf`, the demo configuration.

To try it out, in python:
- generate test files inside `spil_hamlet_conf`
```python
import spil  # adds spil_hamlet_conf to the python path
import hamlet_scripts.save_examples_to_mock_fs as mfs
mfs.run()
```

- try the API
```python
from spil import Sid

sid = Sid("hamlet/a/char/ophelia/model/v001/w/ma")
print(sid)   # should print "hamlet/a/char/ophelia/model/v001/w/ma"
print(sid.type)
print(sid.path())
print(sid.as_query())
```

- try the Finder on test files
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

## Notes

### Default configuration 

To be able to use Spil, a configuration must be added to the python path.    
Spil ships with an example configuration folder named `spil_hamlet_conf`.  
If no configuration is found, the `spil_hamlet_conf` folder is added to the python path during spil import.

It prints the message *"USING DEMO CONFIGURATION... ".*  
Once you add your configuration folder (or the demo configuration folder) to the pythonpath, this message will disappear.

Learn more at the [configuration documentation](configuration.md).



### Install latest from git repo

You can pip install from the git repo:

```shell
pip install git+https://github.com/MichaelHaussmann/spil.git
```

### Experimental plugins
 
The `spil_plugins` folder is currently only available when cloning the repository.
It is not production ready, and not shipped with the release.


### Server Side Install

Work in progress Docker and REST API.  
See [Spil network deployment](client_server.md)


