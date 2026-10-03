# Historias de Usuario

## [HU001] ([#2](https://github.com/manupa16/PaddleSurfTime/issues/2))

Como deportista de paddle surf que vivo en Murcia, lejos de la playa. Me levanto muy temprano para ir a la playa ya que, en caso de que la playa no sea apta para practicar paddle surf, tengo que volver a coger el coche y desplazarme a otra playa cercana para ver si puedo realizarlo allí. El problema es que no tengo forma de saber, antes de salir de casa, si la playa estará apta a la hora a la que llegue, así que si no lo está hago el viaje para nada, y en caso de que lo este, he tenido que madrugar de más por si tenía que desplazarme a otra playa .

**Datos:** playa (ubicación, en latitud y longitud, y orientación en grados de 0 a 360 desde el norte en sentido horario hacia donde mira la playa) y condiciones del mar a una hora concreta, fuerza del viento (km/h), dirección desde la que sopla el viento (grados de 0 a 360, con el mismo criterio), altura de las olas (metros) y bandera (verde, amarilla o roja).
**Ejemplo:** playa de Bolnuevo en Mazarrón (latitud y longitud), orientada a 165°. A las 9:00 hay viento de 12km/h que viene desde 248°, olas de 0,4 metros y bandera verde.

## [HU002] ([#3](https://github.com/manupa16/PaddleSurfTime/issues/3))

Soy deportista de paddle surf que le apasiona el deporte. Bajo a la playa y, cuando no está apta para practicar dicho deporte, no tengo forma de saber a cuál de las playas de alrededor merece la pena ir teniendo en cuenta lo que tardo en llegar a cada una desde donde estoy, y allí lo único que llevo encima es el móvil. Tampoco sé si ninguna está apta, que me ahorraría moverme. Así que acabo probando suerte y recorriendo la costa a ciegas.

**Datos:** Mismos datos que  para HU001, pero de varias playas, además de que se incluye la ubicación del usuario de dónde se encuentra y el tiempo de desplazamiento a cada una.
**Ejemplo:** el usuario está en el Puerto de Mazarrón (latitud, longitud). La playa de Bolnuevo está a 10 minutos y a las 11:00 tiene viento de 18 km/h desde 312°, olas de 0,7 m y bandera amarilla. La de Calblanque está a 35 minutos y a esa hora tiene viento de 9 km/h desde 135°, olas de 0,3 m y bandera verde.

## [HU003] ([#4](https://github.com/manupa16/PaddleSurfTime/issues/4))

Soy deportista de paddle surf, voy a la playa a primera hora que es cuando suelo encontrar mejores condiciones. Alguna vez me ha pasado de llegar y que el mar no se encuentre óptimo, o que justo mejorase cuando me fuera a ir. No tengo forma de saber a qué hora del día son mejores las condiciones en esa playa, así que salgo a ciegas a primera hora en vez de ajustar la hora de salida. Tampoco sé si hoy no hay ninguna franja buena, que me ahorraría ir ese día.

**Datos:** Mismos datos que para HU001, pero para todas las franjas horarias del día no solamente para una.
**Ejemplo:** en la playa de Bolnuevo, a las 8:00 sopla viento de 8 km/h desde 200°, con olas de 0,2 m. A las 12:00, de 20 km/h desde 255°, con olas de 0,6 m y a las 16:00, de 25 km/h desde 280°, con olas de 0,8 m, todas con bandera verde.

Finalmente destacar que las fuentes de datos(así como la heurística) están descritas en [datos.md](datos.md). Por otro lado el contexto de cada historia está en los [user journeys](user_journeys.md)

