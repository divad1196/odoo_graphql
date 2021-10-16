# -*- coding: utf-8 -*-

from odoo import models, tools
from ..utils import handle_graphql, model2name


import logging

_logger = logging.getLogger(__name__)


class GraphQLHandler(models.TransientModel):
    _name = "graphql.handler"

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

    # @tools.ormcache()  # Unable to use a closed cursor
    def get_models(self):
        mapping = {name: model for name, model in self.env.items()}
        mapping.pop("graphql.handler", None)
        return mapping

    # @tools.ormcache()  # Unable to use a closed cursor
    def get_model_mapping(self):
        return {model2name(name): model for name, model in self.get_models().items()}

    def get_allowed_fields(self):
        # Return a dictionnary containing for each model
        # a list of fields allowed for the current user
        # None allows all fields,
        # Empty list allows no field.
        # e.g.: {"helpdesk.ticket": []}
        return {}

    def get_extra_variables(self):
        return self.env.context
