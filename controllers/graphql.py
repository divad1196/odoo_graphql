from odoo import http
from odoo.http import request
import json
from graphql import parse
from ..utils import parse_document


class GraphQL(http.Controller):
    @http.route(
        "/graphql", auth="public", type="http",
        website=True, sitemap=False, csrf=False, cors="*"
    )
    def graphql(self):
        return json.dumps(
            parse_document(
                request.env, parse(request.graphqlrequest)
            )
        )
