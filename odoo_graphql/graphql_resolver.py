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
    FragmentSpreadNode,
    FragmentDefinitionNode
)
# from .utils import model2name, print_node as pn
from .introspection import handle_introspection

import logging
_logger = logging.getLogger(__name__)



def filter_by_directives(node, variables={}):
    """
        Recursively handle every node.
        For each node, the node is remove if they have the directive:
        - skip set to true
        - include set to false
    """
    # FragmentSpreadNode are reference to fragments
    if isinstance(node, FragmentSpreadNode):
        return
    if not node.selection_set:
        return
    # Replace selections by a more convenient list
    selections = []
    for field in node.selection_set.selections:
        if parse_directives(field.directives, variables=variables):
            selections.append(field)
            filter_by_directives(field, variables=variables)
    node.selection_set.selections = selections


def get_definition(doc, operation=None):
    """
        Choose the definition ("operation") to handle

        (This function may be renamed "get_operation_todo")
    """
    # Only consider "operation" nodes
    definitions = [d for d in doc.definitions if "operation" in d.keys]
    if operation is None or len(definitions) == 1:
        return definitions[0]
    for definition in definitions:
        # https://dgraph.io/docs/graphql/api/multiples/#multiple-operations
        # https://github.com/graphql/graphql-spec/issues/29
        if definition.name.value == operation:
            return definition
    return definitions[0]  # Or raise an Exception?


def handle_graphql(
        env, doc, model_mapping,
        variables={}, operation=None, allowed_fields={},
        introspection=False,
    ):
    response = {}
    try:
        data = parse_document(
            env, 
            doc,
            model_mapping,
            variables=variables,
            operation=operation,
            allowed_fields=allowed_fields,
            introspection=introspection,
        )
        response["data"] = data
    except Exception as e:
        raise e  # TODO: Remove the raise error on production
        _logger.critical(e)
        response["data"] = None
        response["errors"] = {"message": str(e)}  # + traceback.format_exc()
    return response


def parse_document(
        env, doc, model_mapping,
        variables={}, operation=None, allowed_fields={},
        introspection=False,
    ):
    if isinstance(doc, str):
        doc = parse(doc)
    doc, fragments = parse_fragments(doc, model_mapping)
    # A document can have many definitions
    definition = get_definition(doc, operation=operation)
    return parse_definition(
        env, definition, model_mapping,
        variables=variables,
        allowed_fields=allowed_fields,
        fragments=fragments,
        introspection=introspection,
    )


def parse_fragments(doc, model_mapping):
    """
        We will isolate the fragments for faster search.
        The types (odoo models) will be known later, we will resolve the FragmentSpreadNode
        the moment the type is known
    """
    fragments = {}
    definitions = []
    for node in doc.definitions:
        if not isinstance(node, FragmentDefinitionNode):
            definitions.append(node)
            continue
        name = node.name.value
        type_cond = node.type_condition.name.value
        # type_cond references an OBJECT TypeKind and can be
        # - a model: SaleOrder
        # - an introspection value: __schema
        tmp = model_mapping.get(type_cond)
        model = tmp._name if tmp is not None else type_cond
        fragments[(name, model)] = node
    doc.definitions = definitions
    return doc, fragments

def parse_directives(directives, variables={}):
    """
        Tells if the definition should be kept or removed
        (it only handles the `include if` and `skip if` directives for the moment)

        Currently return True to keep, False to skip
    """
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
    env,
    definition, model_mapping, variables, mutation, allowed_fields, fragments,
    introspection=False
):
    """
        Process the definition recursively
    """
    data = {}
    for field in definition.selection_set.selections:
        fname = field.alias and field.alias.value or field.name.value
        if introspection:
            res = handle_introspection(env, model_mapping, field, fragments=fragments)
            if res is not None:
                data[fname] = res
                continue
        model = model_mapping.get(field.name.value)
        if model is None:
            raise ValidationError("Model {} does not exists".format(field.name.value))
        data[fname], _ = parse_model_field(
            model,
            field,
            variables,
            mutation=mutation,
            allowed_fields=allowed_fields,
            fragments=fragments,
            # Only the first level can do limit/offset
            # The nested data are retrieved in batch to reduce SQL queries and improve performance
            # Therefore, we cannot apply the limit/offset on the batch queries
            do_limit_offset=True,
        )
    return data


def parse_definition(env, definition, model_mapping,
        variables=None,
        allowed_fields=None,
        fragments={}, 
        introspection=False,
    ):
    """
        Ensure every parameter is defined, then clean data before processing the definition
        by calling `_parse_definition`
    """
    if variables is None:
        variables = {}
    if allowed_fields is None:
        allowed_fields = {}
    dtype = definition.operation.value      # MUTATION OR QUERY
    if dtype not in ("query", "mutation"):  # does not support other types currently
        return None

    filter_by_directives(definition, variables)
    mutation = dtype == "mutation"
    return _parse_definition(
        env,
        definition,
        model_mapping,
        variables,
        mutation,
        allowed_fields,
        fragments,
        introspection=introspection,
    )

def slice_result(res, limit=None, offset=None):
    if limit is None and offset is None:
        return res
    offset = offset or 0
    limit = (limit or 0) + offset
    return res[offset:limit]

def slice_result(res, limit=None, offset=None):
    if limit is None and offset is None:
        return res
    offset = offset or 0
    limit = (limit or 0) + offset
    return res[offset:limit]

def relation_subgathers(records, relational_data, variables, fragments={}):
    """
        Retrieve nested data for relational fields

        When doing a query, we will have nested layers requiring the same treatment.
        To gain performance, every layer will be retrieved at once then dispatched
        through the corresponding records
    """
    subgathers = {}
    for submodel, fname, fields in relational_data:
        sub_records_ids = records.mapped(fname).ids
        aliases = []
        for f in fields:
            # Nb: Even if its the same field, the domain may change
            alias = f.alias and f.alias.value or f.name.value
            tmp, (limit, offset) = parse_model_field(
                submodel, f, variables, ids=sub_records_ids, fragments=fragments
            )
            data = {d["id"]: (i, d) for i, d in enumerate(tmp)}


            # https://stackoverflow.com/questions/8946868/is-there-a-pythonic-way-to-close-over-a-loop-variable
            def subgather(ids, data=data, limit=limit, offset=offset):
                if ids is False:
                    return None
                # We may not receive all ids since records may be archived
                if isinstance(ids, int):
                    return data.get(ids)[1]
                # Since the data are gathered in batch, then dispatched,
                # The order is lost and must be done again.
                res = slice_result([
                    d
                    for _, d in sorted(
                        (d for d in (data.get(rec_id) for rec_id in ids) if d),
                        key=lambda t: t[0],
                    )
                ], limit, offset)
                return res

            aliases.append((alias, subgather))

        subgathers[fname] = aliases
    return subgathers


def make_domain(domain, ids):
    """
        Utility to restrict domain to provided ids.
        If no ids are provided (or not one of list/tuple/int), nothing is done.
    """
    if ids:
        if isinstance(ids, (list, tuple)):
            domain = AND([[("id", "in", ids)], domain])
        elif isinstance(ids, int):
            domain = AND([[("id", "=", ids)], domain])
    return domain


# TODO: make it possible to define custom create/write handlers per models
def retrieve_records(model, field, variables, ids=None, mutation=False, do_limit_offset=False):
    """
        The main goal of this function is to perform a `search` and retrieve records
        If the query is a mutation:
        - Having no `domain` directive defined means we want to create some records
        - if `domain` directive is defined (even an empty list!), then it will perform a write
          Be very cautious not to provide an empty list and write every records by accident!
    """
    domain, kwargs, vals = parse_arguments(field.arguments, variables)
    limit = kwargs.get("limit")
    offset = kwargs.get("offset")
    search_args = (limit, offset)
    # Create is requested
    if mutation and domain is None: 
        try:
            records = model.create(vals)
        except Exception as e:
            if "DETAIL" in str(e):
                model.env.cr.rollback()
                raise ValidationError(str(e).split("\n")[0])
            raise
        return records, search_args

    # Retrieve records
    extra_search_args = {"order": kwargs.get("order")}
    if do_limit_offset:
        extra_search_args = kwargs
    domain = make_domain(domain or [], ids)
    records = model.search(domain, **extra_search_args)

    # Write is requested (mutation with domain provided)
    if mutation: 
        records.write(vals)

    return records, search_args

# Nb: the parameter "ids" is useful for relational fields
def parse_model_field(
    model, field, variables, ids=None, mutation=False, allowed_fields=None,
    fragments={}, do_limit_offset=False,
):
    """
        Nb: This function is (indirectly) recursive.
        It is called inside `relation_subgathers`

        This function will in order:
        1. Retrieve the requested records (only the id in )
    """
    if variables is None:
        variables = {}
    if allowed_fields is None:
        allowed_fields = {}
    records, search_args = retrieve_records(
        model,
        field,
        variables=variables,
        ids=ids,
        mutation=mutation,
        do_limit_offset=do_limit_offset,
    )
    # Short-circuit the whole code
    if not records:
        return [], search_args
    model_name = model._name

    # User may have forgotten to define subfields
    # We use an empty list to prevent it (rise an error instead?)
    fields = []
    if field.selection_set:
        # Resolve fragments
        for f in field.selection_set.selections:
            if not isinstance(f, FragmentSpreadNode):
                fields.append(f)
                continue
            frag = fragments.get((f.name.value, model_name))
            if not frag:
                continue
            for f in frag.selection_set.selections:
                fields.append(f)

    # Remove fields that are not allowed for the user
    # Nb: This fields can be defined by a developer, this is not native in Odoo
    allowed = allowed_fields.get(model_name)
    if allowed is not None:
        fields = [f for f in fields if f.name.value in allowed]
        if not fields:
            return [
                {"id": rid} for rid in records.ids
            ], search_args
    fields_names = [f.name.value for f in fields]

    # Get datas
    relational_data, fields_data = get_fields_data(model, fields)
    subgathers = relation_subgathers(records, relational_data, variables, fragments=fragments)
    records = records.read(fields_names, load=False)

    data = []
    for rec in records:
        tmp = {"id": rec["id"]}
        # Resolve the aliases for simple fields
        for fname, aliases in fields_data:
            for alias in aliases:
                value = rec[fname]
                # Binary fields are decoded into strings for serialization
                if isinstance(value, bytes):
                    value = value.decode()
                tmp[alias] = value
        # 1. Resolve the aliases for relational fields
        # 2. Replace id list by list of records data
        for fname, aliases in subgathers.items():
            ids = rec[fname]
            for alias, subgather in aliases:
                # Here we are retrieving the records data by their id
                tmp[alias] = subgather(ids)
        data.append(tmp)
    return data, search_args


def get_fields_data(model, fields):
    """
        This function does 2 things:
        - Retrieve aliases for fields
        - Split relational fields and the others
          - For relational fields, also retrieve an empty record of the relation
    """
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
def parse_arguments(args, variables=None):  # return a domain and kwargs
    if variables is None:
        variables = {}
    args = {a.name.value: value2py(a.value, variables) for a in args}
    domain = args.pop("domain", None)
    kwargs = {}
    for opt, cast in OPTIONS:
        value = args.pop(opt, None)
        if value:
            kwargs[opt] = cast(value)
    vals = args.pop("vals", {})
    return domain, kwargs, vals


def value2py(value, variables=None):
    if variables is None:
        variables = {}
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
