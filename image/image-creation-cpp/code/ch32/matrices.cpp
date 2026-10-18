#include <iostream>
#include <vector>
#include "matrix.h"
#include "hsv.h"

void printMatrix(const char* label, const Mat3& t) {
    std::cout << label << "\n";
    for (int row = 0; row < 3; ++row) {
        std::cout << "  " << t.m[row][0] << "  " << t.m[row][1] << "  " << t.m[row][2] << "\n";
    }
}

std::vector<PointF> closed(std::vector<PointF> points) {
    if (!points.empty()) {
        points.push_back(points[0]);
    }
    return points;
}

void drawGridPanel(Image& image, const Mat3& t, PointF centre) {
    Mat3 place = translation(centre.x, centre.y) * t;
    for (int i = -3; i <= 3; ++i) {
        double k = i * 20.0;
        Colour col = (i == 0) ? Colour{100, 100, 110} : Colour{195, 195, 205};
        drawLineWu(image, applyToPoint(place, Vec2{k, -60.0}), applyToPoint(place, Vec2{k, 60.0}), col);
        drawLineWu(image, applyToPoint(place, Vec2{-60.0, k}), applyToPoint(place, Vec2{60.0, k}), col);
    }
    PointF o = applyToPoint(place, Vec2{0.0, 0.0});
    drawArrowAA(image, o, applyToPoint(place, Vec2{40.0, 0.0}), 3.0, colours::red);
    drawArrowAA(image, o, applyToPoint(place, Vec2{0.0, 40.0}), 3.0, Colour{0, 150, 0});
}

int main() {
    printMatrix("rotation by 30 degrees:", rotation(degreesToRadians(30.0)));
    Mat3 move = translation(10.0, 5.0);
    Vec2 p = applyToPoint(move, Vec2{3.0, 1.0});
    Vec2 d = applyToDirection(move, Vec2{3.0, 1.0});
    std::cout << "move by (10, 5): the point (3, 1) goes to (" << p.x << ", " << p.y
              << "), the direction (3, 1) stays (" << d.x << ", " << d.y << ")\n";

    printMatrix("translation(10, 5) * scaling(2, 3):", translation(10.0, 5.0) * scaling(2.0, 3.0));
    printMatrix("scaling(2, 3) * translation(10, 5):", scaling(2.0, 3.0) * translation(10.0, 5.0));

    double quarter = degreesToRadians(90.0);
    Vec2 a = applyToPoint(translation(10.0, 0.0) * rotation(quarter), Vec2{1.0, 0.0});
    Vec2 b = applyToPoint(rotation(quarter) * translation(10.0, 0.0), Vec2{1.0, 0.0});
    std::cout << "(1, 0) with translation * rotation: (" << a.x << ", " << a.y << ")\n";
    std::cout << "(1, 0) with rotation * translation: (" << b.x << ", " << b.y << ")\n";

    printMatrix("rotation(20) * rotation(25):",
                rotation(degreesToRadians(20.0)) * rotation(degreesToRadians(25.0)));
    std::cout << "determinants: rotation " << determinant(rotation(degreesToRadians(30.0)))
              << ", scaling(2, 3) " << determinant(scaling(2.0, 3.0)) << ", mirror "
              << determinant(scaling(-1.0, 1.0)) << ", skew " << determinant(skew(0.5, 0.0)) << "\n";

    Image grids(880, 220, colours::white);
    drawGridPanel(grids, identity(), PointF{110.0, 110.0});
    drawGridPanel(grids, rotation(degreesToRadians(30.0)), PointF{330.0, 110.0});
    drawGridPanel(grids, scaling(1.5, 0.6), PointF{550.0, 110.0});
    drawGridPanel(grids, skew(0.5, 0.0), PointF{770.0, 110.0});

    Image letters(600, 160, colours::white);
    std::vector<PointF> letterF = {PointF{-30.0, 0.0},  PointF{-30.0, -100.0}, PointF{30.0, -100.0},
                                   PointF{30.0, -80.0}, PointF{-10.0, -80.0},  PointF{-10.0, -60.0},
                                   PointF{20.0, -60.0}, PointF{20.0, -40.0},   PointF{-10.0, -40.0},
                                   PointF{-10.0, 0.0}};
    const Mat3 shapes[5] = {identity(), skew(-0.3, 0.0), rotation(degreesToRadians(20.0)),
                            scaling(-1.0, 1.0), skew(-0.3, 0.0) * scaling(-1.0, 1.0)};
    for (int i = 0; i < 5; ++i) {
        Mat3 place = translation(60.0 + i * 120.0, 130.0) * shapes[i];
        fillPolygonAA(letters, applyToPoints(place, letterF), Colour{40, 60, 140});
    }

    Image squares(300, 300, colours::white);
    std::vector<PointF> square = {PointF{-100.0, -100.0}, PointF{100.0, -100.0},
                                  PointF{100.0, 100.0}, PointF{-100.0, 100.0}};
    Mat3 step = rotation(degreesToRadians(10.0)) * scaling(0.93, 0.93);
    Mat3 current = identity();
    for (int k = 0; k < 30; ++k) {
        Colour col = toColour(hsvToRgb(HSV{k * 12.0, 0.8, 0.8}));
        std::vector<PointF> corners = applyToPoints(translation(150.0, 150.0) * current, square);
        drawPolylineWu(squares, closed(corners), col);
        current = step * current;
    }

    bool ok = grids.savePPM("grids.ppm");
    ok = ok && letters.savePPM("letters.ppm");
    ok = ok && squares.savePPM("squares.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
