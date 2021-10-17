# -*- coding: utf-8 -*-

# https://github.com/graphql-python/graphql-core
from odoo import tools
from odoo.osv.expression import AND
from graphql.language.ast import (
    VariableNode
)


def parse_document(env, doc, variables={}):  # Un document peut avoir plusieurs définitions
    variables = {**env.context, **variables}
    for definition in doc.definitions:
        return parse_definition(env, definition, variables=variables)


def model2name(model):
    return "".join(p.title() for p in model.split("."))


# See self.clear_caches(): we need a cache that changes with module install?
# @tools.ormcache()
def get_model_mapping(env):
    return {
        model2name(name): model
        for name, model in env.items()
    }

def filter_by_directives(node, variables={}):
    if not node.selection_set:
        return
    selections = []
    for field in node.selection_set.selections:
        if parse_directives(field.directives, variables=variables):
            selections.append(field)
            filter_by_directives(field, variables=variables)
    node.selection_set.selections = selections


def parse_directives(directives, variables={}):
    """Currently return True to keep, False to skip """
    for d in directives:
        if d.name.value == "include":
            for arg in d.arguments:
                if arg.name.value == 'if':
                    value = value2py(arg.value, variables=variables)
                    print("Directive: include if", value)
                    return value
        elif d.name.value == "skip":
            for arg in d.arguments:
                if arg.name.value == 'if':
                    value = value2py(arg.value, variables=variables)
                    return not value
    return True  # Keep by default


def parse_definition(env, d, variables={}):
    type = d.operation.value  # MUTATION OR QUERY
    # name = d.name.value  # Usage in response? Only for debug
    if type != "query":
        return  # Does not support mutations currently

    filter_by_directives(d, variables)

    # for var in d.variable_definitions:
    #     ...

    data = {}
    model_mapping = get_model_mapping(env)
    for field in d.selection_set.selections:
        model = model_mapping[field.name.value]
        fname = field.alias and field.alias.value or field.name.value
        data[fname] = parse_model_field(model, field, variables=variables)
    return data


# Nb: il y a 2 niveau de champs, les racines et ceux dessous
# => on doit parfois récupérer un model, parfois un champs
def parse_model_field(model, field, variables={}, ids=None):
    domain, kwargs = parse_arguments(field.arguments, variables)
    if ids:
        if not isinstance(ids, (list, tuple)):
            ids = [ids]
        domain = AND([
            [("id", "in", ids)],
            domain
        ])
    fields = field.selection_set.selections
    fields_names = [f.name.value for f in fields]

    # Get datas
    records = model.search(domain, **kwargs).read(fields_names, load=False)

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
                            model, f,
                            variables=variables,
                            ids=value,
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
def parse_arguments(args, variables={}):  # return a domain and kwargs
    args = {
        a.name.value: value2py(a.value, variables)
        for a in args
    }
    kwargs = {}
    for opt, cast in OPTIONS:
        value = args.pop(opt, None)
        if value:
            kwargs[opt] = cast(value)
    return args.pop("domain", []), kwargs


def value2py(value, variables={}):
    if isinstance(value, VariableNode):
        return variables.get(value.name.value)
    if hasattr(value, "value"):
        return value.value
    if hasattr(value, "values"):
        return [
            value2py(v, variables=variables)
            for v in value.values
        ]
    raise Exception("Can not convert")
