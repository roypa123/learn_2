#include <climits>
#include <cmath>
#include <iostream>
#include <string>
#include "ellipses.h"

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

void fillEgg(Image& image, double cx, double cy, double a, double bTop, double bBottom,
             Colour c) {
    int x0 = static_cast<int>(std::floor(cx - a));
    int y0 = static_cast<int>(std::floor(cy - bTop));
    int x1 = static_cast<int>(std::ceil(cx + a));
    int y1 = static_cast<int>(std::ceil(cy + bBottom));
    Rect box = clipToImage(Rect{x0, y0, x1, y1}, image);
    for (int y = box.y0; y < box.y1; ++y) {
        for (int x = box.x0; x < box.x1; ++x) {
            double dx = (x + 0.5) - cx;
            double dy = (y + 0.5) - cy;
            double b = (dy < 0.0) ? bTop : bBottom;
            double u = dx / a;
            double v = dy / b;
            if (u * u + v * v <= 1.0) {
                image.setPixel(x, y, c);
            }
        }
    }
}

double orbitY(double a, double b, double x) {
    double t = 1.0 - (x / a) * (x / a);
    if (t < 0.0) {
        return 0.0;
    }
    return b * std::sqrt(t);
}

int main() {
    Image outline(13, 7);
    drawEllipse(outline, 6, 3, 6, 3, colours::white);
    printGrid("ellipse outline, a = 6, b = 3", outline);
    std::cout << "pixels in the outline: " << countLit(outline) << "\n";

    Image filled(13, 7);
    fillEllipse(filled, 6.5, 3.5, 6.0, 3.0, colours::white);
    printGrid("filled ellipse, centre (6.5, 3.5), a = 6, b = 3", filled);
    std::cout << "pixels in the filled ellipse: " << countLit(filled) << "\n";

    Image flat(21, 3);
    drawEllipse(flat, 10, 1, 10, 1, colours::white);
    printGrid("flat ellipse, a = 10, b = 1", flat);

    Image asEllipse(11, 11);
    Image asCircle(11, 11);
    drawEllipse(asEllipse, 5, 5, 5, 5, colours::white);
    drawCircle(asCircle, 5, 5, 5, colours::white);
    std::cout << "ellipse with a = b = 5 is the same as the circle: "
              << (samePixels(asEllipse, asCircle) ? "yes" : "no") << "\n";

    long long big = 4LL * 1000 * 1000 * 1000;
    std::cout << "4 * a * a * b for a = b = 1000: " << big << "\n";
    std::cout << "the biggest int:                " << INT_MAX << "\n";

    Image eye(300, 160, Colour{235, 190, 160});
    fillEllipse(eye, 150.5, 80.5, 120.0, 55.0, colours::white);
    fillCircle(eye, 150.5, 80.5, 42.0, Colour{60, 120, 200});
    fillCircle(eye, 150.5, 80.5, 18.0, colours::black);
    fillCircle(eye, 165.5, 65.5, 8.0, colours::white, 0.8);
    drawEllipse(eye, 150, 80, 120, 55, Colour{90, 50, 40});

    Image egg(200, 240, Colour{200, 225, 245});
    fillEllipse(egg, 100.5, 200.5, 62.0, 12.0, colours::black, 0.25);
    fillEgg(egg, 100.5, 120.5, 60.0, 90.0, 70.0, Colour{250, 240, 215});

    Image orbits(400, 260, Colour{5, 5, 20});
    const int sunX = 200;
    const int sunY = 130;
    const int orbitA[4] = {50, 90, 130, 175};
    const int orbitB[4] = {30, 55, 80, 110};
    const double planetX[4] = {30.0, -60.0, 100.0, -150.0};
    const Colour planetColour[4] = {colours::red, colours::cyan, colours::green, colours::magenta};
    for (int i = 0; i < 4; ++i) {
        drawEllipse(orbits, sunX, sunY, orbitA[i], orbitB[i], Colour{80, 80, 110});
    }
    fillCircle(orbits, sunX + 0.5, sunY + 0.5, 18.0, colours::yellow);
    for (int i = 0; i < 4; ++i) {
        double side = (i % 2 == 0) ? -1.0 : 1.0;
        double planetY = side * orbitY(orbitA[i], orbitB[i], planetX[i]);
        fillCircle(orbits, sunX + planetX[i] + 0.5, sunY + planetY + 0.5, 6.0, planetColour[i]);
    }

    bool ok = eye.savePPM("eye.ppm");
    ok = ok && egg.savePPM("egg.ppm");
    ok = ok && orbits.savePPM("orbits.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
