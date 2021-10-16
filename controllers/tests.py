from .utils import parse_document

from graphql import parse

document = parse("""
{
  topic(name:"graphql") {
    stargazerCount
    relatedTopics {
      name
      stargazerCount
    }
  }
}
""")

parse("""
{
  SaleOrder(domain: [['id', '<', 50]]) {
    amount_total
    order_line {
      name
      price_total
    }
  }
}
""")

# from graphql.language.ast import (
#     ArgumentNode,
#     DocumentNode,
#     FieldNode,
#     OperationDefinitionNode,
# )