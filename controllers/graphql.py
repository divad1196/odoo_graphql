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
        query = request.graphqlrequest
        variables = {}
        try:
            data = json.loads(request.graphqlrequest)
            query = data["query"]
            variables = data.get("variables", {})
        except Exception:
            pass

        return json.dumps(
            parse_document(
                request.env, parse(query), variables=variables
            )
        )
