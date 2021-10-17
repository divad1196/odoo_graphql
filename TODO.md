# TODO



* Support for mutations?
  Dans la plupart des cas, on voudra passer par une route pour faire du traitement spécifique
  On peut imaginer faire du CRUD sur les tickets par exemple.
* Support for operation name
* Support for directives



* See my side project "odoo_nginx_proxy" to handle cors and cache

  ```bash
  HOST_IP=$(ip a show dev eno1 | grep -Po '(?<=inet ).*(?=/)')
  docker run -p 8100:80 -e "PROXY=http://$HOST_IP:8069" -e 'CORS=*' odoo_nginx_proxy
  ```

  

