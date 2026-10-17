#include <cmath>
#include <iostream>
#include <string>
#include <vector>
#include "hsv.h"
#include "triangles.h"

void printGrid(const std::string& title, const Image& img) {
    std::cout << title << ":\n";
    for (int y = 0; y < img.height(); ++y) {
        std::cout << "  ";
        for (int x = 0; x < img.width(); ++x) {
            Colour c = img.getPixel(x, y);
            bool on = c.r != 0 || c.g != 0 || c.b != 0;
            std::cout << (on ? '#' : '.');
        }
        std::cout << "\n";
    }
}

int countLit(const Image& img) {
    int count = 0;
    for (int y = 0; y < img.height(); ++y) {
        for (int x = 0; x < img.width(); ++x) {
            Colour c = img.getPixel(x, y);
            if (c.r != 0 || c.g != 0 || c.b != 0) {
                ++count;
            }
        }
    }
    return count;
}

bool samePixels(const Image& p, const Image& q) {
    if (p.width() != q.width() || p.height() != q.height()) {
        return false;
    }
    for (int y = 0; y < p.height(); ++y) {
        for (int x = 0; x < p.width(); ++x) {
            Colour s = p.getPixel(x, y);
            Colour t = q.getPixel(x, y);
            if (s.r != t.r || s.g != t.g || s.b != t.b) {
                return false;
            }
        }
    }
    return true;
}

enum class EdgeRule { Include, Exclude, TopLeft };

bool coversWithRule(double e, bool topLeft, EdgeRule rule) {
    if (rule == EdgeRule::Include) {
        return e >= 0.0;
    }
    if (rule == EdgeRule::Exclude) {
        return e > 0.0;
    }
    return edgeCovers(e, topLeft);
}

void paintTriangle(Image& image, PointF a, PointF b, PointF c, Colour col, double alpha,
                   EdgeRule rule) {
    if (edgeFunction(a, b, c) < 0.0) {
        std::swap(b, c);
    }
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            PointF p{x + 0.5, y + 0.5};
            bool inside = coversWithRule(edgeFunction(b, c, p), isTopLeft(b, c), rule) &&
                          coversWithRule(edgeFunction(c, a, p), isTopLeft(c, a), rule) &&
                          coversWithRule(edgeFunction(a, b, p), isTopLeft(a, b), rule);
            if (inside) {
                if (alpha >= 1.0) {
                    image.setPixel(x, y, col);
                } else {
                    blendPixel(image, x, y, col, alpha);
                }
            }
        }
    }
}

void showSharedEdge(const std::string& title, EdgeRule rule) {
    PointF p0{0.0, 0.0};
    PointF p1{8.0, 0.0};
    PointF p2{8.0, 8.0};
    PointF p3{0.0, 8.0};
    Image first(8, 8);
    Image second(8, 8);
    paintTriangle(first, p0, p1, p2, colours::white, 1.0, rule);
    paintTriangle(second, p0, p2, p3, colours::white, 1.0, rule);
    int twice = 0;
    int never = 0;
    std::cout << title << ":\n";
    for (int y = 0; y < 8; ++y) {
        std::cout << "  ";
        for (int x = 0; x < 8; ++x) {
            int count = 0;
            if (first.getPixel(x, y).r != 0) {
                ++count;
            }
            if (second.getPixel(x, y).r != 0) {
                ++count;
            }
            if (count == 0) {
                ++never;
                std::cout << '.';
            } else {
                if (count == 2) {
                    ++twice;
                }
                std::cout << count;
            }
        }
        std::cout << "\n";
    }
    std::cout << "  painted twice: " << twice << ", never painted: " << never << "\n";
}

PointF lerpPoint(PointF p, PointF q, double t) {
    return PointF{lerp(p.x, q.x, t), lerp(p.y, q.y, t)};
}

void drawMountain(Image& image, PointF left, PointF peak, PointF right, Colour col) {
    fillTriangle(image, left, peak, right, col);
    PointF capLeft = lerpPoint(peak, left, 0.25);
    PointF capRight = lerpPoint(peak, right, 0.25);
    fillTriangle(image, capLeft, peak, capRight, colours::white);
}

std::vector<PointF> hexagon(double cx, double cy, double r) {
    double h = r * std::sqrt(3.0) / 2.0;
    return {PointF{cx + r, cy}, PointF{cx + r / 2.0, cy + h}, PointF{cx - r / 2.0, cy + h},
            PointF{cx - r, cy}, PointF{cx - r / 2.0, cy - h}, PointF{cx + r / 2.0, cy - h}};
}

int main() {
    PointF a{2.0, 2.0};
    PointF b{10.0, 2.0};
    std::cout << "edge from (2, 2) to (10, 2):\n";
    std::cout << "  E at (6, 5) = " << edgeFunction(a, b, PointF{6.0, 5.0}) << "\n";
    std::cout << "  E at (6, 0) = " << edgeFunction(a, b, PointF{6.0, 0.0}) << "\n";
    std::cout << "  E at (6, 2) = " << edgeFunction(a, b, PointF{6.0, 2.0}) << "\n";

    PointF t0{1.0, 1.0};
    PointF t1{12.0, 4.0};
    PointF t2{4.0, 10.0};
    Image small(14, 12);
    fillTriangle(small, t0, t1, t2, colours::white);
    printGrid("filled triangle (1, 1), (12, 4), (4, 10)", small);
    std::cout << "pixels: " << countLit(small) << ", area: " << triangleArea(t0, t1, t2) << "\n";

    Image swapped(14, 12);
    fillTriangle(swapped, t0, t2, t1, colours::white);
    std::cout << "the other order gives the same pixels: "
              << (samePixels(small, swapped) ? "yes" : "no") << "\n";

    showSharedEdge("shared edge, rule E >= 0", EdgeRule::Include);
    showSharedEdge("shared edge, rule E > 0", EdgeRule::Exclude);
    showSharedEdge("shared edge, top-left rule", EdgeRule::TopLeft);

    Image land(320, 200);
    for (int y = 0; y < 200; ++y) {
        double t = y / 199.0;
        Colour sky = lerpColour(Colour{30, 60, 140}, Colour{250, 180, 120}, t);
        fillRect(land, Rect{0, y, 320, y + 1}, sky);
    }
    fillCircle(land, 280.5, 45.5, 20.0, Colour{255, 230, 150});
    drawMountain(land, PointF{120.0, 170.0}, PointF{230.0, 45.0}, PointF{340.0, 170.0},
                 Colour{120, 110, 150});
    drawMountain(land, PointF{-30.0, 170.0}, PointF{90.0, 30.0}, PointF{210.0, 170.0},
                 Colour{80, 70, 110});
    fillRect(land, Rect{0, 170, 320, 200}, Colour{40, 90, 50});

    Image seams(320, 160, colours::white);
    for (int x = 0; x < 320; x += 40) {
        fillRect(seams, Rect{x, 0, x + 20, 160}, Colour{200, 200, 200});
    }
    std::vector<PointF> left = hexagon(80.5, 80.5, 60.0);
    for (int i = 1; i + 1 < 6; ++i) {
        paintTriangle(seams, left[0], left[i], left[i + 1], Colour{230, 80, 30}, 0.5,
                      EdgeRule::Include);
    }
    fillConvexPolygon(seams, hexagon(240.5, 80.5, 60.0), Colour{230, 80, 30}, 0.5);

    Image wheel(200, 200, colours::white);
    PointF centre{100.0, 100.0};
    std::vector<PointF> corners = hexagon(100.0, 100.0, 90.0);
    for (int i = 0; i < 6; ++i) {
        PointF p = corners[i];
        PointF q = corners[(i + 1) % 6];
        Colour col = toColour(hsvToRgb(HSV{i * 60.0, 0.8, 1.0}));
        fillTriangle(wheel, centre, p, q, col);
        drawTriangle(wheel, Point{100, 100}, Point{roundToInt(p.x), roundToInt(p.y)},
                     Point{roundToInt(q.x), roundToInt(q.y)}, colours::black);
    }

    bool ok = land.savePPM("mountains.ppm");
    ok = ok && seams.savePPM("seams.ppm");
    ok = ok && wheel.savePPM("wheel.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
