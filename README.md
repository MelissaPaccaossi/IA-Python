Instalar python server y los cors

pip install Flask
pip install flask-cors

si es necesario instalar pandas nuevamente
pip install pandas

Para correr el servidor solo se hace:

python server.py

Donder server.py es el nombre del archivo que contiene la logica del servidor
El servidor por defecto escucha en http://127.0.0.1:5000
En nuestro caso solo usaremos por el momento el end point de tipo post siguiente
http://127.0.0.1:5000/recomendar
donde el json que espera recibir en el body es el siguiente:

{
    "usuario_en": [
        {"Titulo": "El Padrino", "rating": 5},
        {"Titulo": "Los Increíbles", "rating": 2},
        {"Titulo": "El Caballero de la Noche", "rating": 1}
    ]
}

Lo que hace el servidor una vez recibida el objeto ejecuta un script con la logica de la recomendacion
luego retorna el resultado