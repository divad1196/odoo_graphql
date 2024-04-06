# Part of Odoo. See LICENSE file for full copyright and licensing details.

from .common import TestGraphQlCommon
from .utils import firstMatching, open_query


class TestArchivedRelationship(TestGraphQlCommon):
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
