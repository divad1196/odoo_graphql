# https://graphql.org/learn/introspection/
# https://docs.cleverbridge.com/api-documentation/graphql-api/doc/schema/schema.spec.html

# https://github.com/graphql-python/graphql-core
from graphql import parse
from odoo.exceptions import ValidationError
from odoo.osv.expression import AND
from graphql.language.ast import (
    VariableNode,
    ValueNode,
    ObjectValueNode,
    ListValueNode,
    IntValueNode,
    FloatValueNode,
)

# __Schema, __Type, __TypeKind, __Field, __InputValue, __EnumValue, __Directive

def handle_introspection(env, model_mapping, field):
    ttype = field.name.value
    if not ttype.startswith("__"):
        return None
    ttype = ttype.lower()
    if ttype == "__schema":
        return handle_schema(env, model_mapping, field)
    if ttype == "__type":
        return handle_type(env)
    if ttype == "__typekind":
        return handle_type_kind(env)
    if ttype == "__field":
        return handle_field(env)
    if ttype == "__inputvalue":
        return handle_input_value(env)
    if ttype == "__enumvalue":
        return handle_enum_value(env)
    if ttype == "__directive":
        return handle_directive(env)
    return None

# https://docs.cleverbridge.com/api-documentation/graphql-api/doc/schema/schema.spec.html
def handle_schema(env, model_mapping, fragments, field):
    print("=" * 80)
    print("handle_schema")
    print(dir(field))
    print(field.arguments)
    print(field.directives)
    print(field.keys)
    print([f.name.value for f in field.selection_set.selections])
    f = [f for f in field.selection_set.selections if f.name.value == "types"][0]
    print("-" * 80)
    print("types")
    print(dir(f))
    print(f.name.value)
    print(f.arguments)
    print(f.directives)
    print(f.keys)
    print([x.name.value for x in f.selection_set.selections])  # FullType: this is a fragment
    # print(model_mapping)
    types = [
        {

        }
    ]
    data = {
        "directives": [],
        "mutationType": None,
        "queryType": None,
        "subscriptionType": None,
        "types": [],
    }
    return {}

# https://docs.cleverbridge.com/api-documentation/graphql-api/doc/schema/type.spec.html
def handle_type(env): # aka the models
    ...

def handle_type_kind(env):
    ...

# https://docs.cleverbridge.com/api-documentation/graphql-api/doc/schema/field.spec.html
def handle_field(env):
    return {
        "args": ...,
        "deprecationReason": None,
        "description": ...,
        "isDeprecated": False,
        "name": ...,
        "type": ...,  # __Type
    }
    ...

# https://docs.cleverbridge.com/api-documentation/graphql-api/doc/schema/inputvalue.spec.html
def handle_input_value(env):
    # 
    ...

def handle_enum_value(env):
    ...

def handle_directive(env):
    ...