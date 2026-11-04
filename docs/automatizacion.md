# Elección de Herramientas
 
## Gestor de dependencias
 
Antes de nada destacar que un PEP se trata de un documento de diseño que informa a la comunidad de Python o describe una nueva característica del lenguaje , de sus procesos o de su entorno. El fichero estándar para declarar las dependencias es `pyproject.toml` , ya que lo definen varios PEP, `PEP 518` crea el fichero para las dependencias necesarias para construir el proyecto. El `PEP 621` define en él la tabla `[project]`, donde van las dependencias del proyecto , y el `PEP 735` se encarga de definir `[dependency-groups]` para las dependencias que no forman parte del paquete que se distribuye. En otras asignaturas, se suele usar `requirements.txt`, pero el propio `PEP 735`indica que no está estandarizado ya que son opciones para `pip` y la documentación de `pip`dice que su formato solo está pensado para que lo lea pip. Luego solo se tienen en cuenta los gestores que trabajan con `pyproject.toml`.
 
Para comparar las distintas opciones que se han investigado, se han seguido unos criterios de la página [pydevtools](https://pydevtools.com/handbook/explanation/which-python-package-manager-should-i-use/), a saber son:

- **Archivo de bloqueo:** si fija la versión exacta de cada dependencia.
- **Gestión del intérprete de Python:** si puede instalar y elegir la versión de Python que usa el proyecto.
- **Qué hay que instalar:** qué hace falta para usarlo.
- **Espacio que ocupa:** lo que ocupa la herramienta una vez instalada.
- **Tiempo de instalación del proyecto:** lo que tarda en instalar el proyecto con sus dependencias.

| Herramienta | Archivo de bloqueo | Gestión del intérprete de Python | Qué hay que instalar | Espacio que ocupa | Tiempo de instalación del proyecto |
|---|---|---|---|
| uv | Sí | Sí | Un único programa | 36 MB (uv) + 324KB (uvx) | 0,035 s |
| Poetry | Sí | Experimental | Un paquete de Python | 65 MB | 2,021 s |
| PDM | Sí | Sí | Un paquete de Python | 32 MB | 2,414 s |
| Hatch | No | Sí | Un paquete de Python | 78 MB | 4,270 s |

Medida de uv:

![Mediciones de uv](medir_uv.png)

![Mediciones de Poetry](medir_poetry.png)

![Mediciones de Pdm](medir_pdm.png)

![Mediciones de Hatch](medir_hatch.png)



## Gestor de tareas
 
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
| Nox | Imperativa | Sí | No | Sí | Sí | No | Un paquete  de Python |
| Tox | Declarativa | Sí | No | Sí | Sí | No | Un paquete de Python |
| Make | Declarativa | No | No | No | Limitado | Sí (POSIX) | Nada |
| Just | Declarativa | No | No | No | Sí | No | Un programa aparte  |


Hatch, Nox, Tox se encargan de gestionar entornos y eso ya lo hace uv, por lo que no son de interés. Por otro lado Make y Just  observamos en la tabla que se parecen en casi todo, salvo el estándar,en qué hay que instalar y los problemas de incompatibilidad de multiplataforma. Aquí nace la duda de sí Just o Make. Según se ha investigado Make presenta diversos problemas multiplataforma, así Just es mejor en este caso, pero esto no es de importancia en nuestro caso al trabajar únicamente en Linux. Además de esto, make es el único que sigue un estándar, y a diferencia de Just, Make no requiere instalar nada Y no añade nada al proyecto. Es cierto que su última versión es de 2023, pero se trata de una herramienta estable y al seguir un estándar POSIX, apenas necesita cambios.

Por tanto, se elige make, que se trata de una herramienta de construcción que se usa como gestor de tareas, donde cada objetivo del `Makefile` es una tarea que se lanza con `make <tarea>`. 
La tarea `check` ejecuta `python3 -m compileall -q src`, que se encarga de compilar los ficheros sin ejecutarlos, comprobando solo la sintaxis.
