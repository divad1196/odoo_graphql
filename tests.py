# from graphql.language.ast import (
#     ArgumentNode,
#     DocumentNode,
#     FieldNode,
#     OperationDefinitionNode,
# )


from graphql import parse
parse_document = odoo.addons.odoo_graphql.parse_document
get_model_mapping = odoo.addons.odoo_graphql.utils.get_model_mapping

document = parse("""
{
  SaleOrder(domain: [["id", "<", 50]]) {
    amount_total
    order_line {
      name
      price_total
    }
  }
}
""")

data = parse_document(env, document)
sales = data["SaleOrder"]
