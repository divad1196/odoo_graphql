DOMAIN_ARG = {
    "name": "domain",
    "description": None,
    "type": {
        "kind": "LIST",
        "name": None,
        "ofType": {
            "kind": "LIST",
            "name": None,
            "ofType": {"kind": "SCALAR", "name": "_Any", "ofType": None},
        },
    },
    "defaultValue": None,
}
LIMIT_ARG = {
    "name": "limit",
    "description": None,
    "type": {"kind": "SCALAR", "name": "Int", "ofType": None},
    "defaultValue": None,
}

OFFSET_ARG = {
    "name": "offset",
    "description": None,
    "type": {"kind": "SCALAR", "name": "Int", "ofType": None},
    "defaultValue": None,
}

ORDER_ARG = {
    "name": "order",
    "description": None,
    "type": {"kind": "SCALAR", "name": "String", "ofType": None},
    "defaultValue": None,
}


DATE_FORMAT = {
    "name": "format",
    "description": None,
    "type": {"kind": "SCALAR", "name": "String", "ofType": None},
    "defaultValue": None,
}


DATETIME_TZ = {
    "name": "tz",
    "description": None,
    "type": {"kind": "SCALAR", "name": "String", "ofType": None},
    "defaultValue": None,
}


DATETIME_TZ = {
    "name": "tz",
    "description": None,
    "type": {"kind": "ENUM", "name": "Timezone", "ofType": None},
    "defaultValue": None,
}


MODELS_ARGS = [
    DOMAIN_ARG,
    LIMIT_ARG,
    OFFSET_ARG,
    ORDER_ARG,
]
