#include <cmath>
#include <iostream>
#include <vector>
#include "image.h"

double inverseLerp(double a, double b, double v) {
    return (v - a) / (b - a);
}

double remap(double v, double inMin, double inMax, double outMin, double outMax) {
    return lerp(outMin, outMax, inverseLerp(inMin, inMax, v));
}

int roundToInt(double v) {
    return static_cast<int>(std::floor(v + 0.5));
}

Colour multiStop(const std::vector<Colour>& stops, double t) {
    if (t <= 0.0) {
        return stops.front();
    }
    if (t >= 1.0) {
        return stops.back();
    }
    double scaled = t * static_cast<double>(stops.size() - 1);
    int i = static_cast<int>(scaled);
    double local = scaled - i;
    return lerpColour(stops[i], stops[i + 1], local);
}

void printColour(const std::string& label, Colour c) {
    std::cout << label << " = (" << static_cast<int>(c.r) << ", "
              << static_cast<int>(c.g) << ", " << static_cast<int>(c.b) << ")\n";
}

int main() {
    Image across(300, 60);
    for (int y = 0; y < across.height(); ++y) {
        for (int x = 0; x < across.width(); ++x) {
            double t = static_cast<double>(x) / (across.width() - 1);
            across.setPixel(x, y, lerpColour(colours::red, colours::blue, t));
        }
    }

    Image sky(200, 300);
    const Colour night{10, 20, 80};
    const Colour sunset{255, 150, 50};
    for (int y = 0; y < sky.height(); ++y) {
        double t = static_cast<double>(y) / (sky.height() - 1);
        Colour c = lerpColour(night, sunset, t);
        for (int x = 0; x < sky.width(); ++x) {
            sky.setPixel(x, y, c);
        }
    }

    Image rainbow(360, 40);
    const std::vector<Colour> stops = {colours::red, colours::yellow, colours::green,
                                       colours::cyan, colours::blue, colours::magenta};
    for (int y = 0; y < rainbow.height(); ++y) {
        for (int x = 0; x < rainbow.width(); ++x) {
            double t = static_cast<double>(x) / (rainbow.width() - 1);
            rainbow.setPixel(x, y, multiStop(stops, t));
        }
    }

    Image graph(201, 201, colours::white);
    const Colour grey{200, 200, 200};
    for (int i = 0; i < 201; ++i) {
        graph.setPixel(i, 100, grey);
        graph.setPixel(100, i, grey);
    }
    for (int px = 0; px < graph.width(); ++px) {
        double mathsX = remap(px, 0, graph.width() - 1, -1.0, 1.0);
        double mathsY = mathsX * mathsX;
        double row = remap(mathsY, -1.0, 1.0, 0, graph.height() - 1);
        int py = (graph.height() - 1) - roundToInt(row);
        graph.setPixel(px, py, colours::red);
    }

    bool ok = across.savePPM("across.ppm");
    ok = ok && sky.savePPM("sky.ppm");
    ok = ok && rainbow.savePPM("rainbow.ppm");
    ok = ok && graph.savePPM("graph.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }

    printColour("red to blue at t = 0.25", lerpColour(colours::red, colours::blue, 0.25));
    printColour("across (150, 0)", across.getPixel(150, 0));
    printColour("rainbow (359, 0)", rainbow.getPixel(359, 0));
    std::cout << "graph: maths x = 0.5 is drawn at row "
              << (graph.height() - 1) - roundToInt(remap(0.25, -1.0, 1.0, 0, 200)) << "\n";

    const double tests[] = {2.4, 2.5, -2.4, -2.6};
    for (double v : tests) {
        std::cout << v << ": cut gives " << static_cast<int>(v + 0.5)
                  << ", floor gives " << roundToInt(v) << "\n";
    }
    return 0;
}
