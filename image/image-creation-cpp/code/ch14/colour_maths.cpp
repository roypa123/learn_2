#include <algorithm>
#include <cstdint>
#include <iostream>
#include "colourf.h"

void printColour(const std::string& label, Colour c) {
    std::cout << label << " = (" << static_cast<int>(c.r) << ", "
              << static_cast<int>(c.g) << ", " << static_cast<int>(c.b) << ")\n";
}

bool insideCircle(int x, int y, double cx, double cy, double radius) {
    double dx = (x + 0.5) - cx;
    double dy = (y + 0.5) - cy;
    return dx * dx + dy * dy <= radius * radius;
}

int main() {
    std::uint8_t a = 200;
    std::uint8_t b = 100;
    int sum = a + b;
    std::uint8_t wrapped = static_cast<std::uint8_t>(a + b);
    std::uint8_t clamped = static_cast<std::uint8_t>(std::min(a + b, 255));
    std::cout << "200 + 100 as int:  " << sum << "\n";
    std::cout << "stored in a byte:  " << static_cast<int>(wrapped) << "\n";
    std::cout << "clamped to 255:    " << static_cast<int>(clamped) << "\n";
    std::cout << "clamp(-20) = " << std::clamp(-20, 0, 255)
              << ", clamp(300) = " << std::clamp(300, 0, 255)
              << ", clamp(128) = " << std::clamp(128, 0, 255) << "\n\n";

    const ColourF red = toColourF(colours::red);
    const ColourF green = toColourF(colours::green);
    const ColourF blue = toColourF(colours::blue);
    const ColourF orange = toColourF(Colour{255, 128, 0});

    printColour("red + green", toColour(red + green));
    printColour("orange * 0.5", toColour(orange * 0.5));
    printColour("white light through cyan glass",
                toColour(toColourF(colours::white) * toColourF(colours::cyan)));
    printColour("orange light on blue paint", toColour(orange * blue));
    std::cout << "distance from red to blue = " << length(red - blue) << "\n";

    Image lights(300, 300);
    for (int y = 0; y < lights.height(); ++y) {
        for (int x = 0; x < lights.width(); ++x) {
            ColourF total;
            if (insideCircle(x, y, 150.0, 110.0, 75.0)) {
                total = total + red;
            }
            if (insideCircle(x, y, 110.0, 180.0, 75.0)) {
                total = total + green;
            }
            if (insideCircle(x, y, 190.0, 180.0, 75.0)) {
                total = total + blue;
            }
            lights.setPixel(x, y, toColour(total));
        }
    }

    Image overflow(256, 100);
    for (int y = 0; y < overflow.height(); ++y) {
        for (int x = 0; x < overflow.width(); ++x) {
            int brighter = x + 100;
            std::uint8_t v = 0;
            if (y < 50) {
                v = static_cast<std::uint8_t>(brighter);
            } else {
                v = static_cast<std::uint8_t>(std::clamp(brighter, 0, 255));
            }
            overflow.setPixel(x, y, Colour{v, v, v});
        }
    }

    bool ok = lights.savePPM("lights.ppm");
    ok = ok && overflow.savePPM("overflow.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    printColour("lights (150, 157)", lights.getPixel(150, 157));
    printColour("overflow (200, 10)", overflow.getPixel(200, 10));
    printColour("overflow (200, 60)", overflow.getPixel(200, 60));
    return 0;
}
