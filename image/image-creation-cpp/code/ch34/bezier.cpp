#include <cmath>
#include <iostream>
#include <vector>
#include "bezier.h"

void printPoint(const char* label, PointF p) {
    std::cout << label << " (" << p.x << ", " << p.y << ")\n";
}

void drawDot(Image& image, PointF p, double r, Colour c) {
    fillCircleAA(image, p.x, p.y, r, c);
}

void drawHandles(Image& image, PointF p0, PointF p1, PointF p2, PointF p3) {
    Colour grey{170, 170, 180};
    drawLineWu(image, p0, p1, grey);
    drawLineWu(image, p2, p3, grey);
    drawDot(image, p0, 3.0, colours::black);
    drawDot(image, p3, 3.0, colours::black);
    drawDot(image, p1, 3.0, Colour{230, 120, 0});
    drawDot(image, p2, 3.0, Colour{230, 120, 0});
}

int main() {
    printPoint("quadratic (0, 0), (50, 100), (100, 0) at t = 0.5:",
               quadraticPoint(PointF{0.0, 0.0}, PointF{50.0, 100.0}, PointF{100.0, 0.0}, 0.5));
    PointF a{0.0, 0.0};
    PointF b{0.0, 100.0};
    PointF c{100.0, 100.0};
    PointF d{100.0, 0.0};
    const double times[3] = {0.25, 0.5, 0.75};
    for (double t : times) {
        PointF p = cubicPoint(a, b, c, d, t);
        PointF q = cubicPointFormula(a, b, c, d, t);
        std::cout << "cubic at t = " << t << ": (" << p.x << ", " << p.y << "), formula ("
                  << q.x << ", " << q.y << ")\n";
    }
    printPoint("tangent at t = 0:", cubicTangent(a, b, c, d, 0.0));
    printPoint("tangent at t = 0.5:", cubicTangent(a, b, c, d, 0.5));
    std::vector<PointF> counted;
    appendCubic(counted, a, b, c, d);
    std::cout << "points used for this curve: " << counted.size() << "\n";

    std::vector<PointF> ring = bezierCircle(PointF{0.0, 0.0}, 100.0);
    double worst = 0.0;
    for (PointF p : ring) {
        worst = std::max(worst, std::fabs(length(p) - 100.0));
    }
    std::cout << "Bezier circle of radius 100: " << ring.size() << " points, largest error "
              << worst << " pixels\n";

    Image steps(400, 300, colours::white);
    PointF p0{40.0, 260.0};
    PointF p1{80.0, 40.0};
    PointF p2{300.0, 30.0};
    PointF p3{360.0, 250.0};
    double t = 0.4;
    PointF q0 = lerpPoint(p0, p1, t);
    PointF q1 = lerpPoint(p1, p2, t);
    PointF q2 = lerpPoint(p2, p3, t);
    PointF r0 = lerpPoint(q0, q1, t);
    PointF r1 = lerpPoint(q1, q2, t);
    PointF s = lerpPoint(r0, r1, t);
    drawPolylineWu(steps, {p0, p1, p2, p3}, Colour{170, 170, 180});
    drawPolylineWu(steps, {q0, q1, q2}, Colour{80, 160, 80});
    drawLineWu(steps, r0, r1, Colour{60, 90, 220});
    drawCubic(steps, p0, p1, p2, p3, colours::black);
    for (PointF p : {p0, p1, p2, p3}) {
        drawDot(steps, p, 4.0, Colour{120, 120, 130});
    }
    for (PointF p : {q0, q1, q2}) {
        drawDot(steps, p, 4.0, Colour{80, 160, 80});
    }
    drawDot(steps, r0, 4.0, Colour{60, 90, 220});
    drawDot(steps, r1, 4.0, Colour{60, 90, 220});
    drawDot(steps, s, 5.0, colours::red);

    Image curves(800, 200, colours::white);
    const PointF shapes[4][4] = {
        {PointF{20.0, 160.0}, PointF{80.0, 20.0}, PointF{120.0, 180.0}, PointF{180.0, 40.0}},
        {PointF{220.0, 170.0}, PointF{230.0, 20.0}, PointF{370.0, 20.0}, PointF{380.0, 170.0}},
        {PointF{420.0, 170.0}, PointF{600.0, 30.0}, PointF{400.0, 30.0}, PointF{580.0, 170.0}},
        {PointF{620.0, 170.0}, PointF{700.0, 20.0}, PointF{700.0, 20.0}, PointF{780.0, 170.0}}};
    for (int i = 0; i < 4; ++i) {
        drawHandles(curves, shapes[i][0], shapes[i][1], shapes[i][2], shapes[i][3]);
        drawCubic(curves, shapes[i][0], shapes[i][1], shapes[i][2], shapes[i][3],
                  Colour{30, 60, 200});
    }

    Image heart(300, 300, Colour{255, 240, 245});
    std::vector<PointF> outline;
    appendCubic(outline, PointF{150.0, 260.0}, PointF{40.0, 180.0}, PointF{50.0, 40.0},
                PointF{150.0, 95.0});
    appendCubic(outline, PointF{150.0, 95.0}, PointF{250.0, 40.0}, PointF{260.0, 180.0},
                PointF{150.0, 260.0});
    fillPolygonAA(heart, outline, Colour{220, 30, 70});

    Image path(500, 300, colours::white);
    std::vector<PointF> stops = {PointF{30.0, 250.0}, PointF{110.0, 80.0}, PointF{200.0, 200.0},
                                 PointF{280.0, 60.0}, PointF{380.0, 220.0}, PointF{470.0, 90.0}};
    drawPolylineWu(path, stops, Colour{200, 200, 210});
    drawPolylineWu(path, smoothPath(stops), Colour{200, 40, 40});
    for (PointF p : stops) {
        drawDot(path, p, 4.0, colours::black);
    }
    std::vector<PointF> circle = bezierCircle(PointF{50.0, 50.0}, 35.0);
    drawPolylineWu(path, circle, Colour{30, 60, 200});

    bool ok = steps.savePPM("steps.ppm");
    ok = ok && curves.savePPM("curves.ppm");
    ok = ok && heart.savePPM("heart.ppm");
    ok = ok && path.savePPM("path.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
