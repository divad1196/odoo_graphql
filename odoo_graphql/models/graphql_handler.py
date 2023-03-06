# -*- coding: utf-8 -*-

from odoo import models, tools
from ..graphql_resolver import handle_graphql
from ..utils import model2name
import json

import logging

_logger = logging.getLogger(__name__)


class GraphQLHandler(models.TransientModel):
    _name = "graphql.handler"

    def has_introspection(self):
        introspection = self.env['ir.config_parameter'].sudo().get_param(
            'odoo_graphql.introspection', ""
        ).strip().lower() == "true"
        return introspection

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
        field_mapping={},
        allowed_fields={},
    ):
        introspection = self.has_introspection()
        # This is the function from ..utils.py file
        return handle_graphql(
            self.env,
            query,
            model_mapping,
            variables=variables,
            operation=operation,
            field_mapping=field_mapping,
            allowed_fields=allowed_fields,
            introspection=introspection
        )

    def handle_graphql(
        self,
        query,
        variables={},
        operation=None,
    ):
        model_mapping = self.get_model_mapping()
        field_mapping = self.get_fields_mapping()
        allowed_fields = self.get_allowed_fields()
        extra_variables = self.get_extra_variables()
        variables = {**extra_variables, **variables}

        response = self._handle_graphql(
            query,
            model_mapping,
            variables=variables,
            operation=operation,
            field_mapping=field_mapping,
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
        # tools.ormcache can not store records directly, we will only store their names
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
    
    @tools.ormcache()
    def get_fields_mapping(self):
        """
            return a mapping per model of their fields'type.
            {
                "sale.order": {
                    "create_date": "date"
                }
            }
            The goal is to be able to call the correct serializer
        """
        self = self.sudo()
        fields = self.env["ir.model.fields"].search([
            ("model_id.transient", "=", False),
            ("ttype", "in", (
                "date", "datetime",
            ))
        ])
        data = {}
        for f in fields:
            model = data.setdefault(f.model_id.model, {})
            model[f.name] = f.ttype
        return data

    @tools.ormcache()
    def get_fields_mapping_by_type(self):
        """
            return a mapping per model of their fields group by type.
            {
                "sale.order": {
                    "date": ["create_date"]
                }
            }
            The goal is to be able to call the correct serializer
        """
        self = self.sudo()
        fields = self.env["ir.model.fields"].search([
            ("model_id.transient", "=", False),
            ("ttype", "in", (
                "date", "datetime",
            ))
        ])
        data = {}
        for f in fields:
            model = data.setdefault(f.model_id.model, {})
            field_type = model.setdefault(f.ttype, [])
            field_type.append(f.name)
        return {}

    def get_extra_variables(self):
        return self.env.context
