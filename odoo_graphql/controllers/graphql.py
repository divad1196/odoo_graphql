from odoo import http
from odoo.http import request, content_disposition
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

        response = request.env["graphql.handler"].handle_graphql(
            query,
            variables=variables,
            operation=operation,
        )
        return json.dumps(response)

    @http.route(
        "/graphql/schema",
        auth="public",
        type="http",
        website=True,
        sitemap=False,
        csrf=False,
    )
    def graphql_schema(self):
        # Nb: Not meant to be displayed
        content = request.env["graphql.handler"].schema()
        response = request.make_response(
            content,
            headers=[
                ("Content-Type", "application/graphql"),
                ("Content-Disposition", content_disposition("schema.graphql")),
            ],
        )
        return response
