# -*- coding: utf-8 -*-

# https://github.com/graphql-python/graphql-core
from graphql import parse
from odoo.exceptions import ValidationError
from odoo.osv.expression import AND
from graphql.language.ast import (
    VariableNode,
    ValueNode,
    ObjectValueNode,
    ListValueNode,
    IntValueNode,
    FloatValueNode,
)
# import traceback

import logging

_logger = logging.getLogger(__name__)


def model2name(model):
    return "".join(p.title() for p in model.split("."))


def filter_by_directives(node, variables={}):
    if not node.selection_set:
        return
    selections = []
    for field in node.selection_set.selections:
        if parse_directives(field.directives, variables=variables):
            selections.append(field)
            filter_by_directives(field, variables=variables)
    node.selection_set.selections = selections


def get_definition(doc, operation=None):
    if operation is None or len(doc.definitions) == 1:
        return doc.definitions[0]
    for definition in doc.definitions:
        # https://dgraph.io/docs/graphql/api/multiples/#multiple-operations
        # https://github.com/graphql/graphql-spec/issues/29
        if definition.name.value == operation:
            return definition
    return doc.definitions[0]  # Or raise an Exception?


def handle_graphql(doc, model_mapping, variables={}, operation=None, allowed_fields={}):
    response = {}
    try:
        data = parse_document(
            doc,
            model_mapping,
            variables=variables,
            operation=operation,
            allowed_fields=allowed_fields,
        )
        response["data"] = data
    except Exception as e:
        _logger.critical(e)
        response["data"] = None
        response["errors"] = {"message": str(e)}  # + traceback.format_exc()
    return response


def parse_document(doc, model_mapping, variables={}, operation=None, allowed_fields={}):
    if isinstance(doc, str):
        doc = parse(doc)

    # A document can have many definitions
    definition = get_definition(doc, operation=operation)
    return parse_definition(
        definition, model_mapping, variables=variables, allowed_fields=allowed_fields
    )


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


def _parse_definition(
    definition, model_mapping, variables={}, mutation=False, allowed_fields={}
):
    data = {}
    for field in definition.selection_set.selections:
        model = model_mapping[field.name.value]
        fname = field.alias and field.alias.value or field.name.value
        data[fname] = parse_model_field(
            model,
            field,
            variables=variables,
            mutation=mutation,
            allowed_fields=allowed_fields,
        )
    return data


def parse_definition(definition, model_mapping, variables={}, allowed_fields={}):
    dtype = definition.operation.value      # MUTATION OR QUERY
    if dtype not in ("query", "mutation"):  # does not support other types currentyl
        return None

    filter_by_directives(definition, variables)
    mutation = dtype == "mutation"
    return _parse_definition(
        definition,
        model_mapping=model_mapping,
        variables=variables,
        mutation=mutation,
        allowed_fields=allowed_fields,
    )


def relation_subgathers(records, relational_data, variables={}):
    subgathers = {}
    for submodel, fname, fields in relational_data:
        sub_records_ids = records.mapped(fname).ids
        aliases = []
        for f in fields:
            # Nb: Even if its the same field, the domain may change
            alias = f.alias and f.alias.value or f.name.value
            tmp = parse_model_field(
                submodel, f, variables=variables, ids=sub_records_ids
            )
            data = {d["id"]: (i, d) for i, d in enumerate(tmp)}

            # https://stackoverflow.com/questions/8946868/is-there-a-pythonic-way-to-close-over-a-loop-variable
            def subgather(ids, data=data):
                if ids is False:
                    return None
                # We may not receive all ids since records may be archived
                if isinstance(ids, int):
                    return data.get(ids)[1]
                # Since the data are gathered in batch, then dispatching,
                # The order is lost and must be done again.
                res = [
                    d
                    for _, d in sorted(
                        (d for d in (data.get(rec_id) for rec_id in ids) if d),
                        key=lambda t: t[0],
                    )
                ]
                return res

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


# TODO: make it possible to define custom create/write handlers per models
def retrieve_records(model, field, variables={}, ids=None, mutation=False):
    domain, kwargs, vals = parse_arguments(field.arguments, variables)
    if mutation and domain is None:  # Create
        try:
            records = model.create(vals)
        except Exception as e:
            if "DETAIL" in str(e):
                model.env.cr.rollback()
                raise ValidationError(str(e).split("\n")[0])
            raise
        return records

    # Retrieve records
    domain = make_domain(domain or [], ids)
    records = model.search(domain, **kwargs)

    if mutation:  # Write
        records.write(vals)

    return records

# Nb: the parameter "ids" is useful for relational fields
def parse_model_field(
    model, field, variables={}, ids=None, mutation=False, allowed_fields={}
):
    records = retrieve_records(
        model,
        field,
        variables=variables,
        ids=ids,
        mutation=mutation,
    )

    # User may have forgotten to define subfields
    # We use an empty list to prevent it,
    # Maybe we should rise an error here instead?
    fields = []
    if field.selection_set:
        fields = field.selection_set.selections
    allowed = allowed_fields.get(model._name)
    if allowed is not None:
        fields = [f for f in fields if f.name.value in allowed]
        if not fields:
            return [
                {"id": rid} for rid in records.ids
            ]
    fields_names = [f.name.value for f in fields]

    # Get datas
    relational_data, fields_data = get_fields_data(model, fields)
    subgathers = relation_subgathers(records, relational_data, variables=variables)
    records = records.read(fields_names, load=False)

    data = []
    for rec in records:
        tmp = {"id": rec["id"]}
        for fname, aliases in fields_data:
            for alias in aliases:
                value = rec[fname]
                if isinstance(value, bytes):
                    value = value.decode()
                tmp[alias] = value

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


# TODO: Add a hook to filter vals?
# https://stackoverflow.com/questions/45674423/how-to-filter-greater-than-in-graphql
def parse_arguments(args, variables={}):  # return a domain and kwargs
    args = {a.name.value: value2py(a.value, variables) for a in args}
    domain = args.pop("domain", None)
    kwargs = {}
    for opt, cast in OPTIONS:
        value = args.pop(opt, None)
        if value:
            kwargs[opt] = cast(value)
    vals = args.pop("vals", {})
    return domain, kwargs, vals


def value2py(value, variables={}):
    if isinstance(value, VariableNode):
        return variables.get(value.name.value)
    if isinstance(value, ValueNode):
        if isinstance(value, ListValueNode):
            return [value2py(v, variables=variables) for v in value.values]
        if isinstance(value, ObjectValueNode):
            return dict(
                (
                    value2py(f.name, variables=variables),
                    value2py(f.value, variables=variables),
                )
                for f in value.fields  # list of ObjectFieldNode
            )
        # For unknown reason, integers and floats are received as string,
        # but not booleans nor list
        if isinstance(value, IntValueNode):
            return int(value.value)
        if isinstance(value, FloatValueNode):
            return float(value.value)
    return value.value
