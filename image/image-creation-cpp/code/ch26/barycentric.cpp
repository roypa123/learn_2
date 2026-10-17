#include <cmath>
#include <iostream>
#include <string>
#include "barycentric.h"

void printWeights(const std::string& name, PointF a, PointF b, PointF c, PointF p) {
    Barycentric w = barycentric(a, b, c, p);
    PointF back = fromBarycentric(a, b, c, w);
    std::cout << name << " (" << p.x << ", " << p.y << "): " << w.l0 << ", " << w.l1 << ", "
              << w.l2 << "  sum " << (w.l0 + w.l1 + w.l2)
              << (allPositive(w) ? "  inside" : "  outside") << "  back to (" << back.x << ", "
              << back.y << ")\n";
}

void printWeightMap(PointF a, PointF b, PointF c, int width, int height) {
    std::cout << "weight of corner A (l0), times 10:\n";
    for (int y = 0; y < height; ++y) {
        std::cout << "  ";
        for (int x = 0; x < width; ++x) {
            Barycentric w = barycentric(a, b, c, PointF{x + 0.5, y + 0.5});
            if (!allPositive(w)) {
                std::cout << '.';
                continue;
            }
            int digit = static_cast<int>(w.l0 * 10.0);
            if (digit > 9) {
                digit = 9;
            }
            std::cout << digit;
        }
        std::cout << "\n";
    }
}

void fillTriangleChecker(Image& image, PointF a, PointF b, PointF c, int squares,
                         Colour first, Colour second) {
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            Barycentric w = barycentric(a, b, c, PointF{x + 0.5, y + 0.5});
            if (!allPositive(w)) {
                continue;
            }
            int u = static_cast<int>(std::floor(w.l1 * squares));
            int v = static_cast<int>(std::floor(w.l2 * squares));
            image.setPixel(x, y, ((u + v) % 2 == 0) ? first : second);
        }
    }
}

int main() {
    PointF a{0.0, 0.0};
    PointF b{10.0, 0.0};
    PointF c{0.0, 10.0};
    PointF centre{(a.x + b.x + c.x) / 3.0, (a.y + b.y + c.y) / 3.0};
    std::cout << "triangle A (0, 0), B (10, 0), C (0, 10); weights l0, l1, l2:\n";
    printWeights("a point", a, b, c, PointF{3.5, 3.5});
    printWeights("the centre", a, b, c, centre);
    printWeights("corner A", a, b, c, a);
    printWeights("middle of BC", a, b, c, PointF{5.0, 5.0});
    printWeights("outside", a, b, c, PointF{8.0, 8.0});
    printWeights("other order", a, c, b, PointF{3.5, 3.5});

    printWeightMap(PointF{0.0, 0.0}, PointF{20.0, 0.0}, PointF{0.0, 10.0}, 20, 10);

    Image rgb(420, 200, colours::white);
    fillTriangleColours(rgb, PointF{110.0, 15.0}, PointF{200.0, 185.0}, PointF{20.0, 185.0},
                        colours::red, colours::green, colours::blue, false);
    fillTriangleColours(rgb, PointF{320.0, 15.0}, PointF{410.0, 185.0}, PointF{230.0, 185.0},
                        colours::red, colours::green, colours::blue, true);

    Image quad(420, 200, colours::white);
    const Colour topLeft = colours::red;
    const Colour topRight = colours::yellow;
    const Colour bottomRight = colours::blue;
    const Colour bottomLeft = colours::yellow;
    PointF p0{20.0, 10.0};
    PointF p1{200.0, 10.0};
    PointF p2{200.0, 190.0};
    PointF p3{20.0, 190.0};
    fillTriangleColours(quad, p0, p1, p2, topLeft, topRight, bottomRight);
    fillTriangleColours(quad, p0, p2, p3, topLeft, bottomRight, bottomLeft);
    for (int y = 10; y < 190; ++y) {
        for (int x = 220; x < 400; ++x) {
            double u = (x + 0.5 - 220.0) / 180.0;
            double v = (y + 0.5 - 10.0) / 180.0;
            Colour top = lerpLinear(topLeft, topRight, u);
            Colour bottom = lerpLinear(bottomLeft, bottomRight, u);
            quad.setPixel(x, y, lerpLinear(top, bottom, v));
        }
    }

    Image pattern(420, 200, Colour{230, 230, 230});
    fillTriangleChecker(pattern, PointF{20.0, 180.0}, PointF{190.0, 180.0}, PointF{20.0, 20.0}, 8,
                        colours::black, colours::white);
    fillTriangleChecker(pattern, PointF{230.0, 150.0}, PointF{400.0, 190.0}, PointF{330.0, 10.0}, 8,
                        Colour{200, 30, 30}, Colour{250, 220, 60});

    bool ok = rgb.savePPM("rgb.ppm");
    ok = ok && quad.savePPM("quad.ppm");
    ok = ok && pattern.savePPM("pattern.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
