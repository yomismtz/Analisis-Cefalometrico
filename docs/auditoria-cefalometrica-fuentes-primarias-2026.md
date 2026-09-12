# Auditoría cefalométrica con fuentes primarias

## Criterio editorial y clínico

La edición **Yom análisis de lateral de cráneo** se construye con un criterio conservador: una medición recibe el nombre de un análisis histórico únicamente cuando su construcción geométrica puede reproducirse a partir de landmarks definidos y existe una fuente original identificable. Las medias y desviaciones de una muestra histórica se muestran como **referencias de esa muestra**, no como normalidad universal ni como diagnóstico.

La cadena de compilación está fijada al commit fuente `4fdbd4aed457aae8ec15e1a23a6ea9830092b3ac` de `yomismtz/Cefalometria-`. Sobre ese estado se aplican, en orden, las correcciones clínicas, la edición standalone y los pases de auditoría de fuentes primarias. Esto hace reproducible cada APK.

## Fuentes originales verificadas

### Steiner

Steiner CC. **Cephalometrics for you and me.** American Journal of Orthodontics. 1953;39(10):729-755. DOI: `10.1016/0002-9416(53)90082-7`.

Se conservan SNA, SNB, ANB, SND, relaciones mandibulares y dentarias de Steiner. La auditoría añade Pg-NB lineal para completar la valoración incisivo-mentón junto con II-NB.

### Downs

Downs WB. **Variations in facial relationships: Their significance in treatment and prognosis.** American Journal of Orthodontics. 1948;34(10):812-840. DOI: `10.1016/0002-9416(48)90015-3`. PMID: `18882558`.

La edición auditada corrige la incompatibilidad previa entre la convención histórica de incisivo inferior/plano oclusal y el ángulo geométrico que realmente calcula el motor. No se conserva `55.8° ± 4.5°` bajo una etiqueta que no corresponde a esa geometría.

### Ricketts

Ricketts RM. **A foundation for cephalometric communication.** American Journal of Orthodontics. 1960;46(5):330-357. DOI: `10.1016/0002-9416(60)90047-6`.

Se incluyen medidas angulares y relaciones lineales con A-Pg, además de una perpendicular firmada anatómica que conserva anterior/posterior aunque la radiografía esté horizontalmente espejada.

### Tweed

Tweed CH. **The diagnostic facial triangle in the control of treatment objectives.** American Journal of Orthodontics. 1969;55(6):651-667. DOI: `10.1016/0002-9416(69)90041-4`. PMID: `5253959`.

FMA, FMIA e IMPA se integran en el análisis único de la edición lateral, en lugar de quedar inaccesibles detrás de un botón oculto.

### Björk / Jarabak

Björk A. **Prediction of mandibular growth rotation.** American Journal of Orthodontics. 1969;55(6):585-599. DOI: `10.1016/0002-9416(69)90036-0`. PMID: `5253957`.

Jarabak JR, Fizzell JA. **Technique and Treatment with Light-wire Edgewise Appliances.** 2nd ed. C.V. Mosby; 1972. ISBN `0801624290`.

Además de los ángulos ya disponibles se calculan S-Go, N-Me e índice S-Go/N-Me ×100.

### Jacobson — Wits

Jacobson A. **The “Wits” appraisal of jaw disharmony.** American Journal of Orthodontics. 1975;67(2):125-138. DOI: `10.1016/0002-9416(75)90065-2`. PMID: `1054214`.

Wits se construye matemáticamente proyectando A y B perpendicularmente sobre el plano oclusal funcional; no se obliga al usuario a marcar AO y BO. Se conserva el signo sagital: positivo en dirección Clase II y negativo en dirección Clase III.

### McNamara

McNamara JA Jr. **A method of cephalometric evaluation.** American Journal of Orthodontics. 1984;86(6):449-469. DOI: `10.1016/S0002-9416(84)90352-X`. PMID: `6594933`.

Se incluyen Co-A, Co-Gn, ENA-Me, A-Nperp, Pg-Nperp, diferencia Co-Gn−Co-A, plano mandibular/Frankfort y dimensiones faríngeas. Las medidas cuya referencia depende de edad, sexo o tamaño facial no reciben un corte universal inventado.

### Holdaway

Holdaway RA. **A soft-tissue cephalometric analysis and its use in orthodontic treatment planning. Part I.** American Journal of Orthodontics. 1983;84(1):1-28. DOI: `10.1016/0002-9416(83)90144-6`. PMID: `6575614`.

Holdaway RA. **A soft-tissue cephalometric analysis and its use in orthodontic treatment planning. Part II.** American Journal of Orthodontics. 1984;85(4):279-293. DOI: `10.1016/0002-9416(84)90185-4`. PMID: `6585146`.

Se incorporan ángulo H, ángulo facial de tejidos blandos, Li-línea H y espesor Pg-Pg'. No se fuerza un único valor del ángulo H independientemente de la convexidad esquelética.

### Burstone COGS

Burstone CJ, James RB, Legan H, Murphy GA, Norton LA. **Cephalometrics for orthognathic surgery.** Journal of Oral Surgery. 1978;36(4):269-277. PMID: `273073`.

El COGS se implementa como análisis quirúrgico real y no como una lista de nombres. El motor construye el plano horizontal HP a 7° de S-N y calcula proyecciones paralelas o perpendiculares a HP. Se incluyen:

- Ar-Ptm y Ptm-N paralelos a HP.
- Convexidad N-A-Pg con signo anatómico.
- N-A, N-B y N-Pg paralelos a HP.
- N-ANS, ANS-Gn y PNS-N perpendiculares a HP.
- MP-HP.
- Alturas dentoalveolares U1-NF, U6-NF, L1-MP y L6-MP.
- PNS-ANS paralelo a HP como medida geométrica descriptiva.
- Ar-Go, Go-Pg y B-Pg paralelo al plano mandibular.
- Ángulo goníaco Ar-Go-Gn.
- OP-HP, A-B/OP, U1-NF y L1-MP.

Las referencias COGS de la tabla histórica se mantienen separadas por sexo cuando el valor original fue verificado. Con sexo no especificado, la app muestra ambas referencias y no clasifica automáticamente. Con sexo especificado, la comparación se expresa como posición respecto de ±1 DE de la muestra caucásica adulta original; no se denomina diagnóstico.

Para verificar la transcripción de la tabla histórica se cotejaron publicaciones científicas indexadas que reproducen las normas originales de Burstone. Cuando una variable geométrica está definida pero su media/DE no fue verificada de forma suficientemente sólida, se conserva como descriptiva.

### Legan–Burstone

Legan HL, Burstone CJ. **Soft tissue cephalometric analysis for orthognathic surgery.** Journal of Oral Surgery. 1980;38(10):744-751. PMID: `6932485`.

El bloque de tejidos blandos complementa COGS e incluye:

- convexidad facial G'-Sn-Pg';
- prognatismo maxilar G'-Sn respecto de HP;
- prognatismo mandibular G'-Pg' respecto de HP;
- razón vertical G'-Sn / Sn-Me';
- ángulo cara inferior-garganta Sn-Gn'-C;
- razón altura-profundidad inferior Sn-Gn'/C-Gn';
- ángulo nasolabial Cm-Sn-Ls;
- protrusión de labios superior e inferior respecto de Sn-Pg';
- profundidad del surco mentolabial;
- razón vertical labio-mentón;
- exposición del incisivo superior;
- espacio interlabial.

Se añadieron Sn, Cm, Gn', Si, Stms y Stmi con guías anatómicas explícitas.

### Sassouni — arquitectura original implementada

Sassouni V. **A roentgenographic cephalometric analysis of cephalo-facio-dental relationships.** American Journal of Orthodontics. 1955;41(10):735-764. DOI: `10.1016/0002-9416(55)90171-8`.

Sassouni no se implementa como tres o cuatro ángulos aislados. La edición auditada incorpora un motor arquitectónico específico:

1. plano basal construido por el punto de tangencia inferior de la silla y paralelo al eje del contorno superior de la base craneal anterior;
2. plano palatino ENP-ENA;
3. plano oclusal arquitectónico de Sassouni;
4. tangente de la base mandibular;
5. centro O obtenido por convergencia geométrica de los planos;
6. discrepancia de cada plano respecto del centro común y ayuda relativa para tipos I-IV y subtipos A/B;
7. comparación de los ángulos basal/palatino y palatino/mandibular;
8. arco anterior con radio O-ANS y residuos radiales de FE, N, U1 y Pg;
9. arco posterior con radio O-Sp y residuo radial de Go;
10. relaciones dentarias originales M' = I' + 10°, m' = i' + 5° y R = i cuando están colocados los landmarks necesarios.

El motor no introduce un umbral milimétrico universal para decidir un “Sassouni normal”, porque el trabajo original no proporciona un corte moderno único para automatizar esa decisión. La clasificación de tipo mostrada por software se identifica como ayuda geométrica y debe confirmarse visualmente.

### Powell

Powell N, Humphreys B. **Proportions of the Aesthetic Face.** Thieme-Stratton; 1984.

Los ángulos nasofrontal, nasofacial, nasomental y mentocervical existentes pasan a formar parte del flujo integral.

## Maduración vertebral y otros módulos de la lateral

La evaluación CVM C2-C4 permanece accesible en la edición dedicada de lateral de cráneo. Asimismo se preservan las mediciones cráneo-cervicales y de vía aérea que pueden calcularse desde la misma telerradiografía. Las dimensiones 2D de vía aérea se presentan como hallazgos cefalométricos y no como diagnóstico de obstrucción o apnea del sueño.

## Reglas de seguridad de la interpretación

- Una media ± DE histórica describe una muestra, no una frontera biológica universal.
- Las normas específicas de sexo, edad, población o protocolo se muestran con ese contexto.
- Las medidas lineales requieren calibración radiográfica válida.
- Las medidas con signo utilizan direcciones anatómicas para evitar invertir una interpretación solo porque una imagen esté espejada.
- Los resultados parciales se permiten: no se obliga a marcar landmarks de un análisis que no se desea realizar.
- La aplicación continúa identificándose como herramienta educativa y no como dispositivo médico.

## Validación de software

Cada cambio de esta auditoría debe pasar la misma cadena antes de fusionarse:

- ejecución de todos los generadores;
- pruebas unitarias de catálogos y geometría;
- Android Lint debug y release;
- compilación del APK;
- instalación en emulador Android;
- arranque en frío y comprobación de que el proceso permanece activo;
- creación del artefacto APK versionado.

La rama no debe fusionarse a `main` si cualquiera de estas etapas falla.
