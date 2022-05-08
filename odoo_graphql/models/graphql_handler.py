# -*- coding: utf-8 -*-

from odoo import models, tools
from ..utils import handle_graphql, model2name
import json

import logging

_logger = logging.getLogger(__name__)


class GraphQLHandler(models.TransientModel):
    _name = "graphql.handler"

    def handle_query(self, query):
        if isinstance(query, bytes):
            query = query.decode()
        variables = {}
        operation = None
        try:  # Usual format is json with "query" and "variables" entries
            data = json.loads(query)
            query = data["query"]
            variables = data.get("variables", {})
            operation = data.get("operationName")
            # An error when authenticating must be sent back
            try:
                auth = data.get("auth", {})
                if auth:
                    login = auth.get("login")
                    password = auth.get("password")
                    if login and password:
                        uid = self.env["res.users"].authenticate(
                            self.env.cr.dbname,
                            login, password,
                            self.env
                        )
                        self = self.with_user(uid)
            except Exception as e:
                return {
                    "errors": {"message": str(e)}  # + traceback.format_exc()
                }
        except Exception:  # We may have pure graphql query
            pass

        response = self.handle_graphql(
            query,
            variables=variables,
            operation=operation,
        )
        return response


    def _handle_graphql(
        self,
        query,
        model_mapping,
        variables={},
        operation=None,
        allowed_fields={},
    ):
        return handle_graphql(
            query,
            model_mapping,
            variables=variables,
            operation=operation,
            allowed_fields=allowed_fields,
        )

    def handle_graphql(
        self,
        query,
        variables={},
        operation=None,
    ):
        model_mapping = self.get_model_mapping()
        allowed_fields = self.get_allowed_fields()
        extra_variables = self.get_extra_variables()
        variables = {**extra_variables, **variables}

        response = self._handle_graphql(
            query,
            model_mapping,
            variables=variables,
            operation=operation,
            allowed_fields=allowed_fields,
        )
        return response

    # @tools.ormcache()  # Unable to use a closed cursor, we can not cache cursor and thus models
    def get_model_mapping(self):
        allowed = set(self._get_allowed_models())
        return {
            model2name(name): model
            for name, model in self.env.items()
            if name in allowed
        }

    @tools.ormcache()
    def _get_allowed_models(self, mode="read"):

        ir_model_ids = (
            self.sudo()
            .env["ir.model"]
            .search(
                [
                    ("transient", "=", False),
                ]
            )
        )

        ir_model_ids = ir_model_ids.filtered(lambda m: m.model in self.env)

        # Check if access exists that allow the user to get informations
        model_access = self.env["ir.model.access"]
        model_by_rights = ir_model_ids.filtered(
            lambda m: model_access.check(m.model, mode=mode, raise_exception=False)
        )

        # Check if rules exists that may allow the user to get informations
        # E.g. Public user can access some products
        ir_rule = self.env["ir.rule"]
        model_by_rules = ir_model_ids.filtered(
            lambda m: ir_rule._get_rules(m.model, mode=mode)
        )

        model_access = model_by_rights | model_by_rules

        return ir_model_ids.mapped("model")

    def get_allowed_models(self, mode="read"):
        ir_model_ids = (
            self.sudo()
            .env["ir.model"]
            .search([("model", "in", self._get_allowed_models())])
        )
        return ir_model_ids

    @tools.ormcache()
    def get_allowed_fields(self):
        # Return a dictionnary containing for each model
        # a list of fields allowed for the current user
        # None allows all fields,
        # Empty list allows no field.
        # e.g.: {"helpdesk.ticket": []}
        return {}

    def get_extra_variables(self):
        return self.env.context

    def _schema_field(self, ir_field, reverse_mapping):
        ttype = ir_field.ttype
        if ir_field.name == "id":
            ttype = "ID"
        elif ttype == "many2one":
            ttype = reverse_mapping.get(ir_field.relation, "Int")
        elif ttype in ("many2many", "one2many"):
            ttype = "[{ttype}]".format(
                ttype=reverse_mapping.get(ir_field.relation, "Int")
            )
        elif ttype in ("integer",):
            ttype = "Int"
        elif ttype in ("float", "monetary"):
            ttype = "Float"
        elif ttype in ("boolean",):
            ttype = "Boolean"
        elif ttype in ("selection",):
            ttype = "[String]"
        else:
            ttype = "String"

        if ir_field.required:
            ttype += "!"

        res = "{name}: {ttype}".format(
            name=ir_field.name,
            ttype=ttype,
        )
        return res

    def _schema(self, ir_model, reverse_mapping, allowed_fields):
        name = reverse_mapping.get(ir_model.model)
        res = "type {name} {{\n".format(name=name)

        fields = ir_model.field_id
        allowed_fields = allowed_fields.get(ir_model.model)
        if allowed_fields is not None:
            fields.filtered(lambda f: f in allowed_fields)

        for f in fields:
            res += "    " + self._schema_field(f, reverse_mapping) + "\n"

        res += "}\n"
        return res

    def schema(self):
        ir_model_ids = self.get_allowed_models()
        mapping = self.get_model_mapping()
        reverse_mapping = {m._name: name for name, m in mapping.items()}
        allowed_fields = self.get_allowed_fields()

        res = "\n".join(
            self._schema(m, reverse_mapping, allowed_fields) for m in ir_model_ids
        )
        return res
