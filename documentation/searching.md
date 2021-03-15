
# --- working draft --- 

- define a search syntax: compact, intuitive, comprehensive, precise (unambiguos), unified (whereever and however we search) for users / techies / computers (protocols) alike

- syntax helpers such as expanders ('**'), extension aliases ('img' -> 'exr, jpg, png')

- search single sid out of list
- search list out of list
- sort list
- group by

- delegate where we search (list, fs, sg, ftrack, cgwire)
- delegate how we sort (string, workflow, date)

- potential multi-step (cgwire -> list -> search) - including caching mechanism

Note that it is quite simple to do object oriented queries by example, given the dictionary nature of the search data.

1) Proof of concept implementation : the list search.

Examples :

'demo/s/s010/*' ->
'from shot select * where sequence = s010 and project = demo'

'demo/s/s010/**/p/ma' ->  'demo/s/s010/*/*/*/*/p/ma' ->
'from file select * where ... '

list search problem :
"we want all the shots from s010 that have maya files"
# would be

'demo/s/s010/**/ma' -> would return a list of all ma files -> would filter out the shots
syntax proposal :

'demo/s/s010/?/**/ma' -> return a list of shot sids that match the pattern.
(database "DISTINCT")
select distinct shot from x where type=s, project=demo, sequence=s010, ext=ma

this would be a rather rare request, from people who know how to formulate it, or from a browser.

'demo/s/?/?/**/ma' -> returns a list with sequence sids, then shots sids, that match the pattern.

The browser would show the general request in the bar, eg:
demo/s/s010/**/ma <- typed, and expanded to the types length
and internally for each column it would use:
demo/s/s010/?/*/*/*/*/*/ma
demo/s/s010/*/?/*/*/*/*/ma
demo/s/s010/*/*/?/*/*/*/ma

This type of result would come from a two pass search: 1) all matching, 2) distinct sids as given type

By default the returned type is the one of the given search, eg:

demo/s/s010/* -> returns shots
demo/s/s010/*/*/*/*/*/*/ma returns files

so demo/s/s010/* and demo/s/s010/? are equal.


Feature list, with tests and examples, in order of implementation.


IMPORTANT:  Clarify Sid vocabulary (type, key, last, etc)
Sid borrows concepts/vocabulary from:
Path (pathlib)
Dict
List

Example:
'image__2d_layer_file'
'image__2d_version'
'cache',
'project'


2) one or more /?/ (question marks), with or without stars.
Finds sids, returning the types specified by the ?
qm_search, uses base search.
Examples:

search_sid = 'pipe/i/s010/*/?/*/*/p/ma'  # the tasks of all shots of sequence s010 that have a published maya file
search_sid = 'pipe/i/s010/?/05_render/*/*/p'  # the shots of sequence s010 that have a published render

To integrate.


3) last / first & grouped by last/first.
Using 1) and 2) but adds sorting and grouping
^ means last, . means first

Examples:
search_sid = 'demo/s/s010/^'  # last shot of sequence s010
search_sid = 'demo/s/s010/*/^'  # last task for all shots of sequence s010
search_sid = 'demo/s/s010/p010/01_layout/*/^/p/mov'  # movie file for last published version of layout
search_sid = 'demo/s/s010/*/^/*/^/p/mov'  # movie file for last published version of last task for all shots in s010

TODO:
- smart sort (by key, using special function, and by delegation (todo later)
- proper support for multiples signs, including smart sort
- add support for "first" : "."
- more stable tests


4) including operators
expand, or, aliases

5) plug to simple Browser, with Sid in bar.



Misc:
https://patents.google.com/patent/US20140279976
https://forums.pyblish.com/t/folder-structure-resolver/82/47
- Function signatures with positional arguments
https://gitlab.com/xiancg/lucidity/tree/Python37
Use case :
What alembics do we have for this sequence ?
Will help find caches even if they are not yet from published files 
History page & Who Uses it ?

