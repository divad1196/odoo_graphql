async function odoo_authenticate(url, database, login, password) {
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
    return fetch(url, parameters).then(r => r.json());
}

async function odoo_logout(url) {
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
    fetch(url, parameters);
}

function graphqlbuilder(url) {
    async function graphql(query, variables={}) {
        return fetch(url, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/graphql',
            },
            body: JSON.stringify({
                query: query,
                variables: variables
            })
        }).then(r => r.json())
    }
    return graphql;
}

function odoo_builder(url, database) {
    return {
        login: (login, password) => {
            return odoo_authenticate(url + "/web/session/authenticate", database, login, password);
        },
        logout: () => {return odoo_logout(url + "/web/session/destroy");},
        graphql: graphqlbuilder(url + '/graphql'),
    }
}