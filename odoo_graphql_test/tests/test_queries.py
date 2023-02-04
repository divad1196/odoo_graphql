# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase
from .common import TestGraphQlCommon
from .utils import open_query, contains, firstMatching, pretty_print

class TestName(TestGraphQlCommon):

    # def setUp(self):
    #     super().setUp()
  
    def test_contact(self):
        print("\n" * 20)
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
  
    def test_introsepction_type(self):
        with open_query("type.gql") as f:
            query = f.read()
        # Must not crash
        res = self.env["graphql.handler"].handle_query(query)
  
    def test_introspection(self):
        print("\n" * 20)
        print("=" * 50)
        with open_query("introspection.gql") as f:
            query = f.read()
        res = self.env["graphql.handler"].handle_query(query)
        # print("\n" * 3)
        # print("v" * 50)
        # pretty_print(res)