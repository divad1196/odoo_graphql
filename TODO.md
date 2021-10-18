# TODO



* Faire le traitement graphql **AU DEBUT** pour éviter de répeter certaines actions
  => créer une structure intermédiaire avec les fonctions nécessaires après/pendant le filtrage
  * Transformation des arguments
  * Préparation des champs à traiter (cf alias et champs relationnels)

* Support for mutations?
  Dans la plupart des cas, on voudra passer par une route pour faire du traitement spécifique
  On peut imaginer faire du CRUD sur les tickets par exemple.
  
* Support for operation name

* add timeout on python side

* Use the correct [response format](https://spec.graphql.org/June2018/#sec-Response-Format)

  



* See my side project "odoo_nginx_proxy" to handle cors and cache

  ```bash
  HOST_IP=$(ip a show dev eno1 | grep -Po '(?<=inet ).*(?=/)')
  docker run -p 8100:80 -e "PROXY=http://$HOST_IP:8069" odoo_nginx
  ```

  

