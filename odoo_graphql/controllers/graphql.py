from odoo import http
from odoo.http import request, content_disposition
# from odoo.service import security
import json
from ..utils import handle_graphql

import logging

_logger = logging.getLogger(__name__)


class GraphQL(http.Controller):
    @http.route(
        "/graphql", auth="none", methods=["POST"], csrf=False, save_session=False
    )
    def graphql(self):
        # https://spec.graphql.org/June2018/#sec-Response-Format
        print("=" * 50)
        query = request.httprequest.data.decode()  # request.graphqlrequest
        variables = {}
        operation = None
        user = request.env.user
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
                    dbname = auth.get("db", request.env.cr.dbname)
                    if login and password:
                        uid = request.env["res.users"].authenticate(
                            dbname,
                            login, password,
                            request.env
                        )
                        user = user.with_user(uid).browse(uid)
            except Exception as e:
                return json.dumps({
                    "errors": {"message": str(e)}  # + traceback.format_exc()
                })
        except Exception:  # We may have pure graphql query
            pass

        response = user.env["graphql.handler"].handle_graphql(
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
