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

op, fragments = doc.definitions[0], doc.definitions[1:]
fs = fragment_spread = op.selection_set.selections[0].selection_set.selections[3].selection_set.selections[0]

schema = op.selection_set.selections[0]


t_insp = type_introspection = parse("""query {
  __type(name: "ResPartner") {
    name
  }
}""").definitions[0]
t_field = t_insp.selection_set.selections[0]