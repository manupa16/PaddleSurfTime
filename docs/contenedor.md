## Criterios de búsqueda

Las imágenes se han buscado en Docker Hub, GitHub Container Registry y Quay. Se han buscado de tres tipos: la oficial de Python, sistemas operativos a los que se les instala Python y las que mantienen otros (buscando "python" y "uv").
Solo se consideran las que permiten usar la última versión de Python.

## Criterios de aceptación

Los criterios se han sacado de lo que pide el guion y de lo que se ha investigado en internet, la [documentación de Docker](https://docs.docker.com/build/building/best-practices/), que pide que la imagen venga de una fuente de confianza y sea pequeña, y el artículo [The best Docker base image for your Python application](https://pythonspeed.com/articles/base-image-python-docker-images/), que compara las imágenes que hay para Python.

- Trae la última versión de Python, porque la imagen es para probar el proyecto con ella.
- Viene de una fuente de fiable (imagen oficial o de editor verificado) y se sigue actualizando.
- Tamaño de descarga, porque la imagen se descarga cada vez que se pasan los tests.
- Lleva solo lo necesario para pasar los tests: Python y uv.

## Candidatas

- `python:3.15.2-slim-trixie`: la oficial de Python sobre Debian 13, variante reducida.
- `python:3.15.2-alpine3.24`: la oficial de Python sobre Alpine.
- `debian:13-slim`: Debian sin Python, que se instala con uv.
- `alpine:3.24`: Alpine sin Python, que se instala con uv.
- `astral/uv:python3.15-trixie-slim`: la de los autores de uv sobre Debian, con Python y uv.
- `astral/uv:python3.15-alpine`: la de los autores de uv sobre Alpine, con Python y uv.

