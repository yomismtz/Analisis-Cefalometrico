package com.yomceph.cephalometric;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Calculates only measurements whose required landmarks are available.
 * This is intentionally independent from Android so geometry can be unit-tested.
 */
public final class CephalometricEngine {

    public enum Position { BELOW_REFERENCE, WITHIN_REFERENCE, ABOVE_REFERENCE, DESCRIPTIVE }

    public static final class Result {
        public final CephalometricReferenceCatalog.Measure measure;
        public final double value;
        public final Position position;

        Result(CephalometricReferenceCatalog.Measure measure, double value, Position position) {
            this.measure = measure;
            this.value = value;
            this.position = position;
        }
    }

    private CephalometricEngine() {}

    public static List<Result> calculateAvailable(
            Map<String, CephalometricMath.Point> landmarks,
            double mmPerPixel
    ) {
        if (landmarks == null || landmarks.isEmpty()) return Collections.emptyList();

        List<Result> results = new ArrayList<>();
        for (CephalometricReferenceCatalog.Measure measure : CephalometricReferenceCatalog.MEASURES) {
            Double value = calculate(measure, landmarks, mmPerPixel);
            if (value == null || Double.isNaN(value) || Double.isInfinite(value)) continue;
            results.add(new Result(measure, value, classify(measure, value)));
        }
        return results;
    }

    public static Map<String, Result> calculateAvailableById(
            Map<String, CephalometricMath.Point> landmarks,
            double mmPerPixel
    ) {
        Map<String, Result> out = new LinkedHashMap<>();
        for (Result result : calculateAvailable(landmarks, mmPerPixel)) {
            out.put(result.measure.id, result);
        }
        return out;
    }

    private static Double calculate(
            CephalometricReferenceCatalog.Measure measure,
            Map<String, CephalometricMath.Point> points,
            double mmPerPixel
    ) {
        if (!containsRequiredPoints(measure, points)) return null;

        switch (measure.geometry) {
            case THREE_POINT_ANGLE:
                return CephalometricMath.angleAt(
                        points.get(measure.points.get(0)),
                        points.get(measure.points.get(1)),
                        points.get(measure.points.get(2))
                );

            case TWO_LINE_ANGLE:
                double raw = CephalometricMath.angleBetweenLines(
                        points.get(measure.points.get(0)),
                        points.get(measure.points.get(1)),
                        points.get(measure.points.get(2)),
                        points.get(measure.points.get(3))
                );
                return chooseConventionClosestToReference(raw, measure.mean);

            case SIGNED_ANB:
                double sna = CephalometricMath.angleAt(
                        points.get("S"), points.get("N"), points.get("A")
                );
                double snb = CephalometricMath.angleAt(
                        points.get("S"), points.get("N"), points.get("B")
                );
                return sna - snb;

            case PERPENDICULAR_DISTANCE:
                if (!(mmPerPixel > 0.0)) return null;
                return CephalometricMath.toMillimetres(
                        CephalometricMath.perpendicularDistance(
                                points.get(measure.points.get(0)),
                                points.get(measure.points.get(1)),
                                points.get(measure.points.get(2))
                        ),
                        mmPerPixel
                );

            case AXIAL_PROJECTION:
                if (!(mmPerPixel > 0.0)) return null;
                return CephalometricMath.toMillimetres(
                        CephalometricMath.axialProjectionDistance(
                                points.get(measure.points.get(0)),
                                points.get(measure.points.get(1)),
                                points.get(measure.points.get(2))
                        ),
                        mmPerPixel
                );

            default:
                return null;
        }
    }

    private static boolean containsRequiredPoints(
            CephalometricReferenceCatalog.Measure measure,
            Map<String, CephalometricMath.Point> points
    ) {
        for (String label : measure.points) {
            if (points.get(label) == null) return false;
        }
        return true;
    }

    private static double chooseConventionClosestToReference(double raw, Double mean) {
        if (mean == null || Double.isNaN(raw)) return raw;
        double supplement = 180.0 - raw;
        return Math.abs(supplement - mean) < Math.abs(raw - mean) ? supplement : raw;
    }

    private static Position classify(CephalometricReferenceCatalog.Measure measure, double value) {
        if (measure.mean == null || measure.tolerance == null) return Position.DESCRIPTIVE;
        double min = measure.mean - measure.tolerance;
        double max = measure.mean + measure.tolerance;
        if (value < min) return Position.BELOW_REFERENCE;
        if (value > max) return Position.ABOVE_REFERENCE;
        return Position.WITHIN_REFERENCE;
    }
}
