import requests
import json

"""
    Use graphql query by providing credentials in the query (instead of using cookies)
"""

query = """query Tickets {
HelpdeskTicket(domain: $domain, limit: $limit) {	
    name
    description
    user: user_id @include(if: $user_info) {
        name
    }
    stage_id {
        name
    }
    partner_id @include(if: $partner_id)  {
        image: image_1920 @include(if: $image)
        user_id {
            name
        }
    }
}
}"""

res = requests.post(
    "http://localhost:8069/graphql",
    headers={
        'Content-Type': 'application/graphql'
    },
    data=json.dumps({
        "query": query,
        "variables": {
            "domain": [],
            "user_info": True,
            "partner_id": True, 
            "limit": 100
        },
        "auth": {
            "login": "dga",
            "password": "admin",
        }
    })
)
print(json.dumps(json.loads(res.content.decode()), indent=4))