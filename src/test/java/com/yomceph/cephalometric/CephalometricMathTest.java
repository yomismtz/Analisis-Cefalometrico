package com.yomceph.cephalometric;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import org.junit.Test;

public class CephalometricMathTest {

    @Test
    public void axialProjection_usesProjectionOnSN() {
        CephalometricMath.Point s = new CephalometricMath.Point(0, 0);
        CephalometricMath.Point n = new CephalometricMath.Point(10, 0);
        CephalometricMath.Point pg = new CephalometricMath.Point(5, 7);

        assertEquals(5.0, CephalometricMath.axialProjectionDistance(s, n, pg), 0.0001);
    }

    @Test
    public void axialProjection_isIndependentOfScreenDirection() {
        CephalometricMath.Point s = new CephalometricMath.Point(10, 0);
        CephalometricMath.Point n = new CephalometricMath.Point(0, 0);
        CephalometricMath.Point pg = new CephalometricMath.Point(5, 7);

        assertEquals(5.0, CephalometricMath.axialProjectionDistance(s, n, pg), 0.0001);
    }

    @Test
    public void perpendicularDistance_isShortestDistanceToLine() {
        CephalometricMath.Point n = new CephalometricMath.Point(0, 0);
        CephalometricMath.Point a = new CephalometricMath.Point(10, 0);
        CephalometricMath.Point incisor = new CephalometricMath.Point(4, 3);

        assertEquals(3.0, CephalometricMath.perpendicularDistance(n, a, incisor), 0.0001);
    }

    @Test
    public void angleAt_returnsRightAngle() {
        CephalometricMath.Point a = new CephalometricMath.Point(1, 0);
        CephalometricMath.Point vertex = new CephalometricMath.Point(0, 0);
        CephalometricMath.Point c = new CephalometricMath.Point(0, 1);

        assertEquals(90.0, CephalometricMath.angleAt(a, vertex, c), 0.0001);
    }

    @Test
    public void zeroLengthAxis_returnsNan() {
        CephalometricMath.Point p = new CephalometricMath.Point(1, 1);
        assertTrue(Double.isNaN(CephalometricMath.axialProjectionDistance(p, p, p)));
    }
}
