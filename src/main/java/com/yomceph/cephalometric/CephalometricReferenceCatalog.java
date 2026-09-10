package com.yomceph.cephalometric;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/**
 * Audited reference catalog for the standalone YomCeph cephalometric module.
 *
 * This class intentionally separates measurement geometry from clinical wording.
 * Values are reference norms, not diagnoses.
 */
public final class CephalometricReferenceCatalog {

    public enum Geometry {
        THREE_POINT_ANGLE,
        TWO_LINE_ANGLE,
        SIGNED_ANB,
        PERPENDICULAR_DISTANCE,
        AXIAL_PROJECTION
    }

    public static final class Measure {
        public final String id;
        public final String name;
        public final Geometry geometry;
        public final List<String> points;
        public final Double mean;
        public final Double tolerance;
        public final String unit;
        public final String referenceText;
        public final String interpretation;

        Measure(
                String id,
                String name,
                Geometry geometry,
                List<String> points,
                Double mean,
                Double tolerance,
                String unit,
                String referenceText,
                String interpretation
        ) {
            this.id = id;
            this.name = name;
            this.geometry = geometry;
            this.points = Collections.unmodifiableList(points);
            this.mean = mean;
            this.tolerance = tolerance;
            this.unit = unit;
            this.referenceText = referenceText;
            this.interpretation = interpretation;
        }
    }

    public static final List<Measure> MEASURES = Collections.unmodifiableList(Arrays.asList(
            m("SNA", "SNA", Geometry.THREE_POINT_ANGLE, p("S", "N", "A"), 82.0, 2.0, "°",
                    "82° ± 2°",
                    "Posición sagital del maxilar respecto a la base craneal SN; corroborar con otras medidas."),

            m("SNB", "SNB", Geometry.THREE_POINT_ANGLE, p("S", "N", "B"), 80.0, 2.0, "°",
                    "80° ± 2°",
                    "Posición sagital mandibular respecto a la base craneal SN; corroborar con otras medidas."),

            m("ANB", "ANB", Geometry.SIGNED_ANB, p("S", "N", "A", "B"), 2.0, 2.0, "°",
                    "2° ± 2°",
                    "Relación sagital maxilomandibular. Un valor aislado no constituye diagnóstico esqueletal definitivo."),

            m("SND", "SND", Geometry.THREE_POINT_ANGLE, p("S", "N", "D"), 76.0, 2.0, "°",
                    "76° ± 2°",
                    "Posición de la región sinfisaria/mentón respecto a la base craneal."),

            m("SN_GOGN", "SN / Go-Gn", Geometry.TWO_LINE_ANGLE, p("S", "N", "Go", "Gn"), 32.0, 4.0, "°",
                    "32° ± 4°",
                    "Divergencia del plano mandibular respecto a SN."),

            m("Y_AXIS", "Eje Y · NS / S-Gn", Geometry.TWO_LINE_ANGLE, p("N", "S", "S", "Gn"), 65.0, 3.0, "°",
                    "65° ± 3°",
                    "Dirección de crecimiento facial respecto a la base craneal; interpretar junto con otras variables verticales."),

            m("OP_SN", "Plano oclusal / SN", Geometry.TWO_LINE_ANGLE, p("Oclusal 1", "Oclusal 2", "S", "N"), 14.0, 3.0, "°",
                    "14° ± 3°",
                    "Inclinación del plano oclusal respecto a SN."),

            m("U1_SN", "Incisivo superior / SN", Geometry.TWO_LINE_ANGLE, p("IS borde", "IS ápice", "S", "N"), 103.0, 4.0, "°",
                    "103° ± 4°",
                    "Inclinación del incisivo superior respecto a SN."),

            m("U1_NA_ANG", "Incisivo superior / NA", Geometry.TWO_LINE_ANGLE, p("IS borde", "IS ápice", "N", "A"), 22.0, 6.0, "°",
                    "22° ± 6°",
                    "Inclinación del incisivo superior respecto a NA."),

            m("L1_NB_ANG", "Incisivo inferior / NB", Geometry.TWO_LINE_ANGLE, p("II borde", "II ápice", "N", "B"), 25.0, 4.0, "°",
                    "25° ± 4°",
                    "Inclinación del incisivo inferior respecto a NB."),

            m("INTERINCISAL", "Ángulo interincisal", Geometry.TWO_LINE_ANGLE, p("IS borde", "IS ápice", "II borde", "II ápice"), 131.0, 4.0, "°",
                    "131° ± 4°",
                    "Relación angular entre los ejes de los incisivos superior e inferior."),

            m("GONIAL", "Ángulo goníaco Ar-Go-Me · complementario", Geometry.THREE_POINT_ANGLE, p("Ar", "Go", "Me"), 130.0, 7.0, "°",
                    "130° ± 7° (123°–137°) · referencia complementaria Björk-Jarabak",
                    "Describe la morfología angular mandibular; no pertenece al bloque clásico de Steiner y debe interpretarse como medida complementaria."),

            m("SL", "Segmento SL", Geometry.AXIAL_PROJECTION, p("S", "N", "Pg"), 51.0, 4.0, "mm",
                    "51 ± 4 mm",
                    "Proyección anteroposterior del pogonion sobre el eje SN medida desde S."),

            m("SE", "Segmento SE", Geometry.AXIAL_PROJECTION, p("S", "N", "Cóndilo posterior"), 22.0, 3.0, "mm",
                    "22 ± 3 mm",
                    "Proyección anteroposterior del punto más posterior del cóndilo sobre el eje SN medida desde S."),

            m("U1_NA_MM", "Incisivo superior a NA", Geometry.PERPENDICULAR_DISTANCE, p("N", "A", "IS borde"), 4.0, null, "mm",
                    "4 mm · valor clásico",
                    "Distancia perpendicular del borde incisal superior a NA. No aplicar una tolerancia automática sin una referencia explícita."),

            m("L1_NB_MM", "Incisivo inferior a NB", Geometry.PERPENDICULAR_DISTANCE, p("N", "B", "II borde"), 4.0, null, "mm",
                    "4 mm · valor clásico",
                    "Distancia perpendicular del borde incisal inferior a NB. No aplicar una tolerancia automática sin una referencia explícita.")
    ));

    private CephalometricReferenceCatalog() {}

    private static Measure m(
            String id,
            String name,
            Geometry geometry,
            List<String> points,
            Double mean,
            Double tolerance,
            String unit,
            String referenceText,
            String interpretation
    ) {
        return new Measure(id, name, geometry, points, mean, tolerance, unit, referenceText, interpretation);
    }

    private static List<String> p(String... points) {
        return Arrays.asList(points);
    }
}
