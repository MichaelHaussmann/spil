from pprint import pprint
from spil_plugins.sg.connect_sg import get_sg

sg = get_sg()

#
schema = sg.schema_entity_read()
pprint(schema)

# detailed
schema = sg.schema_read()
for k, v in schema.get().items():
    print(k)
    pprint(v)
    input()      # input() is used to pause the output, because it is very long