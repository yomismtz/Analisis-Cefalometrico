package com.yomceph.cephalometric;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import java.util.HashMap;
import java.util.Map;

import org.junit.Test;

public class CephalometricEngineTest {

    @Test
    public void partialLandmarks_returnOnlyComputableMeasurements() {
        Map<String, CephalometricMath.Point> p = new HashMap<>();
        p.put("S", new CephalometricMath.Point(-1, 0));
        p.put("N", new CephalometricMath.Point(0, 0));
        p.put("A", polarFromN(82));

        Map<String, CephalometricEngine.Result> results =
                CephalometricEngine.calculateAvailableById(p, Double.NaN);

        assertTrue(results.containsKey("SNA"));
        assertFalse(results.containsKey("SNB"));
        assertFalse(results.containsKey("SL"));
        assertEquals(82.0, results.get("SNA").value, 0.0001);
    }

    @Test
    public void linearMeasurements_requireCalibration() {
        Map<String, CephalometricMath.Point> p = new HashMap<>();
        p.put("S", new CephalometricMath.Point(0, 0));
        p.put("N", new CephalometricMath.Point(100, 0));
        p.put("Pg", new CephalometricMath.Point(51, 20));

        Map<String, CephalometricEngine.Result> uncalibrated =
                CephalometricEngine.calculateAvailableById(p, Double.NaN);
        assertFalse(uncalibrated.containsKey("SL"));

        Map<String, CephalometricEngine.Result> calibrated =
                CephalometricEngine.calculateAvailableById(p, 1.0);
        assertTrue(calibrated.containsKey("SL"));
        assertEquals(51.0, calibrated.get("SL").value, 0.0001);
        assertEquals(
                CephalometricEngine.Position.WITHIN_REFERENCE,
                calibrated.get("SL").position
        );
    }

    @Test
    public void twoLineAngle_choosesPublishedConventionClosestToReference() {
        Map<String, CephalometricMath.Point> p = new HashMap<>();
        p.put("IS borde", new CephalometricMath.Point(0, 0));
        p.put("IS ápice", new CephalometricMath.Point(1, 0));
        p.put("II borde", new CephalometricMath.Point(0, 0));

        double radians = Math.toRadians(49.0);
        p.put("II ápice", new CephalometricMath.Point(Math.cos(radians), Math.sin(radians)));

        Map<String, CephalometricEngine.Result> results =
                CephalometricEngine.calculateAvailableById(p, Double.NaN);

        assertTrue(results.containsKey("INTERINCISAL"));
        assertEquals(131.0, results.get("INTERINCISAL").value, 0.0001);
    }

    private static CephalometricMath.Point polarFromN(double angleDeg) {
        // Vector N->S points to 180°. To form an 82° SNA angle, N->A is at 98°.
        double radians = Math.toRadians(180.0 - angleDeg);
        return new CephalometricMath.Point(Math.cos(radians), Math.sin(radians));
    }
}
