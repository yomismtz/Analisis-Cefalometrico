from pathlib import Path
import re

ROOT = Path('.')
java_dir = ROOT / 'app/src/main/java/com/cefalo/angulos'

# Second primary-source pass: complete a small set of measurements that require
# signed perpendicular geometry and add the core Holdaway H-line variables.

# 1) Angular catalog: Holdaway H angle + soft-tissue facial angle.
catalog = java_dir / 'MeasurementCatalog.java'
c = catalog.read_text(encoding='utf-8')
if 'Holdaway · ángulo H' not in c:
    method = re.compile(
        r'(public static List<MeasurementDefinition> steiner\(\) \{[\s\S]*?)(\n        return list;\n    \})',
        re.M,
    )
    addition = r'''
        // Holdaway 1983/1984: soft-tissue balance cannot be inferred from hard
        // tissue alone. H angle is reported descriptively because Holdaway
        // explicitly related its ideal value to the underlying skeletal convexity.
        list.add(m(
                "Holdaway · ángulo H · N'-Pg' / Pg'-Ls",
                TWO_LINES,
                p("Pg'", "N'", "Pg'", "Ls"),
                Double.NaN,
                Double.NaN,
                "Holdaway 1983-1984 · el valor ideal del ángulo H varía con la convexidad esquelética; no aplicar un corte universal aislado",
                "Marque N' y Pg' para la línea facial blanda y Ls (labiale superius) para la línea H Pg'-Ls.",
                "",
                "Ángulo H de Holdaway. Interprételo junto con convexidad esquelética, soporte labial y espesor de tejidos blandos; no se clasifica automáticamente con un único valor.",
                "",
                false
        ));

        list.add(m(
                "Holdaway · ángulo facial de tejidos blandos · FH / N'-Pg'",
                TWO_LINES,
                p("Po", "Or", "N'", "Pg'"),
                Double.NaN,
                Double.NaN,
                "Holdaway · relación del perfil facial blando con Frankfort; norma dependiente de población/protocolo",
                "Trace Frankfort Po-Or y la línea facial de tejidos blandos N'-Pg'.",
                "",
                "Describe la inclinación global del perfil blando. Interpretar como parte del análisis de Holdaway, no como diagnóstico aislado.",
                "",
                true
        ));
'''
    c, n = method.subn(lambda m: m.group(1) + addition + m.group(2), c, count=1)
    if n != 1:
        raise RuntimeError('Could not add Holdaway angular variables')
catalog.write_text(c, encoding='utf-8')

# 2) Add a mirror-invariant signed perpendicular type.
linear_def = java_dir / 'LinearMeasurementDefinition.java'
ld = linear_def.read_text(encoding='utf-8')
if 'ANATOMICAL_PERPENDICULAR' not in ld:
    anchor = '''        RATIO_PERCENT
    }'''
    replacement = '''        RATIO_PERCENT,
        ANATOMICAL_PERPENDICULAR
    }'''
    if anchor not in ld:
        raise RuntimeError('Expected audited linear type enum not found')
    ld = ld.replace(anchor, replacement, 1)
linear_def.write_text(ld, encoding='utf-8')

linear_catalog = java_dir / 'LinearMeasurementCatalog.java'
l = linear_catalog.read_text(encoding='utf-8')
if 'Type.ANATOMICAL_PERPENDICULAR' not in l:
    anchor = 'import static com.cefalo.angulos.LinearMeasurementDefinition.Type.RATIO_PERCENT;\n'
    if anchor not in l:
        raise RuntimeError('Audited linear imports not found')
    l = l.replace(
        anchor,
        anchor + 'import static com.cefalo.angulos.LinearMeasurementDefinition.Type.ANATOMICAL_PERPENDICULAR;\n',
        1,
    )

if 'Ricketts · convexidad · A a N-Pg' not in l:
    method = re.compile(
        r'(public static List<LinearMeasurementDefinition> cephalometric\(\) \{[\s\S]*?)(\n        return list;\n    \})',
        re.M,
    )
    addition = r'''
        // Steiner: add the missing chin-to-NB linear counterpart so the classic
        // lower-incisor/chin balance can be inspected from the same tracing.
        list.add(m(
                "Steiner · Pogonion a NB · lineal",
                PERPENDICULAR_ABS,
                RANGE,
                p("N", "B", "Pg"),
                Double.NaN,
                Double.NaN,
                "Pg-NB en mm · comparar con la posición lineal del incisivo inferior a NB; no imponer tolerancia universal",
                "",
                "Distancia perpendicular de Pogonion a NB. Úsela junto con II-NB para valorar el equilibrio incisivo-mentón.",
                ""
        ));

        // Ricketts 1960 explicitly described facial contour plus the upper and
        // lower incisor relationships to the A-Po denture plane. Sign is defined
        // anatomically: positive = anterior in the Po->Or direction.
        list.add(m(
                "Ricketts · convexidad · A a N-Pg",
                ANATOMICAL_PERPENDICULAR,
                RANGE,
                p("N", "Pg", "A", "Po", "Or"),
                Double.NaN,
                Double.NaN,
                "Distancia firmada de A al plano facial N-Pg · Ricketts; cambia con edad y patrón facial",
                "",
                "Positivo = A anterior al plano N-Pg; negativo = A posterior. Medida de contorno/perfil que debe interpretarse con edad y el resto del análisis.",
                ""
        ));

        list.add(m(
                "Ricketts · U1 a A-Pg · lineal",
                ANATOMICAL_PERPENDICULAR,
                RANGE,
                p("A", "Pg", "IS borde", "Po", "Or"),
                Double.NaN,
                Double.NaN,
                "Relación lineal firmada del incisivo superior con A-Pg · Ricketts",
                "",
                "Positivo = borde incisal anterior a A-Pg; negativo = posterior. Interpretar con edad, patrón facial y la inclinación angular del incisivo.",
                ""
        ));

        list.add(m(
                "Ricketts · L1 a A-Pg · lineal",
                ANATOMICAL_PERPENDICULAR,
                RANGE,
                p("A", "Pg", "II borde", "Po", "Or"),
                Double.NaN,
                Double.NaN,
                "Relación lineal firmada del incisivo inferior con A-Pg · Ricketts 1960",
                "",
                "Positivo = borde incisal anterior a A-Pg; negativo = posterior. Esta relación fue una de las variables dentarias centrales descritas por Ricketts.",
                ""
        ));

        // Holdaway H line. The original papers stress profile balance rather
        // than one fixed universal norm, so these remain descriptive.
        list.add(m(
                "Holdaway · labio inferior a línea H",
                ANATOMICAL_PERPENDICULAR,
                RANGE,
                p("Pg'", "Ls", "Li", "Po", "Or"),
                Double.NaN,
                Double.NaN,
                "Li-H en mm · Holdaway; interpretar junto con ángulo H, convexidad y espesor de tejidos blandos",
                "",
                "Positivo = labio inferior anterior a la línea H; negativo = posterior. No aplicar un corte universal aislado.",
                ""
        ));

        list.add(m(
                "Holdaway · espesor de mentón blando · Pg-Pg'",
                DISTANCE,
                RANGE,
                p("Pg", "Pg'"),
                Double.NaN,
                Double.NaN,
                "Pg-Pg' en mm · componente de espesor de tejidos blandos; dependiente de población/sexo",
                "",
                "Espesor del mentón blando entre Pogonion óseo y Pogonion de tejidos blandos. Interpretar con normas de población apropiadas.",
                ""
        ));
'''
    l, n = method.subn(lambda m: m.group(1) + addition + m.group(2), l, count=1)
    if n != 1:
        raise RuntimeError('Could not add Ricketts/Steiner/Holdaway linear variables')
linear_catalog.write_text(l, encoding='utf-8')

# 3) Implement signed anatomical perpendicular in AnalysisActivity.
activity = java_dir / 'AnalysisActivity.java'
a = activity.read_text(encoding='utf-8')
if 'Type.ANATOMICAL_PERPENDICULAR' not in a:
    anchor = '''        if (def.type == LinearMeasurementDefinition.Type.AXIAL_OFFSET) {
'''
    branch = r'''        if (def.type == LinearMeasurementDefinition.Type.ANATOMICAL_PERPENDICULAR) {
            PointF lineA = measurementView.getPoint(def.pointLabels[0]);
            PointF lineB = measurementView.getPoint(def.pointLabels[1]);
            PointF target = measurementView.getPoint(def.pointLabels[2]);
            PointF anteriorA = measurementView.getPoint(def.pointLabels[3]);
            PointF anteriorB = measurementView.getPoint(def.pointLabels[4]);
            if (lineA == null || lineB == null || target == null
                    || anteriorA == null || anteriorB == null) return null;

            double dx = lineB.x - lineA.x;
            double dy = lineB.y - lineA.y;
            double len2 = dx * dx + dy * dy;
            if (len2 == 0.0) return null;

            double t = ((target.x - lineA.x) * dx + (target.y - lineA.y) * dy) / len2;
            double projX = lineA.x + t * dx;
            double projY = lineA.y + t * dy;
            double offX = target.x - projX;
            double offY = target.y - projY;
            double magnitude = Math.hypot(offX, offY) * mmPerPixel;

            double ax = anteriorB.x - anteriorA.x;
            double ay = anteriorB.y - anteriorA.y;
            double anteriorLength = Math.hypot(ax, ay);
            if (anteriorLength == 0.0) return null;

            double anteriorDot = offX * (ax / anteriorLength) + offY * (ay / anteriorLength);
            if (Math.abs(anteriorDot) < 1e-9) return 0.0;
            return anteriorDot > 0.0 ? magnitude : -magnitude;
        }

'''
    if anchor not in a:
        raise RuntimeError('Could not add anatomical perpendicular calculation')
    a = a.replace(anchor, branch + anchor, 1)
activity.write_text(a, encoding='utf-8')

# 4) Landmark definitions for the two Holdaway points not previously required.
guide = java_dir / 'PointGuide.java'
p = guide.read_text(encoding='utf-8')
if 'GUIDE.put("Ls",' not in p:
    anchor = '        GUIDE.put("Pg\'", "Pogonion de tejidos blandos (Pg\'): punto más anterior del mentón blando.");\n'
    if anchor not in p:
        raise RuntimeError('Soft-tissue guide anchor changed upstream')
    additions = (
        '        GUIDE.put("Ls", "Labiale superius (Ls): punto más anterior del bermellón del labio superior en el perfil de tejidos blandos; junto con Pg\' forma la línea H de Holdaway.");\n'
        '        GUIDE.put("Li", "Labiale inferius (Li): punto más anterior del bermellón del labio inferior. La distancia a la línea H Pg\'-Ls se informa con signo anatómico.");\n'
    )
    p = p.replace(anchor, anchor + additions, 1)
guide.write_text(p, encoding='utf-8')

# 5) Guardrails and unit catalog checks.
test_dir = ROOT / 'app/src/test/java/com/cefalo/angulos'
test_dir.mkdir(parents=True, exist_ok=True)
(test_dir / 'PrimarySourceSoftTissueAndRickettsTest.java').write_text(r'''package com.cefalo.angulos;

import static org.junit.Assert.assertTrue;
import org.junit.Test;

public class PrimarySourceSoftTissueAndRickettsTest {
    @Test public void verifiedAdditionalMeasuresArePresent() {
        String angular = MeasurementCatalog.steiner().toString();
        String linear = LinearMeasurementCatalog.cephalometric().toString();
        assertTrue(angular.contains("Holdaway · ángulo H"));
        assertTrue(linear.contains("Steiner · Pogonion a NB"));
        assertTrue(linear.contains("Ricketts · convexidad"));
        assertTrue(linear.contains("Ricketts · U1 a A-Pg"));
        assertTrue(linear.contains("Ricketts · L1 a A-Pg"));
        assertTrue(linear.contains("Holdaway · labio inferior a línea H"));
        assertTrue(LinearMeasurementDefinition.Type.valueOf("ANATOMICAL_PERPENDICULAR") != null);
    }
}
''', encoding='utf-8')

checks = {
    'Holdaway H angle': 'Holdaway · ángulo H' in catalog.read_text(encoding='utf-8'),
    'signed perpendicular type': 'ANATOMICAL_PERPENDICULAR' in linear_def.read_text(encoding='utf-8'),
    'Steiner Pg-NB': 'Steiner · Pogonion a NB' in linear_catalog.read_text(encoding='utf-8'),
    'Ricketts contour': 'Ricketts · convexidad · A a N-Pg' in linear_catalog.read_text(encoding='utf-8'),
    'Ricketts upper incisor APg': 'Ricketts · U1 a A-Pg' in linear_catalog.read_text(encoding='utf-8'),
    'Ricketts lower incisor APg': 'Ricketts · L1 a A-Pg' in linear_catalog.read_text(encoding='utf-8'),
    'Holdaway lower lip H': 'Holdaway · labio inferior a línea H' in linear_catalog.read_text(encoding='utf-8'),
    'Ls guide': 'GUIDE.put("Ls",' in guide.read_text(encoding='utf-8'),
    'Li guide': 'GUIDE.put("Li",' in guide.read_text(encoding='utf-8'),
}
missing = [name for name, ok in checks.items() if not ok]
if missing:
    raise RuntimeError('Primary-source extra audit incomplete: ' + ', '.join(missing))

print('Added mirror-invariant Ricketts A-Pg variables, Steiner Pg-NB, and core Holdaway H-line measures.')
