# Elección de Herramientas
 
## Gestor de dependencias
 
Antes de nada destacar que un PEP se trata de un documento de diseño que informa a la comunidad de Python o describe una nueva característica del lenguaje , de sus procesos o de su entorno. El fichero estándar para declarar las dependencias es `pyproject.toml` , ya que lo definen varios PEP, `PEP 518` crea el fichero para las dependencias necesarias para construir el proyecto. El `PEP 621` define en él la tabla `[project]`, donde van las dependencias del proyecto , y el `PEP 735` se encarga de definir `[dependency-groups]` para las dependencias que no forman parte del paquete que se distribuye. En otras asignaturas, se suele usar `requirements.txt`, pero el propio `PEP 735`indica que no está estandarizado ya que son opciones para `pip` y la documentación de `pip`dice que su formato solo está pensado para que lo lea pip. Luego solo se tienen en cuenta los gestores que trabajan con `pyproject.toml`.
 
Para comparar las distintas opciones que se han investigado, se han seguido unos criterios de la página [pydevtools](https://pydevtools.com/handbook/explanation/which-python-package-manager-should-i-use/), a saber son:

- **Lockfile:** si genera un archivo con la versión exacta de cada dependencia, para que el entorno sea el mismo en cualquier máquina donde se instale.
- **Gestión del intérprete de Python:** si puede instalar y elegir la versión de Python que usa el proyecto.
- **¿Hay que instalar algo?:** si hace falta instalar algo antes de poder usarlo.
- **Espacio a ocupar:** lo que ocupa la herramienta una vez instalada.
- **Tiempo de instalación de la herramienta:** lo que tarda en instalarse el propio gestor.
- **Tiempo de instalación del proyecto:** lo que tarda en instalar el proyecto con sus dependencias.

Destacar que debajo de la tabla se incluyen unas capturas, para constrastar los datos,sobre las diversas mediciones realizadas sobre los gestores.

| Herramienta | Lockfile | Gestión del intérprete de Python | Hay que instalar algo | Espacio que ocupa | Tiempo de instalación de la herramienta | Tiempo de instalación del proyecto |
|---|---|---|---|---|---|---|
| uv | Sí | Sí | No, es un único programa | 36 MB (uv) + 324KB (uvx) | 1,632 s | 0,035 s |
| Poetry | Sí | Experimental | Sí, Python | 65 MB | 2,050 s | 2,021 s |
| PDM | Sí | Sí | Sí, Python | 32 MB | 1,471 s | 2,414 s |
| Hatch | Con plugin | Sí | Sí, Python | 78 MB | 3,027 s | 4,270 s |

Medida de uv:

![Mediciones de uv](medir_uv.png)

Medida de Poetry:

![Mediciones de Poetry](medir_poetry.png)

Medida de pdm:

![Mediciones de PDM](medir_pdm.png)

Medida de hatch:

![Mediciones de Hatch](medir_hatch.png)

Tiempo de instalación de uv:

![Tiempo de instalación de uv](instalar_uv.png)

Tiempo de instalación de Poetry:

![Tiempo de instalación de Poetry](instalar_poetry.png)

Tiempo de instalación de PDM:

![Tiempo de instalación de PDM](instalar_pdm.png)

Tiempo de instalación de Hatch:

![Tiempo de instalación de Hatch](instalar_hatch.png)



Además de los criterios de pydevtools, se han incluido el espacio que ocupa cada herramienta, lo que tarda en instalarse y lo que tarda en instalar el proyecto. Se han incluido porque según indica el guion, lo que se elija ahora se va a usar en entornos donde la velocidad de instalación y de ejecución es esencial. En un workflow sin caché cada ejecución empieza en un entorno vacío, así que hay que instalar primero el gestor y después el proyecto, y los dos tiempos se suman.

Hatch no trae lockfile. Para tener el mismo entorno en distintas máquinas hay que añadir el plugin hatch-pip-compile, que genera el lockfile con pip-compile y vuelve a sincronizar el entorno cuando cambian las dependencias. Es decir, lo que en uv, Poetry o PDM viene de serie, en Hatch depende de instalar algo más. Además es el que más ocupa (78 MB), el que más tarda en instalarse (3,027 s) y el que más tarda en instalar el proyecto (4,270 s), por lo que se descarta. Por otro lado, Poetry puede instalar la versión de Python que pide el proyecto, pero esa función todavía es experimental, además de que ocupa 65 MB.

Entre PDM y uv, PDM ocupa algo menos y se instala un poco antes, pero uv instala el proyecto mucho más rápido. Sumando los dos tiempos, uv tarda en total 1,667 s y PDM 3,885 s. Además, PDM es un paquete de Python que trae sus propias dependencias, mientras que uv es un único programa, donde en un entorno vacío como un workflow, se instala sin necesidad de Python, descarga él mismo la versión de Python que pide el proyecto e instala las dependencias desde su `lockfile`, luego con una sola herramienta el entorno queda siempre igual. Por todo esto se elige uv.

## Gestor de tareas
 
 Un gestor de tareas permite lanzar, como subcomandos de un solo programa, todas las tareas que hay que llevar a cabo en el proyecto definidas en un único fichero. Ahora mismo la única tarea del proyecto es comprobar la sintaxis (`check`).

Se comparan make, invoke y just. Destacar que uv no permite definir tareas, luego no sirve como gestor de tareas. Los criterios a saber son los siguientes:

- **Estándar:** si la herramienta sigue un estándar.
- **¿Hay que instalar algo?** si hace falta instalar algo antes de poder usarla.
- **Espacio que ocupa:** lo que ocupa la herramienta una vez instalada.
- **Tiempo en ejecutar check:** lo que tarda en lanzar la tarea de comprobar la sintaxis.

Al igual que para el gestor de dependencias, se adjuntan capturas mostrando las mediciones, para constrastar los datos.

| Herramienta | Estándar | Hay que instalar algo | Espacio que ocupa | Tiempo en ejecutar `check` |
|---|---|---|---|---|
| make | Sí (POSIX) | No | 284 KB | 0,106 s |
| just | No | Sí, un único programa | 6,3 MB | 0,100 s |
| invoke | No | Sí, un paquete de Python | 780 KB | 0,262 s |

Medida de Make:

![Mediciones de Make](medir_make.png)

Mediciones de Just:

![Mediciones de Just](medir_just.png)

Mediciones de Invoke:

![Mediciones de Invoke](medir_invoke.png)

En la tabla se ve que invoke es un paquete de Python que hay que instalar y es el que más tarda en ejecutar `check`. Por otro lado, make y just tardan prácticamente lo mismo, pero lo que sí los diferencia es que make sigue un estándar (POSIX), no hay que instalar nada y ocupa 284 KB frente a los 6,3 MB de just, lo que importa en contenedores por la misma razón que para el gestor de dependencias.

Por tanto, se elige make, donde cada objetivo del `Makefile` es una tarea que se lanza con `make<tarea>` . La tarea check ejecuta `python3 -m compileall -q src/paddlesurf_time`, que compila los ficheros del modelo sin ejecutarlos, comprobando solo su sintaxis.