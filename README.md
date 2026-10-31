# PaddleSurfTime

## Descripción del Problema

Soy un apasionado del deporte y este verano he empezado a practicar paddle surf. Durante estos meses me he ido moviendo por diversas playas de Málaga, Murcia y Granada, y mi problema es que en varias de ellas, pese a que hubiera bandera verde y el baño estuviera permitido, no podía practicarlo, ya que el mar no estaba en condiciones para hacerlo de forma óptima.

Esto se debía a que hacía viento, que daba lugar a pequeñas corrientes o incluso, muchas veces, a olas que, por muy pequeñas que fueran, imposibilitaban la práctica. Y todo esto no era previsible, ya que, pese a que podía consultar las banderas o el viento, eso no me confirmaba si era posible practicar paddle surf. Por eso, unas 10-15 veces no pude sacar la tabla y tuve que coger el coche hacia otro lugar a ver si encontraba una playa donde sí se pudiera, lo que me supuso una gran pérdida de tiempo y gasolina, además de un hartazgo increíble.

## Estado del Proyecto

El proyecto está en fase de planificación, están definidos los usuarios, historias de usuario y dos milestones.

## Planificación

- [User Journeys](docs/user_journeys.md): se incluyen los user journeys y su relación con las historias de usuario.
- [Personas](docs/personas.md): se incluyen los perfiles de usuario de los que salen las historias de usuario.
- [Historias de Usuario](docs/historias_de_usuario.md): se incluyen las historias de usuario del proyecto.
- [Milestones](docs/milestones.md): se incluyen los milestones.

## Automatización de Tareas
 
### Gestor de dependencias
 
Las dependencias se expresan en dos partes: un fichero donde se declaran y un programa que lo interpreta y las instala. En Python el fichero es `pyproject.toml`,siendo este el estandar, mientras que las dependencias del proyecto van en `[project]` y las que solo hacen falta para desarrollar, como las bibliotecas de test, a través de `[dependency-groups]`. Donde `[project]` sigue PEP 621 y `[dependency-groups]` sigue PEP 735, siendo los PEP los documentos oficiales donde se definen los estándares de Python.
 
Ahora mismo el código solo usa la biblioteca estándar, pero tendrá dependencias más adelante, por ejemplo cuando se añadan los tests. Por otro lado, lo que el proyecto necesita del gestor es que siga ese estándar y que instale las dependencias igual en cualquier máquina, es decir, en un entorno virtual propio del proyecto y con las versiones fijadas en un archivo de bloqueo.

Las opciones que se han investigado son pip, uv, poetry, pdm, hatch y Pipenv. Pipenv no sigue el estándar porque usa su propio `Pipfile`. Aparte, pip solo instala, no crea el entorno ni el fichero de bloqueo.Por otro lado, uv, poetry, pdm y hatch cumplen las dos cosas que se han indicado antes. Cabe destacar que todos publican versiones este año, luego el mantenimiento no los diferencia.

Luego lo que los diferencia es lo que hace falta para usarlos. poetry, pdm y hatch son paquetes de Python,para instalarlos hace falta tener antes Python y pip, traen sus propias dependencias y hay que tenerlos en un entorno distinto del del proyecto para que no se mezclen con las suyas. Mientras que uv es un único programa que no depende de ningún paquete de Python. Además, respeta la versión de Python que pide `requires-python` en `pyproject.toml` y, si no está en el sistema, la descarga  así que la versión del lenguaje y las dependencias las controla la misma herramienta.

Por eso se elige uv. De manera que, cuando haya bibliotecas de test, se declararán en un grupo de `[dependency-groups]`,quedando fijadas en `uv.lock`. Por último, destacar que uv no permite definir tareas, así que no sirve como gestor de tareas.

### Gestor de tareas
 
El proyecto necesita un gestor de tareas, esto es, un fichero en la raíz del repositorio donde cada tarea tenga un nombre y se lance con una orden. Ahora mismo solo se ha incluido la tarea de comprobar la sintaxis,más adelante se incluirán tareas para instalar las dependencias, ejecutar tests...
 
Se han investigado los siguientes:
 
- Gestores de dependencias con tareas: Pipenv, pdm y hatch.
- Gestores de entornos con tareas: nox y tox.
- Gestores de tareas: make, just, task, invoke, doit, poethepoet y taskipy.

Pipenv, pdm y hatch hacen lo mismo que uv, por tannto usarlos para las tareas supondría tener dos gestores de dependencias en el proyecto. Por otro lado, nox, tox, invoke, doit, poethepoet y taskipy son paquetes de Python con lo que el proyecto tendría una dependencia solo para lanzar tareas. A su vez, pdm, hatch, tox, poethepoet y taskipy pueden guardar las tareas en `pyproject.toml`, pero cada uno en su propia sección y con su propio formato, que no forma parte del estándar. Por último, just y task no son paquetes de Python, pero son programas que habría que instalar aparte.

Por tanto, se elige make, que se trata de una herramienta de construcción que se usa como gestor de tareas, donde cada objetivo del `Makefile` es una tarea que se lanza con `make <tarea>`. Además ya está disponible en el sistema y no implica tener que instalar nada más.

La tarea `check` ejecuta `python3 -m compileall -q src`, que se encarga de compilar los ficheros sin ejecutarlos, comprobando solo la sintaxis.


## Comprobación del código

La clase principal es `Playa` localizada en `src/paddlesurf_time/playa.py` . Se encarga de representar una playa con su nombre, municipio, orientación y guarda las condiciones del mar. Se usará para ver si en esa playa se puede practicar paddle surf según esas condiciones.

Es necesario `make` y Python 3.14. Con pyenv se instal así:

```
pyenv install 3.14
``` 

Para comprobar que el código es sintácticamente correcto, desde la raíz del repositorio se ejecuta:

```
make check
```

Si el código es correcto, se termina sin mostrar ningún error, en caso contrario, se indica el fichero y la línea donde está el error de sintaxis.

## Documentación adicional

- [Fuentes de datos y heurística](docs/datos.md)
- [Juego de rol](docs/juego_de_rol.md)
- [Configuración del entorno](docs/entorno.md)





