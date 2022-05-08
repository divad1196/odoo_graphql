"""
    Basique graphql usage (authentication made using stored cookies)
"""

import json
from libs.graphql import Graphql


graphql = Graphql("http://localhost:8069", "graphql")
graphql.login("admin", "admin")


query = """mutation InsertResPartner {
    insertResPartner: ResPartner(
        vals: {
            active: true,
            name: "Company 1",
            company_type: "company",
            city: "Pradejov",
            street: "Kosmicka 22",
            street2: "",
            zip: "12346",
            comment: "<p>bla bla bla</p>",
            phone: "",
            mobile: "777111222",
            website: "http://xxx.cz",
            email: "nejaky@email.com",
            lang: "fr_FR",
            employee: false,
            currency_id: 22
        }
    )
    {
        active
        city
        comment
        company_type
        id
        name
        phone
        mobile
        website
        email
        lang
        street
        street2
        zip
        currency_id
        employee
    }
}"""

res = graphql.graphql(query)
print(res.content.decode())

query2 = """query Tickets {
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
res = graphql.graphql(query2, {
    "domain": [],
    "user_info": True,
    "partner_id": True, 
    "limit": 100
})
print(json.dumps(json.loads(res.content.decode()), indent=4))
