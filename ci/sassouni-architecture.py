from pathlib import Path
import re

ROOT = Path(".")
JAVA = ROOT / "app/src/main/java/com/cefalo/angulos"
TEST = ROOT / "app/src/test/java/com/cefalo/angulos"
TEST.mkdir(parents=True, exist_ok=True)

# Sassouni 1955 architectural analysis, implemented from the original plane,
# convergence, arc and dental-relation definitions. No later textbook cutoff is
# relabeled as an original Sassouni norm.

gradle = ROOT / "app/build.gradle"
g = gradle.read_text(encoding="utf-8")
g = re.sub(r"versionCode\s+\d+", "versionCode 36", g, count=1)
g = re.sub(r"versionName\s+'[^']+'", "versionName '1.35'", g, count=1)
gradle.write_text(g, encoding="utf-8")

# Pure-Java geometry so local JVM tests can verify the architecture.
geom = JAVA / "SassouniGeometry.java"
geom.write_text(r'''package com.cefalo.angulos;

import java.util.Map;

public final class SassouniGeometry {
    private SassouniGeometry() {}

    public static final class Result {
        public double centerX, centerY, convergenceRms;
        public double[] omittedResiduals;
        public int dominantPlane = -1;
        public String subtype;
        public double basalPalatal, palatalMandibular, angularEqualityError;
        public double radiusAnterior, radiusPosterior;
        public double feArcResidual = Double.NaN;
        public double nasionArcResidual = Double.NaN;
        public double u1ArcResidual = Double.NaN;
        public double pgArcResidual = Double.NaN;
        public double goPosteriorArcResidual = Double.NaN;
        public double upperMolarIncisorError = Double.NaN;
        public double lowerMolarIncisorError = Double.NaN;
        public double ramalIncisorError = Double.NaN;
    }

    private static final class Line {
        final double a,b,c;
        Line(double[] p, double dx, double dy) {
            double m=Math.hypot(dx,dy);
            if(m==0.0) throw new IllegalArgumentException("zero line");
            a=-dy/m; b=dx/m; c=-(a*p[0]+b*p[1]);
        }
        double distance(double[] p){return Math.abs(a*p[0]+b*p[1]+c);}
        double[] project(double[] p){
            double d=a*p[0]+b*p[1]+c;
            return new double[]{p[0]-a*d,p[1]-b*d};
        }
    }

    public static Result calculate(Map<String,double[]> p) {
        double[] si=p.get("Sella inf."), acbp=p.get("ACB post."), acba=p.get("ACB ant.");
        double[] enp=p.get("ENP"), ena=p.get("ENA");
        double[] op=p.get("Sass Oc post."), oa=p.get("Sass Oc ant.");
        double[] mp=p.get("Mand base post."), ma=p.get("Mand base ant.");
        if(si==null||acbp==null||acba==null||enp==null||ena==null||op==null||oa==null||mp==null||ma==null)
            return null;
        try {
            Line basal=new Line(si,acba[0]-acbp[0],acba[1]-acbp[1]);
            Line palatal=new Line(enp,ena[0]-enp[0],ena[1]-enp[1]);
            Line occlusal=new Line(op,oa[0]-op[0],oa[1]-op[1]);
            Line mandibular=new Line(mp,ma[0]-mp[0],ma[1]-mp[1]);
            Line[] lines={basal,palatal,occlusal,mandibular};
            double[] center=leastSquares(lines,-1);
            if(center==null)return null;

            Result r=new Result();
            r.centerX=center[0]; r.centerY=center[1];
            double sum=0;
            for(Line l:lines){double d=l.distance(center);sum+=d*d;}
            r.convergenceRms=Math.sqrt(sum/4.0);

            r.omittedResiduals=new double[4];
            double max=-1,second=-1; int dominant=-1;
            for(int i=0;i<4;i++){
                double[] oc=leastSquares(lines,i);
                double residual=oc==null?Double.NaN:lines[i].distance(oc);
                r.omittedResiduals[i]=residual;
                if(!Double.isNaN(residual)){
                    if(residual>max){second=max;max=residual;dominant=i;}
                    else if(residual>second)second=residual;
                }
            }
            // Relative dominance only: this is an engineering aid, not an
            // invented Sassouni millimetric diagnostic threshold.
            if(dominant>=0 && max>0 && max>=2.0*Math.max(second,1e-9))r.dominantPlane=dominant;

            if(r.dominantPlane>=0){
                double[] proj=lines[r.dominantPlane].project(center);
                double[] n=p.get("N"), me=p.get("Me");
                if(n!=null&&me!=null){
                    double ix=me[0]-n[0],iy=me[1]-n[1],im=Math.hypot(ix,iy);
                    if(im>0){
                        double dot=(proj[0]-center[0])*(ix/im)+(proj[1]-center[1])*(iy/im);
                        r.subtype=dot<0?"A":"B";
                    }
                }
            }

            r.basalPalatal=acute(acbp,acba,enp,ena);
            r.palatalMandibular=acute(enp,ena,mp,ma);
            r.angularEqualityError=Math.abs(r.basalPalatal-r.palatalMandibular);

            r.radiusAnterior=dist(center,ena);
            double[] fe=p.get("FE"), n=p.get("N"), u1=p.get("IS borde"), pg=p.get("Pg");
            if(fe!=null)r.feArcResidual=dist(center,fe)-r.radiusAnterior;
            if(n!=null)r.nasionArcResidual=dist(center,n)-r.radiusAnterior;
            if(u1!=null)r.u1ArcResidual=dist(center,u1)-r.radiusAnterior;
            if(pg!=null)r.pgArcResidual=dist(center,pg)-r.radiusAnterior;

            double[] sp=p.get("Sp"),go=p.get("Go");
            if(sp!=null){
                r.radiusPosterior=dist(center,sp);
                if(go!=null)r.goPosteriorArcResidual=dist(center,go)-r.radiusPosterior;
            }else r.radiusPosterior=Double.NaN;

            double[] u6c=p.get("U6 cusp"),u6r=p.get("U6 raíz"),u1a=p.get("IS ápice");
            if(u6c!=null&&u6r!=null&&u1!=null&&u1a!=null){
                double M=acute(u6c,u6r,enp,ena);
                double I=acute(u1,u1a,enp,ena);
                r.upperMolarIncisorError=M-(I+10.0);
            }

            double[] l6c=p.get("L6 cusp"),l6r=p.get("L6 raíz"),l1=p.get("II borde"),l1a=p.get("II ápice");
            if(l6c!=null&&l6r!=null&&l1!=null&&l1a!=null){
                double m=acute(l6c,l6r,mp,ma);
                double i=acute(l1,l1a,mp,ma);
                r.lowerMolarIncisorError=m-(i+5.0);
            }

            double[] rs=p.get("Rama post sup."),ri=p.get("Rama post inf.");
            if(rs!=null&&ri!=null&&l1!=null&&l1a!=null){
                double R=acute(rs,ri,op,oa);
                double i=acute(l1,l1a,op,oa);
                r.ramalIncisorError=R-i;
            }
            return r;
        }catch(IllegalArgumentException ex){return null;}
    }

    private static double[] leastSquares(Line[] lines,int omit){
        double aa=0,ab=0,bb=0,ac=0,bc=0;
        for(int i=0;i<lines.length;i++){
            if(i==omit)continue;
            Line l=lines[i];
            aa+=l.a*l.a;ab+=l.a*l.b;bb+=l.b*l.b;ac+=l.a*l.c;bc+=l.b*l.c;
        }
        double det=aa*bb-ab*ab;
        if(Math.abs(det)<1e-9)return null;
        return new double[]{(-ac*bb+ab*bc)/det,(-aa*bc+ab*ac)/det};
    }
    private static double dist(double[] a,double[] b){return Math.hypot(b[0]-a[0],b[1]-a[1]);}
    private static double acute(double[] a,double[] b,double[] c,double[] d){
        double x1=b[0]-a[0],y1=b[1]-a[1],x2=d[0]-c[0],y2=d[1]-c[1];
        double m1=Math.hypot(x1,y1),m2=Math.hypot(x2,y2);
        if(m1==0||m2==0)return 0;
        double cs=(x1*x2+y1*y2)/(m1*m2);
        cs=Math.max(-1,Math.min(1,cs));
        double raw=Math.toDegrees(Math.acos(cs));
        return Math.min(raw,180.0-raw);
    }
}
''',encoding="utf-8")

# New architectural landmarks are not all ordinary measurement inputs; append
# them to the integrated landmark list while preserving partial-result behavior.
activity=JAVA/"AnalysisActivity.java"
a=activity.read_text(encoding="utf-8")
anchor="        return new ArrayList<>(ordered);\n"
if '"Sella inf."' not in a:
    addition=r'''        String[] sassouniArchitecture = {
                "Sella inf.", "ACB post.", "ACB ant.",
                "Sass Oc post.", "Sass Oc ant.",
                "Mand base post.", "Mand base ant.",
                "Sp", "FE", "U6 raíz", "L6 raíz",
                "Rama post sup.", "Rama post inf."
        };
        for (String label : sassouniArchitecture) ordered.add(label);

'''
    if anchor not in a:raise RuntimeError("Landmark list anchor changed upstream")
    a=a.replace(anchor,addition+anchor,1)

# Reusable text generator.
if "private String sassouniSummaryText()" not in a:
    insert="    private void addTweedSummary(LinearLayout container) {\n"
    method=r'''    private String sassouniSummaryText() {
        java.util.Map<String, double[]> map = new java.util.HashMap<>();
        for (String label : landmarks) {
            PointF p = measurementView.getPoint(label);
            if (p != null) map.put(label, new double[]{p.x, p.y});
        }
        SassouniGeometry.Result r = SassouniGeometry.calculate(map);
        if (r == null) return null;

        double scale = (!Double.isNaN(mmPerPixel) && mmPerPixel > 0.0) ? mmPerPixel : 1.0;
        String unit = (!Double.isNaN(mmPerPixel) && mmPerPixel > 0.0) ? " mm" : " px";
        String[] typeNames = {"I · basal", "II · palatino", "III · oclusal", "IV · mandibular"};
        String type = r.dominantPlane >= 0
                ? "candidato tipo " + typeNames[r.dominantPlane] + (r.subtype == null ? "" : r.subtype)
                : "sin un plano único claramente dominante";

        StringBuilder t = new StringBuilder();
        t.append("Sassouni 1955 · arquitectura original\n");
        t.append(String.format(Locale.US,
                "Convergencia 4 planos: RMS %.2f%s · %s\n",
                r.convergenceRms * scale, unit, type));
        t.append(String.format(Locale.US,
                "Basal/palatino %.1f° · palatino/mandibular %.1f° · diferencia %.1f°\n",
                r.basalPalatal, r.palatalMandibular, r.angularEqualityError));

        if (!Double.isNaN(r.feArcResidual) || !Double.isNaN(r.nasionArcResidual)
                || !Double.isNaN(r.u1ArcResidual) || !Double.isNaN(r.pgArcResidual)) {
            t.append("Arco anterior (+ fuera / − dentro): ");
            if(!Double.isNaN(r.feArcResidual))t.append(String.format(Locale.US,"FE %.2f%s · ",r.feArcResidual*scale,unit));
            if(!Double.isNaN(r.nasionArcResidual))t.append(String.format(Locale.US,"N %.2f%s · ",r.nasionArcResidual*scale,unit));
            if(!Double.isNaN(r.u1ArcResidual))t.append(String.format(Locale.US,"U1 %.2f%s · ",r.u1ArcResidual*scale,unit));
            if(!Double.isNaN(r.pgArcResidual))t.append(String.format(Locale.US,"Pg %.2f%s",r.pgArcResidual*scale,unit));
            t.append("\n");
        }
        if(!Double.isNaN(r.goPosteriorArcResidual))
            t.append(String.format(Locale.US,"Arco posterior: Go %.2f%s\n",r.goPosteriorArcResidual*scale,unit));
        if(!Double.isNaN(r.upperMolarIncisorError))
            t.append(String.format(Locale.US,"M'−(I'+10°): %.1f°\n",r.upperMolarIncisorError));
        if(!Double.isNaN(r.lowerMolarIncisorError))
            t.append(String.format(Locale.US,"m'−(i'+5°): %.1f°\n",r.lowerMolarIncisorError));
        if(!Double.isNaN(r.ramalIncisorError))
            t.append(String.format(Locale.US,"R−i: %.1f°\n",r.ramalIncisorError));
        t.append("La selección tipo A/B es una ayuda geométrica relativa; no se inventa un umbral milimétrico de normalidad que Sassouni no publicó.");
        return t.toString();
    }

    private void addSassouniSummary(LinearLayout container) {
        String text = sassouniSummaryText();
        if (text == null) return;
        TextView summary = new TextView(this);
        summary.setText(text);
        summary.setTextSize(13f);
        summary.setTextColor(getColor(R.color.text_primary));
        summary.setGravity(Gravity.CENTER);
        summary.setTextAlignment(View.TEXT_ALIGNMENT_CENTER);
        summary.setIncludeFontPadding(false);
        summary.setLineSpacing(0f,1.06f);
        summary.setBackgroundResource(R.drawable.button_soft_mint_centered);
        summary.setPadding(dp(12),dp(10),dp(12),dp(10));
        LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,ViewGroup.LayoutParams.WRAP_CONTENT);
        lp.setMargins(0,dp(4),0,dp(10));
        summary.setLayoutParams(lp);
        container.addView(summary);
    }

'''
    if insert not in a:raise RuntimeError("Could not place Sassouni summary methods")
    a=a.replace(insert,method+insert,1)

if "addSassouniSummary(container);" not in a:
    insert="        TextView saveAnnotated =\n"
    if insert not in a:raise RuntimeError("Results export anchor missing")
    a=a.replace(insert,"        addSassouniSummary(container);\n\n"+insert,1)

activity.write_text(a,encoding="utf-8")

# Point guides.
guide=JAVA/"PointGuide.java"
p=guide.read_text(encoding="utf-8")
if 'GUIDE.put("Sella inf.",' not in p:
    anchor='        GUIDE.put("Oclusal 2",'
    idx=p.find(anchor)
    if idx<0:raise RuntimeError("PointGuide anchor missing")
    end=p.find("\n",idx)
    additions=r'''
        GUIDE.put("Sella inf.", "Sassouni · punto de tangencia inferior de la silla turca: por aquí pasa el plano basal, paralelo al eje del contorno superior de la base craneal anterior.");
        GUIDE.put("ACB post.", "Sassouni · referencia posterior del eje del contorno SUPERIOR de la base craneal anterior. Junto con ACB ant. define la dirección basal; no equivale automáticamente a S-N.");
        GUIDE.put("ACB ant.", "Sassouni · referencia anterior del eje del contorno SUPERIOR de la base craneal anterior.");
        GUIDE.put("Sass Oc post.", "Sassouni · punto posterior del plano oclusal arquitectónico, en la región de las cúspides mesiales de los primeros molares permanentes según el método original.");
        GUIDE.put("Sass Oc ant.", "Sassouni · punto anterior del plano oclusal arquitectónico, en la referencia incisal central correspondiente.");
        GUIDE.put("Mand base post.", "Sassouni · punto posterior de apoyo de la tangente al borde inferior mandibular.");
        GUIDE.put("Mand base ant.", "Sassouni · punto anterior de apoyo de la tangente al borde inferior mandibular.");
        GUIDE.put("Sp", "Sassouni · punto de la pared posterior de la silla usado para definir el radio del arco posterior desde O.");
        GUIDE.put("FE", "Sassouni · unión frontoetmoidal (FE), referencia del arco facial anterior.");
        GUIDE.put("U6 raíz", "Centro/apice radicular del primer molar superior usado para definir su eje longitudinal en la relación dentaria de Sassouni.");
        GUIDE.put("L6 raíz", "Centro/apice radicular del primer molar inferior usado para definir su eje longitudinal en la relación dentaria de Sassouni.");
        GUIDE.put("Rama post sup.", "Sassouni · punto superior de apoyo para la tangente posterior de la rama mandibular.");
        GUIDE.put("Rama post inf.", "Sassouni · punto inferior de apoyo para la tangente posterior de la rama mandibular.");
'''
    p=p[:end+1]+additions+p[end+1:]
guide.write_text(p,encoding="utf-8")

# Unit tests: exact convergence and missing-data behavior.
(TEST/"SassouniGeometryTest.java").write_text(r'''package com.cefalo.angulos;
import static org.junit.Assert.*;
import java.util.*;
import org.junit.Test;

public class SassouniGeometryTest {
    private static double[] p(double x,double y){return new double[]{x,y};}
    @Test public void exactConvergenceRecoversO(){
        Map<String,double[]> m=new HashMap<>();
        m.put("Sella inf.",p(100,100));m.put("ACB post.",p(0,100));m.put("ACB ant.",p(200,100));
        m.put("ENP",p(50,50));m.put("ENA",p(150,150));
        m.put("Sass Oc post.",p(50,150));m.put("Sass Oc ant.",p(150,50));
        m.put("Mand base post.",p(100,0));m.put("Mand base ant.",p(100,200));
        SassouniGeometry.Result r=SassouniGeometry.calculate(m);
        assertNotNull(r);assertEquals(100.0,r.centerX,0.01);assertEquals(100.0,r.centerY,0.01);
        assertEquals(0.0,r.convergenceRms,0.01);assertEquals(-1,r.dominantPlane);
    }
    @Test public void missingRequiredPlaneReturnsNull(){
        Map<String,double[]> m=new HashMap<>();
        assertNull(SassouniGeometry.calculate(m));
    }
}
''',encoding="utf-8")

checks={
    "version":"versionName '1.35'" in gradle.read_text(encoding="utf-8"),
    "geometry":geom.exists(),
    "landmarks":'"Sella inf."' in activity.read_text(encoding="utf-8"),
    "summary":"addSassouniSummary(container);" in activity.read_text(encoding="utf-8"),
    "guide":'GUIDE.put("Sella inf.",' in guide.read_text(encoding="utf-8"),
}
missing=[k for k,v in checks.items() if not v]
if missing:raise RuntimeError("Sassouni audit incomplete: "+", ".join(missing))
print("Sassouni 1955 architectural convergence, arcs, and dental relational checks integrated.")
