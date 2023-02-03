# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase
from .common import TestGraphQlCommon
from .utils import open_query, contains, firstMatching

class TestName(TestGraphQlCommon):

    # def setUp(self):
    #     super().setUp()
  
    def test_contact(self):
        print("\n" * 50)
        print("=" * 50)
        with open_query("contacts.gql") as f:
            query = f.read()
        res = self.env["graphql.handler"].handle_query(query)
        print(res)
        partner = firstMatching(res["data"]["ResPartner"], lambda p: p["parent_id"] is not None)
        print(partner)
        self.assertTrue(contains(partner, ("id", "name", "parent_id")))
        parent = partner["parent_id"]
        print(parent)
        self.assertTrue(contains(parent, ("id", "name", "email")))
        # self.assertIn(("id", "name", "email"), parent)
  
    # def test_introspection(self):
    #     print("\n" * 50)
    #     print("=" * 50)
    #     with open_query("introspection.gql") as f:
    #         query = f.read()
    #     res = self.env["graphql.handler"].handle_query(query)
    #     print(res)