#include <iostream>
#include <string>
#include "draw.h"

void printRect(const std::string& label, Rect r) {
    std::cout << label << ": (" << r.x0 << ", " << r.y0 << ") to (" << r.x1 << ", " << r.y1
              << "), " << rectWidth(r) << " x " << rectHeight(r);
    if (isEmpty(r)) {
        std::cout << " (empty)";
    }
    std::cout << "\n";
}

int main() {
    printRect("makeRect(10, 20, 30, 40)", makeRect(10, 20, 30, 40));
    printRect("fromCorners(50, 30, 20, 10)", fromCorners(50, 30, 20, 10));
    printRect("overlap", intersect(makeRect(0, 0, 100, 100), makeRect(60, 70, 100, 100)));
    printRect("no overlap", intersect(makeRect(0, 0, 10, 10), makeRect(20, 0, 10, 10)));

    Image scene(320, 240);
    for (int y = 0; y < scene.height(); ++y) {
        double t = static_cast<double>(y) / (scene.height() - 1);
        Colour sky = lerpLinear(Colour{60, 120, 220}, Colour{200, 230, 255}, t);
        fillRect(scene, Rect{0, y, scene.width(), y + 1}, sky);
    }
    printRect("ground, clipped", clipToImage(makeRect(-50, 200, 400, 100), scene));
    fillRect(scene, makeRect(-50, 200, 400, 100), Colour{70, 140, 60});

    const Rect house = makeRect(90, 110, 140, 90);
    fillRect(scene, house, Colour{230, 200, 150});
    strokeRect(scene, house, 3, Colour{90, 60, 40});
    for (int step = 0; step < 5; ++step) {
        fillRect(scene, makeRect(80 + step * 16, 110 - (step + 1) * 10, 160 - step * 32, 10),
                 Colour{170, 50, 40});
    }
    fillRect(scene, makeRect(145, 150, 30, 50), Colour{110, 70, 40});
    for (int i = 0; i < 2; ++i) {
        Rect window = makeRect(105 + i * 85, 125, 30, 25);
        fillRect(scene, window, Colour{250, 240, 170});
        strokeRect(scene, window, 2, colours::white);
    }
    fillRectAlpha(scene, makeRect(200, 20, 160, 45), colours::white, 0.6);

    int count = 0;
    Rect left = makeRect(0, 0, 10, 1);
    Rect right = makeRect(10, 0, 10, 1);
    for (int x = 0; x < 20; ++x) {
        if (contains(left, x, 0)) {
            ++count;
        }
        if (contains(right, x, 0)) {
            ++count;
        }
    }
    std::cout << "touching rectangles cover " << count << " pixels of 20\n";

    if (!scene.savePPM("house.ppm")) {
        std::cout << "could not write house.ppm\n";
        return 1;
    }
    return 0;
}
