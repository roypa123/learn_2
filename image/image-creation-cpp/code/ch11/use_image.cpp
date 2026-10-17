#include <iostream>
#include "image.h"

void printColour(const std::string& label, Colour c) {
    std::cout << label << " = (" << static_cast<int>(c.r) << ", "
              << static_cast<int>(c.g) << ", "
              << static_cast<int>(c.b) << ")\n";
}

int main() {
    Image first(3, 2);
    first.setPixel(0, 0, colours::red);
    first.setPixel(1, 0, colours::green);
    first.setPixel(2, 0, colours::blue);
    first.setPixel(0, 1, colours::yellow);
    first.setPixel(1, 1, colours::white);
    first.setPixel(2, 1, colours::black);

    Image stripes(90, 60, colours::white);
    for (int y = 0; y < stripes.height(); ++y) {
        for (int x = 0; x < stripes.width(); ++x) {
            if (y < 20) {
                stripes.setPixel(x, y, Colour{255, 128, 0});
            } else if (y >= 40) {
                stripes.setPixel(x, y, Colour{0, 128, 255});
            }
        }
    }

    Image gradient(256, 256);
    for (int y = 0; y < gradient.height(); ++y) {
        for (int x = 0; x < gradient.width(); ++x) {
            Colour c{static_cast<std::uint8_t>(x), static_cast<std::uint8_t>(y), 128};
            gradient.setPixel(x, y, c);
        }
    }

    bool ok = first.savePPM("first.ppm");
    ok = ok && stripes.savePPM("stripes.ppm");
    ok = ok && gradient.savePPM("gradient.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }

    printColour("gradient (200, 50)", gradient.getPixel(200, 50));
    printColour("gradient (300, 300)", gradient.getPixel(300, 300));
    printColour("stripes (10, 30)", stripes.getPixel(10, 30));
    std::cout << "stripes is " << stripes.width() << " x " << stripes.height()
              << ", " << stripes.data().size() << " bytes\n";
    return 0;
}
