import json
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class TestApollo(http.Controller):
    @http.route(
        "/graphql/test-modules/apollo", type="http", website=True, sitemap=False
    )
    def test_apollo(self):
        return request.render("odoo_graphql_test.test-graphql")

    @http.route(
        "/graphql/test-modules/sse", type="http", website=True, sitemap=False
    )
    def test_sse(self):
        return request.render("odoo_graphql_test.test-sse")
