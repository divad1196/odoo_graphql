# TODO



* Performance: Faire les requêtes par niveau et réassembler ensuite ?
  Sinon, voir si je peux améliorer le pré-assemblage actuel autrement

* Support for mutations: Elles sont sur 1 seul niveau apparement, donc ok?
  
* Support for operation name

* add timeout on python side

* Use the correct [response format](https://spec.graphql.org/June2018/#sec-Response-Format)

  



* See my side project "odoo_nginx_proxy" to handle cors and cache

  ```bash
  HOST_IP=$(ip a show dev eno1 | grep -Po '(?<=inet ).*(?=/)')
  docker run -p 8100:80 -e "PROXY=http://$HOST_IP:8069" odoo_nginx
  ```

  

