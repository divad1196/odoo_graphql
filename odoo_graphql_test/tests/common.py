# -*- coding: utf-8 -*-

# from odoo.tests import common
from odoo.addons.product.tests.common import TestProductCommon

class TestGraphQlCommon(TestProductCommon):

    @classmethod
    def setUpClass(cls):
        super(TestGraphQlCommon, cls).setUpClass()

