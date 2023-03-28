"""
https://typesense.org/docs/0.24.0/api/collections.html#schema-parameters
"""
from spil_plugins.typesense.connect_ts import get_ts

# {project}/{type:s}/{sequence}/{shot}/{task}/{version}/{state}/{ext:scenes}',
# '{project}/{type:a}/{assettype}/{asset}/{task}/{version}/{state}/{ext:scenes}',

all_schema = {
  'name': 'all',
  'fields': [
    {'name': 'text', 'type': 'string'},
    {'name': 'project', 'type': 'string', 'facet': True},
    {'name': 'sid', 'type': 'string', 'sort': True},
    {'name': 'type', 'type': 'string', 'facet': True},
    {'name': 'length', 'type': 'int32', 'facet': True},
    {'name': 'task', 'type': 'string', 'optional': True},
    {'name': 'version', 'type': 'string', 'sort': True, 'optional': True},
    {'name': 'state', 'type': 'string', 'optional': True},
    {'name': 'ext', 'type': 'string', 'optional': True},
  ],
  'default_sorting_field': 'sid',
  # 'symbols_to_index': ["/"],
  # "token_separators": ["/"]
}

client = get_ts()
client.collections['shots'].delete()
client.collections.create(all_schema)
# client.collections.update(shots_schema)