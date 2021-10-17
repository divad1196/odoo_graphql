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
    var res = (await fetch(url + "/web/session/authenticate", parameters)).json();
    return res;
}

function graphqlbuilder(url) {
    function graphql(query, variables={}) {
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
            })
    }
    return graphql;
}


// var graphql = graphqlbuilder('http://192.168.1.113:8100/graphql')