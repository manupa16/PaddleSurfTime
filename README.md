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
 
Ahora mismo el código solo usa la biblioteca estándar, pero tendrá dependencias más adelante, por ejemplo cuando se añadan los tests. Por eso, antes de comparar las opciones se han fijado estos criterios, que se usarán para decidir:

- **Estándar:** si lee las dependencias del fichero `pyproject.toml`.
- **Entorno y bloqueo :** si instala las dependencias en un entorno solo para el proyecto y guarda sus versiones exactas en un archivo.
- **Qué hace falta para instalarlo:** cuántas dependencias añade.
- **Mantenimiento:** Si ha publicado versiones este año.


| Herramienta | Estándar | Entorno y bloqueo | Qué hace falta para instalarlo | Mantenimiento |
|---|---|---|---|---|
| pip | Sí | No | Viene con Python | Sí |
| uv | Sí | Sí | Nada, es un único programa | Sí |
| poetry | Sí | Sí | Python, pip y sus propias dependencias | Sí |
| pdm | Sí | Sí | Python, pip y sus propias dependencias | Sí |
| hatch | Sí | Sí | Python, pip y sus propias dependencias | Sí |
| Pipenv | No, usa `Pipfile` | Sí | Python, pip y sus propias dependencias | Sí |

Por eso se elige uv, es el único que cumple con los dos primeros criterios sin necesitar nada más para instalarse. Además respeta la versión de Python que pide `requires-python` en `pyproject.toml` y en caso de que no está en el sistema, la descarga, de manera que la versión del lenguaje y las dependencias las controla la misma herramienta. Por otro lado cuando haya bibliotecas de test, se declararán en un grupo de `[dependency-groups]`quedando fijas en `uv.lock` . Por último destacar que uv no permite definir tareas, luego no sirve como gestor de tareas.

### Gestor de tareas
 
El proyecto necesita un gestor de tareas, esto es, un fichero en la raíz del repositorio donde cada tarea tenga un nombre y se lance con una orden. Ahora mismo solo se ha incluido la tarea de comprobar la sintaxis y la de ejecutar tests.

Antes de comparar las opciones se han fijado estos criterios, para basarse a la hora de decidir:

- **Estándar:** si el fichero de tareas sigue un estándar.
- **Qué añade al proyecto:** si hay que instalarlo como dependencia o como un programa aparte.
- **Qué más gestiona:** si además de tareas gestiona dependencias.
- **Última versión:** año en el que se publica.

| Herramienta | Estándar | Qué añade al proyecto | Qué más gestiona | Última versión |
|---|---|---|---|---|
| make | Sí, POSIX | Nada ya está en el sistema | Nada | 2023 |
| just | No, `justfile` | Un programa aparte | Nada | 2026 |
| task | No, `Taskfile.yml` | Un programa aparte | Nada | 2026 |
| invoke | No, `tasks.py` | Una dependencia de Python | Nada | 2026 |
| doit | No, `dodo.py` | Una dependencia de Python | Nada | 2026 |
| poethepoet | No, formato propio en `pyproject.toml` | Una dependencia de Python | Nada | 2026 |
| taskipy | No, formato propio en `pyproject.toml` | Una dependencia de Python | Nada | 2024 |
| nox | No, `noxfile.py` | Una dependencia de Python | Entornos | 2026 |
| tox | No, formato propio | Una dependencia de Python | Entornos | 2026 |
| Pipenv | No, `Pipfile` | Una dependencia de Python | Dependencias, como uv | 2026 |
| pdm | No, formato propio en `pyproject.toml` | Una dependencia de Python | Dependencias como uv | 2026 |
| hatch | No, formato propio en `pyproject.toml` | Una dependencia de Python | Dependencias como uv | 2026 |


Por tanto, se elige make, que se trata de una herramienta de construcción que se usa como gestor de tareas, donde cada objetivo del `Makefile` es una tarea que se lanza con `make <tarea>`. Es el único que sigue un estándar y no añade nada al proyecto, ya que just y task habría que instalarlos en cada máquina donde se trabaje con él, y los demás añadirían una dependencia de Python solo para lanzar tareas o duplicarían lo que ya hace uv. Su última versión es de 2023, pero es una herramienta estable y al ser un estándar POSIX, apenas necesita cambios.

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