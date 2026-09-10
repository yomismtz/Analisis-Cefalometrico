# YomCeph · Análisis cefalométrico

Repositorio dedicado exclusivamente al módulo de **análisis cefalométrico lateral** de YomCeph.

## Alcance

Este repositorio no se presenta como una reproducción literal de un único análisis de autor. Integra medidas cefalométricas clásicas y complementarias que pueden calcularse de forma reproducible en una telerradiografía lateral, indicando para cada una su construcción, referencia e interpretación.

## Flujo previsto

1. Seleccionar el análisis cefalométrico.
2. Seleccionar la telerradiografía lateral.
3. Asignar nombre o número de estudio, nombre/diferenciador y edad.
4. Calibrar cuando se vayan a obtener medidas lineales en milímetros.
5. Seleccionar explícitamente cada punto antes de colocarlo.
6. Permitir zoom y desplazamiento de la imagen sin crear puntos accidentalmente.
7. Mantener pulsado/arrastrar el punto seleccionado para corregirlo con precisión.
8. Calcular únicamente las mediciones cuyos puntos necesarios estén presentes.
9. Exportar imagen con puntos, imagen con trazado e informe de resultados.

## Medidas lineales incorporadas a la especificación

- Segmento SL: 51 ± 4 mm.
- Segmento SE: 22 ± 3 mm.
- Incisivo superior a NA: 4 mm (distancia perpendicular).
- Incisivo inferior a NB: 4 mm (distancia perpendicular).

Las normas dependen del análisis y de la población de referencia. La aplicación debe mostrar la fuente y evitar convertir una medida aislada en un diagnóstico clínico.

## Estado

La auditoría clínica y el catálogo de medidas se están construyendo primero para que la implementación Android se apoye en definiciones verificadas y no en nombres o tablas ambiguas.
