const _odoo_utils = {
    odoo_authenticate: async function(url, database, login, password) {
        headers = new Headers({
            'Content-Type': 'application/json'
        });
        parameters = {
            method: 'POST',
            headers: headers,
            credentials: 'include',
            mode: 'cors',  // https://developer.mozilla.org/en-US/docs/Web/API/Request/mode
            // referrerPolicy: "strict-origin-when-cross-origin", // no-referrer
            cache: 'default',
            body: JSON.stringify({
                "jsonrpc": "2.0",
                "id": null,
                "method": "call",
                "params": {
                    "db": database,
                    "login": login,
                    "password": password
                }
            })
        };
        return fetch(url, parameters).then(r => r.json()).then((data) => {
            if(data.result) {
                return data.result;
            }
            if(data.error && data.error.code != 100) {
                throw data.error.message;
            }
            return null;
        });
    },

    odoo_session: async function(url) {
        headers = new Headers({
            'Content-Type': 'application/json'
        });
        parameters = {
            method: 'POST',
            headers: headers,
            credentials: 'include',
            mode: 'cors',  // https://developer.mozilla.org/en-US/docs/Web/API/Request/mode
            // referrerPolicy: "strict-origin-when-cross-origin", // no-referrer
            cache: 'default',
            body: JSON.stringify({
                "jsonrpc": "2.0",
                "id": null,
            })
        };
        return fetch(url, parameters).then(r => r.json()).then((data) => {
            if(data.result) {
                return data.result;
            }
            if(data.error && data.error.code != 100) {
                throw data.error.message;
            }
            return null;
        });
    },

    odoo_logout: async function(url) {
        headers = new Headers({
            'Content-Type': 'application/json'
        });
        parameters = {
            method: 'POST',
            headers: headers,
            credentials: 'include',
            mode: 'cors',  // https://developer.mozilla.org/en-US/docs/Web/API/Request/mode
            // referrerPolicy: "strict-origin-when-cross-origin", // no-referrer
            cache: 'default',
            body: JSON.stringify({
                "jsonrpc": "2.0",
                "id": null,
            })
        };
        return fetch(url, parameters);
    },

    graphqlbuilder: function(url) {
        async function graphql(query, variables={}, operationName=null) {
            let body = {
                query: query,
                variables: variables
            };
            if(operationName) {
                body["operationName"] = operationName.toString();
            }
            return fetch(url, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/graphql',
                },
                body: JSON.stringify(body)
            }).then(r => r.json()).then((r) => {
                if(r.errors)
                    throw r.errors;
                return r.data;
            })
        }
        return graphql;
    }
}


function odoo_builder(url, database) {
    return {
        login: (login, password) => {
            return _odoo_utils.odoo_authenticate(url + "/web/session/authenticate", database, login, password);
        },
        logout: () => {return _odoo_utils.odoo_logout(url + "/web/session/destroy");},
        graphql: _odoo_utils.graphqlbuilder(url + '/graphql'),
        session: () => {return _odoo_utils.odoo_session(url + '/web/session/get_session_info')},
    }
}