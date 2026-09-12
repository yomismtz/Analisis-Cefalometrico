# Auditoría cefalométrica con fuentes primarias — 12 de septiembre de 2026

## Objetivo

Esta auditoría revisa la edición independiente **Yom análisis de lateral de cráneo** contra publicaciones originales y libros originales identificables. El criterio de integración es conservador: una medición solo se automatiza cuando su construcción geométrica puede reproducirse de manera explícita con los landmarks disponibles. Cuando una norma depende de edad, sexo, tamaño craneofacial, población o protocolo, la app evita imponer un único intervalo como si fuera universal.

La auditoría se aplica después de toda la cadena de generación del proyecto, de modo que revisa el catálogo que realmente termina dentro del APK y no solamente el archivo fuente intermedio.

## Fuentes originales verificadas

### Steiner

- Steiner CC. **Cephalometrics for you and me.** American Journal of Orthodontics. 1953;39(10):729-755. DOI: `10.1016/0002-9416(53)90082-7`.
- Fuente editorial: https://www.sciencedirect.com/science/article/pii/0002941653900827

Se conservan SNA, SNB, ANB, SND, SN/Go-Gn, relaciones incisivas con NA/NB, plano oclusal/SN e interincisal. La auditoría añade la distancia de Pogonion a NB para que pueda valorarse junto con la distancia del incisivo inferior a NB, sin imponer una tolerancia universal automática.

### Downs

- Downs WB. **Variations in facial relationships: Their significance in treatment and prognosis.** American Journal of Orthodontics. 1948;34(10):812-840. DOI: `10.1016/0002-9416(48)90015-3`. PMID: `18882558`.
- Fuente editorial: https://www.sciencedirect.com/science/article/pii/0002941648900153
- PubMed: https://pubmed.ncbi.nlm.nih.gov/18882558/

Se auditan el ángulo facial, eje Y, plano oclusal/Frankfort, convexidad y plano A-B. Se corrige la variable incisivo inferior/plano oclusal para que el número mostrado corresponda a la geometría que calcula el motor. En el método clásico esta variable suele expresarse como desviación respecto de una perpendicular al plano oclusal; YomCeph muestra el ángulo geométrico equivalente para no mezclar dos convenciones distintas.

**Nota de evidencia:** la identidad, diseño y publicación del análisis se verificaron en el trabajo original. Algunos valores tabulares exactos que no aparecen en el resumen del editor se cotejaron además con reproducciones técnicas posteriores; no se presentan como si fueran nuevos datos originales.

### Ricketts

- Ricketts RM. **A foundation for cephalometric communication.** American Journal of Orthodontics. 1960;46(5):330-357. DOI: `10.1016/0002-9416(60)90047-6`.
- Fuente editorial: https://www.sciencedirect.com/science/article/pii/0002941660900476

El artículo original describe cinco componentes centrales: ángulo facial, eje XY, medida de contorno y relación de los incisivos superior e inferior con el plano A-Po. La edición auditada conserva/añade la profundidad maxilar, eje facial, inclinaciones incisivas y, en esta revisión, incorpora medidas lineales firmadas de convexidad A–N-Pg, U1–A-Pg y L1–A-Pg. El signo se determina mediante una dirección anatómica anterior Po→Or y permanece estable si la radiografía está espejada horizontalmente.

### Tweed

- Tweed CH. **The diagnostic facial triangle in the control of treatment objectives.** American Journal of Orthodontics. 1969;55(6):651-667. DOI: `10.1016/0002-9416(69)90041-4`. PMID: `5253959`.
- PubMed: https://pubmed.ncbi.nlm.nih.gov/5253959/

La aplicación ya contenía FMA, FMIA e IMPA. El problema de la edición independiente era de accesibilidad: el botón Tweed estaba oculto y el catálogo no se agregaba al análisis único. La auditoría integra estas tres medidas dentro del trazado cefalométrico integral.

### Björk y Jarabak

- Björk A. **Prediction of mandibular growth rotation.** American Journal of Orthodontics. 1969;55(6):585-599. DOI: `10.1016/0002-9416(69)90036-0`. PMID: `5253957`.
- Fuente editorial: https://www.sciencedirect.com/science/article/pii/0002941669900360
- Jarabak JR, Fizzell JA. **Technique and Treatment with Light-wire Edgewise Appliances.** 2nd ed. C.V. Mosby, 1972. ISBN: `0801624290`, `9780801624292`.
- Catálogo bibliográfico: https://search.worldcat.org/title/Technique-and-treatment-with-light-wire-edgewise-appliances/oclc/589296

Ya estaban presentes ángulo de silla, articular, goníaco total y sus componentes. La auditoría añade las alturas S-Go y N-Me y el índice porcentual S-Go/N-Me × 100. El porcentaje se calcula sin depender de la calibración porque es una razón de longitudes en la misma imagen.

### Jacobson — Wits

- Jacobson A. **The “Wits” appraisal of jaw disharmony.** American Journal of Orthodontics. 1975;67(2):125-138. DOI: `10.1016/0002-9416(75)90065-2`. PMID: `1054214`.
- Fuente editorial: https://www.sciencedirect.com/science/article/pii/0002941675900652
- PubMed: https://pubmed.ncbi.nlm.nih.gov/1054214/

El artículo original define AO y BO como las proyecciones perpendiculares de A y B sobre el plano oclusal. En la muestra original, AO y BO coincidían en promedio en mujeres, mientras que en varones BO estaba aproximadamente 1 mm por delante de AO. Clase II produce lectura positiva y Clase III negativa.

La auditoría añade **Wits AO-BO** sin pedir al usuario que marque AO y BO: la aplicación los construye matemáticamente desde A, B y el plano oclusal funcional. La dirección posterior→anterior del plano se fija con Oclusal 2→Oclusal 1 para conservar el signo incluso si la imagen fue espejada.

### McNamara

- McNamara JA Jr. **A method of cephalometric evaluation.** American Journal of Orthodontics. 1984;86(6):449-469. DOI: `10.1016/S0002-9416(84)90352-X`. PMID: `6594933`.
- Fuente editorial: https://www.sciencedirect.com/science/article/pii/S000294168490352X
- PubMed: https://pubmed.ncbi.nlm.nih.gov/6594933/

La edición previa ya añadía Co-A, Co-Gn, ENA-Me y dimensiones faríngeas. Esta auditoría añade:

- Punto A a perpendicular de Nasion.
- Pogonion a perpendicular de Nasion.
- Diferencia maxilomandibular `(Co-Gn) − (Co-A)`.
- Relación del plano mandibular con Frankfort.

Las longitudes y posiciones se mantienen descriptivas cuando la norma correcta requiere edad, sexo o tamaño facial. No se inventa una única “normalidad” para todos los pacientes.

### Holdaway

- Holdaway RA. **A soft-tissue cephalometric analysis and its use in orthodontic treatment planning. Part I.** American Journal of Orthodontics. 1983;84(1):1-28. DOI: `10.1016/0002-9416(83)90144-6`. PMID: `6575614`.
- PubMed: https://pubmed.ncbi.nlm.nih.gov/6575614/
- Holdaway RA. **A soft-tissue cephalometric analysis and its use in orthodontic treatment planning. Part II.** American Journal of Orthodontics. 1984;85(4):279-293. DOI: `10.1016/0002-9416(84)90185-4`. PMID: `6585146`.
- PubMed: https://pubmed.ncbi.nlm.nih.gov/6585146/

Holdaway advierte que los tejidos blandos no pueden inferirse adecuadamente solo a partir de estructuras duras y que el ángulo H debe aumentar conforme aumenta la convexidad esquelética. Por ello la auditoría incorpora, sin un corte universal automático:

- Ángulo H `N'-Pg' / Pg'-Ls`.
- Ángulo facial de tejidos blandos respecto de Frankfort.
- Distancia firmada del labio inferior a la línea H.
- Espesor Pg-Pg' del mentón blando.

Se añaden los landmarks Ls y Li con definiciones anatómicas explícitas.

### Powell

- Powell N, Humphreys B. **Proportions of the Aesthetic Face.** Thieme-Stratton, New York, 1984.
- Catálogo bibliográfico: https://search.worldcat.org/title/Proportions-of-the-aesthetic-face/oclc/10183397

La app ya incluía los ángulos nasofrontal, nasofacial, nasomental y mentocervical. Igual que Tweed, el problema era que el módulo quedaba oculto en la edición independiente. La auditoría agrega su catálogo al análisis único.

### Sassouni — fuente verificada, integración deliberadamente pendiente

- Sassouni V. **A roentgenographic cephalometric analysis of cephalo-facio-dental relationships.** American Journal of Orthodontics. 1955;41(10):735-764. DOI: `10.1016/0002-9416(55)90171-8`.
- Fuente editorial: https://www.sciencedirect.com/science/article/pii/0002941655901718

El método es arquitectónico y depende de construcciones y relaciones geométricas que el motor actual no representa de forma completa. No se añade una versión abreviada etiquetada falsamente como “Sassouni completo”. Requiere un motor específico de planos convergentes/arcos y pruebas geométricas propias.

### Burstone / Legan — fuentes verificadas, integración completa pendiente

- Burstone CJ, James RB, Legan H, Murphy GA, Norton LA. **Cephalometrics for orthognathic surgery.** Journal of Oral Surgery. 1978;36(4):269-277. PMID: `273073`.
- PubMed: https://pubmed.ncbi.nlm.nih.gov/273073/
- Legan HL, Burstone CJ. **Soft tissue cephalometric analysis for orthognathic surgery.** Journal of Oral Surgery. 1980;38(10):744-751. PMID: `6932485`.
- PubMed: https://pubmed.ncbi.nlm.nih.gov/6932485/

El análisis de Burstone fue diseñado específicamente para cirugía maxilofacial y usa mediciones principalmente lineales que deben ser reproducibles para predicciones quirúrgicas. Legan/Burstone complementa ese sistema con tejidos blandos. No se integran todavía como “COGS completo” porque hacen falta landmarks, referencias horizontales y reglas quirúrgicas específicas que deben implementarse y probarse como un subsistema separado.

## Cambios funcionales introducidos por la auditoría

1. **Wits AO-BO real**, construido automáticamente y con signo estable ante espejo.
2. **McNamara ampliado:** A-Nperp, Pg-Nperp, diferencia Co-Gn−Co-A y plano mandibular/Frankfort, además de Co-A, Co-Gn y ENA-Me ya existentes.
3. **Björk-Jarabak:** S-Go, N-Me e índice S-Go/N-Me ×100.
4. **Ricketts:** convexidad firmada A–N-Pg y relaciones lineales U1/L1 a A-Pg, además de medidas angulares ya existentes.
5. **Steiner:** Pg-NB lineal para completar la valoración incisivo-mentón con II-NB.
6. **Holdaway:** ángulo H, ángulo facial blando, Li-H y espesor Pg-Pg'.
7. **Tweed, Powell, postura cráneo-cervical y vía aérea** pasan a formar parte del análisis único de la edición independiente en vez de quedar inaccesibles detrás de botones ocultos.
8. **Corrección de Downs:** se elimina la asociación incorrecta de 55.8° con incisivo inferior/plano oclusal y se expresa la geometría de forma consistente con el motor angular.
9. **Nuevo tipo geométrico de perpendicular firmada anatómica**, que usa Po→Or para definir “anterior” y conserva el signo aunque una imagen esté horizontalmente espejada.
10. **Reproducibilidad:** el workflow fija la aplicación fuente al commit `4fdbd4aed457aae8ec15e1a23a6ea9830092b3ac`, evitando que la misma versión se reconstruya con una rama cambiante.

## Qué no se debe afirmar todavía

- No debe llamarse **Sassouni completo** hasta que se implemente y pruebe su construcción arquitectónica propia.
- No debe llamarse **Burstone/COGS completo** ni **Legan-Burstone completo** hasta implementar la totalidad de landmarks y referencias quirúrgicas.
- El subconjunto de Holdaway añadido no equivale todavía a todas las variables históricas de Holdaway.
- Las dimensiones 2D de vía aérea no diagnostican por sí solas obstrucción ni apnea del sueño.
- Las normas cefalométricas no deben extrapolarse automáticamente entre edades, sexos y poblaciones cuando la fuente original o la literatura posterior demuestra dependencia de esos factores.

## Validación de software requerida antes de fusionar

La rama de auditoría debe pasar, como mínimo:

- ejecución de toda la cadena generadora;
- guardrails de presencia de mediciones;
- pruebas unitarias;
- Android Lint debug y release;
- compilación del APK debug;
- instalación en emulador Android;
- arranque en frío y permanencia del proceso;
- generación del artefacto APK.

La fusión a `main` no debe hacerse solo porque los scripts sean sintácticamente válidos: el workflow completo debe terminar en verde.
