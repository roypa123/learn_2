#include <iostream>
#include <vector>
#include "transform.h"
#include "hsv.h"

void printPoint(const char* label, Vec2 p) {
    std::cout << label << " (" << p.x << ", " << p.y << ")\n";
}

std::vector<PointF> closed(std::vector<PointF> points) {
    if (!points.empty()) {
        points.push_back(points[0]);
    }
    return points;
}

int main() {
    double quarter = degreesToRadians(90.0);
    printPoint("translate (3, 1) by (10, 5):", translate(Vec2{3.0, 1.0}, Vec2{10.0, 5.0}));
    printPoint("scale (4, 6) by 2 about (2, 2):",
               scaleAbout(Vec2{4.0, 6.0}, Vec2{2.0, 2.0}, 2.0, 2.0));
    printPoint("mirror (5, 3) about x = 2:", scaleAbout(Vec2{5.0, 3.0}, Vec2{2.0, 0.0}, -1.0, 1.0));
    printPoint("rotate (3, 1) by 90 degrees:", rotate(Vec2{3.0, 1.0}, quarter));
    printPoint("rotate (2, 1) by 30 degrees:", rotate(Vec2{2.0, 1.0}, degreesToRadians(30.0)));
    printPoint("rotate (5, 2) by 90 degrees about (2, 2):",
               rotateAbout(Vec2{5.0, 2.0}, Vec2{2.0, 2.0}, quarter));
    printPoint("(1, 0): rotate 90, then move by (10, 0):",
               translate(rotate(Vec2{1.0, 0.0}, quarter), Vec2{10.0, 0.0}));
    printPoint("(1, 0): move by (10, 0), then rotate 90:",
               rotate(translate(Vec2{1.0, 0.0}, Vec2{10.0, 0.0}), quarter));
    Vec2 v{3.0, 4.0};
    std::cout << "length of (3, 4) before and after a 37 degree turn: " << length(v) << ", "
              << length(rotate(v, degreesToRadians(37.0))) << "\n";
    Rect box = tiltedEllipseBox(PointF{0.0, 0.0}, 60.0, 20.0, degreesToRadians(30.0));
    std::cout << "box of a = 60, b = 20 tilted 30 degrees: " << box.x0 << ", " << box.y0 << " to "
              << box.x1 << ", " << box.y1 << "\n";
    PointF origin{0.0, 0.0};
    double thirty = degreesToRadians(30.0);
    bool first = insideTiltedEllipse(Vec2{47.0, 27.0}, origin, 60.0, 20.0, thirty);
    bool second = insideTiltedEllipse(Vec2{55.0, 0.0}, origin, 60.0, 20.0, thirty);
    std::cout << "is (47, 27) inside it? " << (first ? "yes" : "no") << ", is (55, 0)? "
              << (second ? "yes" : "no") << "\n";

    Image fan(300, 300, colours::white);
    PointF c{150.0, 150.0};
    std::vector<PointF> square = {c, c + Vec2{100.0, 0.0}, c + Vec2{100.0, 100.0},
                                  c + Vec2{0.0, 100.0}};
    for (int i = 0; i < 12; ++i) {
        Colour col = toColour(hsvToRgb(HSV{i * 30.0, 0.8, 0.85}));
        std::vector<PointF> turned = rotatePoints(square, c, degreesToRadians(i * 30.0));
        drawPolylineWu(fan, closed(turned), col);
    }

    Image flower(300, 300, Colour{235, 245, 235});
    for (int i = 0; i < 8; ++i) {
        double angle = degreesToRadians(i * 45.0);
        PointF petal = pointOnCircle(c, 70.0, angle);
        Colour col = toColour(hsvToRgb(HSV{320.0 + i * 5.0, 0.6, 0.95}));
        fillTiltedEllipseAA(flower, petal, 70.0, 24.0, angle, col);
    }
    fillCircleAA(flower, c.x, c.y, 30.0, Colour{250, 200, 40});

    Image compare(400, 200, colours::white);
    double tilt = degreesToRadians(30.0);
    Colour blue{40, 90, 200};
    fillPolygonAA(compare, tiltedEllipsePoints(PointF{100.0, 100.0}, 80.0, 35.0, tilt, 100), blue);
    fillTiltedEllipseAA(compare, PointF{300.0, 100.0}, 80.0, 35.0, tilt, blue);
    drawPolylineWu(compare, closed(tiltedEllipsePoints(PointF{300.0, 100.0}, 80.0, 35.0, tilt, 12)),
                   colours::red);

    Image figures(600, 220, colours::white);
    std::vector<PointF> house = {PointF{-40.0, 0.0},   PointF{40.0, 0.0},    PointF{40.0, -60.0},
                                 PointF{50.0, -60.0},  PointF{35.0, -72.0},  PointF{35.0, -95.0},
                                 PointF{25.0, -95.0},  PointF{25.0, -80.0},  PointF{0.0, -100.0},
                                 PointF{-50.0, -60.0}, PointF{-40.0, -60.0}};
    PointF ground{0.0, 0.0};
    Colour houseColour{200, 90, 50};
    fillPolygonAA(figures, translatePoints(house, Vec2{80.0, 180.0}), houseColour);
    fillPolygonAA(figures, translatePoints(scalePoints(house, ground, 1.5, 1.5), Vec2{220.0, 180.0}),
                  houseColour);
    fillPolygonAA(figures, translatePoints(scalePoints(house, ground, -1.0, 1.0), Vec2{370.0, 180.0}),
                  houseColour);
    fillPolygonAA(figures, translatePoints(scalePoints(house, ground, 1.0, 0.5), Vec2{510.0, 180.0}),
                  houseColour);
    drawLine(figures, 0, 180, 599, 180, Colour{120, 120, 120});

    Image trail(600, 200, Colour{20, 20, 40});
    std::vector<PointF> star = starPoints(origin, 30.0, 12.0, 5, degreesToRadians(-90.0));
    for (int i = 0; i < 9; ++i) {
        std::vector<PointF> spun = rotatePoints(star, origin, degreesToRadians(i * 15.0));
        std::vector<PointF> placed = translatePoints(spun, Vec2{60.0 + i * 60.0, 100.0});
        Colour col = toColour(hsvToRgb(HSV{40.0 + i * 20.0, 0.7, 0.4 + i * 0.07}));
        fillPolygonAA(trail, placed, col);
    }

    bool ok = fan.savePPM("fan.ppm");
    ok = ok && flower.savePPM("flower.ppm");
    ok = ok && compare.savePPM("compare.ppm");
    ok = ok && figures.savePPM("figures.ppm");
    ok = ok && trail.savePPM("trail.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
