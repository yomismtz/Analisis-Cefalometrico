package com.yomceph.cephalometric;

/** Pure geometry used by the standalone cephalometric module. */
public final class CephalometricMath {

    public static final class Point {
        public final double x;
        public final double y;

        public Point(double x, double y) {
            this.x = x;
            this.y = y;
        }
    }

    private CephalometricMath() {}

    public static double distance(Point a, Point b) {
        return Math.hypot(b.x - a.x, b.y - a.y);
    }

    public static double angleAt(Point a, Point vertex, Point c) {
        double v1x = a.x - vertex.x;
        double v1y = a.y - vertex.y;
        double v2x = c.x - vertex.x;
        double v2y = c.y - vertex.y;
        return angleBetween(v1x, v1y, v2x, v2y);
    }

    public static double angleBetweenLines(Point a, Point b, Point c, Point d) {
        return angleBetween(
                b.x - a.x,
                b.y - a.y,
                d.x - c.x,
                d.y - c.y
        );
    }

    /** Absolute shortest distance from point p to the infinite line a-b. */
    public static double perpendicularDistance(Point a, Point b, Point p) {
        double dx = b.x - a.x;
        double dy = b.y - a.y;
        double length = Math.hypot(dx, dy);
        if (length == 0.0) return Double.NaN;
        return Math.abs(dx * (a.y - p.y) - (a.x - p.x) * dy) / length;
    }

    /**
     * Length from a to the orthogonal projection of p on the axis a-b.
     * Used by SL (S,N,Pg) and SE (S,N,posterior condylar point).
     * The absolute value makes the result independent of screen left/right orientation.
     */
    public static double axialProjectionDistance(Point a, Point b, Point p) {
        double dx = b.x - a.x;
        double dy = b.y - a.y;
        double length = Math.hypot(dx, dy);
        if (length == 0.0) return Double.NaN;

        double ux = dx / length;
        double uy = dy / length;
        double projection = (p.x - a.x) * ux + (p.y - a.y) * uy;
        return Math.abs(projection);
    }

    public static double toMillimetres(double pixels, double mmPerPixel) {
        if (!(mmPerPixel > 0.0)) return Double.NaN;
        return pixels * mmPerPixel;
    }

    private static double angleBetween(double v1x, double v1y, double v2x, double v2y) {
        double m1 = Math.hypot(v1x, v1y);
        double m2 = Math.hypot(v2x, v2y);
        if (m1 == 0.0 || m2 == 0.0) return Double.NaN;

        double cos = (v1x * v2x + v1y * v2y) / (m1 * m2);
        cos = Math.max(-1.0, Math.min(1.0, cos));
        return Math.toDegrees(Math.acos(cos));
    }
}
