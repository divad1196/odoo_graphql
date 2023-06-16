# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase
from .common import TestGraphQlCommon
from .utils import get_query, contains, firstMatching, pretty_print

class TestFilteredRelationship(TestGraphQlCommon):

    def test_filtered_relationship(self):
        query = get_query("contact_filtered_tag.gql")
        # These are demo data
        partner = self.env.ref("base.res_partner_address_15") # Brandon Freeman
        tag = self.env.ref("base.res_partner_category_8")
        partner.category_id |= tag

        res = firstMatching(self.handle_query(
            query,
            variables={
                "domain": []
            }
        )["data"]["ResPartner"], lambda p: p["id"] == partner.id)

        assert res["category_id"] is not None
        res = firstMatching(self.handle_query(
            query,
            variables={
                "domain": [("1", "=", "0")]
            }
        )["data"]["ResPartner"], lambda p: p["id"] == partner.id)
        assert res["category_id"] is None
