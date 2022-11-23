

```bash
docker run --rm -p 8100:80 --name graphql_proxy -e 'PROXY=http://192.168.1.113:8069' -e 'CORS="http://official.localhost:8010"' odoo_nginx_proxy  # Nb: protocol, domain AND port must be correct for cors !
python3 -m http.server 8010   # official.localhost:8010
python3 -m http.server 8020   # malicious.localhost:8020

```

