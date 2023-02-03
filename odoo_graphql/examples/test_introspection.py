# https://github.com/graphql-python/graphql-core
from graphql import parse
from graphql.language.ast import (
    VariableNode,
    ValueNode,
    ObjectValueNode,
    ListValueNode,
    IntValueNode,
    FloatValueNode,
    FragmentSpreadNode,
)

import json

# print node
def pn(node):
    print(json.dumps(node.to_dict(), indent=4))

with open("graphiql_query.gql") as f:
    doc = parse(f.read())

n = doc.definitions[0]  # normal node
fs = fragment_spread = n.selection_set.selections[0].selection_set.selections[3].selection_set.selections[0]