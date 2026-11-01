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
 
Las dependencias se expresan en dos partes que son: un fichero donde se declaran y un programa que lo interpreta y las instala. En Python el fichero es `pyproject.toml`,siendo este el estandar, mientras que las dependencias del proyecto van en `[project]` y las que solo hacen falta para desarrollar, como las bibliotecas de test, a través de `[dependency-groups]`.
 
Para comparar las distintas opciones que se han investigado, se han seguido unos criterios de la página [pydevtools](https://pydevtools.com/handbook/explanation/which-python-package-manager-should-i-use/), a saber son:

- **Estándar:** si usa los metadatos del PEP 621.
- **Archivo de bloqueo:** si fija la versión exacta de cada dependencia.
- **Gestión del intérprete de Python:** si puede instalar y elegir la versión de Python que usa el proyecto.
- **Qué hay que instalar:** qué hace falta para usarlo.

| Herramienta | Estándar | Archivo de bloqueo | Gestión del intérprete de Python | Qué hay que instalar |
|---|---|---|---|---|
| pip | Sí | No | No | Nada, viene con Python |
| uv | Sí | Sí | Sí | Un único programa |
| Poetry | Sí | Sí | Experimental | Un paquete de Python |
| PDM | Sí | Sí | Sí | Un paquete de Python |
| Hatch | Sí | Sí | Sí | Un paquete de Python |
| Pipenv | No, usa `Pipfile` | Sí | Solo con pyenv | Un paquete de Python |

Pip a diferencia del resto no guarda las versiones exactas que se instalan, así que cada instalación puede ser diferente.No tiene un sistema para manejar las versiones de python, es decir, si la herramienta puede instalar y elegir la version de python que usa el proyecto. Por otro lado Pipenv, utiliza su propio formato Pipfile, en vez de usar pyproject.toml. Descartando ambos, se manejan las opciones de uv, Poetry, PDM y Hatch, sin embargo, se observa que uv es un único programa, mientras que los otros son paquetes de Python que hay que instalar con sus dependencias. En conlusión se elige uv, ya que a difrencia de los comentados, se trata de un gestor de dependencias que no añade dependencias que mantener. Además respeta la versión de Python que pide `requires-python` en `pyproject.toml` y en caso de que no está en el sistema, la descarga, de manera que la versión del lenguaje y las dependencias las controla la misma herramienta. Destacar que uv no permite definir tareas,así que no sirve como gestor de tareas.


### Gestor de tareas
 
El proyecto necesita un gestor de tareas, esto es, un fichero en la raíz del repositorio donde cada tarea tenga un nombre y se lance con una orden. Ahora mismo solo se ha incluido la tarea de comprobar la sintaxis y la de ejecutar tests.

Para comparar las distintas ocpiones se han tomados varios criterios de la siguiente pagína web [pyOpenSci](https://www.pyopensci.org/python-package-guide/maintain-automate/task-runners.html) , junto al estándar y que es necesario para instalarlos:

- **Configuración:** declarativa (si las tareas se describen en un fichero de configuración) o imperativa (se escriben como código Python).
- **Entornos:** si crea y gestiona entornos virtuales.
- **Empaquetado:** si además sirve para construir y publicar el paquete.
- **Varias versiones de Python:** si permite ejecutar los tests con distintas versiones de Python.
- **Multiplataforma:** si funciona igual en Linux, macOS y Windows.
- **Estándar:** si el fichero de tareas sigue un estándar.
- **Qué hay que instalar:** si hay que instalar algo para usarlo.

| Herramienta | Configuración | Entornos | Empaquetado | Varias versiones de Python | Multiplataforma | Estándar | Qué hay que instalar |
|---|---|---|---|---|---|---|---|
| Hatch | Declarativa | Sí | Sí | Sí | Sí | No | Un paquete de Python |
| Nox | Imperativa | Sí | No | Sí | Sí | No | Un paquete de Python |
| Tox | Declarativa | Sí | No | Sí | Sí | No | Un paquete de Python |
| Make | Declarativa | No | No | No | Limitado | Sí (POSIX) | Nada |
| Just | Declarativa | No | No | No | Sí | No | Un programa aparte |


Hatch, Nox, Tox se encargan de gestionar entornos y eso ya lo hace uv, por lo que no son de interés. Por otro lado Make y Just  observamos en la tabla que se parecen en casi todo, salvo el estándar,en qué hay que instalar y los problemas de incompatibilidad de multiplataforma. Aquí nace la duda de sí Just o Make. Según se ha investigado Make presenta diversos problemas multiplataforma, así Just es mejor en este caso, pero esto no es de importancia en nuestro caso al trabajar únicamente en Linux. Además de esto, make es el único que sigue un estándar, y a diferencia de Just, Make no requiere instalar nada Y no añade nada al proyecto. Es cierto que su última versión es de 2023, pero se trata de una herramienta estable y al seguir un estándar POSIX, apenas necesita cambios.

Por tanto, se elige make, que se trata de una herramienta de construcción que se usa como gestor de tareas, donde cada objetivo del `Makefile` es una tarea que se lanza con `make <tarea>`. 
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