#include <iostream>
#include <string>
#include "circles.h"
#include "hsv.h"

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

int main() {
    Image naive(11, 11);
    drawCircleNaive(naive, 5, 5, 5, colours::white);
    printGrid("naive circle, radius 5", naive);

    Image midpoint(11, 11);
    drawCircle(midpoint, 5, 5, 5, colours::white);
    printGrid("midpoint circle, radius 5", midpoint);
    std::cout << "pixels in the midpoint circle: " << countLit(midpoint) << "\n";

    Image disc(11, 11);
    fillCircle(disc, 5.5, 5.5, 5.0, colours::white);
    printGrid("filled disc, centre (5.5, 5.5), radius 5", disc);
    std::cout << "pixels in the filled disc: " << countLit(disc) << "\n";

    Image target(220, 220, colours::white);
    for (int r = 10; r <= 100; r += 10) {
        Colour c = (r % 20 == 0) ? colours::red : colours::blue;
        drawCircle(target, 110, 110, r, c);
    }

    Image bubbles(300, 200, Colour{20, 30, 60});
    for (int i = 0; i < 12; ++i) {
        double cx = 25.0 + i * 23.0;
        double cy = 100.0 + ((i % 3) - 1) * 45.0;
        double radius = 15.0 + (i % 4) * 8.0;
        Colour c = toColour(hsvToRgb(HSV{i * 30.0, 0.7, 1.0}));
        fillCircle(bubbles, cx, cy, radius, c, 0.5);
        drawCircle(bubbles, roundToInt(cx), roundToInt(cy), roundToInt(radius), colours::white);
    }

    bool ok = target.savePPM("target.ppm");
    ok = ok && bubbles.savePPM("bubbles.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
