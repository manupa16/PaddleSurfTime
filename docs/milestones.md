# Milestones

## [Milestone 0: Análisis del Problema](https://github.com/manupa16/PaddleSurfTime/milestone/1)

Este milestone resuelve la primera parte del problema que plantea HU001(#2), esto es, representar cómo se encuentra una playa a una hora concreta. Para ello a partir de las palabras clave de HU001 (#2) se abren issues que recogen los distintos problemas que hay en la historia, cada uno enlazado a ella. Donde en cada issue se razona si el concepto es un objeto valor o una entidad, partiendo de un objeto valor  que no dependa de otro. 

Para ver que es válido en la revisión del PR se recorre un proceso que va desde el código hasta la historia de usuario. Cada parte del código tiene que venir de un commit y a su vez dicho commit tiene que indicar el issue que resuelve. Donde dicho issue(como se ha indicado arriba) tiene que recoger un problema de HU001 (#2), en el que están razonados si los conceptos son objeto valor o entidad.Por último con el código se tienen que poder crear los datos del ejemplo de HU001 (#2).

Se trata de un mínimo viable porque solo resuelve la parte de representar cómo está una playa a una hora y viable porque sin él no se podría empezar con la lógica.


## [Milestone 1: Primera lógica de negocio](https://github.com/manupa16/PaddleSurfTime/milestone/2)

Este milestone resuelve la segunda parte del problema que plantea HU001 (#2) añadiendo la lógica de negocio sobre lo obtenido en el milestone anterior. Para ello esa parte se divide en problemas más sencillos donde cada uno se recoge en un issue enlazado a HU001 (#2) que no se cierran hasta que tengan tests que comprueben su solución.

Para ver que es válido, los tests se ejecutan de forma automática cada vez que se sube un cambio al repositorio y tienen que pasar todos. Donde cada test tiene que venir de un issue y ese issue de un problema de HU001 (#2).

Se trata de un mínimo viable porque solo resuelve HU001, y es viable porque con él ya se puede saber si merece la pena ir a una playa.



