from odoo import http
from odoo.http import request, content_disposition
from odoo.exceptions import ValidationError
import werkzeug
import json

import logging

_logger = logging.getLogger(__name__)


class GraphQL(http.Controller):
    @http.route(
        "/graphql", auth="public", type="http", website=True, sitemap=False, csrf=False,
    )
    def graphql(self):
        # https://spec.graphql.org/June2018/#sec-Response-Format
        query = request.httprequest.data.decode()  # request.graphqlrequest
        response = request.env["graphql.handler"].handle_query(query)
        payload = json.dumps(response, indent=4)
        # print(payload)
        return payload

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

    @http.route(
        "/graphiql", type="http", website=True, sitemap=False
    )
    def graphiql(self):
        introspection = request.env["graphql.handler"].has_introspection()
        if not introspection:
            raise werkzeug.exceptions.NotFound()
            # raise ValidationError("Introspection is not allowed")
        return request.render("odoo_graphql.graphiql")