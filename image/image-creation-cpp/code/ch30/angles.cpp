#include <cmath>
#include <iostream>
#include <vector>
#include "angles.h"
#include "hsv.h"

int main() {
    const double table[7] = {0.0, 30.0, 45.0, 60.0, 90.0, 180.0, 360.0};
    std::cout << "degrees, radians, cos, sin:\n";
    for (double d : table) {
        double r = degreesToRadians(d);
        std::cout << "  " << d << ", " << r << ", " << std::cos(r) << ", " << std::sin(r) << "\n";
    }
    double t = degreesToRadians(37.0);
    std::cout << "cos^2 + sin^2 at 37 degrees = "
              << std::cos(t) * std::cos(t) + std::sin(t) * std::sin(t) << "\n";

    std::cout << "the five star corners of Chapter 25:\n";
    for (int k = 0; k < 5; ++k) {
        Vec2 v = fromAngle(degreesToRadians(-90.0 + 72.0 * k));
        std::cout << "  " << k << ": (" << v.x << ", " << v.y << ")\n";
    }

    std::cout << "angleOf in degrees: (1, 1) " << radiansToDegrees(angleOf(Vec2{1.0, 1.0}))
              << ", (0, 1) " << radiansToDegrees(angleOf(Vec2{0.0, 1.0})) << ", (-1, 0) "
              << radiansToDegrees(angleOf(Vec2{-1.0, 0.0})) << ", (0, -1) "
              << radiansToDegrees(angleOf(Vec2{0.0, -1.0})) << "\n";
    std::cout << "angleBetween in degrees: (1, 0) and (1, 1) "
              << radiansToDegrees(angleBetween(Vec2{1.0, 0.0}, Vec2{1.0, 1.0}))
              << ", (3, 4) and (-4, 3) "
              << radiansToDegrees(angleBetween(Vec2{3.0, 4.0}, Vec2{-4.0, 3.0})) << "\n";

    Image clock(300, 300, Colour{225, 228, 235});
    PointF c{150.0, 150.0};
    Colour dark{40, 40, 55};
    fillCircleAA(clock, c.x, c.y, 130.0, colours::white);
    drawCircleWu(clock, c.x, c.y, 130.0, dark);
    for (int i = 0; i < 60; ++i) {
        double angle = degreesToRadians(i * 6.0 - 90.0);
        if (i % 5 == 0) {
            fillCapsuleAA(clock, pointOnCircle(c, 104.0, angle), pointOnCircle(c, 120.0, angle),
                          3.0, dark);
        } else {
            PointF dotCentre = pointOnCircle(c, 118.0, angle);
            fillCircleAA(clock, dotCentre.x, dotCentre.y, 1.5, Colour{140, 140, 150});
        }
    }
    double minutes = 10.0;
    double hours = 10.0 + minutes / 60.0;
    double hourAngle = degreesToRadians(hours * 30.0 - 90.0);
    double minuteAngle = degreesToRadians(minutes * 6.0 - 90.0);
    fillCapsuleAA(clock, c, pointOnCircle(c, 65.0, hourAngle), 5.0, dark);
    fillCapsuleAA(clock, c, pointOnCircle(c, 100.0, minuteAngle), 3.5, dark);
    fillCircleAA(clock, c.x, c.y, 6.0, Colour{200, 40, 40});

    Image shapes(600, 220, colours::white);
    for (int sides = 3; sides <= 8; ++sides) {
        double x = 50.0 + (sides - 3) * 100.0;
        Colour col = toColour(hsvToRgb(HSV{(sides - 3) * 60.0, 0.7, 0.9}));
        double up = degreesToRadians(-90.0);
        fillPolygonAA(shapes, regularPolygon(PointF{x, 60.0}, 40.0, sides, up), col);
        fillPolygonAA(shapes, starPoints(PointF{x, 165.0}, 45.0, 20.0, sides, up), col);
    }

    Image waves(400, 200, colours::white);
    drawLine(waves, 0, 100, 399, 100, Colour{190, 190, 190});
    std::vector<PointF> sine;
    std::vector<PointF> cosine;
    for (int x = 0; x <= 400; x += 2) {
        double angle = 2.0 * kPi * x / 200.0;
        sine.push_back(PointF{x + 0.5, 100.0 - 60.0 * std::sin(angle)});
        cosine.push_back(PointF{x + 0.5, 100.0 - 60.0 * std::cos(angle)});
    }
    drawPolylineWu(waves, sine, Colour{30, 60, 200});
    drawPolylineWu(waves, cosine, Colour{200, 40, 40});

    Image spiral(300, 300, colours::white);
    PointF previous = c;
    for (int i = 1; i <= 640; ++i) {
        double angle = i * 0.05;
        PointF p = pointOnCircle(c, 4.0 * angle, angle);
        Colour col = toColour(hsvToRgb(HSV{radiansToDegrees(angle), 0.8, 0.85}));
        drawLineWu(spiral, previous, p, col);
        previous = p;
    }

    Image orbits(400, 260, Colour{5, 5, 20});
    const double orbitA[4] = {50.0, 90.0, 130.0, 175.0};
    const double orbitB[4] = {30.0, 55.0, 80.0, 110.0};
    const double planetAngle[4] = {30.0, 150.0, 250.0, 320.0};
    const Colour planetColour[4] = {colours::red, colours::cyan, colours::green, colours::magenta};
    PointF sun{200.0, 130.0};
    for (int k = 0; k < 4; ++k) {
        std::vector<PointF> path;
        for (int i = 0; i <= 120; ++i) {
            path.push_back(pointOnEllipse(sun, orbitA[k], orbitB[k], 2.0 * kPi * i / 120.0));
        }
        drawPolylineWu(orbits, path, Colour{80, 80, 110});
    }
    fillCircleAA(orbits, sun.x, sun.y, 18.0, colours::yellow);
    for (int k = 0; k < 4; ++k) {
        PointF p = pointOnEllipse(sun, orbitA[k], orbitB[k], degreesToRadians(planetAngle[k]));
        fillCircleAA(orbits, p.x, p.y, 6.0, planetColour[k]);
    }

    bool ok = clock.savePPM("clock.ppm");
    ok = ok && shapes.savePPM("shapes.ppm");
    ok = ok && waves.savePPM("waves.ppm");
    ok = ok && spiral.savePPM("spiral.ppm");
    ok = ok && orbits.savePPM("orbits.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
