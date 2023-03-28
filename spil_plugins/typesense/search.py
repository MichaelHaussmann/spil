from pprint import pprint
from scripts.example_sids import sids as sidlist
from spil import FindInList
from spil_plugins.typesense.connect_ts import get_ts

search_parameters = {
  'q'         : 'hamlet sq010 anim',
  'query_by'  : 'text',
  'sort_by'   : 'length:asc',
  'per_page'  : 250,
  'page'      : 1
}

client = get_ts()
response = client.collections['all'].documents.search(search_parameters)
# pprint(response)

hits = response.get("hits")
found_ts = []
for hit in hits:
  found_ts.append(hit.get("document").get("sid"))

found_f = [str(s) for s in FindInList(sidlist).find("hamlet/s/sq010/*/anim/**")]

pprint(found_f)
pprint(found_ts)

diffs = set(found_f) ^ set(found_ts)
pprint(diffs)