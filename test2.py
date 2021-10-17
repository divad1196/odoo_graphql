import requests
# from graphql import parse

query = """
query Test {
  ProductTemplate(domain: []) {
    name
    variants: product_variant_ids {
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
        params={"db": "open-net-test"},
        # headers={"Content-type": "text/"},
        headers={"Content-type": "application/graphql"},
    )
    print(res.content.decode())


test()
