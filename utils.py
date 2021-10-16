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
    if type != "query":
        return  # Does not support mutations currently

    # for directive in d.directives:
    #     ...
    # for var in d.variable_definitions:
    #     ...

    data = {}
    model_mapping = get_model_mapping(env)
    for field in d.selection_set.selections:
        name = field.name.value
        model = model_mapping[name]
        data[name] = parse_model_field(model, field)
    return data


# Nb: il y a 2 niveau de champs, les racines et ceux dessous
# => on doit parfois récupérer un model, parfois un champs
def parse_model_field(model, field, ids=None):
    domain = parse_arguments(field.arguments)
    if ids:
        domain = AND([
            [("id", "in", ids)]
        ])
    fields = field.selection_set.selections
    fields_names = [f.name.value for f in fields]
    relations = get_relational_fields(model, fields)

    records = model.search_read(domain, fields_names)
    if relations:
        for rec in records:
            for rel, model_name, field in relations:
                rec[rel] = parse_model_field(
                    model.env[model_name], field, ids=rec[rel],
                )
    return records


def get_relational_fields(model, fields):
    relations = []
    for field in fields:
        name = field.name.value
        f = model._fields[name]
        if f.relational:
            relations.append(
                (name, f.comodel_name, field)
            )
    return relations

# https://stackoverflow.com/questions/45674423/how-to-filter-greater-than-in-graphql
def parse_arguments(args):  # return a domain
    # Todo: ajouter support pour d'autres valeurs, comme limit, order, ..
    # for a in args:
    #     breakpoint()
    args = {
        a.name.value: value2py(a.value)
        for a in args
    }
    return args.get("domain", [])

def value2py(value):
    if hasattr(value, "value"):
        return value.value
    if hasattr(value, "values"):
        return [
            value2py(v)
            for v in value.values
        ]
    raise Exception("Can not convert")