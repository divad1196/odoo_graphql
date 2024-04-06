# https://graphql.org/learn/introspection/
# https://docs.cleverbridge.com/api-documentation/graphql-api/doc/schema/schema.spec.html

# https://github.com/graphql-python/graphql-core
from odoo.exceptions import ValidationError

from .graphql_definitions.basic_types import ALL_TYPES
from .graphql_definitions.directives import DIRECTIVES
from .graphql_definitions.field_args import DATE_FORMAT, DATETIME_TZ, MODELS_ARGS
from .utils import lazy, model2name, resolve_data

# __Schema, __Type, __TypeKind, __Field, __InputValue, __EnumValue, __Directive


def handle_introspection(env, model_mapping, field, fragments={}):
    ttype = field.name.value
    if not ttype.startswith("__"):
        return None
    ttype = ttype.lower()
    if ttype == "__type":
        return handle_type(env, model_mapping, field, fragments=fragments)
    # if ttype == "__typekind":
    #     return handle_type_kind(env)
    # if ttype == "__field":
    #     return handle_field(env, model_mapping, field, fragments=fragments)
    # if ttype == "__inputvalue":
    #     return handle_input_value(env)
    # if ttype == "__enumvalue":
    #     return handle_enum_value(env)
    # if ttype == "__directive":
    #     return handle_directive(env)
    if ttype == "__schema":
        return handle_schema(env, model_mapping, field, fragments=fragments)
    return None


def model2type(model, node=None):
    """
    Convert a model to a graphql __Type
    https://docs.cleverbridge.com/api-documentation/graphql-api/doc/schema/type.spec.html
    """
    if node is None:
        return _model2type(model)

    ttype = model2name(model._name)

    def get_fields():
        fields = (
            (model._fields.get(f.name.value), f) for f in node.selection_set.selections
        )
        return (
            [  # (includeDeprecated: Boolean)
                field2type(f, n) for f, n in fields if f and not f.name.startswith("__")
            ],
        )

    data = {
        "description": model._description or "",
        "enumValues": None,
        "fields": lazy(get_fields),
        "inputFields": None,
        "interfaces": [
            # __Type!
        ],
        "kind": "OBJECT",
        "name": ttype,
        "possibleTypes": None,
    }
    return resolve_data(node, data)


def _model2type(model):
    """
    Convert a model to a graphql __Type
    https://docs.cleverbridge.com/api-documentation/graphql-api/doc/schema/type.spec.html
    """
    ttype = model2name(model._name)
    return {
        "description": model._description or "",
        "enumValues": None,
        "fields": [  # (includeDeprecated: Boolean)
            field2type(f) for f in model._fields.values() if not f.name.startswith("__")
        ],
        "inputFields": None,
        "interfaces": [
            # __Type!
        ],
        "kind": "OBJECT",
        "name": ttype,
        "possibleTypes": None,
    }


# Map every field type in odoo to graphql type
FIELDTYPE_TO_KIND = {
    "boolean": "Boolean",
    "integer": "_Any",
    "float": "_Any",
    "monetary": "_Any",
    "char": "String",
    "text": "String",
    "html": "String",
    "date": "String",
    "datetime": "String",
    "binary": "String",
    "selection": "String",
}


def get_field_args(relational=True, field=None):
    if not relational:
        if not field:
            return []
        if field.type == "date":
            return [
                DATE_FORMAT,
            ]
        if field.type == "datetime":
            return [DATE_FORMAT, DATETIME_TZ]
        return []
    return MODELS_ARGS


def get_field_type_data(field):
    if field.relational:
        return {
            "kind": "OBJECT",
            "name": model2name(field.comodel_name),
            "ofType": None,
        }
    return {
        "kind": "SCALAR",
        "name": FIELDTYPE_TO_KIND.get(field.type, "_Any"),
        "ofType": None,
    }


def field2type(field, node=None):
    """
    Convert a model to a graphql __Type
    https://docs.cleverbridge.com/api-documentation/graphql-api/doc/schema/type.spec.html
    """
    type_data = get_field_type_data(field)
    relational = field.type in ("one2many", "many2many")
    if relational:
        type_data = {"kind": "LIST", "name": None, "ofType": type_data}
    if field.required:
        type_data = {"kind": "NON_NULL", "name": None, "ofType": type_data}
    return resolve_data(
        node,
        {
            "name": field.name,
            "description": field.string or field.name,
            "args": get_field_args(relational, field),
            "type": type_data,
        },
    )


# https://docs.cleverbridge.com/api-documentation/graphql-api/doc/schema/schema.spec.html
def handle_schema(env, model_mapping, field, fragments={}):
    # TODO: Re-add the possibility to hide transient models
    models = list(env.values())
    # models = [
    #     model
    #     for model in env.values()
    #     if not model._transient
    # ]
    models_types = [model2type(model) for model in models]
    models_types = [t for t in models_types if t["fields"]]
    # TODO: Remove fields that reference types that where removed?
    query_type = {
        "kind": "OBJECT",
        "name": "Query",
        "description": None,
        "fields": [
            {
                "name": model_name,
                "description": None,
                "args": get_field_args(True),
                "type": {
                    "kind": "OBJECT",
                    "name": model_name,
                    "ofType": None,
                },
            }
            for model_name in (m["name"] for m in models_types)
        ],
        "inputFields": None,
        "interfaces": [],
        "enumValues": None,
        "possibleTypes": None,
    }
    types = [*ALL_TYPES, query_type, *models_types]
    return {
        "directives": DIRECTIVES,
        "mutationType": None,
        "queryType": {
            "name": query_type["name"],
        },
        "subscriptionType": None,
        "types": types,
    }


# https://docs.cleverbridge.com/api-documentation/graphql-api/doc/schema/type.spec.html
def handle_type(env, model_mapping, field, fragments={}):  # aka the models
    name = next(
        (a.value.value for a in field.arguments if a.name.value == "name"), None
    )
    if name is None:
        raise ValidationError("Missing argument `name` for __type")
    model = model_mapping.get(name)
    if model is None:
        raise ValidationError(f"Type `{name}` does not exist")
    return model2type(model, field)


# def handle_type_kind(env):
#     ...

# # https://docs.cleverbridge.com/api-documentation/graphql-api/doc/schema/field.spec.html
# def handle_field(env, model_mapping, field, fragments={}):
#     return field2type
#     ...

# # https://docs.cleverbridge.com/api-documentation/graphql-api/doc/schema/inputvalue.spec.html
# def handle_input_value(env):
#     #
#     ...

# def handle_enum_value(env):
#     ...

# def handle_directive(env):
#     ...
