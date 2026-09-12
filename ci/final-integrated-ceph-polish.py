from pathlib import Path
import re

ROOT=Path(".")
JAVA=ROOT/"app/src/main/java/com/cefalo/angulos"

gradle=ROOT/"app/build.gradle"
g=gradle.read_text(encoding="utf-8")
g=re.sub(r"versionCode\s+\d+","versionCode 37",g,count=1)
g=re.sub(r"versionName\s+'[^']+'","versionName '1.36'",g,count=1)
gradle.write_text(g,encoding="utf-8")

activity=JAVA/"AnalysisActivity.java"
a=activity.read_text(encoding="utf-8")

# PNS-ANS is geometrically valid COGS, but do not attach a sex-specific
# mean/SD unless the exact historical table row is independently verified.
a=a.replace(
'            case "Burstone COGS · ENP-ENA // HP": return new SexNorm(53.9,3.8,50.0,2.4);\n',
''
)

# Report/PDF must use the same sex-aware COGS references as the on-screen dialog.
report_old='''                            value,
                            def.normText
                    );

            canvas.drawText(valueLine, left + 30, top + 94, valuePaint);

            drawWrappedText(
                    canvas,
                    def.diagnosis(value),
'''
report_new='''                            value,
                            angularNormText(def, value)
                    );

            canvas.drawText(valueLine, left + 30, top + 94, valuePaint);

            drawWrappedText(
                    canvas,
                    angularDiagnosis(def, value),
'''
if report_old in a:
    a=a.replace(report_old,report_new,1)
elif "angularNormText(def, value)" not in a:
    raise RuntimeError("Could not make exported angular references sex-aware")

# Reserve report space for the Sassouni architectural block when enough
# landmarks have been placed.
height_old='''                ((definitions.size() + linearCount) * rowHeight) +
                (linearCount > 0 ? 60 : 0) +
                footerHeight;'''
height_new='''                ((definitions.size() + linearCount) * rowHeight) +
                (linearCount > 0 ? 60 : 0) +
                (sassouniSummaryText() != null ? 430 : 0) +
                footerHeight;'''
if height_old in a:
    a=a.replace(height_old,height_new,1)

# Add Sassouni to image/PDF report after calculated rows.
footer_anchor='''        Paint footerPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
'''
if "String sassouniReport = sassouniSummaryText();" not in a:
    block=r'''        String sassouniReport = sassouniSummaryText();
        if (sassouniReport != null) {
            y += 30;
            float left = margin;
            float top = y;
            float right = width - margin;
            float bottom = y + 380;
            RectF rect = new RectF(left, top, right, bottom);
            canvas.drawRoundRect(rect, 30f, 30f, cardPaint);
            canvas.drawRoundRect(rect, 30f, 30f, strokePaint);
            canvas.drawText("Sassouni · arquitectura original", left + 30, top + 48, namePaint);
            drawWrappedText(
                    canvas,
                    sassouniReport.replace("Sassouni 1955 · arquitectura original\n", ""),
                    left + 30,
                    top + 94,
                    right - 30,
                    detailPaint,
                    32f
            );
            y += 400;
        }

'''
    if footer_anchor not in a:
        raise RuntimeError("Report footer anchor missing")
    a=a.replace(footer_anchor,block+footer_anchor,1)

activity.write_text(a,encoding="utf-8")

checks={
 "version":"versionName '1.36'" in gradle.read_text(encoding="utf-8"),
 "no guessed PNS-ANS norm":'case "Burstone COGS · ENP-ENA // HP"' not in activity.read_text(encoding="utf-8"),
 "report refs":"angularNormText(def, value)" in activity.read_text(encoding="utf-8"),
 "report Sassouni":"String sassouniReport = sassouniSummaryText();" in activity.read_text(encoding="utf-8"),
}
missing=[k for k,v in checks.items() if not v]
if missing:raise RuntimeError("Final ceph polish incomplete: "+", ".join(missing))
print("Final integrated cephalometric report polish applied; build 1.36.")
