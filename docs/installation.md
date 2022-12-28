# Installation

## Prerequisites
- python 3.7

## pip

```shell
# Install latest release
$ pip install spil

# Or install latest version
$ pip install git+https://github.com/MichaelHaussmann/spil.git
```

To be able to use Spil, the configuration folder must be added to the python path.
Spil ships with an example configuration named `hamlet_conf`, including a demo *Hamlet* project.   
To try Spil, just add the `hamlet_conf` to the python path.


## rez package

You could either install using rez pip: 
```shell
# Install latest release
$ rez pip -i spil

# Or install latest version
$ rez pip -i git+https://github.com/MichaelHaussmann/spil.git
```
Or use the package.py file is contained in Spil.

It is recommended to create a distinct rez package for the configuration files, to be able to create evolving and potentially project dependent configurations.  
The config package could be versioned by current year, for example 2023.0.1


## Testing the install

You can test the installation with the shipped demo config `hamlet_conf`.

To do so:
- add the `hamlet_conf` folder to the python path
- open **spil_fs_conf.py** and edit the `project_root` entry to give a usable path on your system (will be written to).
- open **spil_fs_server_onf.py** and edit the `project_root` entry to give a usable path on your system (will be written to).
- run **save_examples_to_mock_fs.py**: this will create dummy project files and folders on disk

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

