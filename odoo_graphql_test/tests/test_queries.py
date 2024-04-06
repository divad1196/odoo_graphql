# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.osv import expression

from .common import TestGraphQlCommon
from .utils import contains, firstMatching, get_query, open_query


class TestName(TestGraphQlCommon):
    # def setUp(self):
    #     super().setUp()

    def test_contact(self):
        with open_query("contacts.gql") as f:
            query = f.read()
        res = self.env["graphql.handler"].handle_query(query)
        partner = firstMatching(
            res["data"]["ResPartner"], lambda p: p["parent_id"] is not None
        )
        self.assertTrue(contains(partner, ("id", "name", "parent_id")))
        parent = partner["parent_id"]
        self.assertTrue(contains(parent, ("id", "name", "email")))
        # self.assertIn(("id", "name", "email"), parent)

    def test_introsepction_type(self):
        with open_query("type.gql") as f:
            query = f.read()
        # Must not crash
        res = self.env["graphql.handler"].handle_query(query)

    def test_introspection(self):
        with open_query("introspection.gql") as f:
            query = f.read()
        res = self.env["graphql.handler"].handle_query(query)
        # print("\n" * 3)
        # print("v" * 50)
        # pretty_print(res)

    def test_many2many_relationship(self):
        with open_query("contacts.gql") as f:
            query = f.read()
        # These are demo data
        partner = self.env.ref("base.res_partner_address_15")  # Brandon Freeman
        tag = self.env.ref("base.res_partner_category_8")
        partner.category_id |= tag
        res = firstMatching(
            self.handle_query(query)["data"]["ResPartner"],
            lambda p: p["id"] == partner.id,
        )
        assert res["category_id"]
        tag.active = False
        res = firstMatching(
            self.handle_query(query)["data"]["ResPartner"],
            lambda p: p["id"] == partner.id,
        )
        assert not res["category_id"]

    def test_many2one_relationship(self):
        with open_query("contacts.gql") as f:
            query = f.read()
        # These are demo data
        partner = self.env.ref("base.res_partner_address_15")  # Brandon Freeman
        user = self.env.ref("base.user_demo")
        partner.user_id = user
        res = firstMatching(
            self.handle_query(query)["data"]["ResPartner"],
            lambda p: p["id"] == partner.id,
        )
        assert res["user_id"] is not None
        user.active = False
        res = firstMatching(
            self.handle_query(query)["data"]["ResPartner"],
            lambda p: p["id"] == partner.id,
        )
        assert res["user_id"] is None
        user.active = True

    def test_filtered_relationship(self):
        query = get_query("contact_filtered_tag.gql")
        # These are demo data
        partner = self.env.ref("base.res_partner_address_15")  # Brandon Freeman
        tag = self.env.ref("base.res_partner_category_8")
        partner.category_id |= tag

        res = firstMatching(
            self.handle_query(query, variables={"domain": []})["data"]["ResPartner"],
            lambda p: p["id"] == partner.id,
        )
        assert res["category_id"]
        res = firstMatching(
            self.handle_query(query, variables={"domain": expression.FALSE_DOMAIN})[
                "data"
            ]["ResPartner"],
            lambda p: p["id"] == partner.id,
        )
        assert not res["category_id"]
