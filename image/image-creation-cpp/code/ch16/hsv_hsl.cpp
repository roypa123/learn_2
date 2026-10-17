#include <cmath>
#include <iostream>
#include <string>
#include "hsv.h"

double roundTo(double v, double factor) {
    return std::floor(v * factor + 0.5) / factor;
}

void describe(const std::string& name, Colour c) {
    HSV hsv = rgbToHsv(toColourF(c));
    HSL hsl = rgbToHsl(toColourF(c));
    std::cout << name << ": HSV (" << roundTo(hsv.h, 10) << ", " << roundTo(hsv.s, 1000)
              << ", " << roundTo(hsv.v, 1000) << ")   HSL (" << roundTo(hsl.h, 10) << ", "
              << roundTo(hsl.s, 1000) << ", " << roundTo(hsl.l, 1000) << ")\n";
}

void printColour(const std::string& label, Colour c) {
    std::cout << label << " = (" << static_cast<int>(c.r) << ", "
              << static_cast<int>(c.g) << ", " << static_cast<int>(c.b) << ")\n";
}

int main() {
    describe("orange", Colour{255, 128, 0});
    describe("pink  ", Colour{255, 192, 203});
    describe("grey  ", Colour{128, 128, 128});
    printColour("HSV (120, 1, 1)  ", toColour(hsvToRgb(HSV{120.0, 1.0, 1.0})));
    printColour("HSV (240, 0.5, 1)", toColour(hsvToRgb(HSV{240.0, 0.5, 1.0})));
    printColour("HSL (240, 1, 0.75)", toColour(hslToRgb(HSL{240.0, 1.0, 0.75})));
    printColour("red shifted by 120", shiftHue(colours::red, 120.0));

    Image strip(360, 40);
    for (int y = 0; y < strip.height(); ++y) {
        for (int x = 0; x < strip.width(); ++x) {
            strip.setPixel(x, y, toColour(hsvToRgb(HSV{static_cast<double>(x), 1.0, 1.0})));
        }
    }

    Image picker(256, 256);
    for (int y = 0; y < picker.height(); ++y) {
        for (int x = 0; x < picker.width(); ++x) {
            double s = x / 255.0;
            double v = 1.0 - y / 255.0;
            picker.setPixel(x, y, toColour(hsvToRgb(HSV{210.0, s, v})));
        }
    }

    Image lightness(360, 120);
    for (int y = 0; y < lightness.height(); ++y) {
        double l = 0.25 * (y / 40 + 1);
        for (int x = 0; x < lightness.width(); ++x) {
            HSL hsl{static_cast<double>(x), 1.0, l};
            lightness.setPixel(x, y, toColour(hslToRgb(hsl)));
        }
    }

    const Colour barColours[6] = {colours::red, colours::green, colours::blue,
                                  colours::yellow, colours::cyan, colours::magenta};
    Image shifted(360, 80);
    for (int y = 0; y < shifted.height(); ++y) {
        for (int x = 0; x < shifted.width(); ++x) {
            shifted.setPixel(x, y, shiftHue(barColours[x / 60], 120.0));
        }
    }

    bool ok = strip.savePPM("hue_strip.ppm");
    ok = ok && picker.savePPM("picker.ppm");
    ok = ok && lightness.savePPM("lightness.ppm");
    ok = ok && shifted.savePPM("bars_shifted.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
