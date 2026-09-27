# Milestones

Destacar que los milestones están también registrado en este repositorio. A la hora de describirlos he optado por usar una plantilla común.

## [Milestone 0: Representación de playas y condiciones](https://github.com/manupa16/PaddleSurfTime/milestone/1)

**Qué  se entrega:** Se entrega la representación de las dos entidades del problema: la playa, con su ubicación y su orientación, y las condiciones del mar en una hora concreta, con la hora, la fuerza y la dirección del viento, la altura de las olas y la bandera.

**Qué lo hace válido:** Se puede representar cualquier playa con sus datos reales y las condiciones del mar en una determinada hora sin perder ninguna de las variables. Además el modelo rechaza valores de variables que no existen en la realidad:
- **Dirección del viento y orientación de la playa:** se rechaza toda medida fuera del rango 0-360 grados.
- **Altura de olas:** se rechaza toda altura menor estricta que cero.
- **Fuerza del viento:** solo se rechazan valores negativos.
- **Bandera:** se rechaza cualquier valor que no sea verde,amarilla o roja.
Donde todo lo anterior se comprueba mediante comprobaciones automáticas.

**Soporte:** Se entregará como un paquete escrito en Python, alojado en este mismo repositorio, sobre el que se construirá la lógica de decisión del milestone siguiente.

**Historia de Usuario Asociada:** HU001 (#2) .

**Se trata de un mínimo viable** porque en relación al mínimo todavía no incluye la decisión de si es una playa apta, los umbrales de viento y oleaje, la comparación entre viento y orientación de la playa, y  la elección entre varias playas.  Es viable porque los datos vienen de fuentes distintas, cada una con su formato, y sin una manera única de escribirlos no se puede comparar ni decidir nada.

## [Milestone 1: Evaluación de condiciones para practicar paddle surf](https://github.com/manupa16/PaddleSurfTime/milestone/2)

**Qué se entrega:** Se entrega la heurística que, a partir de una playa y de las condiciones del mar en una hora concreta, determina si la playa es apta o no a esa hora y, cuando no lo es , el motivo.
La decisión se toma en tres pasos: se descarta la playa si la bandera es roja o amarilla, luego se compara la dirección del viento con la orientación de la playa, ya que el viento que sopla mar adentro es el peligroso. Y finalemente se comprueba que el viento y las olas estén por debajo de unos umbrales.

**Qué lo hace válido:** El producto es válido cuando, para un conjunto de casos de prueba cuyo resultado se conoce de antemano, la decisión que toma la heurística coincide con el resultado esperado. Los casos cubren las tres reglas de la heurística:
- Bandera roja, con viento y oleaje dentro de los umbrales-> no apto, por bandera.
- Viento hacia el mar por enciam del umbral, con bandera verde y oleaje bajo -> no apta, por viento.
- Bandera amarilla, con viento y olejae dentro de los umbrales -> no apta, por la bandera.
- Bandera verde, viento flojo y oleaje debajo del umbral -> apta.
Estos casos se recogen en tests automáticos que se ejecutan en cada cambio del repositorio.

**Soporte:** Se entregará como un módulo dentro del paquete de Python del repositorio, construido sobre las entidades del milestone 0. Incluye además los tests que comprueban los casos anteriores y la configuracion automatica para ejectuarlos automaticamente.

**Historia de Usuario Asociada:**  HU001 (#2)

**Se trata de un mínimo viable**, porque en relación al mínimo decide sobre una única playa y una única hora, no compara varias playas ni tiene en cuenta la distancia , ni busca tampoco las mejores franjas horarias. Por otro lado es viable porque se consegui responder a la pregunta que origina el problema, que es si merece la pena coger el coche o no para ir a una determinada playa.

