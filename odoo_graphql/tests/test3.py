import requests
import json

def authenticate(url, database, login, password):
    data = json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "method": "call",
            "params": {
                "db": database,
                "login": login,
                "password": password
            }
        },
        indent=4
    )
    print(data)
    res = requests.post(
        url + "/web/session/authenticate",
        headers={'Content-Type': "application/json"},
        data=data,
    )
    return res
