
# Faster Spil

The goal is to speed Spil up. 
What can there be done ?

## Resolver

The core of Spil is the resolver, from Sid string to dict, and from path strings to dicts (and vice-versa).
These are not IO bound operations, but CPU operations (mainly regular expression pattern matching).
Async will not be of any help.

### Options

- core implementation in a faster language (C++, rust)
  High price to pay: development, platform specific binary management.
- Implementing in Cython.
  Not trivial to obtain a performance gain 
  (http://romankleiner.blogspot.com/2015/06/cython-and-regular-expressions.html)
- Internal usage of Googles RE2 regex engine
  https://github.com/andreasvc/pyre2
  Quick simple tests showed no improvement over standard re package.
- memory caching

### Memory Caching
Memory caching was implemented in the new [resolva](https://github.com/MichaelHaussmann/resolva) resolver.  
Regex compiles are kept in memory (Resolver instance cache) and resolves are memoize.  
The previous resolver lib (Lucidity) was used without any caching, so regex compiles would occur very often.
(this was not a Lucidity problem, but a usage problem).  
Since update, Sid instantiation performance is up x3 to x30.


## Finders 

### FindInPaths

This is the most used Finder, which looks up file systems using glob.

(Example of async-wrapping-sync approach: https://github.com/Tinche/aiofiles/blob/main/src/aiofiles/os.py)

#### Attempts to use asyncio versions
Tests show no performance gain with aiopath and anyio glob implementations (to the contrary, they are both way slower than the python default glob, in our tests).
See *globbing* folder for scripts.


### Notes

- A "hamlet" Sid string is approx. 40 characters long, so weights ~40 bytes
- Measure the weight of the Sid in memory ?
  https://code.activestate.com/recipes/577504/



