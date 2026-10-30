# Automatización de Tareas
 
## Gestor de dependencias
 
Las dependencias se expresan en dos partes: un fichero donde se declaran y un programa que lo interpreta y las instala. En Python el fichero es `pyproject.toml`,siendo este el estandar, mientras que las dependencias del proyecto van en `[project]` y las que solo hacen falta para desarrollar, como las bibliotecas de test, a través de `[dependency-groups]`. Donde `[project]` sigue PEP 621 y `[dependency-groups]` sigue PEP 735, siendo los PEP los documentos oficiales donde se definen los estándares de Python.
 
Ahora mismo el código solo usa la biblioteca estándar, pero tendrá dependencias más adelante, por ejemplo cuando se añadan los tests. Por otro lado, lo que el proyecto necesita del gestor es que siga ese estándar y que instale las dependencias igual en cualquier máquina, es decir, en un entorno virtual propio del proyecto y con las versiones fijadas en un archivo de bloqueo.

Las opciones que se han investigado son pip, uv, poetry, pdm, hatch y Pipenv. Pipenv no sigue el estándar porque usa su propio `Pipfile`. Aparte, pip solo instala, no crea el entorno ni el fichero de bloqueo.Por otro lado, uv, poetry, pdm y hatch cumplen las dos cosas que se han indicado antes. Cabe destacar que todos publican versiones este año, luego el mantenimiento no los diferencia.

Luego lo que los diferencia es lo que hace falta para usarlos. poetry, pdm y hatch son paquetes de Python,para instalarlos hace falta tener antes Python y pip, traen sus propias dependencias y hay que tenerlos en un entorno distinto del del proyecto para que no se mezclen con las suyas. Mientras que uv es un único programa que no depende de ningún paquete de Python. Además, respeta la versión de Python que pide `requires-python` en `pyproject.toml` y, si no está en el sistema, la descarga  así que la versión del lenguaje y las dependencias las controla la misma herramienta.

Por eso se elige uv. De manera que, cuando haya bibliotecas de test, se declararán en un grupo de `[dependency-groups]`,quedando fijadas en `uv.lock`. Por último, destacar que uv no permite definir tareas, así que no sirve como gestor de tareas.

## Gestor de tareas
 
El proyecto necesita un gestor de tareas, esto es, un fichero en la raíz del repositorio donde cada tarea tenga un nombre y se lance con una orden. Ahora mismo solo se ha incluido la tarea de comprobar la sintaxis,más adelante se incluirán tareas para instalar las dependencias, ejecutar tests...
 
Se han investigado los siguientes:
 
- Gestores de dependencias con tareas: Pipenv, pdm y hatch.
- Gestores de entornos con tareas: nox y tox.
- Gestores de tareas: make, just, task, invoke, doit, poethepoet y taskipy.

Pipenv, pdm y hatch hacen lo mismo que uv, por tannto usarlos para las tareas supondría tener dos gestores de dependencias en el proyecto. Por otro lado, nox, tox, invoke, doit, poethepoet y taskipy son paquetes de Python con lo que el proyecto tendría una dependencia solo para lanzar tareas. A su vez, pdm, hatch, tox, poethepoet y taskipy pueden guardar las tareas en `pyproject.toml`, pero cada uno en su propia sección y con su propio formato, que no forma parte del estándar. Por último, just y task no son paquetes de Python, pero son programas que habría que instalar aparte.

Por tanto, se elige make, que se trata de una herramienta de construcción que se usa como gestor de tareas, donde cada objetivo del `Makefile` es una tarea que se lanza con `make <tarea>`. Además ya está disponible en el sistema y no implica tener que instalar nada más.

La tarea `check` ejecuta `python3 -m compileall -q src`, que se encarga de compilar los ficheros sin ejecutarlos, comprobando solo la sintaxis.


