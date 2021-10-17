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
    lines: order_line {
      name
      price_total
    }
    line_ids: order_line
  }
}
""")


data = parse_document(env, document)
sales = data["SaleOrder"]




query = """
  query HeroNameAndFriends($episode: Episode) {
    hero(episode: $episode) {
      name
      friends {
        name
      }
    }
  }
"""

variables = {
  "episode": "JEDI"
}

document = parse(query)