# -*- coding: utf-8 -*-

# https://github.com/graphql-python/graphql-core
from odoo import tools
from odoo.osv.expression import AND


def parse_document(env, doc):  # Un document peut avoir plusieurs définitions
    for definition in doc.definitions:
        return parse_definition(env, definition)


def model2name(model):
    return "".join(p.title() for p in model.split("."))

# @tools.ormcache()
def get_model_mapping(env):
    return {
        model2name(name): model
        for name, model in env.items()
    }

def parse_definition(env, d):
    type = d.operation.value  # MUTATION OR QUERY
    # name = d.name.value  # Usage in response? Only for debug
    if type != "query":
        return  # Does not support mutations currently

    # for directive in d.directives:
    #     ...
    # for var in d.variable_definitions:
    #     ...

    data = {}
    model_mapping = get_model_mapping(env)
    for field in d.selection_set.selections:
        model = model_mapping[field.name.value]
        fname = field.alias and field.alias.value or field.name.value
        data[fname] = parse_model_field(model, field)
    return data


# Nb: il y a 2 niveau de champs, les racines et ceux dessous
# => on doit parfois récupérer un model, parfois un champs
def parse_model_field(model, field, ids=None):
    domain, kwargs = parse_arguments(field.arguments)
    if ids:
        domain = AND([
            [("id", "in", ids)],
            domain
        ])
    fields = field.selection_set.selections
    fields_names = [f.name.value for f in fields]

    # Get datas
    records = model.search_read(domain, fields_names, **kwargs)

    fields_data = get_fields_data(model, fields)
    data = []
    for rec in records:
        tmp = {}
        for key, value in rec.items():
            model, fname, fields = fields_data.get(key, (None, None, None))
            if model is not None:
                for f in fields:
                    fname = f.alias and f.alias.value or f.name.value
                    if not f.selection_set:
                        tmp[fname] = value
                    else:
                        tmp[fname] = parse_model_field(
                            model, f, ids=value,
                        )
            elif fields:
                for f in fields:
                    tmp[fname] = value
            else:
                tmp[key] = value  # e.g.: id is gathered even if not requested
        data.append(tmp)
    return data

def get_fields_data(model, fields):
    relations = {}
    for field in fields:
        name = field.name.value
        fname = field.alias and field.alias.value or name
        f = model._fields[name]
        r = relations.setdefault(
            name,
            (
                model.env[f.comodel_name] if f.relational else None,
                fname,
                []
            )
        )
        r[2].append(field)
    return relations


OPTIONS = [
    ("offset", int),
    ("limit", int),
    ("order", str)
]

# https://stackoverflow.com/questions/45674423/how-to-filter-greater-than-in-graphql
def parse_arguments(args):  # return a domain
    # Todo: ajouter support pour d'autres valeurs, comme limit, order, ..
    # for a in args:
    #     breakpoint()
    args = {
        a.name.value: value2py(a.value)
        for a in args
    }
    kwargs = {}
    for opt, cast in OPTIONS:
        value = args.pop(opt, None)
        if value:
            kwargs[opt] = cast(value)
    return args.pop("domain", []), kwargs

def value2py(value):
    if hasattr(value, "value"):
        return value.value
    if hasattr(value, "values"):
        return [
            value2py(v)
            for v in value.values
        ]
    raise Exception("Can not convert")