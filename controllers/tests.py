# from graphql.language.ast import (
#     ArgumentNode,
#     DocumentNode,
#     FieldNode,
#     OperationDefinitionNode,
# )


from graphql import parse
parse_document = odoo.addons.odoo_graphql.parse_document

document = parse("""
{
  SaleOrder(domain: [["id", "<", 17]]) {
    amount_total
    order_line {
      name
      price_total
    }
  }
}
""")

data = parse_document(env, document)
d = data["SaleOrder"][0]
