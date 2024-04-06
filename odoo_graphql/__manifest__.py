{
    "name": "Odoo GraphQL",
    "version": "2.1",
    "author": "Gallay David",
    "category": "Extra Tools",
    "website": "https://github.com/divad1196/odoo_graphql",
    "summary": "Allow to use GraphQL with Odoo",
    "depends": [
        "base",
    ],
    "data": [
        "templates/graphiql.xml",
    ],
    "external_dependencies": {
        "python": ["graphql-core"],
    },
    "images": [
        "static/description/thumbnail.jpg",
    ],
    "installable": True,
    "auto_install": False,
}
