# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.osv import expression

from .common import TestGraphQlCommon
from .utils import contains, firstMatching, get_query, open_query


class TestField(TestGraphQlCommon):
    # def setUp(self):
    #     super().setUp()

    def test_empty_date_fields(self):
        with open_query("dummy.gql") as f:
            query = f.read()

        dummy = self.env["graphql.dummy.default.test.model"].create({})
        res = self.env["graphql.handler"].handle_query(query)
        print(res)