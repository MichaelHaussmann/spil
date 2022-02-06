### Configuration

See config.md

### Create a Sid / Get a Sid

Creating a Sid with a Sid string 

```
a_shot = Sid('roju/s/sq0010/sh0020')
```

Creating a Sid with a path
```
path = "/prods/romeo_juliette/assets/chars/romeo/3d/modeling/works/romeo_v001.ma"
romeo_file = Sid(path=path)
```

### Modify a Sid

Get with
```
Sid('roju/s/sq0030/sh0100/animation').get_with(task='rendering')
```
returns `Sid('roju/s/sq0030/sh0100/rendering')`

### Use a Sid


### Search for Sids




### Match Sids