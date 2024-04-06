{
    "name": "Odoo GraphQL Tests",
    "version": "1.0",
    "author": "Gallay David",
    "category": "Extra Tools",
    "license": "LGPL-3",
    "website": "https://github.com/divad1196/odoo_graphql",
    "summary": "This test the odoo_graphql module. It install other module for the tests that must not be added to the main module",
    "depends": ["product", "odoo_graphql"],
    "data": [
        "templates/interface.xml",
    ],
    "installable": True,
    "auto_install": False,
}
