# -*- coding: utf-8 -*-

# from odoo.tests import common
from odoo.addons.product.tests.common import TestProductCommon

class TestGraphQlCommonWithoutIntrospection(TestProductCommon):

    @classmethod
    def setUpClass(cls):
        super(TestGraphQlCommonWithoutIntrospection, cls).setUpClass()



class TestGraphQlCommon(TestGraphQlCommonWithoutIntrospection):

    @classmethod
    def setUpClass(cls):
        super(TestGraphQlCommon, cls).setUpClass()
        cls.env['ir.config_parameter'].create({
            "key": "odoo_graphql.introspection",
            "value": "True",
        })

