# README



### CORS

Not handled in this module.
If needed, use a proxy or a module allowing cors in Odoo.
E.g.: My side project [odoo_nginx_proxy](https://github.com/divad1196/odoo_nginx_proxy)

```bash
HOST_IP=$(ip a show dev eno1 | grep -Po '(?<=inet ).*(?=/)')
docker run -p 8100:80 -e "PROXY=http://$HOST_IP:8069" odoo_nginx
```

Nb: For production, explicitly set the CORS environnement variable



#### Reminder

* The following headers must be set and **NOT** be using the wildcard

  * Access-Control-Allow-Origin
  * Access-Control-Allow-Methods
  * Access-Control-Allow-Headers

* You will probably need to deal with creadentials, the following header value must be "true"
  Access-Control-Allow-Credentials: true

* fetch won't allows cors and credentials by default

  ```js
  credentials: 'include',
  mode: 'cors',  // https://developer.mozilla.org/en-US/docs/Web/API/Request/mode
  ```

  





### Tests

Run a server for dev

```bash
python3 -m http.server 8200                
```

The frontend_alpines.html file is there to provide an example