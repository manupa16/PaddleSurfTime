# Elección de Herramientas
 
## Gestor de dependencias
 
Antes de nada destacar que un PEP se trata de un documento de diseño que informa a la comunidad de Python o describe una nueva característica del lenguaje, de sus procesos o de su entorno. El fichero estándar para declarar las dependencias es `pyproject.toml`, ya que lo definen varios PEP, `PEP 518` crea el fichero para las dependencias necesarias para construir el proyecto. El `PEP 621` define en él la tabla `[project]`, donde van las dependencias del proyecto, y el `PEP 735` se encarga de definir `[dependency-groups]` para las dependencias que no forman parte del paquete que se distribuye. En otras asignaturas, se suele usar `requirements.txt`, pero el propio `PEP 735` indica que no está estandarizado ya que son opciones para `pip` y la documentación de `pip` dice que su formato solo está pensado para que lo lea pip. Luego solo se tienen en cuenta los gestores que trabajan con `pyproject.toml`.
 
Todos los gestores que se comparan tienen que poder hacer despliegues idempotentes, es decir, que al instalar el proyecto en cualquier máquina, y las veces que sea, quede siempre el mismo entorno con las mismas versiones de las dependencias. Esto es necesario porque el proyecto se va a instalar en workflows y contenedores que empiezan vacíos, y si cada instalación sacara versiones distintas, los tests podrían pasar en una y fallar en otra sin haber cambiado el código. Los cuatro lo cumplen guardando la versión exacta de cada dependencia (uv en `uv.lock`, Poetry en `poetry.lock`, PDM en `pdm.lock` y Hatch en `pylock.toml`) e instalando a partir de ella, así que no sirve para elegir entre ellos y no se incluye en la tabla. Para elegir se usan estos criterios:

- **¿Hay que instalar algo?:** si hace falta instalar algo antes de poder usarlo. En un entorno vacío, cada cosa que haya que instalar antes es tiempo que se suma y un paso más que puede fallar.
- **Tiempo de instalación de la herramienta:** lo que tarda en descargarse e instalarse el propio gestor.
- **Tiempo de instalación del proyecto:** lo que tarda en instalar el proyecto con sus dependencias.

Destacar que debajo de la tabla se incluyen unas capturas, para constrastar los datos,sobre las diversas mediciones realizadas sobre los gestores.

| Herramienta | Hay que instalar algo | Tiempo de instalación de la herramienta | Tiempo de instalación del proyecto |
|---|---|---|---|
| uv | No, es un único programa | 1,632 s | 0,035 s |
| Poetry | Sí, Python | 2,050 s | 2,021 s |
| PDM | Sí, Python | 1,471 s | 2,414 s |
| Hatch | Sí, Python | 3,027 s | 4,270 s |

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



Se miden los dos tiempos porque, según indica el guion, lo que se elija ahora se va a usar en entornos donde la velocidad de instalación es esencial. En un workflow sin caché cada ejecución empieza en un entorno vacío, así que hay que instalar primero el gestor y después el proyecto, y los dos tiempos se suman.

Hatch es el que más tarda en instalarse (3,027 s) y en instalar el proyecto (4,270 s), y Poetry es el siguiente en instalar el proyecto (2,021 s), así que se descartan. Entre PDM y uv, PDM se instala un poco antes, pero uv instala el proyecto mucho más rápido: sumando los dos tiempos, uv tarda 1,667 s y PDM 3,885 s. Además, PDM necesita Python para instalarse y uv es un único programa que no necesita nada. Por eso se elige uv.

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