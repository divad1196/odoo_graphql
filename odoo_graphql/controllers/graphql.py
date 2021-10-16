from odoo import http
from odoo.http import request
import json
from ..utils import handle_graphql

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

        response = handle_graphql(
            request.env, query, variables=variables, operation=operation
        )
        return json.dumps(response)
