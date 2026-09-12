from pathlib import Path
import re

ROOT = Path(".")
java_dir = ROOT / "app/src/main/java/com/cefalo/angulos"

# Primary-source audit pass for the dedicated lateral-cephalometric edition.
# Runs AFTER ci/standalone-lateral.py, so it audits the final generated source
# rather than a partial intermediate catalog.

# -----------------------------------------------------------------------------
# 1) Version identity for the audited build.
# -----------------------------------------------------------------------------
gradle = ROOT / "app/build.gradle"
g = gradle.read_text(encoding="utf-8")
g = re.sub(r"versionCode\s+\d+", "versionCode 34", g, count=1)
g = re.sub(r"versionName\s+'[^']+'", "versionName '1.33'", g, count=1)
gradle.write_text(g, encoding="utf-8")

# -----------------------------------------------------------------------------
# 2) Correct a known Downs mismatch generated upstream.
#
# Downs' lower-incisor/occlusal-plane variable is conventionally reported as
# deviation from a right angle (about 14.5 degrees in the classic analysis).
# MeasurementView calculates the geometric angle between the two lines, so this
# standalone edition reports the equivalent geometric value (~104.5 degrees)
# rather than silently labeling an unrelated 55.8-degree value as Downs.
# -----------------------------------------------------------------------------
catalog = java_dir / "MeasurementCatalog.java"
c = catalog.read_text(encoding="utf-8")

old_downs = '''                "Downs · Incisivo inferior / plano oclusal",
                TWO_LINES,
                p("II borde", "II ápice", "Oclusal 1", "Oclusal 2"),
                51.3,
                60.3,
                "55.8° ± 4.5° · referencia clásica de Downs",'''
new_downs = '''                "Downs · Incisivo inferior / plano oclusal · ángulo geométrico",
                TWO_LINES,
                p("II borde", "II ápice", "Oclusal 1", "Oclusal 2"),
                101.0,
                108.0,
                "104.5° ± 3.5° geométricos · equivalente a 14.5° ± 3.5° de desviación respecto a la perpendicular en Downs",'''
if old_downs in c:
    c = c.replace(old_downs, new_downs, 1)
elif "55.8° ± 4.5° · referencia clásica de Downs" in c:
    raise RuntimeError("Downs lower-incisor block changed upstream; audit replacement must be reviewed")
else:
    raise RuntimeError("Downs lower-incisor/occlusal-plane measurement not found")

# McNamara includes the mandibular-plane relation to Frankfort. Keep it
# explicitly labeled in the integrated catalog; no universal automatic cutoff
# is imposed because the original composite standards vary with size/sex/age.
if "McNamara · plano mandibular · FH / Go-Me" not in c:
    method = re.compile(
        r'(public static List<MeasurementDefinition> steiner\(\) \{[\s\S]*?)(\n        return list;\n    \})',
        re.M,
    )
    angular_addition = r'''
        list.add(m(
                "McNamara · plano mandibular · FH / Go-Me",
                TWO_LINES,
                p("Po", "Or", "Go", "Me"),
                Double.NaN,
                Double.NaN,
                "McNamara 1984 · Po-Or / Go-Me · interpretar con la norma compuesta correspondiente a edad/sexo/tamaño facial",
                "Trace Frankfort anatómico Po-Or y el plano mandibular Go-Me.",
                "",
                "Medida vertical del análisis de McNamara. Se informa sin imponer un umbral universal; correlacione con altura facial anteroinferior, longitudes efectivas y eje facial.",
                "",
                true
        ));
'''
    c, n = method.subn(lambda m: m.group(1) + angular_addition + m.group(2), c, count=1)
    if n != 1:
        raise RuntimeError("Could not add McNamara mandibular-plane angle")

catalog.write_text(c, encoding="utf-8")

# -----------------------------------------------------------------------------
# 3) Extend the linear engine with reproducible constructions needed by
#    Jacobson Wits, McNamara and the Jarabak face-height ratio.
# -----------------------------------------------------------------------------
linear_def = java_dir / "LinearMeasurementDefinition.java"
ld = linear_def.read_text(encoding="utf-8")
if "WITS" not in ld:
    old = '''        AXIAL_PROJECTION
    }'''
    new = '''        AXIAL_PROJECTION,
        AXIAL_OFFSET,
        DISTANCE_DIFFERENCE,
        WITS,
        RATIO_PERCENT
    }'''
    if old not in ld:
        raise RuntimeError("LinearMeasurementDefinition.Type enum changed upstream")
    ld = ld.replace(old, new, 1)
linear_def.write_text(ld, encoding="utf-8")

linear_catalog = java_dir / "LinearMeasurementCatalog.java"
l = linear_catalog.read_text(encoding="utf-8")

type_import_anchor = (
    "import static com.cefalo.angulos.LinearMeasurementDefinition.Type.AXIAL_PROJECTION;\n"
)
if "Type.WITS" not in l:
    if type_import_anchor not in l:
        raise RuntimeError("Linear catalog type-import anchor changed upstream")
    l = l.replace(
        type_import_anchor,
        type_import_anchor
        + "import static com.cefalo.angulos.LinearMeasurementDefinition.Type.AXIAL_OFFSET;\n"
        + "import static com.cefalo.angulos.LinearMeasurementDefinition.Type.DISTANCE_DIFFERENCE;\n"
        + "import static com.cefalo.angulos.LinearMeasurementDefinition.Type.WITS;\n"
        + "import static com.cefalo.angulos.LinearMeasurementDefinition.Type.RATIO_PERCENT;\n",
        1,
    )

if "Jacobson · Wits · AO-BO" not in l:
    method = re.compile(
        r'(public static List<LinearMeasurementDefinition> cephalometric\(\) \{[\s\S]*?)(\n        return list;\n    \})',
        re.M,
    )
    linear_addition = r'''
        // Jacobson 1975: project A and B perpendicularly onto the functional
        // occlusal plane. The signed AO-BO distance is positive when AO is
        // anterior to BO (Class-II direction) and negative when BO is anterior.
        list.add(m(
                "Jacobson · Wits · AO-BO",
                WITS,
                RANGE,
                p("Oclusal 2", "Oclusal 1", "A", "B"),
                Double.NaN,
                Double.NaN,
                "Jacobson 1975: mujeres ≈0 mm; varones ≈−1 mm en la muestra adulta original con excelente oclusión",
                "",
                "AO-BO se informa con signo sobre el plano oclusal funcional. Positivo = AO por delante de BO; negativo = BO por delante de AO. Interpretar junto con ANB y el patrón vertical.",
                ""
        ));

        // McNamara 1984: Nasion perpendicular is perpendicular to anatomic
        // Frankfort through N. A signed offset along Po->Or is mirror-invariant:
        // positive means anterior to N-perpendicular, negative posterior.
        list.add(m(
                "McNamara · Punto A a perpendicular de Nasion",
                AXIAL_OFFSET,
                RANGE,
                p("Po", "Or", "N", "A"),
                Double.NaN,
                Double.NaN,
                "A-Nperp en mm · referencia de McNamara dependiente de edad/tamaño facial; dentición mixta ≈0 mm y adulto ≈+1 mm en la descripción original",
                "",
                "Posición anteroposterior del maxilar respecto a Nasion perpendicular. Signo positivo = A anterior a Nperp; negativo = posterior.",
                ""
        ));

        list.add(m(
                "McNamara · Pogonion a perpendicular de Nasion",
                AXIAL_OFFSET,
                RANGE,
                p("Po", "Or", "N", "Pg"),
                Double.NaN,
                Double.NaN,
                "Pg-Nperp en mm · interpretar con las normas compuestas de McNamara para edad/sexo/tamaño facial",
                "",
                "Posición anteroposterior del mentón óseo respecto a Nasion perpendicular. Signo positivo = Pg anterior a Nperp; negativo = posterior.",
                ""
        ));

        list.add(m(
                "McNamara · diferencia maxilomandibular · Co-Gn − Co-A",
                DISTANCE_DIFFERENCE,
                RANGE,
                p("Co", "Gn", "Co", "A"),
                Double.NaN,
                Double.NaN,
                "(Co-Gn) − (Co-A) en mm · norma compuesta dependiente de tamaño facial/edad/sexo",
                "",
                "Diferencia entre longitud mandibular efectiva y longitud maxilar efectiva. No se aplica un corte universal automático.",
                ""
        ));

        // Jarabak/Fizzell: the face-height ratio uses the same four landmarks.
        // Individual heights are also exposed so the user can audit the ratio.
        list.add(m(
                "Björk-Jarabak · altura facial posterior · S-Go",
                DISTANCE,
                RANGE,
                p("S", "Go"),
                Double.NaN,
                Double.NaN,
                "S-Go en mm · componente posterior del índice de altura facial",
                "",
                "Altura facial posterior S-Go; interpretar junto con N-Me y el índice porcentual.",
                ""
        ));

        list.add(m(
                "Björk-Jarabak · altura facial anterior · N-Me",
                DISTANCE,
                RANGE,
                p("N", "Me"),
                Double.NaN,
                Double.NaN,
                "N-Me en mm · componente anterior del índice de altura facial",
                "",
                "Altura facial anterior total N-Me; interpretar junto con S-Go y el índice porcentual.",
                ""
        ));

        list.add(m(
                "Björk-Jarabak · índice de altura facial · S-Go / N-Me",
                RATIO_PERCENT,
                RANGE,
                p("S", "Go", "N", "Me"),
                Double.NaN,
                Double.NaN,
                "S-Go / N-Me × 100 · índice porcentual; comparar con la referencia Björk-Jarabak apropiada",
                "",
                "Índice porcentual de altura facial posterior/anterior. Se informa como proporción y debe interpretarse junto con los ángulos de silla, articular y goníaco.",
                ""
        ));
'''
    l, n = method.subn(lambda m: m.group(1) + linear_addition + m.group(2), l, count=1)
    if n != 1:
        raise RuntimeError("Could not extend standalone primary-source linear catalog")

linear_catalog.write_text(l, encoding="utf-8")

# -----------------------------------------------------------------------------
# 4) Make the one-button standalone edition genuinely comprehensive.
#
# The source app keeps Tweed, Powell, craniocervical and airway definitions in
# separate modes. The standalone home hides those launchers, so without this
# merge those measurements become unreachable. Append them by unique name.
# -----------------------------------------------------------------------------
activity = java_dir / "AnalysisActivity.java"
a = activity.read_text(encoding="utf-8")

default_block = '''        } else {
            definitions = MeasurementCatalog.steiner();
            linearDefinitions = LinearMeasurementCatalog.cephalometric();
        }
'''
comprehensive_block = '''        } else {
            definitions = new ArrayList<>(MeasurementCatalog.steiner());
            addUniqueAngular(definitions, MeasurementCatalog.tweed());
            addUniqueAngular(definitions, MeasurementCatalog.powell());
            addUniqueAngular(definitions, MeasurementCatalog.vertebral());
            addUniqueAngular(definitions, MeasurementCatalog.airwayAngles());

            linearDefinitions = new ArrayList<>(LinearMeasurementCatalog.cephalometric());
            addUniqueLinear(linearDefinitions, LinearMeasurementCatalog.rocabado());
            addUniqueLinear(linearDefinitions, LinearMeasurementCatalog.airway());
        }
'''
if "addUniqueAngular(definitions, MeasurementCatalog.tweed())" not in a:
    if default_block not in a:
        raise RuntimeError("AnalysisActivity default catalog block changed upstream")
    a = a.replace(default_block, comprehensive_block, 1)

helper_anchor = '''    private List<String> buildLandmarkList(
'''
if "private void addUniqueAngular(" not in a:
    helpers = r'''    private void addUniqueAngular(
            List<MeasurementDefinition> target,
            List<MeasurementDefinition> source
    ) {
        if (source == null) return;
        Set<String> names = new LinkedHashSet<>();
        for (MeasurementDefinition def : target) {
            if (def != null) names.add(def.name);
        }
        for (MeasurementDefinition def : source) {
            if (def != null && names.add(def.name)) target.add(def);
        }
    }

    private void addUniqueLinear(
            List<LinearMeasurementDefinition> target,
            List<LinearMeasurementDefinition> source
    ) {
        if (source == null) return;
        Set<String> names = new LinkedHashSet<>();
        for (LinearMeasurementDefinition def : target) {
            if (def != null) names.add(def.name);
        }
        for (LinearMeasurementDefinition def : source) {
            if (def != null && names.add(def.name)) target.add(def);
        }
    }

'''
    if helper_anchor not in a:
        raise RuntimeError("Could not place unique-catalog helpers")
    a = a.replace(helper_anchor, helpers + helper_anchor, 1)

calc_old = '''    private Double calculateLinear(
            LinearMeasurementDefinition def
    ) {
        if (def == null
                || Double.isNaN(mmPerPixel)
                || mmPerPixel <= 0) {
            return null;
        }

        if (def.type == LinearMeasurementDefinition.Type.DISTANCE) {
'''
calc_new = '''    private Double calculateLinear(
            LinearMeasurementDefinition def
    ) {
        if (def == null) {
            return null;
        }

        if (def.type == LinearMeasurementDefinition.Type.RATIO_PERCENT) {
            PointF a = measurementView.getPoint(def.pointLabels[0]);
            PointF b = measurementView.getPoint(def.pointLabels[1]);
            PointF c = measurementView.getPoint(def.pointLabels[2]);
            PointF d = measurementView.getPoint(def.pointLabels[3]);
            if (a == null || b == null || c == null || d == null) return null;

            double numerator = Math.hypot(b.x - a.x, b.y - a.y);
            double denominator = Math.hypot(d.x - c.x, d.y - c.y);
            if (denominator == 0.0) return null;
            return (numerator / denominator) * 100.0;
        }

        if (Double.isNaN(mmPerPixel) || mmPerPixel <= 0) {
            return null;
        }

        if (def.type == LinearMeasurementDefinition.Type.DISTANCE) {
'''
if "Type.RATIO_PERCENT" not in a:
    if calc_old not in a:
        raise RuntimeError("AnalysisActivity calculateLinear guard changed upstream")
    a = a.replace(calc_old, calc_new, 1)

distance_anchor = '''            ) * mmPerPixel;
        }

        if (def.type == LinearMeasurementDefinition.Type.AXIAL_PROJECTION) {
'''
if "Type.WITS" not in a:
    extended_calc = '''            ) * mmPerPixel;
        }

        if (def.type == LinearMeasurementDefinition.Type.AXIAL_OFFSET) {
            PointF axisStart = measurementView.getPoint(def.pointLabels[0]);
            PointF axisEnd = measurementView.getPoint(def.pointLabels[1]);
            PointF origin = measurementView.getPoint(def.pointLabels[2]);
            PointF target = measurementView.getPoint(def.pointLabels[3]);
            if (axisStart == null || axisEnd == null || origin == null || target == null) return null;

            double dx = axisEnd.x - axisStart.x;
            double dy = axisEnd.y - axisStart.y;
            double length = Math.hypot(dx, dy);
            if (length == 0.0) return null;

            return (((target.x - origin.x) * dx + (target.y - origin.y) * dy) / length)
                    * mmPerPixel;
        }

        if (def.type == LinearMeasurementDefinition.Type.DISTANCE_DIFFERENCE) {
            PointF a1 = measurementView.getPoint(def.pointLabels[0]);
            PointF a2 = measurementView.getPoint(def.pointLabels[1]);
            PointF b1 = measurementView.getPoint(def.pointLabels[2]);
            PointF b2 = measurementView.getPoint(def.pointLabels[3]);
            if (a1 == null || a2 == null || b1 == null || b2 == null) return null;

            double first = Math.hypot(a2.x - a1.x, a2.y - a1.y);
            double second = Math.hypot(b2.x - b1.x, b2.y - b1.y);
            return (first - second) * mmPerPixel;
        }

        if (def.type == LinearMeasurementDefinition.Type.WITS) {
            PointF posterior = measurementView.getPoint(def.pointLabels[0]);
            PointF anterior = measurementView.getPoint(def.pointLabels[1]);
            PointF pointA = measurementView.getPoint(def.pointLabels[2]);
            PointF pointB = measurementView.getPoint(def.pointLabels[3]);
            if (posterior == null || anterior == null || pointA == null || pointB == null) return null;

            double dx = anterior.x - posterior.x;
            double dy = anterior.y - posterior.y;
            double length = Math.hypot(dx, dy);
            if (length == 0.0) return null;

            double ao = ((pointA.x - posterior.x) * dx + (pointA.y - posterior.y) * dy) / length;
            double bo = ((pointB.x - posterior.x) * dx + (pointB.y - posterior.y) * dy) / length;
            return (ao - bo) * mmPerPixel;
        }

        if (def.type == LinearMeasurementDefinition.Type.AXIAL_PROJECTION) {
'''
    if distance_anchor not in a:
        raise RuntimeError("AnalysisActivity distance calculation anchor changed upstream")
    a = a.replace(distance_anchor, extended_calc, 1)

dialog_value = 'String.format(Locale.US, "%.2f mm", value)'
if dialog_value in a:
    a = a.replace(dialog_value, "formatLinearValue(def, value)", 1)

pdf_value = '''                String valueLine =
                        String.format(
                                Locale.US,
                                "%.2f mm   ·   Referencia: %s",
                                value,
                                linearNormText(def, value)
                        );'''
pdf_replacement = '''                String valueLine =
                        formatLinearValue(def, value) +
                        "   ·   Referencia: " +
                        linearNormText(def, value);'''
if pdf_value in a:
    a = a.replace(pdf_value, pdf_replacement, 1)

format_anchor = '''    private Double calculateLinear(
'''
if "private String formatLinearValue(" not in a:
    formatter = r'''    private String formatLinearValue(
            LinearMeasurementDefinition def,
            double value
    ) {
        if (def != null
                && def.type == LinearMeasurementDefinition.Type.RATIO_PERCENT) {
            return String.format(Locale.US, "%.1f %%", value);
        }
        return String.format(Locale.US, "%.2f mm", value);
    }

'''
    if format_anchor not in a:
        raise RuntimeError("Could not place linear value formatter")
    a = a.replace(format_anchor, formatter + format_anchor, 1)

activity.write_text(a, encoding="utf-8")

# -----------------------------------------------------------------------------
# 5) Landmark help: clarify the functional occlusal-plane direction used for
#    Wits without inventing AO/BO points the user would have to place manually.
# -----------------------------------------------------------------------------
guide = java_dir / "PointGuide.java"
p = guide.read_text(encoding="utf-8")
p = p.replace(
    'GUIDE.put("Oclusal 1", "Plano oclusal, punto anterior: ubique el punto medio de la sobremordida en la región incisiva cuando sea visible; use el mismo criterio de construcción del plano oclusal seleccionado.");',
    'GUIDE.put("Oclusal 1", "Plano oclusal funcional, punto anterior: ubique el punto medio de la sobremordida/intercuspidación en la región anterior según el protocolo. Para Wits, Oclusal 1 es el extremo anterior del eje; la app proyecta A y B automáticamente y no se marcan AO/BO.");'
)
p = p.replace(
    'GUIDE.put("Oclusal 2", "Plano oclusal, punto posterior: ubique el punto medio de la intercuspidación de los primeros molares permanentes o la referencia posterior definida por el protocolo. Debe formar con Oclusal 1 un único plano reproducible.");',
    'GUIDE.put("Oclusal 2", "Plano oclusal funcional, punto posterior: ubique el punto medio de la intercuspidación posterior (habitualmente primeros molares permanentes) según el protocolo. Para Wits, Oclusal 2 es el extremo posterior y Oclusal 1 el anterior; la app conserva así el signo AO-BO aunque la imagen esté espejada.");'
)
guide.write_text(p, encoding="utf-8")

# -----------------------------------------------------------------------------
# 6) Unit tests and guardrails.
# -----------------------------------------------------------------------------
test_dir = ROOT / "app/src/test/java/com/cefalo/angulos"
test_dir.mkdir(parents=True, exist_ok=True)
test = test_dir / "PrimarySourceCephalometricAuditTest.java"
test.write_text(r'''package com.cefalo.angulos;

import static org.junit.Assert.assertTrue;

import org.junit.Test;

public class PrimarySourceCephalometricAuditTest {
    private static boolean hasAngular(String token) {
        for (MeasurementDefinition def : MeasurementCatalog.steiner()) {
            if (def.name.contains(token)) return true;
        }
        return false;
    }

    private static boolean hasLinear(String token) {
        for (LinearMeasurementDefinition def : LinearMeasurementCatalog.cephalometric()) {
            if (def.name.contains(token)) return true;
        }
        return false;
    }

    @Test public void primarySourceAdditionsArePresent() {
        assertTrue(hasAngular("McNamara · plano mandibular"));
        assertTrue(hasLinear("Jacobson · Wits"));
        assertTrue(hasLinear("Punto A a perpendicular de Nasion"));
        assertTrue(hasLinear("Pogonion a perpendicular de Nasion"));
        assertTrue(hasLinear("diferencia maxilomandibular"));
        assertTrue(hasLinear("índice de altura facial"));
    }

    @Test public void linearEngineContainsDerivedTypes() {
        assertTrue(LinearMeasurementDefinition.Type.valueOf("WITS") != null);
        assertTrue(LinearMeasurementDefinition.Type.valueOf("AXIAL_OFFSET") != null);
        assertTrue(LinearMeasurementDefinition.Type.valueOf("DISTANCE_DIFFERENCE") != null);
        assertTrue(LinearMeasurementDefinition.Type.valueOf("RATIO_PERCENT") != null);
    }
}
''', encoding="utf-8")

checks = {
    "version 1.33": "versionName '1.33'" in gradle.read_text(encoding="utf-8"),
    "Downs correction": "104.5° ± 3.5° geométricos" in catalog.read_text(encoding="utf-8"),
    "Wits catalog": "Jacobson · Wits · AO-BO" in linear_catalog.read_text(encoding="utf-8"),
    "McNamara A-Nperp": "Punto A a perpendicular de Nasion" in linear_catalog.read_text(encoding="utf-8"),
    "McNamara Pg-Nperp": "Pogonion a perpendicular de Nasion" in linear_catalog.read_text(encoding="utf-8"),
    "McNamara differential": "diferencia maxilomandibular" in linear_catalog.read_text(encoding="utf-8"),
    "Jarabak ratio": "índice de altura facial" in linear_catalog.read_text(encoding="utf-8"),
    "comprehensive Tweed merge": "addUniqueAngular(definitions, MeasurementCatalog.tweed())" in activity.read_text(encoding="utf-8"),
    "comprehensive Powell merge": "addUniqueAngular(definitions, MeasurementCatalog.powell())" in activity.read_text(encoding="utf-8"),
    "comprehensive cervical merge": "addUniqueLinear(linearDefinitions, LinearMeasurementCatalog.rocabado())" in activity.read_text(encoding="utf-8"),
    "comprehensive airway merge": "addUniqueLinear(linearDefinitions, LinearMeasurementCatalog.airway())" in activity.read_text(encoding="utf-8"),
}
missing = [name for name, ok in checks.items() if not ok]
if missing:
    raise RuntimeError("Primary-source cephalometric audit incomplete: " + ", ".join(missing))

print(
    "Primary-source audit applied: Wits, expanded McNamara, Jarabak face-height "
    "index, corrected Downs geometry, and previously hidden Tweed/Powell/"
    "craniocervical/airway measurements integrated into the standalone analysis."
)
