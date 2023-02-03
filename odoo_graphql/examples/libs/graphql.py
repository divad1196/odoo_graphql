import graphql
import requests
import json

class Graphql:
    def __init__(self, url, database):
        self._url = url
        self._database = database
        self._session = requests.session()
    def login(self, login, password):
        res = self._session.post(
            self._url + "/web/session/authenticate",
            headers={
                'Content-Type': 'application/json'
            },
            data=json.dumps({
                "jsonrpc": "2.0",
                "id": None,
                "method": "call",
                "params": {
                    "db": self._database,
                    "login": login,
                    "password": password,
                }
            })
        )
        return res
    def logout(self):
        res = self._session.post(
            self._url + "/web/session/destroy",
            headers={
                'Content-Type': 'application/json'
            },
            data=json.dumps({
                "jsonrpc": "2.0",
                "id": None,
            })
        )
        return res
    def graphql(self, query, variables={}, operationName=None):
        body = {
                "query": query,
                "variables": variables,
            }
        if operationName:
            body["operationName"] = str(operationName)
        res = self._session.post(
            self._url + "/graphql",
            headers={
                'Content-Type': 'application/graphql'
            },
            data=json.dumps(body)
        )
        return res