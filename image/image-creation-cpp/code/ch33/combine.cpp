#include <iostream>
#include <vector>
#include "combine.h"

double clean(double v) {
    return (v == 0.0) ? 0.0 : v;
}

void printMatrix(const char* label, const Mat3& t) {
    std::cout << label << "\n";
    for (int row = 0; row < 3; ++row) {
        std::cout << "  " << clean(t.m[row][0]) << "  " << clean(t.m[row][1]) << "  "
                  << clean(t.m[row][2]) << "\n";
    }
}

Image makeTestPicture() {
    Image pic(120, 90, colours::white);
    for (int y = 0; y < 90; ++y) {
        for (int x = 0; x < 120; ++x) {
            if ((x / 15 + y / 15) % 2 == 0) {
                pic.setPixel(x, y, Colour{200, 215, 240});
            }
        }
    }
    drawArrowAA(pic, PointF{60.0, 78.0}, PointF{60.0, 12.0}, 10.0, colours::red);
    fillCircleAA(pic, 15.0, 15.0, 8.0, Colour{0, 150, 0});
    return pic;
}

void drawArm(Image& image, const Mat3& base, double shoulder, double elbow, double wrist,
             Colour col) {
    PointF origin{0.0, 0.0};
    Mat3 upper = base * rotation(degreesToRadians(shoulder));
    fillCapsuleAA(image, applyToPoint(upper, origin), applyToPoint(upper, PointF{100.0, 0.0}), 9.0,
                  col);
    Mat3 fore = upper * translation(100.0, 0.0) * rotation(degreesToRadians(elbow));
    fillCapsuleAA(image, applyToPoint(fore, origin), applyToPoint(fore, PointF{80.0, 0.0}), 7.0, col);
    Mat3 hand = fore * translation(80.0, 0.0) * rotation(degreesToRadians(wrist));
    PointF wristPoint = applyToPoint(hand, origin);
    fillCapsuleAA(image, wristPoint, applyToPoint(hand, PointF{20.0, -10.0}), 3.0, col);
    fillCapsuleAA(image, wristPoint, applyToPoint(hand, PointF{20.0, 10.0}), 3.0, col);
    PointF elbowPoint = applyToPoint(fore, origin);
    fillCircleAA(image, elbowPoint.x, elbowPoint.y, 9.0, Colour{60, 60, 70});
}

int main() {
    Vec2 turned = applyToPoint(rotationAbout(PointF{2.0, 2.0}, degreesToRadians(90.0)),
                               Vec2{5.0, 2.0});
    std::cout << "rotationAbout (2, 2) by 90 degrees sends (5, 2) to (" << turned.x << ", "
              << turned.y << ")\n";
    printMatrix("scalingAbout((2, 2), 2, 2):", scalingAbout(PointF{2.0, 2.0}, 2.0, 2.0));

    Mat3 m = translation(10.0, 5.0) * scaling(2.0, 4.0);
    Mat3 back;
    inverse(m, back);
    printMatrix("M = translation(10, 5) * scaling(2, 4):", m);
    printMatrix("inverse of M:", back);
    printMatrix("M * inverse:", m * back);

    Mat3 spin = rotationAbout(PointF{50.0, 50.0}, degreesToRadians(30.0)) * scaling(1.5, 1.5);
    Mat3 unspin;
    inverse(spin, unspin);
    Vec2 there = applyToPoint(spin, Vec2{7.0, 3.0});
    Vec2 home = applyToPoint(unspin, there);
    std::cout << "(7, 3) goes to (" << there.x << ", " << there.y << ") and comes back to ("
              << home.x << ", " << home.y << ")\n";
    Mat3 flat;
    std::cout << "can scaling(1, 0) be undone? " << (inverse(scaling(1.0, 0.0), flat) ? "yes" : "no")
              << "\n";

    Image pic = makeTestPicture();
    Mat3 placeRotated = translation(100.0, 110.0) * rotation(degreesToRadians(30.0)) *
                        translation(-60.0, -45.0);
    Rect box = transformedBox(placeRotated, pic.width(), pic.height());
    std::cout << "box of the turned picture: " << box.x0 << ", " << box.y0 << " to " << box.x1
              << ", " << box.y1 << "\n";

    Image arm(400, 300, Colour{240, 240, 235});
    fillRect(arm, Rect{170, 250, 230, 300}, Colour{90, 90, 100});
    Mat3 shoulderPlace = translation(200.0, 250.0);
    drawArm(arm, shoulderPlace, -140.0, 60.0, 30.0, Colour{190, 200, 230});
    drawArm(arm, shoulderPlace, -100.0, 30.0, -20.0, Colour{120, 140, 210});
    drawArm(arm, shoulderPlace, -60.0, 40.0, 20.0, Colour{40, 70, 180});

    Image solar(400, 400, Colour{5, 5, 20});
    Mat3 sunPlace = translation(200.0, 200.0);
    std::vector<PointF> planetPath;
    std::vector<PointF> moonPath;
    PointF origin{0.0, 0.0};
    for (int i = 0; i <= 720; ++i) {
        double t = 2.0 * kPi * i / 720.0;
        Mat3 planet = sunPlace * rotation(t) * translation(130.0, 0.0);
        Mat3 moon = planet * rotation(13.0 * t) * translation(35.0, 0.0);
        planetPath.push_back(applyToPoint(planet, origin));
        moonPath.push_back(applyToPoint(moon, origin));
    }
    drawPolylineWu(solar, planetPath, Colour{70, 70, 100});
    drawPolylineWu(solar, moonPath, Colour{60, 160, 170});
    fillCircleAA(solar, 200.0, 200.0, 25.0, colours::yellow);
    double now = degreesToRadians(40.0);
    Mat3 planetNow = sunPlace * rotation(now) * translation(130.0, 0.0);
    Mat3 moonNow = planetNow * rotation(13.0 * now) * translation(35.0, 0.0);
    PointF p = applyToPoint(planetNow, origin);
    PointF q = applyToPoint(moonNow, origin);
    fillCircleAA(solar, p.x, p.y, 10.0, Colour{60, 120, 255});
    fillCircleAA(solar, q.x, q.y, 4.0, colours::white);

    Image moved(600, 220, Colour{230, 230, 230});
    drawImageTransformed(moved, pic, placeRotated);
    drawImageTransformed(moved, pic, translation(300.0, 110.0) * scaling(1.6, 1.6) *
                                         translation(-60.0, -45.0));
    drawImageTransformed(moved, pic, translation(500.0, 110.0) * skew(0.5, 0.0) *
                                         translation(-60.0, -45.0));

    Image holes(600, 255, Colour{230, 230, 230});
    drawImageForward(holes, pic, translation(0.0, 15.0) * scaling(2.5, 2.5));
    drawImageTransformed(holes, pic, translation(300.0, 15.0) * scaling(2.5, 2.5));

    bool ok = arm.savePPM("arm.ppm");
    ok = ok && solar.savePPM("solar.ppm");
    ok = ok && moved.savePPM("moved.ppm");
    ok = ok && holes.savePPM("holes.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
