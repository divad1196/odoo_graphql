# -*- coding: utf-8 -*-

# https://github.com/graphql-python/graphql-core
from odoo import tools
from odoo.osv.expression import AND
from graphql.language.ast import (
    VariableNode,
    ValueNode,
    ListValueNode,
    IntValueNode,
    FloatValueNode,
)


def model2name(model):
    return "".join(p.title() for p in model.split("."))


# See self.clear_caches(): we need a cache that changes with module install?
# @tools.ormcache()
def get_model_mapping(env):
    return {model2name(name): model for name, model in env.items()}


def filter_by_directives(node, variables={}):
    if not node.selection_set:
        return
    selections = []
    for field in node.selection_set.selections:
        if parse_directives(field.directives, variables=variables):
            selections.append(field)
            filter_by_directives(field, variables=variables)
    node.selection_set.selections = selections


def parse_document(
    env, doc, variables={}
):  # Un document peut avoir plusieurs définitions
    variables = {**env.context, **variables}
    model_mapping = get_model_mapping(env)
    for definition in doc.definitions:
        return parse_definition(env, definition, model_mapping, variables=variables)


def parse_directives(directives, variables={}):
    """Currently return True to keep, False to skip"""
    for d in directives:
        if d.name.value == "include":
            for arg in d.arguments:
                if arg.name.value == "if":
                    value = value2py(arg.value, variables=variables)
                    return value
        elif d.name.value == "skip":
            for arg in d.arguments:
                if arg.name.value == "if":
                    value = value2py(arg.value, variables=variables)
                    return not value
    return True  # Keep by default


def parse_definition(env, d, model_mapping, variables={}):
    type = d.operation.value  # MUTATION OR QUERY
    # name = d.name.value  # Usage in response? Only for debug
    if type != "query":
        return  # Does not support mutations currently

    filter_by_directives(d, variables)

    data = {}
    for field in d.selection_set.selections:
        model = model_mapping[field.name.value]
        fname = field.alias and field.alias.value or field.name.value
        data[fname] = parse_model_field(model, field, variables=variables)
    return data


def relation_subgathers(records, relational_data, variables={}):
    subgathers = {}
    for submodel, fname, fields in relational_data:
        sub_records_ids = records.mapped(fname).ids
        aliases = []
        for f in fields:
            alias = f.alias and f.alias.value or f.name.value
            tmp = parse_model_field(
                submodel, f, variables=variables, ids=sub_records_ids
            )
            data = {d["id"]: d for d in tmp}

            # https://stackoverflow.com/questions/8946868/is-there-a-pythonic-way-to-close-over-a-loop-variable
            def subgather(ids, data=data):
                if ids is False:
                    return None
                # Possible de ne pas avoir l'id recherché ou bug?
                # => Oui a cause des records archivés
                if isinstance(ids, int):
                    return data.get(ids)
                return [d for d in (data.get(rec_id) for rec_id in ids) if d]

            aliases.append((alias, subgather))

        subgathers[fname] = aliases
    return subgathers


def make_domain(domain, ids):
    if ids:
        if isinstance(ids, (list, tuple)):
            domain = AND([[("id", "in", ids)], domain])
        elif isinstance(ids, int):
            domain = AND([[("id", "=", ids)], domain])
    return domain


# Nb: il y a 2 niveau de champs, les racines et ceux dessous
# => on doit parfois récupérer un model, parfois un champs
def parse_model_field(model, field, variables={}, ids=None):
    domain, kwargs = parse_arguments(field.arguments, variables)
    fields = field.selection_set.selections
    fields_names = [f.name.value for f in fields]

    # Get datas
    records = model.search(make_domain(domain, ids), **kwargs)

    relational_data, fields_data = get_fields_data(model, fields)
    subgathers = relation_subgathers(records, relational_data, variables=variables)
    records = records.read(fields_names, load=False)

    data = []
    for rec in records:
        tmp = {"id": rec["id"]}
        for fname, aliases in fields_data:
            for alias in aliases:
                tmp[alias] = rec[fname]

        for fname, aliases in subgathers.items():
            ids = rec[fname]
            for alias, subgather in aliases:
                tmp[alias] = subgather(ids)
        data.append(tmp)
    return data


def get_fields_data(model, fields):
    relations = {}
    basic_fields = {}
    for field in fields:
        name = field.name.value
        f = model._fields[name]
        if f.relational:
            r = relations.setdefault(
                name,
                (
                    model.env[f.comodel_name],
                    name,
                    [],
                ),
            )
            r[2].append(field)
        else:
            r = basic_fields.setdefault(
                name,
                (
                    name,
                    [],
                ),
            )
            r[1].append(field.alias and field.alias.value or field.name.value)

    return relations.values(), basic_fields.values()


OPTIONS = [("offset", int), ("limit", int), ("order", str)]


# https://stackoverflow.com/questions/45674423/how-to-filter-greater-than-in-graphql
def parse_arguments(args, variables={}):  # return a domain and kwargs
    args = {a.name.value: value2py(a.value, variables) for a in args}
    kwargs = {}
    for opt, cast in OPTIONS:
        value = args.pop(opt, None)
        if value:
            kwargs[opt] = cast(value)
    return args.pop("domain", []), kwargs


def value2py(value, variables={}):
    if isinstance(value, VariableNode):
        return variables.get(value.name.value)
    if isinstance(value, ValueNode):
        if isinstance(value, ListValueNode):
            return [value2py(v, variables=variables) for v in value.values]
        # For unknown reason, integers and floats are received as string,
        # but not booleans nor list
        if isinstance(value, IntValueNode):
            return int(value.value)
        if isinstance(value, FloatValueNode):
            return float(value.value)
        return value.value

    raise Exception("Can not convert")
