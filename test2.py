import requests

query2 = """
{
  SaleOrder(domain: [["id", "<", 50]]) {
    amount_total
    order_line {
      name
      price_total
    }
  }
}
"""

query = """
{
  ProductTemplate(domain: []) {
    name
  }
}
"""

query = """
{
  ProductTemplate(domain: []) {
    name
    product_variant_ids {
      name
    }
  }
}
"""


res = requests.post(
    "http://localhost:8069/graphql?database=open-net-test",
    data=query,
    params={"db": "open-net-test"},
    # headers={"Content-type": "text/"},
    headers={"Content-type": "application/graphql"},
)
print(res.content.decode())