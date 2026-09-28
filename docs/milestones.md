# Milestones

Destacar que los milestones están también registrado en este repositorio. A la hora de describirlos he optado por usar una plantilla común.

## [Milestone 0: Representación de playas y condiciones](https://github.com/manupa16/PaddleSurfTime/milestone/1)

**Qué  se entrega:** Se entregan las playas y las condiciones del mar que aparecen en las historias de usuario, con los datos que se indican en las mismas, de forma que se puedan crear y manejar a través de código

**Qué lo hace válido:** La validez se comprueba mediante comprobaciones automáticas en el propio paquete. Se considerará válido cuando otra presona pueda instalarlo, crear con él una playa y unas condiciones reales, y las comprobaciones lo pasen. Destacar que los casos cubren los valores que no existen en la realidad:
- **Dirección del viento y orientación de la playa:** se rechaza toda medida fuera del rango 0-360 grados.
- **Altura de olas:** se rechaza toda altura menor estricta que cero.
- **Fuerza del viento:** solo se rechazan valores negativos.
- **Bandera:** se rechaza cualquier valor que no sea verde,amarilla o roja.

**Soporte:** Se entregará como un paquete escrito en Python, alojado en este mismo repositorio, sobre el que se construirá la lógica de decisión del milestone siguiente.

**Historia de Usuario Asociada:** HU001 (#2) .

**Se trata de un mínimo viable** porque en relación al mínimo todavía no incluye la decisión de si es una playa apta, los umbrales de viento y oleaje, la comparación entre viento y orientación de la playa, ni la elección entre varias playas.  Es viable porque los datos vienen de fuentes distintas, cada una con su formato, y sin una manera única de escribirlos no se puede comparar ni decidir nada.

## [Milestone 1: Evaluación de condiciones para practicar paddle surf](https://github.com/manupa16/PaddleSurfTime/milestone/2)

**Qué se entrega:** Se entrega la decisión de si una playa es apta a una hora concreta y cuando no lo es, el motivo, aplicando la heurística descrita en [datos.md](datos.md).

**Qué lo hace válido:** El producto es válido cuando, para un conjunto de casos de prueba cuyo resultado se conoce de antemano, la decisión que toma la heurística coincide con el resultado esperado. Los casos cubren las tres reglas de la heurística:
- Bandera roja, con viento y oleaje dentro de los umbrales-> no apto, por bandera.
- Viento hacia el mar por enciam del umbral, con bandera verde y oleaje bajo -> no apta, por viento.
- Bandera amarilla, con viento y olejae dentro de los umbrales -> no apta, por la bandera.
- Bandera verde, viento flojo y oleaje debajo del umbral -> apta.
Estos casos se recogen en tests automáticos que se ejecutan en cada cambio del repositorio.

**Soporte:** Se entregará como un módulo dentro del paquete de Python del repositorio, construido sobre las entidades del milestone 0. Incluye además los tests que comprueban los casos anteriores y la configuracion automatica para ejectuarlos automaticamente.

**Historia de Usuario Asociada:**  HU001 (#2)

**Se trata de un mínimo viable**, porque en relación al mínimo decide sobre una única playa y una única hora, no compara varias playas ni tiene en cuenta la distancia , ni busca tampoco las mejores franjas horarias. Por otro lado es viable porque se consegui responder a la pregunta que origina el problema, que es si merece la pena coger el coche o no para ir a una determinada playa.

