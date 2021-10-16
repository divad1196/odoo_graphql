import requests
# from graphql import parse

query = """
query Test {
  products: ProductTemplate(domain: []) {
    name
    list_price
    variants: product_variant_ids(limit: 5) {
      name
    }
    variants_ids: product_variant_ids
  }
}
"""


def test():
    res = requests.post(
        "http://localhost:8069/graphql",
        data=query,
        params={"db": "graphql"},
        # headers={"Content-type": "text/"},
        headers={"Content-type": "application/graphql"},
    )
    print(res.content.decode())


test()
