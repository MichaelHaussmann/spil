


# Spil Glossary

Most of Spils API is self explanatory.
Nevertheless, a bit of share vocabulary helps.


### Sid


### Type
As it's core, the Sid is a dictionary associated to a type.
The type is the key of the mapping template.
It is composed of a "basetype" and a "subtype"

Examples: 
`shot__file`, `shot__task`, `asset__version`

### Basetype

The basetype is the first part of the type.  
Example:  
for type `shot__file` --> basetype = `shot` 
```
>>> Sid('roju/s/sq0030/sh0100/animation').basetype
"shot"
```
### keytype


### Extrapolate

From an iterable containing leaf node paths, extrapolates all the subnode paths.

This is useful when the data source quickly provides leaves only, but we want to find child data.

Example: 

The path 
```
"TEST/A/CHR/HERO/MOD/V001/W/avi"
```  
will generate:
```
"TEST/A/CHR/HERO/MOD/V001/W", 
"TEST/A/CHR/HERO/MOD/V001", 
"TEST/A/CHR/HERO/MOD",
"TEST/A/CHR/HERO",
"TEST/A/CHR",
"TEST/A",
"TEST"
```