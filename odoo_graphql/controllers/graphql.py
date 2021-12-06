from odoo import http
from odoo.http import request
import json
from ..utils import handle_graphql, get_model_mapping

import logging

_logger = logging.getLogger(__name__)


class GraphQL(http.Controller):
    @http.route(
        "/graphql", auth="public", type="http", website=True, sitemap=False, csrf=False
    )
    def graphql(self):
        # https://spec.graphql.org/June2018/#sec-Response-Format
        query = request.httprequest.data.decode()  # request.graphqlrequest
        variables = {}
        operation = None
        try:  # Usual format is json with "query" and "variables" entries
            data = json.loads(query)
            query = data["query"]
            variables = data.get("variables", {})
            operation = data.get("operationName")
        except Exception:
            pass

        model_mapping = self.get_model_mapping()
        allowed_fields = self.get_allowed_fields()
        extra_variables = self.get_extra_variables()
        variables = {**extra_variables, **variables}

        response = handle_graphql(
            query,
            model_mapping,
            variables=variables,
            operation=operation,
            allowed_fields=allowed_fields,
        )
        return json.dumps(response)

    def get_allowed_fields(self):
        # Return a dictionnary containing for each model
        # a list of fields allowed for the current user
        # None allows all fields,
        # Empty list allows no field.
        return {"helpdesk.ticket": []}

    def get_model_mapping(self):
        return get_model_mapping(request.env)

    def get_extra_variables(self):
        return request.env.context
