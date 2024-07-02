SCALAR = (
    {
        "name": "SCALAR",
        "description": "Indicates this type is a scalar.",
        "isDeprecated": False,
        "deprecationReason": None,
    },
)
OBJECT = (
    {
        "name": "OBJECT",
        "description": "Indicates this type is an object. `fields` and `interfaces` are valid fields.",
        "isDeprecated": False,
        "deprecationReason": None,
    },
)
INTERFACE = (
    {
        "name": "INTERFACE",
        "description": "Indicates this type is an interface. `fields`, `interfaces`, and `possibleTypes` are valid fields.",
        "isDeprecated": False,
        "deprecationReason": None,
    },
)
UNION = (
    {
        "name": "UNION",
        "description": "Indicates this type is a union. `possibleTypes` is a valid field.",
        "isDeprecated": False,
        "deprecationReason": None,
    },
)
ENUM = (
    {
        "name": "ENUM",
        "description": "Indicates this type is an enum. `enumValues` is a valid field.",
        "isDeprecated": False,
        "deprecationReason": None,
    },
)
INPUT_OBJECT = (
    {
        "name": "INPUT_OBJECT",
        "description": "Indicates this type is an input object. `inputFields` is a valid field.",
        "isDeprecated": False,
        "deprecationReason": None,
    },
)
LIST = {
    "name": "LIST",
    "description": "Indicates this type is a list. `ofType` is a valid field.",
    "isDeprecated": False,
    "deprecationReason": None,
}

NON_NULL = {
    "name": "NON_NULL",
    "description": "Indicates this type is a non-None. `ofType` is a valid field.",
    "isDeprecated": False,
    "deprecationReason": None,
}

TYPE_KINDS = {
    "SCALAR": SCALAR,
    "OBJECT": OBJECT,
    "INTERFACE": INTERFACE,
    "UNION": UNION,
    "ENUM": ENUM,
    "INPUT_OBJECT": INPUT_OBJECT,
    "LIST": LIST,
    "NON_NULL": NON_NULL,
}
