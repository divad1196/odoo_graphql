# from odoo.tests import common
from odoo.addons.product.tests.common import TestProductCommon


class TestGraphQlCommonWithoutIntrospection(TestProductCommon):
    def handle_query(self, *args, **kwargs):
        return self.env["graphql.handler"].handle_graphql(*args, **kwargs)
        # return self.env["graphql.handler"].handle_query(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        super(TestGraphQlCommonWithoutIntrospection, cls).setUpClass()
        cls.env["ir.config_parameter"].search(
            [
                ("key", "=", "odoo_graphql.introspection"),
            ]
        ).unlink()


class TestGraphQlCommon(TestGraphQlCommonWithoutIntrospection):
    @classmethod
    def setUpClass(cls):
        super(TestGraphQlCommon, cls).setUpClass()
        cls.env["ir.config_parameter"].create(
            {
                "key": "odoo_graphql.introspection",
                "value": "True",
            }
        )
