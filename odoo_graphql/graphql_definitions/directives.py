INCLUDE = {
    "name": "include",
    "description": "Directs the executor to include this field or fragment only when the `if` argument is true.",
    "locations": ["FIELD", "FRAGMENT_SPREAD", "INLINE_FRAGMENT"],
    "args": [
    {
        "name": "if",
        "description": "Included when true.",
        "type": {
        "kind": "NON_NULL",
        "name": None,
        "ofType": {
            "kind": "SCALAR",
            "name": "Boolean",
            "ofType": None
        }
        },
        "defaultValue": None
    }
    ]
}

SKIP = {
    "name": "skip",
    "description": "Directs the executor to skip this field or fragment when the `if` argument is true.",
    "locations": ["FIELD", "FRAGMENT_SPREAD", "INLINE_FRAGMENT"],
    "args": [
    {
        "name": "if",
        "description": "Skipped when true.",
        "type": {
        "kind": "NON_NULL",
        "name": None,
        "ofType": {
            "kind": "SCALAR",
            "name": "Boolean",
            "ofType": None
        }
        },
        "defaultValue": None
    }
    ]
}

DIRECTIVES = [
    INCLUDE,
    SKIP
]