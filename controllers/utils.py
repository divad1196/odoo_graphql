# -*- coding: utf-8 -*-

# https://github.com/graphql-python/graphql-core
from odoo.osv.expression import AND


def parse_document(env, doc):  # Un document peut avoir plusieurs définitions
    for definition in doc.definitions:
        parse_definition(env, definition)


def parse_definition(env, d):
    type = d.operation.value  # MUTATION OR QUERY
    if type != "query":
        return  # Does not support mutations currently

    # for directive in d.directives:
    #     ...
    # for var in d.variable_definitions:
    #     ...

    data = {}
    for field in d.d.selection_set.selections:
        name = field.name.value
        model = get_model_by_name(env, name)
        data[name] = parse_model_field(model, field)
    return data


def get_model_by_name(env, name):
    # Todo
    return "sale.order"

# Nb: il y a 2 niveau de champs, les racines et ceux dessous
# => on doit parfois récupérer un model, parfois un champs
def parse_model_field(model, field, ids=None):
    domain = parse_arguments(field.arguments)
    if ids:
        domain = AND([
            [("id", "in", ids)]
        ])
    fields = field.selection_set.selections
    fields_names = [f.name.values for f in fields]
    relations = get_relational_fields(model, fields)

    records = model.search_read(domain, fields_names)
    if relations:
        for rec in records:
            for rel, model_name, field in relations.items():
                rec[rel] = parse_model_field(
                    model.env[model_name], field
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
    args = {
        a.name.value: a.value.value
        for a in args
    }
    return args.get("domain", [])
