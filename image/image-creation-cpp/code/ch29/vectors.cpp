#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
#include "vec2.h"

void show(const std::string& name, Vec2 v) {
    std::cout << name << " = (" << v.x << ", " << v.y << ")\n";
}

int main() {
    Vec2 a{3.0, 4.0};
    Vec2 b{2.0, -1.0};
    show("a + b", a + b);
    show("a - b", a - b);
    show("a * 2", a * 2.0);
    std::cout << "length of a = " << length(a) << "\n";
    show("normalize(a)", normalize(a));
    std::cout << "dot(a, b) = " << dot(a, b) << ", cross(a, b) = " << cross(a, b) << "\n";
    show("perpendicular(a)", perpendicular(a));
    std::cout << "dot(a, perpendicular(a)) = " << dot(a, perpendicular(a)) << "\n";

    Vec2 right{1.0, 0.0};
    std::cout << "dot with (1, 0): (1, 1) -> " << dot(right, Vec2{1.0, 1.0}) << ", (0, 1) -> "
              << dot(right, Vec2{0.0, 1.0}) << ", (-1, 1) -> " << dot(right, Vec2{-1.0, 1.0})
              << "\n";

    Vec2 pa{2.0, 2.0};
    Vec2 pb{10.0, 2.0};
    Vec2 pp{6.0, 5.0};
    std::cout << "edgeFunction = " << edgeFunction(pa, pb, pp)
              << ", cross(B - A, P - A) = " << cross(pb - pa, pp - pa) << "\n";

    std::cout << "distance from (4, 0) to the line (0, 0)-(3, 4) = "
              << distanceToLine(Vec2{4.0, 0.0}, Vec2{0.0, 0.0}, Vec2{3.0, 4.0}) << "\n";
    show("project (4, 0) onto (3, 4)", project(Vec2{4.0, 0.0}, Vec2{3.0, 4.0}));
    show("reflect (3, -4) on a floor with normal (0, 1)", reflect(Vec2{3.0, -4.0}, Vec2{0.0, 1.0}));

    Vec2 s0{0.0, 0.0};
    Vec2 s1{10.0, 0.0};
    const Vec2 tests[3] = {Vec2{-3.0, 4.0}, Vec2{4.0, 3.0}, Vec2{13.0, 4.0}};
    for (Vec2 p : tests) {
        Vec2 q = closestPointOnSegment(p, s0, s1);
        std::cout << "closest point to (" << p.x << ", " << p.y << ") is (" << q.x << ", " << q.y
                  << "), distance " << distanceToSegment(p, s0, s1) << "\n";
    }

    Image add(400, 300, colours::white);
    Vec2 origin{40.0, 250.0};
    Vec2 va{180.0, -60.0};
    Vec2 vb{100.0, -150.0};
    drawLineWu(add, origin + vb, origin + va + vb, Colour{200, 200, 200});
    drawLineWu(add, origin + va, origin + va + vb, Colour{200, 200, 200});
    drawLineWu(add, origin, origin + vb, Colour{200, 200, 200});
    drawArrowAA(add, origin, origin + va, 3.0, Colour{40, 80, 200});
    drawArrowAA(add, origin + va, origin + va + vb, 3.0, Colour{200, 40, 40});
    drawArrowAA(add, origin, origin + va + vb, 3.0, Colour{30, 150, 60});

    Image field(400, 400, Colour{15, 20, 35});
    Vec2 centre{200.0, 200.0};
    for (int gy = 20; gy < 400; gy += 40) {
        for (int gx = 20; gx < 400; gx += 40) {
            Vec2 p{gx + 0.5, gy + 0.5};
            Vec2 v = perpendicular(p - centre) * 0.12;
            double len = length(v);
            if (len > 30.0) {
                v = v * (30.0 / len);
            }
            double t = std::min(len / 30.0, 1.0);
            Colour col = lerpColour(Colour{80, 160, 255}, Colour{255, 120, 60}, t);
            drawArrowAA(field, p - v * 0.5, p + v * 0.5, 2.0, col);
        }
    }

    Image bounce(400, 300, colours::white);
    strokeRect(bounce, Rect{10, 10, 390, 290}, 2, Colour{120, 120, 120});
    Vec2 pos{50.0, 60.0};
    Vec2 vel{5.0, 0.0};
    const Vec2 gravity{0.0, 0.25};
    std::vector<PointF> trail;
    for (int step = 0; step < 160; ++step) {
        trail.push_back(pos);
        vel = vel + gravity;
        pos = pos + vel;
        if (pos.x < 20.0 || pos.x > 380.0) {
            vel = reflect(vel, Vec2{1.0, 0.0});
            pos.x = std::clamp(pos.x, 20.0, 380.0);
        }
        if (pos.y < 20.0 || pos.y > 280.0) {
            vel = reflect(vel, Vec2{0.0, 1.0});
            pos.y = std::clamp(pos.y, 20.0, 280.0);
        }
    }
    drawPolylineWu(bounce, trail, Colour{160, 160, 200});
    for (int i = 0; i < static_cast<int>(trail.size()); i += 16) {
        fillCircleAA(bounce, trail[i].x, trail[i].y, 7.0, Colour{230, 90, 40});
    }

    Image figure(300, 300, Colour{250, 245, 230});
    Colour ink{40, 40, 60};
    fillCircleAA(figure, 150.0, 70.0, 30.0, ink);
    fillCapsuleAA(figure, Vec2{150.0, 100.0}, Vec2{150.0, 190.0}, 8.0, ink);
    fillCapsuleAA(figure, Vec2{150.0, 120.0}, Vec2{95.0, 160.0}, 6.0, ink);
    fillCapsuleAA(figure, Vec2{150.0, 120.0}, Vec2{210.0, 95.0}, 6.0, ink);
    fillCapsuleAA(figure, Vec2{150.0, 190.0}, Vec2{110.0, 270.0}, 7.0, ink);
    fillCapsuleAA(figure, Vec2{150.0, 190.0}, Vec2{195.0, 268.0}, 7.0, ink);

    bool ok = add.savePPM("add.ppm");
    ok = ok && field.savePPM("field.ppm");
    ok = ok && bounce.savePPM("bounce.ppm");
    ok = ok && figure.savePPM("figure.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
