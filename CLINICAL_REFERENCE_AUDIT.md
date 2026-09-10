# Auditoría clínica · módulo Análisis cefalométrico

Fecha de revisión: 2026-09-10

## Decisión de nomenclatura

El módulo se denominará **Análisis cefalométrico**. No se etiquetará como “Análisis de Steiner” porque YomCeph integra medidas clásicas de Steiner junto con medidas complementarias de otras referencias. El informe podrá indicar la fuente histórica de cada medición individual sin atribuir el conjunto completo a un solo autor.

## Medidas cefalométricas con construcción y referencia suficientemente claras

| Medida | Construcción | Referencia adoptada | Interpretación que puede mostrarse |
|---|---|---:|---|
| SNA | ángulo S-N-A, vértice N | 82° ± 2° | posición sagital del maxilar respecto a SN; no diagnosticar aisladamente |
| SNB | ángulo S-N-B, vértice N | 80° ± 2° | posición sagital mandibular respecto a SN |
| ANB | diferencia angular SNA-SNB / relación A-N-B | 2° ± 2° | tendencia sagital maxilomandibular; corroborar con otras medidas |
| SND | ángulo entre SN y ND | 76° ± 2° | posición de la región sinfisaria/mentón respecto a la base craneal |
| SN-GoGn | ángulo entre SN y Go-Gn | 32° ± 4° | divergencia del plano mandibular respecto a SN |
| Plano oclusal-SN | ángulo entre plano oclusal y SN | 14° ± 3° | inclinación del plano oclusal respecto a la base craneal |
| U1-SN | eje longitudinal del incisivo superior con SN | 103° ± 4° | inclinación del incisivo superior respecto a SN |
| U1-NA angular | eje longitudinal del incisivo superior con NA | 22° ± 6° | inclinación del incisivo superior respecto a NA |
| L1-NB angular | eje longitudinal del incisivo inferior con NB | 25° ± 4° | inclinación del incisivo inferior respecto a NB |
| Interincisal | ejes longitudinales U1 y L1 | 131° ± 4° | relación angular entre incisivos; menor valor = mayor proinclinación relativa |
| SL | proyección sobre SN desde S hasta L; L es la intersección de SN con la perpendicular a SN que pasa por Pg | 51 ± 4 mm | posición anteroposterior del pogonion respecto a S sobre el eje SN |
| SE | proyección sobre SN desde S hasta E; E es la intersección de SN con la perpendicular a SN que pasa por el punto más posterior del cóndilo mandibular | 22 ± 3 mm | posición anteroposterior del cóndilo respecto a S sobre el eje SN |
| U1-NA lineal | distancia perpendicular del borde incisal U1 a la línea NA | 4 mm como valor clásico | protrusión/retrusión dentoalveolar superior; evitar clasificar con tolerancia no documentada |
| L1-NB lineal | distancia perpendicular del borde incisal L1 a la línea NB | 4 mm como valor clásico | protrusión/retrusión dentoalveolar inferior; evitar clasificar con tolerancia no documentada |

## Correcciones respecto al catálogo actual de YomCeph

1. Cambiar SN-GoGn de 32° ± 5° a **32° ± 4°** en la referencia clásica adoptada.
2. Cambiar plano oclusal-SN de 14° ± 2° a **14° ± 3°**.
3. Cambiar U1-NA angular de 22° ± 2° a **22° ± 6°**.
4. Cambiar L1-NB angular de 25° ± 2° a **25° ± 4°**.
5. Cambiar interincisal de 131° ± 6° a **131° ± 4°**.
6. Añadir **SL 51 ± 4 mm** y **SE 22 ± 3 mm**.
7. Añadir las distancias lineales **U1-NA = 4 mm** y **L1-NB = 4 mm** cuando exista calibración.
8. Las medidas SN-Frankfort, Frankfort-plano palatino, A-B/Go-Gn y Ar-Go-Me no deben mostrarse como si fueran parte del bloque clásico de Steiner. Si permanecen en YomCeph, deben figurar como **complementarias**, con fuente propia y sin mezclar su norma con la referencia clásica.

## Geometría de SL y SE para implementación

No deben pedirse al usuario los puntos construidos L y E como si fueran landmarks anatómicos independientes.

- Para SL se marcan S, N y Pg. El software proyecta Pg perpendicularmente sobre SN y obtiene L; SL es la distancia S-L.
- Para SE se marcan S, N y el punto más posterior del contorno condilar. El software proyecta ese punto perpendicularmente sobre SN y obtiene E; SE es la distancia S-E.

Esto reduce puntos artificiales y hace el trazado más reproducible.

## Medidas candidatas que NO se incorporan todavía como automáticas

- U1-plano palatino: aparece en fuentes docentes y revisiones, pero la convención angular puede expresarse como ángulo agudo o suplementario; se verificará antes de programarlo.
- Pg-NB: aparece en tablas docentes con distintos criterios; requiere fijar exactamente si se mide Pg óseo, tejidos blandos y la dirección/signo de la perpendicular.
- Eje Y / NS-SGn: es clínicamente útil, pero no se incorporará hasta fijar una referencia poblacional y una convención geométrica única.
- Wits: útil como medida sagital complementaria, pero no pertenece al conjunto clásico y sus valores dependen de sexo, plano oclusal y referencia adoptada.

## Fuentes principales consultadas

- Ibarra et al. Design of Open Code Software to Downs and Steiner Lateral Cephalometric Analysis with Tracing Landmarks. *Applied System Innovation*. 2022. https://www.mdpi.com/2673-6470/2/2/8
- Evaluación del análisis cefalométrico de Steiner en individuos con percepción estéticamente aceptable. 2024. https://scielo.senescyt.gob.ec/scielo.php?pid=S2661-67422024000300088&script=sci_arttext

## Regla para el informe

YomCeph debe calcular únicamente las mediciones para las que estén presentes todos los puntos necesarios. Una medida ausente no debe impedir generar un informe parcial. Cada resultado debe mostrar: valor, referencia utilizada, interpretación prudente y fuente/referencia del método.
