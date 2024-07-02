from .utils import timezones

BOOLEAN = {
    "kind": "SCALAR",
    "name": "Boolean",
    "description": "The `Boolean` scalar type represents `true` or `False`.",
    "fields": None,
    "inputFields": None,
    "interfaces": None,
    "enumValues": None,
    "possibleTypes": None,
}

# TODO: Date, Datetime, Decimal and Int
# https://docs.cleverbridge.com/api-documentation/graphql-api/doc/schema/date.doc.html

STRING = {
    "kind": "SCALAR",
    "name": "String",
    "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.",
    "fields": None,
    "inputFields": None,
    "interfaces": None,
    "enumValues": None,
    "possibleTypes": None,
}

ID = {
    "kind": "SCALAR",
    "name": "ID",
    "description": 'The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.',
    "fields": None,
    "inputFields": None,
    "interfaces": None,
    "enumValues": None,
    "possibleTypes": None,
}

INT = {
    "kind": "SCALAR",
    "name": "Int",
    "description": "The `Int` scalar represent an integer.",
    "fields": None,
    "inputFields": None,
    "interfaces": None,
    "enumValues": None,
    "possibleTypes": None,
}

ANY = {
    "kind": "SCALAR",
    "name": "_Any",
    "description": None,
    "fields": None,
    "inputFields": None,
    "interfaces": None,
    "enumValues": None,
    "possibleTypes": None,
}

SERVICE = {
    "kind": "OBJECT",
    "name": "_Service",
    "description": None,
    "fields": [
        {
            "name": "sdl",
            "description": "The sdl representing the federated service capabilities. Includes federation directives, removes federation types, and includes rest of full schema after schema directives have been applied",
            "args": [],
            "type": {"kind": "SCALAR", "name": "String", "ofType": None},
            "isDeprecated": False,
            "deprecationReason": None,
        }
    ],
    "inputFields": None,
    "interfaces": [],
    "enumValues": None,
    "possibleTypes": None,
}

SCHEMA = {
    "kind": "OBJECT",
    "name": "__Schema",
    "description": "A GraphQL Schema defines the capabilities of a GraphQL server. It exposes all available types and directives on the server, as well as the entry points for query, mutation, and subscription operations.",
    "fields": [
        {
            "name": "description",
            "description": None,
            "args": [],
            "type": {"kind": "SCALAR", "name": "String", "ofType": None},
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "types",
            "description": "A list of all types supported by this server.",
            "args": [],
            "type": {
                "kind": "NON_NULL",
                "name": None,
                "ofType": {
                    "kind": "LIST",
                    "name": None,
                    "ofType": {
                        "kind": "NON_NULL",
                        "name": None,
                        "ofType": {"kind": "OBJECT", "name": "__Type", "ofType": None},
                    },
                },
            },
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "queryType",
            "description": "The type that query operations will be rooted at.",
            "args": [],
            "type": {
                "kind": "NON_NULL",
                "name": None,
                "ofType": {"kind": "OBJECT", "name": "__Type", "ofType": None},
            },
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "mutationType",
            "description": "If this server supports mutation, the type that mutation operations will be rooted at.",
            "args": [],
            "type": {"kind": "OBJECT", "name": "__Type", "ofType": None},
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "subscriptionType",
            "description": "If this server support subscription, the type that subscription operations will be rooted at.",
            "args": [],
            "type": {"kind": "OBJECT", "name": "__Type", "ofType": None},
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "directives",
            "description": "A list of all directives supported by this server.",
            "args": [],
            "type": {
                "kind": "NON_NULL",
                "name": None,
                "ofType": {
                    "kind": "LIST",
                    "name": None,
                    "ofType": {
                        "kind": "NON_NULL",
                        "name": None,
                        "ofType": {
                            "kind": "OBJECT",
                            "name": "__Directive",
                            "ofType": None,
                        },
                    },
                },
            },
            "isDeprecated": False,
            "deprecationReason": None,
        },
    ],
    "inputFields": None,
    "interfaces": [],
    "enumValues": None,
    "possibleTypes": None,
}

TYPE = {
    "kind": "OBJECT",
    "name": "__Type",
    "description": "The fundamental unit of any GraphQL Schema is the type. There are many kinds of types in GraphQL as represented by the `__TypeKind` enum.\n\nDepending on the kind of a type, certain fields describe information about that type. Scalar types provide no information beyond a name, description and optional `specifiedByUrl`, while Enum types provide their values. Object and Interface types provide the fields they describe. Abstract types, Union and Interface, provide the Object types possible at runtime. List and NonNull types compose other types.",
    "fields": [
        {
            "name": "kind",
            "description": None,
            "args": [],
            "type": {
                "kind": "NON_NULL",
                "name": None,
                "ofType": {"kind": "ENUM", "name": "__TypeKind", "ofType": None},
            },
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "name",
            "description": None,
            "args": [],
            "type": {"kind": "SCALAR", "name": "String", "ofType": None},
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "description",
            "description": None,
            "args": [],
            "type": {"kind": "SCALAR", "name": "String", "ofType": None},
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "specifiedByUrl",
            "description": None,
            "args": [],
            "type": {"kind": "SCALAR", "name": "String", "ofType": None},
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "fields",
            "description": None,
            "args": [
                {
                    "name": "includeDeprecated",
                    "description": None,
                    "type": {"kind": "SCALAR", "name": "Boolean", "ofType": None},
                    "defaultValue": "False",
                }
            ],
            "type": {
                "kind": "LIST",
                "name": None,
                "ofType": {
                    "kind": "NON_NULL",
                    "name": None,
                    "ofType": {"kind": "OBJECT", "name": "__Field", "ofType": None},
                },
            },
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "interfaces",
            "description": None,
            "args": [],
            "type": {
                "kind": "LIST",
                "name": None,
                "ofType": {
                    "kind": "NON_NULL",
                    "name": None,
                    "ofType": {"kind": "OBJECT", "name": "__Type", "ofType": None},
                },
            },
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "possibleTypes",
            "description": None,
            "args": [],
            "type": {
                "kind": "LIST",
                "name": None,
                "ofType": {
                    "kind": "NON_NULL",
                    "name": None,
                    "ofType": {"kind": "OBJECT", "name": "__Type", "ofType": None},
                },
            },
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "enumValues",
            "description": None,
            "args": [
                {
                    "name": "includeDeprecated",
                    "description": None,
                    "type": {"kind": "SCALAR", "name": "Boolean", "ofType": None},
                    "defaultValue": "False",
                }
            ],
            "type": {
                "kind": "LIST",
                "name": None,
                "ofType": {
                    "kind": "NON_NULL",
                    "name": None,
                    "ofType": {"kind": "OBJECT", "name": "__EnumValue", "ofType": None},
                },
            },
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "inputFields",
            "description": None,
            "args": [
                {
                    "name": "includeDeprecated",
                    "description": None,
                    "type": {"kind": "SCALAR", "name": "Boolean", "ofType": None},
                    "defaultValue": "False",
                }
            ],
            "type": {
                "kind": "LIST",
                "name": None,
                "ofType": {
                    "kind": "NON_NULL",
                    "name": None,
                    "ofType": {
                        "kind": "OBJECT",
                        "name": "__InputValue",
                        "ofType": None,
                    },
                },
            },
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "ofType",
            "description": None,
            "args": [],
            "type": {"kind": "OBJECT", "name": "__Type", "ofType": None},
            "isDeprecated": False,
            "deprecationReason": None,
        },
    ],
    "inputFields": None,
    "interfaces": [],
    "enumValues": None,
    "possibleTypes": None,
}

TYPE_KIND = {
    "kind": "ENUM",
    "name": "__TypeKind",
    "description": "An enum describing what kind of type a given `__Type` is.",
    "fields": None,
    "inputFields": None,
    "interfaces": None,
    "enumValues": [
        {
            "name": "SCALAR",
            "description": "Indicates this type is a scalar.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "OBJECT",
            "description": "Indicates this type is an object. `fields` and `interfaces` are valid fields.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "INTERFACE",
            "description": "Indicates this type is an interface. `fields`, `interfaces`, and `possibleTypes` are valid fields.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "UNION",
            "description": "Indicates this type is a union. `possibleTypes` is a valid field.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "ENUM",
            "description": "Indicates this type is an enum. `enumValues` is a valid field.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "INPUT_OBJECT",
            "description": "Indicates this type is an input object. `inputFields` is a valid field.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "LIST",
            "description": "Indicates this type is a list. `ofType` is a valid field.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "NON_NULL",
            "description": "Indicates this type is a non-None. `ofType` is a valid field.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
    ],
    "possibleTypes": None,
}

FIELD = {
    "kind": "OBJECT",
    "name": "__Field",
    "description": "Object and Interface types are described by a list of Fields, each of which has a name, potentially a list of arguments, and a return type.",
    "fields": [
        {
            "name": "name",
            "description": None,
            "args": [],
            "type": {
                "kind": "NON_NULL",
                "name": None,
                "ofType": {"kind": "SCALAR", "name": "String", "ofType": None},
            },
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "description",
            "description": None,
            "args": [],
            "type": {"kind": "SCALAR", "name": "String", "ofType": None},
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "args",
            "description": None,
            "args": [
                {
                    "name": "includeDeprecated",
                    "description": None,
                    "type": {"kind": "SCALAR", "name": "Boolean", "ofType": None},
                    "defaultValue": "False",
                }
            ],
            "type": {
                "kind": "NON_NULL",
                "name": None,
                "ofType": {
                    "kind": "LIST",
                    "name": None,
                    "ofType": {
                        "kind": "NON_NULL",
                        "name": None,
                        "ofType": {
                            "kind": "OBJECT",
                            "name": "__InputValue",
                            "ofType": None,
                        },
                    },
                },
            },
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "type",
            "description": None,
            "args": [],
            "type": {
                "kind": "NON_NULL",
                "name": None,
                "ofType": {"kind": "OBJECT", "name": "__Type", "ofType": None},
            },
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "isDeprecated",
            "description": None,
            "args": [],
            "type": {
                "kind": "NON_NULL",
                "name": None,
                "ofType": {"kind": "SCALAR", "name": "Boolean", "ofType": None},
            },
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "deprecationReason",
            "description": None,
            "args": [],
            "type": {"kind": "SCALAR", "name": "String", "ofType": None},
            "isDeprecated": False,
            "deprecationReason": None,
        },
    ],
    "inputFields": None,
    "interfaces": [],
    "enumValues": None,
    "possibleTypes": None,
}

INPUT_VALUE = {
    "kind": "OBJECT",
    "name": "__InputValue",
    "description": "Arguments provided to Fields or Directives and the input fields of an InputObject are represented as Input Values which describe their type and optionally a default value.",
    "fields": [
        {
            "name": "name",
            "description": None,
            "args": [],
            "type": {
                "kind": "NON_NULL",
                "name": None,
                "ofType": {"kind": "SCALAR", "name": "String", "ofType": None},
            },
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "description",
            "description": None,
            "args": [],
            "type": {"kind": "SCALAR", "name": "String", "ofType": None},
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "type",
            "description": None,
            "args": [],
            "type": {
                "kind": "NON_NULL",
                "name": None,
                "ofType": {"kind": "OBJECT", "name": "__Type", "ofType": None},
            },
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "defaultValue",
            "description": "A GraphQL-formatted string representing the default value for this input value.",
            "args": [],
            "type": {"kind": "SCALAR", "name": "String", "ofType": None},
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "isDeprecated",
            "description": None,
            "args": [],
            "type": {
                "kind": "NON_NULL",
                "name": None,
                "ofType": {"kind": "SCALAR", "name": "Boolean", "ofType": None},
            },
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "deprecationReason",
            "description": None,
            "args": [],
            "type": {"kind": "SCALAR", "name": "String", "ofType": None},
            "isDeprecated": False,
            "deprecationReason": None,
        },
    ],
    "inputFields": None,
    "interfaces": [],
    "enumValues": None,
    "possibleTypes": None,
}

ENUM_VALUE = {
    "kind": "OBJECT",
    "name": "__EnumValue",
    "description": "One possible value for a given Enum. Enum values are unique values, not a placeholder for a string or numeric value. However an Enum value is returned in a JSON response as a string.",
    "fields": [
        {
            "name": "name",
            "description": None,
            "args": [],
            "type": {
                "kind": "NON_NULL",
                "name": None,
                "ofType": {"kind": "SCALAR", "name": "String", "ofType": None},
            },
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "description",
            "description": None,
            "args": [],
            "type": {"kind": "SCALAR", "name": "String", "ofType": None},
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "isDeprecated",
            "description": None,
            "args": [],
            "type": {
                "kind": "NON_NULL",
                "name": None,
                "ofType": {"kind": "SCALAR", "name": "Boolean", "ofType": None},
            },
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "deprecationReason",
            "description": None,
            "args": [],
            "type": {"kind": "SCALAR", "name": "String", "ofType": None},
            "isDeprecated": False,
            "deprecationReason": None,
        },
    ],
    "inputFields": None,
    "interfaces": [],
    "enumValues": None,
    "possibleTypes": None,
}

DIRECTIVE = {
    "kind": "OBJECT",
    "name": "__Directive",
    "description": "A Directive provides a way to describe alternate runtime execution and type validation behavior in a GraphQL document.\n\nIn some cases, you need to provide options to alter GraphQL's execution behavior in ways field arguments will not suffice, such as conditionally including or skipping a field. Directives provide this by describing additional information to the executor.",
    "fields": [
        {
            "name": "name",
            "description": None,
            "args": [],
            "type": {
                "kind": "NON_NULL",
                "name": None,
                "ofType": {"kind": "SCALAR", "name": "String", "ofType": None},
            },
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "description",
            "description": None,
            "args": [],
            "type": {"kind": "SCALAR", "name": "String", "ofType": None},
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "isRepeatable",
            "description": None,
            "args": [],
            "type": {
                "kind": "NON_NULL",
                "name": None,
                "ofType": {"kind": "SCALAR", "name": "Boolean", "ofType": None},
            },
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "locations",
            "description": None,
            "args": [],
            "type": {
                "kind": "NON_NULL",
                "name": None,
                "ofType": {
                    "kind": "LIST",
                    "name": None,
                    "ofType": {
                        "kind": "NON_NULL",
                        "name": None,
                        "ofType": {
                            "kind": "ENUM",
                            "name": "__DirectiveLocation",
                            "ofType": None,
                        },
                    },
                },
            },
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "args",
            "description": None,
            "args": [
                {
                    "name": "includeDeprecated",
                    "description": None,
                    "type": {"kind": "SCALAR", "name": "Boolean", "ofType": None},
                    "defaultValue": "False",
                }
            ],
            "type": {
                "kind": "NON_NULL",
                "name": None,
                "ofType": {
                    "kind": "LIST",
                    "name": None,
                    "ofType": {
                        "kind": "NON_NULL",
                        "name": None,
                        "ofType": {
                            "kind": "OBJECT",
                            "name": "__InputValue",
                            "ofType": None,
                        },
                    },
                },
            },
            "isDeprecated": False,
            "deprecationReason": None,
        },
    ],
    "inputFields": None,
    "interfaces": [],
    "enumValues": None,
    "possibleTypes": None,
}

DIRECTIVE_LOCATION = {
    "kind": "ENUM",
    "name": "__DirectiveLocation",
    "description": "A Directive can be adjacent to many parts of the GraphQL language, a __DirectiveLocation describes one such possible adjacencies.",
    "fields": None,
    "inputFields": None,
    "interfaces": None,
    "enumValues": [
        {
            "name": "QUERY",
            "description": "Location adjacent to a query operation.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "MUTATION",
            "description": "Location adjacent to a mutation operation.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "SUBSCRIPTION",
            "description": "Location adjacent to a subscription operation.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "FIELD",
            "description": "Location adjacent to a field.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "FRAGMENT_DEFINITION",
            "description": "Location adjacent to a fragment definition.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "FRAGMENT_SPREAD",
            "description": "Location adjacent to a fragment spread.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "INLINE_FRAGMENT",
            "description": "Location adjacent to an inline fragment.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "VARIABLE_DEFINITION",
            "description": "Location adjacent to a variable definition.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "SCHEMA",
            "description": "Location adjacent to a schema definition.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "SCALAR",
            "description": "Location adjacent to a scalar definition.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "OBJECT",
            "description": "Location adjacent to an object type definition.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "FIELD_DEFINITION",
            "description": "Location adjacent to a field definition.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "ARGUMENT_DEFINITION",
            "description": "Location adjacent to an argument definition.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "INTERFACE",
            "description": "Location adjacent to an interface definition.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "UNION",
            "description": "Location adjacent to a union definition.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "ENUM",
            "description": "Location adjacent to an enum definition.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "ENUM_VALUE",
            "description": "Location adjacent to an enum value definition.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "INPUT_OBJECT",
            "description": "Location adjacent to an input object type definition.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
        {
            "name": "INPUT_FIELD_DEFINITION",
            "description": "Location adjacent to an input object field definition.",
            "isDeprecated": False,
            "deprecationReason": None,
        },
    ],
    "possibleTypes": None,
}


DATETIME_TZ_ENUM = {
    "kind": "ENUM",
    "name": "Timezone",
    "description": "",
    "fields": None,
    "inputFields": None,
    "interfaces": None,
    "enumValues": [
        {
            "name": tz,
            "description": description,
            "isDeprecated": False,
            "deprecationReason": None,
        }
        for tz, description in timezones.items()
    ],
    "possibleTypes": None,
}


# QUERY = {
#     "kind": "OBJECT",
#     "name": "Query",
#     "description": None,
#     "fields": [
#         # TODO
#         # all fields already mentionned, again
#     ],
#     "inputFields": None,
#     "interfaces": [],
#     "enumValues": None,
#     "possibleTypes": None
# }

ALL_TYPES_MAPPING = {
    "BOOLEAN": BOOLEAN,
    "STRING": STRING,
    "ID": ID,
    "INT": INT,
    "ANY": ANY,
    "SERVICE": SERVICE,
    "SCHEMA": SCHEMA,
    "TYPE": TYPE,
    "TYPE_KIND": TYPE_KIND,
    "FIELD": FIELD,
    "INPUT_VALUE": INPUT_VALUE,
    "ENUM_VALUE": ENUM_VALUE,
    "DIRECTIVE": DIRECTIVE,
    "DIRECTIVE_LOCATION": DIRECTIVE_LOCATION,
    "DATETIME_TZ_ENUM": DATETIME_TZ_ENUM,
    # "QUERY": QUERY,
}
ALL_TYPES = list(ALL_TYPES_MAPPING.values())
