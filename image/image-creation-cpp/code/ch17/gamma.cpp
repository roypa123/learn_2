#include <cmath>
#include <iostream>
#include <string>
#include "grey.h"
#include "srgb.h"

double roundTo(double v, double factor) {
    return std::floor(v * factor + 0.5) / factor;
}

void printColour(const std::string& label, Colour c) {
    std::cout << label << " = (" << static_cast<int>(c.r) << ", "
              << static_cast<int>(c.g) << ", " << static_cast<int>(c.b) << ")\n";
}

int main() {
    const int bytes[5] = {0, 64, 128, 188, 255};
    for (int b : bytes) {
        std::cout << "byte " << b << " gives " << roundTo(srgbToLinear(b / 255.0), 10000)
                  << " of full light\n";
    }
    std::cout << "half the light needs byte "
              << static_cast<int>(toByte(linearToSrgb(0.5))) << "\n";
    std::cout << "gamma 2.2 guess for byte 128: "
              << roundTo(std::pow(128 / 255.0, 2.2), 10000) << "\n\n";

    printColour("red-green middle, byte lerp  ", lerpColour(colours::red, colours::green, 0.5));
    printColour("red-green middle, linear lerp", lerpLinear(colours::red, colours::green, 0.5));

    const Colour orange{255, 128, 0};
    double lum = luminance(orange);
    std::cout << "orange: luma byte " << static_cast<int>(greyByte(orange))
              << ", luminance " << roundTo(lum, 1000)
              << ", as a grey byte " << static_cast<int>(toByte(linearToSrgb(lum))) << "\n";

    Image checks(300, 100);
    for (int y = 0; y < checks.height(); ++y) {
        for (int x = 0; x < checks.width(); ++x) {
            Colour c;
            if (x < 100) {
                c = ((x + y) % 2 == 0) ? colours::black : colours::white;
            } else if (x < 200) {
                c = Colour{128, 128, 128};
            } else {
                c = Colour{188, 188, 188};
            }
            checks.setPixel(x, y, c);
        }
    }

    Image blends(300, 100);
    for (int y = 0; y < blends.height(); ++y) {
        for (int x = 0; x < blends.width(); ++x) {
            double t = static_cast<double>(x) / (blends.width() - 1);
            Colour c = (y < 50) ? lerpColour(colours::red, colours::green, t)
                                : lerpLinear(colours::red, colours::green, t);
            blends.setPixel(x, y, c);
        }
    }

    Image steps(320, 100);
    for (int y = 0; y < steps.height(); ++y) {
        for (int x = 0; x < steps.width(); ++x) {
            int band = x / 20;
            std::uint8_t v = 0;
            if (y < 50) {
                v = static_cast<std::uint8_t>(band * 17);
            } else {
                v = toByte(linearToSrgb(band / 15.0));
            }
            steps.setPixel(x, y, Colour{v, v, v});
        }
    }

    bool ok = checks.savePPM("checks.ppm");
    ok = ok && blends.savePPM("blends.ppm");
    ok = ok && steps.savePPM("steps.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
