#include <iostream>
#include <string>
#include <vector>
#include "hsv.h"
#include "lines.h"

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

int main() {
    Image a(6, 3);
    drawLineShallow(a, 0, 0, 5, 2, colours::white);
    printGrid("shallow Bresenham (0, 0) to (5, 2)", a);

    Image b(3, 7);
    drawLine(b, 0, 0, 2, 6, colours::white);
    printGrid("drawLine (0, 0) to (2, 6)", b);

    Image tieDDA(3, 2);
    drawLineDDA(tieDDA, 0, 0, 2, 1, colours::white);
    printGrid("DDA (0, 0) to (2, 1)", tieDDA);

    Image tieShallow(3, 2);
    drawLineShallow(tieShallow, 0, 0, 2, 1, colours::white);
    printGrid("shallow Bresenham (0, 0) to (2, 1)", tieShallow);

    Image tieGeneral(3, 2);
    drawLine(tieGeneral, 0, 0, 2, 1, colours::white);
    printGrid("drawLine (0, 0) to (2, 1)", tieGeneral);

    std::vector<Point> pts = linePoints(10, 10, 70, 10);
    std::cout << "points on (10, 10) to (70, 10): " << pts.size() << "\n";

    Image fan(200, 200, colours::white);
    for (int i = 0; i < 200; i += 10) {
        Colour c = toColour(hsvToRgb(HSV{i * 1.8, 0.9, 0.8}));
        drawLine(fan, 100, 100, i, 0, c);
        drawLine(fan, 100, 100, 199, i, c);
        drawLine(fan, 100, 100, 199 - i, 199, c);
        drawLine(fan, 100, 100, 0, 199 - i, c);
    }

    Image styles(300, 200, colours::white);
    drawLine(styles, 20, 30, 280, 60, colours::black);
    drawThickLine(styles, 20, 80, 280, 110, 5, colours::blue);
    drawDashedLine(styles, 20, 130, 280, 160, 10, 6, colours::red);
    const int xs[5] = {40, 120, 200, 160, 60};
    const int ys[5] = {190, 170, 190, 140, 140};
    for (int i = 0; i < 5; ++i) {
        int j = (i + 1) % 5;
        drawLine(styles, xs[i], ys[i], xs[j], ys[j], Colour{0, 140, 0}, false);
    }

    bool ok = fan.savePPM("fan_bresenham.ppm");
    ok = ok && styles.savePPM("styles.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
