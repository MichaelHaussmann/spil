# Spil network deployment

Client / Server deployment of Spil is still experimental, and work in progress.

## Server side Spil

A fastapi powered Spil REST API is currently under development.

It allows access to the Crud interface via a rest api.
- /find/{config}/{sid}
- /get/{config}/{sid}
- /write/{config}/{sid}

## Client Side Spil

A FindInSpilRest Finder is also in development. 

It is able to consume the Spil rest API.
This Finder can replace any other finder, and be used without any change in the code.


## Client-Server

Spil can run both on client and server
With a server instance, serving the rest API.
And a client instance, consuming the rest API, for example used by the UI.

To make this happen clients and servers just need to use different configs.

Finders are interchangeable and connectable.
The spil_data_conf defines which Finder is used for which data type.

#### Connectable Finders

Some Finders call or use other Finders.
For example:
- FindInAll 
  Calls do_find on other finders, depending on a config.
- FindInCache 
  Caches the result of other Finders
- FindInSpilRest
  Calls the Spil Rest API, which in turn calls Finders.

