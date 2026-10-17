#include <iostream>
#include <string>
#include "grey.h"

void printRow(const std::string& name, Colour c) {
    ColourF f = toColourF(c);
    std::cout << name << ": average " << static_cast<int>(toByte(plainAverage(f)))
              << ", luma " << static_cast<int>(greyByte(c)) << "\n";
}

int main() {
    const Colour barColours[6] = {colours::red, colours::green, colours::blue,
                                  colours::yellow, colours::cyan, colours::magenta};
    const std::string names[6] = {"red    ", "green  ", "blue   ",
                                  "yellow ", "cyan   ", "magenta"};
    for (int i = 0; i < 6; ++i) {
        printRow(names[i], barColours[i]);
    }
    printRow("white  ", colours::white);

    Image bars(360, 80);
    for (int y = 0; y < bars.height(); ++y) {
        for (int x = 0; x < bars.width(); ++x) {
            bars.setPixel(x, y, barColours[x / 60]);
        }
    }

    Image averaged = bars;
    for (int y = 0; y < averaged.height(); ++y) {
        for (int x = 0; x < averaged.width(); ++x) {
            ColourF f = toColourF(averaged.getPixel(x, y));
            std::uint8_t v = toByte(plainAverage(f));
            averaged.setPixel(x, y, Colour{v, v, v});
        }
    }

    const Colour orange{255, 128, 0};
    Image steps(250, 50);
    for (int y = 0; y < steps.height(); ++y) {
        for (int x = 0; x < steps.width(); ++x) {
            double amount = (x / 50) * 0.25;
            steps.setPixel(x, y, desaturate(orange, amount));
        }
    }

    bool ok = bars.savePPM("bars.ppm");
    ok = ok && averaged.savePPM("bars_average.ppm");
    ok = ok && saveGreyPGM(bars, "bars_luma.pgm");
    ok = ok && steps.savePPM("desaturate.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }

    Colour half = desaturate(orange, 0.5);
    Colour full = desaturate(orange, 1.0);
    std::cout << "\norange half grey = (" << static_cast<int>(half.r) << ", "
              << static_cast<int>(half.g) << ", " << static_cast<int>(half.b) << ")\n";
    std::cout << "orange full grey = (" << static_cast<int>(full.r) << ", "
              << static_cast<int>(full.g) << ", " << static_cast<int>(full.b) << ")\n";
    return 0;
}
