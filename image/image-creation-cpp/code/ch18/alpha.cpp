#include <cmath>
#include <iostream>
#include <string>
#include "alpha.h"

double roundTo(double v, double factor) {
    return std::floor(v * factor + 0.5) / factor;
}

void printColour(const std::string& label, Colour c) {
    std::cout << label << " = (" << static_cast<int>(c.r) << ", "
              << static_cast<int>(c.g) << ", " << static_cast<int>(c.b) << ")\n";
}

void printFA(const std::string& label, ColourFA c) {
    std::cout << label << " = (" << roundTo(c.r, 1000) << ", " << roundTo(c.g, 1000) << ", "
              << roundTo(c.b, 1000) << ", alpha " << roundTo(c.a, 1000) << ")\n";
}

bool insideCircle(int x, int y, double cx, double cy, double radius) {
    double dx = (x + 0.5) - cx;
    double dy = (y + 0.5) - cy;
    return dx * dx + dy * dy <= radius * radius;
}

Colour checker(int x, int y) {
    bool light = ((x / 20) + (y / 20)) % 2 == 0;
    return light ? Colour{230, 230, 230} : Colour{150, 150, 150};
}

int main() {
    const ColourF red = toLinear(colours::red);
    const ColourF blue = toLinear(colours::blue);

    ColourFA a = overStraight(withAlpha(red, 0.5), withAlpha(blue, 1.0));
    printColour("50% red over solid blue  ", fromLinear(ColourF{a.r, a.g, a.b}));
    printFA("50% red over 50% blue    ", overStraight(withAlpha(red, 0.5), withAlpha(blue, 0.5)));
    ColourFA p = overPremultiplied(premultiply(withAlpha(red, 0.5)),
                                   premultiply(withAlpha(blue, 0.5)));
    printFA("same, premultiplied      ", p);
    printFA("premultiplied, undone    ", unpremultiply(p));

    printColour("80% red over solid blue  ", blendOver(colours::blue, colours::red, 0.8));
    printColour("80% blue over solid red  ", blendOver(colours::red, colours::blue, 0.8));
    printColour("50% white over black, bytes ", lerpColour(colours::black, colours::white, 0.5));
    printColour("50% white over black, linear", blendOver(colours::black, colours::white, 0.5));

    Image glass(300, 200);
    for (int y = 0; y < glass.height(); ++y) {
        for (int x = 0; x < glass.width(); ++x) {
            glass.setPixel(x, y, checker(x, y));
        }
    }
    const double cxs[3] = {120.0, 180.0, 150.0};
    const double cys[3] = {80.0, 80.0, 130.0};
    const Colour inks[3] = {colours::red, colours::green, colours::blue};
    for (int i = 0; i < 3; ++i) {
        for (int y = 0; y < glass.height(); ++y) {
            for (int x = 0; x < glass.width(); ++x) {
                if (insideCircle(x, y, cxs[i], cys[i], 55.0)) {
                    blendPixel(glass, x, y, inks[i], 0.6);
                }
            }
        }
    }

    Image fade(300, 80);
    for (int y = 0; y < fade.height(); ++y) {
        for (int x = 0; x < fade.width(); ++x) {
            double alpha = static_cast<double>(x) / (fade.width() - 1);
            Colour back = checker(x, y);
            Colour c = (y < 40) ? lerpColour(back, colours::red, alpha)
                                : blendOver(back, colours::red, alpha);
            fade.setPixel(x, y, c);
        }
    }

    bool ok = glass.savePPM("glass.ppm");
    ok = ok && fade.savePPM("fade.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
