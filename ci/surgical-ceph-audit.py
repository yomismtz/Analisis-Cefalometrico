from pathlib import Path
import re

ROOT = Path(".")
JAVA = ROOT / "app/src/main/java/com/cefalo/angulos"
TEST = ROOT / "app/src/test/java/com/cefalo/angulos"
TEST.mkdir(parents=True, exist_ok=True)

# Burstone COGS (1978) + Legan-Burstone soft tissue (1980), primary-source pass.
gradle = ROOT / "app/build.gradle"
g = gradle.read_text(encoding="utf-8")
g = re.sub(r"versionCode\s+\d+", "versionCode 35", g, count=1)
g = re.sub(r"versionName\s+'[^']+'", "versionName '1.34'", g, count=1)
gradle.write_text(g, encoding="utf-8")

# --- Angular types and geometry ------------------------------------------------
measurement_def = JAVA / "MeasurementDefinition.java"
md = measurement_def.read_text(encoding="utf-8")
old_enum = "public enum Type { THREE_POINTS, TWO_LINES, SIGNED_ANB }"
new_enum = "public enum Type { THREE_POINTS, TWO_LINES, SIGNED_ANB, HP_ANGLE, SIGNED_CHAIN_ANGLE }"
if old_enum in md:
    md = md.replace(old_enum, new_enum, 1)
elif "HP_ANGLE" not in md or "SIGNED_CHAIN_ANGLE" not in md:
    raise RuntimeError("MeasurementDefinition.Type changed upstream")
measurement_def.write_text(md, encoding="utf-8")

view = JAVA / "MeasurementView.java"
v = view.read_text(encoding="utf-8")
if "definition.type == MeasurementDefinition.Type.HP_ANGLE" not in v:
    anchor = "        if (definition.type == MeasurementDefinition.Type.THREE_POINTS) {\n"
    addition = r'''        if (definition.type == MeasurementDefinition.Type.HP_ANGLE) {
            if (definition.pointLabels.length < 6) return null;
            PointF lineA = getPoint(definition.pointLabels[0]);
            PointF lineB = getPoint(definition.pointLabels[1]);
            PointF s = getPoint(definition.pointLabels[2]);
            PointF n = getPoint(definition.pointLabels[3]);
            PointF po = getPoint(definition.pointLabels[4]);
            PointF or = getPoint(definition.pointLabels[5]);
            if (lineA == null || lineB == null || s == null || n == null
                    || po == null || or == null) return null;
            double[] hp = constructedHpDirection(s, n, po, or);
            if (hp == null) return null;
            double tx = lineB.x - lineA.x;
            double ty = lineB.y - lineA.y;
            double tm = Math.hypot(tx, ty);
            if (tm == 0.0) return null;
            double cos = (tx * hp[0] + ty * hp[1]) / tm;
            cos = Math.max(-1.0, Math.min(1.0, cos));
            double raw = Math.toDegrees(Math.acos(cos));
            return Math.min(raw, 180.0 - raw);
        }

        if (definition.type == MeasurementDefinition.Type.SIGNED_CHAIN_ANGLE) {
            if (definition.pointLabels.length < 5) return null;
            PointF first = getPoint(definition.pointLabels[0]);
            PointF vertex = getPoint(definition.pointLabels[1]);
            PointF last = getPoint(definition.pointLabels[2]);
            PointF po = getPoint(definition.pointLabels[3]);
            PointF or = getPoint(definition.pointLabels[4]);
            if (first == null || vertex == null || last == null || po == null || or == null) return null;
            double magnitude = angleBetweenVectors(first, vertex, vertex, last);
            double dx = last.x - first.x;
            double dy = last.y - first.y;
            double len2 = dx * dx + dy * dy;
            if (len2 == 0.0) return null;
            double t = ((vertex.x - first.x) * dx + (vertex.y - first.y) * dy) / len2;
            double projX = first.x + t * dx;
            double projY = first.y + t * dy;
            double offX = vertex.x - projX;
            double offY = vertex.y - projY;
            double ax = or.x - po.x;
            double ay = or.y - po.y;
            double am = Math.hypot(ax, ay);
            if (am == 0.0) return null;
            double anteriorDot = offX * (ax / am) + offY * (ay / am);
            if (Math.abs(anteriorDot) < 1e-9) return 0.0;
            return anteriorDot > 0.0 ? magnitude : -magnitude;
        }

'''
    if anchor not in v:
        raise RuntimeError("MeasurementView calculate anchor changed upstream")
    v = v.replace(anchor, addition + anchor, 1)

if "private double[] constructedHpDirection(" not in v:
    anchor = "    private double angleAtVertex(PointF a, PointF b, PointF c) {\n"
    helper = r'''    private double[] constructedHpDirection(PointF s, PointF n, PointF po, PointF or) {
        double sx = n.x - s.x, sy = n.y - s.y;
        double sm = Math.hypot(sx, sy);
        double fx = or.x - po.x, fy = or.y - po.y;
        double fm = Math.hypot(fx, fy);
        if (sm == 0.0 || fm == 0.0) return null;
        sx /= sm; sy /= sm; fx /= fm; fy /= fm;
        double a = Math.toRadians(7.0), ca = Math.cos(a), sa = Math.sin(a);
        double p1x = sx * ca - sy * sa, p1y = sx * sa + sy * ca;
        double p2x = sx * ca + sy * sa, p2y = -sx * sa + sy * ca;
        double d1 = Math.abs(p1x * fx + p1y * fy), d2 = Math.abs(p2x * fx + p2y * fy);
        double hx = d1 >= d2 ? p1x : p2x, hy = d1 >= d2 ? p1y : p2y;
        if (hx * fx + hy * fy < 0.0) { hx = -hx; hy = -hy; }
        return new double[]{hx, hy};
    }

'''
    if anchor not in v:
        raise RuntimeError("Could not place HP geometry helper")
    v = v.replace(anchor, helper + anchor, 1)
view.write_text(v, encoding="utf-8")

# --- Linear types -------------------------------------------------------------
linear_def = JAVA / "LinearMeasurementDefinition.java"
ld = linear_def.read_text(encoding="utf-8")
if "HP_PROJECTION_ABS" not in ld:
    pattern = re.compile(r"(ANATOMICAL_PERPENDICULAR)(\s*\n\s*})")
    ld, n = pattern.subn(
        r"\1,\n        HP_PROJECTION_ABS,\n        HP_OFFSET,\n        HP_PERPENDICULAR_ABS,\n"
        r"        POINT_TO_LINE_ABS,\n        LINE_PROJECTION_ABS,\n        RATIO_DECIMAL,\n        HP_PERP_RATIO\2",
        ld, count=1
    )
    if n != 1:
        raise RuntimeError("Could not extend final linear type enum")
linear_def.write_text(ld, encoding="utf-8")

linear_catalog = JAVA / "LinearMeasurementCatalog.java"
lc = linear_catalog.read_text(encoding="utf-8")
if "Type.HP_PROJECTION_ABS" not in lc:
    anchor = "import static com.cefalo.angulos.LinearMeasurementDefinition.Type.ANATOMICAL_PERPENDICULAR;\n"
    imports = (
        "import static com.cefalo.angulos.LinearMeasurementDefinition.Type.HP_PROJECTION_ABS;\n"
        "import static com.cefalo.angulos.LinearMeasurementDefinition.Type.HP_OFFSET;\n"
        "import static com.cefalo.angulos.LinearMeasurementDefinition.Type.HP_PERPENDICULAR_ABS;\n"
        "import static com.cefalo.angulos.LinearMeasurementDefinition.Type.POINT_TO_LINE_ABS;\n"
        "import static com.cefalo.angulos.LinearMeasurementDefinition.Type.LINE_PROJECTION_ABS;\n"
        "import static com.cefalo.angulos.LinearMeasurementDefinition.Type.RATIO_DECIMAL;\n"
        "import static com.cefalo.angulos.LinearMeasurementDefinition.Type.HP_PERP_RATIO;\n"
    )
    if anchor not in lc:
        raise RuntimeError("Audited linear import anchor missing")
    lc = lc.replace(anchor, anchor + imports, 1)

if "Burstone COGS · Ar-Ptm // HP" not in lc:
    method = re.compile(
        r'(public static List<LinearMeasurementDefinition> cephalometric\(\) \{[\s\S]*?)(\n        return list;\n    \})',
        re.M,
    )
    additions = r'''
        // Burstone et al. 1978 — COGS. HP is constructed 7 degrees from S-N.
        list.add(m("Burstone COGS · Ar-Ptm // HP", HP_PROJECTION_ABS, RANGE,
                p("Ar", "Ptm", "S", "N", "Po", "Or"), Double.NaN, Double.NaN,
                "COGS 1978 · referencia original dependiente de sexo", "",
                "Longitud Ar-Ptm proyectada paralela a HP.", ""));
        list.add(m("Burstone COGS · Ptm-N // HP", HP_PROJECTION_ABS, RANGE,
                p("Ptm", "N", "S", "N", "Po", "Or"), Double.NaN, Double.NaN,
                "COGS 1978 · referencia original dependiente de sexo", "",
                "Longitud Ptm-N proyectada paralela a HP.", ""));
        list.add(m("Burstone COGS · N-A // HP", HP_OFFSET, RANGE,
                p("N", "A", "S", "N", "Po", "Or"), Double.NaN, Double.NaN,
                "COGS 1978 · referencia original dependiente de sexo", "",
                "Posición sagital de A respecto de N sobre HP; positivo = anterior.", ""));
        list.add(m("Burstone COGS · N-B // HP", HP_OFFSET, RANGE,
                p("N", "B", "S", "N", "Po", "Or"), Double.NaN, Double.NaN,
                "COGS 1978 · referencia original dependiente de sexo", "",
                "Posición sagital de B respecto de N sobre HP; positivo = anterior.", ""));
        list.add(m("Burstone COGS · N-Pg // HP", HP_OFFSET, RANGE,
                p("N", "Pg", "S", "N", "Po", "Or"), Double.NaN, Double.NaN,
                "COGS 1978 · referencia original dependiente de sexo", "",
                "Posición sagital de Pg respecto de N sobre HP; positivo = anterior.", ""));
        list.add(m("Burstone COGS · N-ENA ⟂ HP", HP_PERPENDICULAR_ABS, RANGE,
                p("N", "ENA", "S", "N", "Po", "Or"), Double.NaN, Double.NaN,
                "COGS 1978 · N-ANS", "", "Altura anterior superior N-ANS.", ""));
        list.add(m("Burstone COGS · ENA-Gn ⟂ HP", HP_PERPENDICULAR_ABS, RANGE,
                p("ENA", "Gn", "S", "N", "Po", "Or"), Double.NaN, Double.NaN,
                "COGS 1978 · ANS-Gn", "", "Altura anterior inferior ANS-Gn.", ""));
        list.add(m("Burstone COGS · ENP-N ⟂ HP", HP_PERPENDICULAR_ABS, RANGE,
                p("ENP", "N", "S", "N", "Po", "Or"), Double.NaN, Double.NaN,
                "COGS 1978 · PNS-N", "", "Altura posterior PNS-N perpendicular a HP.", ""));
        list.add(m("Burstone COGS · U1-NF · altura", POINT_TO_LINE_ABS, RANGE,
                p("ENP", "ENA", "IS borde"), Double.NaN, Double.NaN,
                "COGS 1978 · U1 a plano nasal", "", "Altura dentoalveolar anterior maxilar.", ""));
        list.add(m("Burstone COGS · U6-NF · altura", POINT_TO_LINE_ABS, RANGE,
                p("ENP", "ENA", "U6 cusp"), Double.NaN, Double.NaN,
                "COGS 1978 · U6 a plano nasal", "", "Altura dentoalveolar posterior maxilar.", ""));
        list.add(m("Burstone COGS · L1-MP · altura", POINT_TO_LINE_ABS, RANGE,
                p("Go", "Me", "II borde"), Double.NaN, Double.NaN,
                "COGS 1978 · L1 a plano mandibular", "", "Altura dentoalveolar anterior mandibular.", ""));
        list.add(m("Burstone COGS · L6-MP · altura", POINT_TO_LINE_ABS, RANGE,
                p("Go", "Me", "L6 cusp"), Double.NaN, Double.NaN,
                "COGS 1978 · L6 a plano mandibular", "", "Altura dentoalveolar posterior mandibular.", ""));
        list.add(m("Burstone COGS · ENP-ENA // HP", HP_PROJECTION_ABS, RANGE,
                p("ENP", "ENA", "S", "N", "Po", "Or"), Double.NaN, Double.NaN,
                "COGS 1978 · PNS-ANS", "", "Longitud maxilar PNS-ANS paralela a HP.", ""));
        list.add(m("Burstone COGS · Ar-Go", DISTANCE, RANGE,
                p("Ar", "Go"), Double.NaN, Double.NaN,
                "COGS 1978 · altura de rama", "", "Longitud Ar-Go.", ""));
        list.add(m("Burstone COGS · Go-Pg", DISTANCE, RANGE,
                p("Go", "Pg"), Double.NaN, Double.NaN,
                "COGS 1978 · longitud del cuerpo", "", "Longitud Go-Pg.", ""));
        list.add(m("Burstone COGS · B-Pg // MP", LINE_PROJECTION_ABS, RANGE,
                p("B", "Pg", "Go", "Me"), Double.NaN, Double.NaN,
                "COGS 1978 · profundidad de sínfisis", "", "Componente B-Pg paralelo a MP.", ""));
        list.add(m("Burstone COGS · A-B / OP", WITS, RANGE,
                p("Oclusal 2", "Oclusal 1", "A", "B"), Double.NaN, Double.NaN,
                "COGS 1978 · A-B proyectado en plano oclusal", "",
                "Discrepancia sagital A-B sobre el plano oclusal.", ""));

        // Legan & Burstone 1980 — soft tissue.
        list.add(m("Legan-Burstone · prognatismo maxilar · G'-Sn // HP", HP_OFFSET, RANGE,
                p("G'", "Sn", "S", "N", "Po", "Or"), 3.0, 9.0,
                "6 ± 3 mm · Legan-Burstone 1980",
                "Por debajo de ±1 DE de la muestra original.", "Dentro de ±1 DE de la muestra original.",
                "Por encima de ±1 DE de la muestra original."));
        list.add(m("Legan-Burstone · prognatismo mandibular · G'-Pg' // HP", HP_OFFSET, RANGE,
                p("G'", "Pg'", "S", "N", "Po", "Or"), -4.0, 4.0,
                "0 ± 4 mm · Legan-Burstone 1980",
                "Por debajo de ±1 DE de la muestra original.", "Dentro de ±1 DE de la muestra original.",
                "Por encima de ±1 DE de la muestra original."));
        list.add(m("Legan-Burstone · razón altura vertical · G'-Sn / Sn-Me'", HP_PERP_RATIO, RANGE,
                p("G'", "Sn", "Sn", "Me'", "S", "N", "Po", "Or"), Double.NaN, Double.NaN,
                "1.0 · razón original; sin DE universal", "",
                "Razón vertical superior/inferior; interpretar descriptivamente.", ""));
        list.add(m("Legan-Burstone · razón altura-profundidad inferior · Sn-Gn' / C-Gn'", RATIO_DECIMAL, RANGE,
                p("Sn", "Gn'", "C", "Gn'"), Double.NaN, Double.NaN,
                "1.2 · razón original; sin DE universal", "",
                "Razón de altura facial inferior/profundidad cervical.", ""));
        list.add(m("Legan-Burstone · labio superior a Sn-Pg'", POINT_TO_LINE_ABS, RANGE,
                p("Sn", "Pg'", "Ls"), 2.0, 4.0, "3 ± 1 mm · Legan-Burstone 1980",
                "Por debajo de ±1 DE de la muestra original.", "Dentro de ±1 DE de la muestra original.",
                "Por encima de ±1 DE de la muestra original."));
        list.add(m("Legan-Burstone · labio inferior a Sn-Pg'", POINT_TO_LINE_ABS, RANGE,
                p("Sn", "Pg'", "Li"), 1.0, 3.0, "2 ± 1 mm · Legan-Burstone 1980",
                "Por debajo de ±1 DE de la muestra original.", "Dentro de ±1 DE de la muestra original.",
                "Por encima de ±1 DE de la muestra original."));
        list.add(m("Legan-Burstone · surco mentolabial · Si a Li-Pg'", POINT_TO_LINE_ABS, RANGE,
                p("Li", "Pg'", "Si"), 2.0, 6.0, "4 ± 2 mm · Legan-Burstone 1980",
                "Por debajo de ±1 DE de la muestra original.", "Dentro de ±1 DE de la muestra original.",
                "Por encima de ±1 DE de la muestra original."));
        list.add(m("Legan-Burstone · razón labio-mentón · Sn-Stms / Stmi-Me'", HP_PERP_RATIO, RANGE,
                p("Sn", "Stms", "Stmi", "Me'", "S", "N", "Po", "Or"), Double.NaN, Double.NaN,
                "0.5 · razón original; sin DE universal", "",
                "Razón vertical labio superior/segmento labio inferior-mentón.", ""));
        list.add(m("Legan-Burstone · exposición incisivo superior · Stms-U1", HP_PERPENDICULAR_ABS, RANGE,
                p("Stms", "IS borde", "S", "N", "Po", "Or"), 0.0, 4.0,
                "2 ± 2 mm · Legan-Burstone 1980",
                "Por debajo de ±1 DE de la muestra original.", "Dentro de ±1 DE de la muestra original.",
                "Por encima de ±1 DE de la muestra original."));
        list.add(m("Legan-Burstone · espacio interlabial · Stms-Stmi", HP_PERPENDICULAR_ABS, RANGE,
                p("Stms", "Stmi", "S", "N", "Po", "Or"), 0.0, 4.0,
                "2 ± 2 mm · Legan-Burstone 1980",
                "Por debajo de ±1 DE de la muestra original.", "Dentro de ±1 DE de la muestra original.",
                "Por encima de ±1 DE de la muestra original."));
'''
    lc, n = method.subn(lambda m: m.group(1) + additions + m.group(2), lc, count=1)
    if n != 1:
        raise RuntimeError("Could not append COGS/Legan linear catalog")
linear_catalog.write_text(lc, encoding="utf-8")

# --- Angular catalog ----------------------------------------------------------
catalog = JAVA / "MeasurementCatalog.java"
c = catalog.read_text(encoding="utf-8")
if "Burstone COGS · convexidad N-A-Pg" not in c:
    method = re.compile(
        r'(public static List<MeasurementDefinition> steiner\(\) \{[\s\S]*?)(\n        return list;\n    \})',
        re.M,
    )
    additions = r'''
        list.add(m("Burstone COGS · convexidad N-A-Pg",
                MeasurementDefinition.Type.SIGNED_CHAIN_ANGLE,
                p("N", "A", "Pg", "Po", "Or"), Double.NaN, Double.NaN,
                "COGS 1978 · referencia original dependiente de sexo",
                "N-A-Pg con signo anatómico.", "", "Convexidad COGS.", "", false));
        list.add(m("Burstone COGS · MP-HP",
                MeasurementDefinition.Type.HP_ANGLE,
                p("Go", "Me", "S", "N", "Po", "Or"), Double.NaN, Double.NaN,
                "COGS 1978 · referencia original dependiente de sexo",
                "Go-Me respecto del HP construido 7° de S-N.", "", "MP-HP.", "", false));
        list.add(m("Burstone COGS · ángulo goníaco Ar-Go-Gn",
                THREE_POINTS, p("Ar", "Go", "Gn"), Double.NaN, Double.NaN,
                "COGS 1978 · referencia original dependiente de sexo",
                "Ar-Go-Gn; Go es el vértice.", "", "Ángulo goníaco COGS.", "", false));
        list.add(m("Burstone COGS · OP-HP",
                MeasurementDefinition.Type.HP_ANGLE,
                p("Oclusal 2", "Oclusal 1", "S", "N", "Po", "Or"), Double.NaN, Double.NaN,
                "COGS 1978 · referencia original dependiente de sexo",
                "Plano oclusal respecto de HP.", "", "OP-HP.", "", false));
        list.add(m("Burstone COGS · U1-NF", TWO_LINES,
                p("IS borde", "IS ápice", "ENP", "ENA"), Double.NaN, Double.NaN,
                "COGS 1978 · referencia original dependiente de sexo",
                "Eje U1 respecto del plano nasal/palatino.", "", "U1-NF.", "", true));
        list.add(m("Burstone COGS · L1-MP", TWO_LINES,
                p("II borde", "II ápice", "Go", "Me"), Double.NaN, Double.NaN,
                "COGS 1978 · referencia original dependiente de sexo",
                "Eje L1 respecto del plano mandibular.", "", "L1-MP.", "", true));

        list.add(m("Legan-Burstone · convexidad facial · G'-Sn-Pg'", TWO_LINES,
                p("G'", "Sn", "Sn", "Pg'"), 8.0, 16.0,
                "12 ± 4° · Legan-Burstone 1980", "Trace G'-Sn y Sn-Pg'.",
                "Por debajo de ±1 DE de la muestra original.", "Dentro de ±1 DE de la muestra original.",
                "Por encima de ±1 DE de la muestra original.", false));
        list.add(m("Legan-Burstone · ángulo cara inferior-garganta · Sn-Gn'-C", THREE_POINTS,
                p("Sn", "Gn'", "C"), 93.0, 107.0,
                "100 ± 7° · Legan-Burstone 1980", "Gn' es el vértice.",
                "Por debajo de ±1 DE de la muestra original.", "Dentro de ±1 DE de la muestra original.",
                "Por encima de ±1 DE de la muestra original.", false));
        list.add(m("Legan-Burstone · ángulo nasolabial · Cm-Sn-Ls", THREE_POINTS,
                p("Cm", "Sn", "Ls"), 94.0, 110.0,
                "102 ± 8° · Legan-Burstone 1980", "Sn es el vértice.",
                "Por debajo de ±1 DE de la muestra original.", "Dentro de ±1 DE de la muestra original.",
                "Por encima de ±1 DE de la muestra original.", false));
'''
    c, n = method.subn(lambda m: m.group(1) + additions + m.group(2), c, count=1)
    if n != 1:
        raise RuntimeError("Could not append COGS/Legan angular catalog")
catalog.write_text(c, encoding="utf-8")

# --- AnalysisActivity derived linear engine + dynamic COGS references --------
activity = JAVA / "AnalysisActivity.java"
a = activity.read_text(encoding="utf-8")

if "private double[] constructedHpDirection(" not in a:
    anchor = "    private String formatLinearValue(\n"
    helper = r'''    private double[] constructedHpDirection(PointF s, PointF n, PointF po, PointF or) {
        if (s == null || n == null || po == null || or == null) return null;
        double sx = n.x - s.x, sy = n.y - s.y, sm = Math.hypot(sx, sy);
        double fx = or.x - po.x, fy = or.y - po.y, fm = Math.hypot(fx, fy);
        if (sm == 0.0 || fm == 0.0) return null;
        sx /= sm; sy /= sm; fx /= fm; fy /= fm;
        double r = Math.toRadians(7.0), ca = Math.cos(r), sa = Math.sin(r);
        double p1x = sx * ca - sy * sa, p1y = sx * sa + sy * ca;
        double p2x = sx * ca + sy * sa, p2y = -sx * sa + sy * ca;
        double d1 = Math.abs(p1x * fx + p1y * fy), d2 = Math.abs(p2x * fx + p2y * fy);
        double hx = d1 >= d2 ? p1x : p2x, hy = d1 >= d2 ? p1y : p2y;
        if (hx * fx + hy * fy < 0.0) { hx = -hx; hy = -hy; }
        return new double[]{hx, hy};
    }

    private double pointToLinePixels(PointF a, PointF b, PointF p) {
        double dx = b.x - a.x, dy = b.y - a.y, len = Math.hypot(dx, dy);
        if (len == 0.0) return Double.NaN;
        return Math.abs(dx * (p.y - a.y) - dy * (p.x - a.x)) / len;
    }

'''
    if anchor not in a:
        raise RuntimeError("Could not place HP helpers")
    a = a.replace(anchor, helper + anchor, 1)

old_formatter = '''        if (def != null
                && def.type == LinearMeasurementDefinition.Type.RATIO_PERCENT) {
            return String.format(Locale.US, "%.1f %%", value);
        }
        return String.format(Locale.US, "%.2f mm", value);'''
new_formatter = '''        if (def != null
                && def.type == LinearMeasurementDefinition.Type.RATIO_PERCENT) {
            return String.format(Locale.US, "%.1f %%", value);
        }
        if (def != null
                && (def.type == LinearMeasurementDefinition.Type.RATIO_DECIMAL
                || def.type == LinearMeasurementDefinition.Type.HP_PERP_RATIO)) {
            return String.format(Locale.US, "%.2f", value);
        }
        return String.format(Locale.US, "%.2f mm", value);'''
if old_formatter in a:
    a = a.replace(old_formatter, new_formatter, 1)

guard = '''        if (Double.isNaN(mmPerPixel) || mmPerPixel <= 0) {
            return null;
        }
'''
if "def.type == LinearMeasurementDefinition.Type.RATIO_DECIMAL" not in a:
    pre = r'''        if (def.type == LinearMeasurementDefinition.Type.RATIO_DECIMAL) {
            PointF a1 = measurementView.getPoint(def.pointLabels[0]);
            PointF a2 = measurementView.getPoint(def.pointLabels[1]);
            PointF b1 = measurementView.getPoint(def.pointLabels[2]);
            PointF b2 = measurementView.getPoint(def.pointLabels[3]);
            if (a1 == null || a2 == null || b1 == null || b2 == null) return null;
            double d1 = Math.hypot(a2.x - a1.x, a2.y - a1.y);
            double d2 = Math.hypot(b2.x - b1.x, b2.y - b1.y);
            return d2 == 0.0 ? null : d1 / d2;
        }

        if (def.type == LinearMeasurementDefinition.Type.HP_PERP_RATIO) {
            PointF a1 = measurementView.getPoint(def.pointLabels[0]);
            PointF a2 = measurementView.getPoint(def.pointLabels[1]);
            PointF b1 = measurementView.getPoint(def.pointLabels[2]);
            PointF b2 = measurementView.getPoint(def.pointLabels[3]);
            PointF s = measurementView.getPoint(def.pointLabels[4]);
            PointF n = measurementView.getPoint(def.pointLabels[5]);
            PointF po = measurementView.getPoint(def.pointLabels[6]);
            PointF or = measurementView.getPoint(def.pointLabels[7]);
            if (a1 == null || a2 == null || b1 == null || b2 == null
                    || s == null || n == null || po == null || or == null) return null;
            double[] hp = constructedHpDirection(s, n, po, or);
            if (hp == null) return null;
            double nx = -hp[1], ny = hp[0];
            double d1 = Math.abs((a2.x - a1.x) * nx + (a2.y - a1.y) * ny);
            double d2 = Math.abs((b2.x - b1.x) * nx + (b2.y - b1.y) * ny);
            return d2 == 0.0 ? null : d1 / d2;
        }

'''
    if guard not in a:
        raise RuntimeError("Calibration guard missing")
    a = a.replace(guard, pre + guard, 1)

distance_anchor = "        if (def.type == LinearMeasurementDefinition.Type.DISTANCE) {\n"
if "def.type == LinearMeasurementDefinition.Type.HP_PROJECTION_ABS" not in a:
    derived = r'''        if (def.type == LinearMeasurementDefinition.Type.HP_PROJECTION_ABS
                || def.type == LinearMeasurementDefinition.Type.HP_OFFSET
                || def.type == LinearMeasurementDefinition.Type.HP_PERPENDICULAR_ABS) {
            PointF first = measurementView.getPoint(def.pointLabels[0]);
            PointF second = measurementView.getPoint(def.pointLabels[1]);
            PointF s = measurementView.getPoint(def.pointLabels[2]);
            PointF n = measurementView.getPoint(def.pointLabels[3]);
            PointF po = measurementView.getPoint(def.pointLabels[4]);
            PointF or = measurementView.getPoint(def.pointLabels[5]);
            if (first == null || second == null || s == null || n == null || po == null || or == null) return null;
            double[] hp = constructedHpDirection(s, n, po, or);
            if (hp == null) return null;
            double vx = second.x - first.x, vy = second.y - first.y;
            if (def.type == LinearMeasurementDefinition.Type.HP_PERPENDICULAR_ABS) {
                return Math.abs(vx * (-hp[1]) + vy * hp[0]) * mmPerPixel;
            }
            double along = vx * hp[0] + vy * hp[1];
            return (def.type == LinearMeasurementDefinition.Type.HP_PROJECTION_ABS
                    ? Math.abs(along) : along) * mmPerPixel;
        }

        if (def.type == LinearMeasurementDefinition.Type.POINT_TO_LINE_ABS) {
            PointF x = measurementView.getPoint(def.pointLabels[0]);
            PointF y = measurementView.getPoint(def.pointLabels[1]);
            PointF p = measurementView.getPoint(def.pointLabels[2]);
            if (x == null || y == null || p == null) return null;
            double px = pointToLinePixels(x, y, p);
            return Double.isNaN(px) ? null : px * mmPerPixel;
        }

        if (def.type == LinearMeasurementDefinition.Type.LINE_PROJECTION_ABS) {
            PointF p1 = measurementView.getPoint(def.pointLabels[0]);
            PointF p2 = measurementView.getPoint(def.pointLabels[1]);
            PointF r1 = measurementView.getPoint(def.pointLabels[2]);
            PointF r2 = measurementView.getPoint(def.pointLabels[3]);
            if (p1 == null || p2 == null || r1 == null || r2 == null) return null;
            double rx = r2.x - r1.x, ry = r2.y - r1.y, rm = Math.hypot(rx, ry);
            if (rm == 0.0) return null;
            return Math.abs(((p2.x-p1.x)*rx + (p2.y-p1.y)*ry) / rm) * mmPerPixel;
        }

'''
    if distance_anchor not in a:
        raise RuntimeError("Distance anchor missing")
    a = a.replace(distance_anchor, derived + distance_anchor, 1)

if "private static final class SexNorm" not in a:
    anchor = "    private String resultsSafetyNotice() {\n"
    norms = r'''    private static final class SexNorm {
        final double mm, ms, fm, fs;
        SexNorm(double mm, double ms, double fm, double fs) {
            this.mm=mm; this.ms=ms; this.fm=fm; this.fs=fs;
        }
    }

    private SexNorm burstoneNorm(String name) {
        if (name == null) return null;
        switch (name) {
            case "Burstone COGS · Ar-Ptm // HP": return new SexNorm(37.1,2.8,32.8,1.9);
            case "Burstone COGS · Ptm-N // HP": return new SexNorm(52.8,4.1,50.9,3.0);
            case "Burstone COGS · convexidad N-A-Pg": return new SexNorm(3.9,6.4,2.6,5.1);
            case "Burstone COGS · N-A // HP": return new SexNorm(0.0,3.7,-2.0,3.7);
            case "Burstone COGS · N-B // HP": return new SexNorm(-5.3,6.7,-6.9,4.3);
            case "Burstone COGS · N-Pg // HP": return new SexNorm(-4.3,8.5,-6.5,5.1);
            case "Burstone COGS · N-ENA ⟂ HP": return new SexNorm(54.7,3.2,50.0,2.4);
            case "Burstone COGS · ENA-Gn ⟂ HP": return new SexNorm(68.6,3.8,61.3,3.3);
            case "Burstone COGS · ENP-N ⟂ HP": return new SexNorm(53.9,1.7,50.6,2.2);
            case "Burstone COGS · MP-HP": return new SexNorm(23.0,5.9,24.2,5.0);
            case "Burstone COGS · U1-NF · altura": return new SexNorm(30.5,2.1,27.5,1.7);
            case "Burstone COGS · U6-NF · altura": return new SexNorm(26.2,2.0,23.0,1.3);
            case "Burstone COGS · L1-MP · altura": return new SexNorm(45.0,2.1,40.8,1.8);
            case "Burstone COGS · L6-MP · altura": return new SexNorm(35.8,2.6,32.1,1.9);
            case "Burstone COGS · ENP-ENA // HP": return new SexNorm(53.9,3.8,50.0,2.4);
            case "Burstone COGS · Ar-Go": return new SexNorm(52.0,4.2,46.8,2.5);
            case "Burstone COGS · Go-Pg": return new SexNorm(83.7,4.6,74.3,5.8);
            case "Burstone COGS · B-Pg // MP": return new SexNorm(8.9,1.7,7.2,1.9);
            case "Burstone COGS · ángulo goníaco Ar-Go-Gn": return new SexNorm(119.1,6.5,122.0,6.9);
            case "Burstone COGS · OP-HP": return new SexNorm(6.2,5.1,7.1,2.5);
            case "Burstone COGS · A-B / OP": return new SexNorm(-1.1,2.0,-0.4,2.5);
            case "Burstone COGS · U1-NF": return new SexNorm(111.0,4.7,112.5,5.3);
            case "Burstone COGS · L1-MP": return new SexNorm(95.9,5.2,95.9,5.7);
            default: return null;
        }
    }

    private String burstoneReferenceText(String name, boolean degrees) {
        SexNorm r = burstoneNorm(name);
        if (r == null) return null;
        String u = degrees ? "°" : " mm";
        if ("Masculino".equals(patientSex))
            return String.format(Locale.US, "Burstone COGS 1978 · varones caucásicos adultos %.1f ± %.1f%s", r.mm,r.ms,u);
        if ("Femenino".equals(patientSex))
            return String.format(Locale.US, "Burstone COGS 1978 · mujeres caucásicas adultas %.1f ± %.1f%s", r.fm,r.fs,u);
        return String.format(Locale.US,
                "Burstone COGS 1978 · varones %.1f±%.1f%s · mujeres %.1f±%.1f%s; seleccione sexo para comparar ±1 DE",
                r.mm,r.ms,u,r.fm,r.fs,u);
    }

    private String burstoneDiagnosis(String name, double value) {
        SexNorm r = burstoneNorm(name);
        if (r == null) return null;
        double mean, sd; String group;
        if ("Masculino".equals(patientSex)) { mean=r.mm; sd=r.ms; group="varones"; }
        else if ("Femenino".equals(patientSex)) { mean=r.fm; sd=r.fs; group="mujeres"; }
        else return "Resultado calculado; no se clasifica porque la tabla COGS original es específica por sexo.";
        double min=mean-sd, max=mean+sd;
        String pos=value<min?"por debajo":value>max?"por encima":"dentro";
        return "El valor está "+pos+" de ±1 DE de la muestra original de "+group+
                " caucásicos adultos. Es una referencia histórica, no un diagnóstico.";
    }

    private String angularNormText(MeasurementDefinition def, double value) {
        String x=burstoneReferenceText(def.name,true);
        return x!=null?x:def.normText;
    }

    private String angularDiagnosis(MeasurementDefinition def, double value) {
        String x=burstoneDiagnosis(def.name,value);
        return x!=null?x:def.diagnosis(value);
    }

'''
    if anchor not in a:
        raise RuntimeError("resultsSafetyNotice anchor missing")
    a = a.replace(anchor, norms + anchor, 1)

old = '''                    "   ·   Referencia: " +
                    def.normText +
                    "\\n" +
                    def.diagnosis(value)
'''
new = '''                    "   ·   Referencia: " +
                    angularNormText(def, value) +
                    "\\n" +
                    angularDiagnosis(def, value)
'''
if old in a:
    a = a.replace(old, new, 1)

norm_anchor = '''    private String linearNormText(
            LinearMeasurementDefinition def,
            double value
    ) {
'''
if "burstoneReferenceText(def.name, false)" not in a:
    if norm_anchor not in a:
        raise RuntimeError("linearNormText missing")
    a = a.replace(norm_anchor, norm_anchor + '''        String burstone = burstoneReferenceText(def.name, false);
        if (burstone != null) return burstone;
''', 1)

diag_anchor = '''    private String linearDiagnosis(
            LinearMeasurementDefinition def,
            double value
    ) {
'''
if "burstoneDiagnosis(def.name, value)" not in a:
    if diag_anchor not in a:
        raise RuntimeError("linearDiagnosis missing")
    a = a.replace(diag_anchor, diag_anchor + '''        String burstone = burstoneDiagnosis(def.name, value);
        if (burstone != null) return burstone;
''', 1)

activity.write_text(a, encoding="utf-8")

# --- Point guides -------------------------------------------------------------
guide = JAVA / "PointGuide.java"
p = guide.read_text(encoding="utf-8")
if 'GUIDE.put("Ptm",' not in p:
    anchor = '        GUIDE.put("Oclusal 2",'
    idx = p.find(anchor)
    if idx < 0:
        raise RuntimeError("PointGuide anchor missing")
    end = p.find("\n", idx)
    additions = r'''
        GUIDE.put("Ptm", "Pterygomaxillare (Ptm): punto más posterosuperior de la fisura pterigomaxilar; COGS lo utiliza para Ar-Ptm y Ptm-N.");
        GUIDE.put("U6 cusp", "Cúspide mesiovestibular del primer molar superior permanente seleccionado para el trazado.");
        GUIDE.put("L6 cusp", "Cúspide mesiovestibular del primer molar inferior permanente seleccionado para el trazado.");
        GUIDE.put("Sn", "Subnasale (Sn): máxima concavidad donde la columela se une con el labio superior.");
        GUIDE.put("Cm", "Columella (Cm): punto de la columela usado con Sn y Ls para el ángulo nasolabial.");
        GUIDE.put("Gn'", "Gnathion de tejidos blandos (Gn'): punto anteroinferior del contorno del mentón blando.");
        GUIDE.put("Si", "Sulcus inferius/mentolabial (Si): máxima concavidad entre labio inferior y pogonion blando.");
        GUIDE.put("Stms", "Stomion superius (Stms): punto más inferior del labio superior en la hendidura oral.");
        GUIDE.put("Stmi", "Stomion inferius (Stmi): punto más superior del labio inferior en la hendidura oral.");
'''
    p = p[:end+1] + additions + p[end+1:]
guide.write_text(p, encoding="utf-8")

(TEST / "SurgicalCephalometricAuditTest.java").write_text(r'''package com.cefalo.angulos;
import static org.junit.Assert.*;
import org.junit.Test;
public class SurgicalCephalometricAuditTest {
    private static boolean a(String s){for(MeasurementDefinition d:MeasurementCatalog.steiner())if(d.name.contains(s))return true;return false;}
    private static boolean l(String s){for(LinearMeasurementDefinition d:LinearMeasurementCatalog.cephalometric())if(d.name.contains(s))return true;return false;}
    @Test public void sourceAnalysesPresent(){
        assertTrue(a("Burstone COGS · convexidad"));
        assertTrue(a("Legan-Burstone · convexidad facial"));
        assertTrue(l("Burstone COGS · Ar-Ptm"));
        assertTrue(l("Burstone COGS · U6-NF"));
        assertTrue(l("Legan-Burstone · espacio interlabial"));
    }
    @Test public void geometryTypesPresent(){
        assertNotNull(MeasurementDefinition.Type.valueOf("HP_ANGLE"));
        assertNotNull(MeasurementDefinition.Type.valueOf("SIGNED_CHAIN_ANGLE"));
        assertNotNull(LinearMeasurementDefinition.Type.valueOf("HP_PROJECTION_ABS"));
        assertNotNull(LinearMeasurementDefinition.Type.valueOf("HP_PERP_RATIO"));
    }
}
''', encoding="utf-8")

checks = {
    "version": "versionName '1.34'" in gradle.read_text(encoding="utf-8"),
    "COGS": "Burstone COGS · Ar-Ptm // HP" in linear_catalog.read_text(encoding="utf-8"),
    "Legan": "Legan-Burstone · espacio interlabial" in linear_catalog.read_text(encoding="utf-8"),
    "Ptm": 'GUIDE.put("Ptm",' in guide.read_text(encoding="utf-8"),
}
missing=[k for k,v in checks.items() if not v]
if missing: raise RuntimeError("Surgical ceph audit incomplete: "+", ".join(missing))
print("Burstone COGS and Legan-Burstone soft-tissue analysis integrated from original-source definitions.")
