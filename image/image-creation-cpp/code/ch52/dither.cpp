#include <cmath>
#include <iostream>
#include <string>
#include <vector>
#include "dither.h"
#include "deflate.h"

std::string oneDecimal(double v) {
    const long long n = std::llround(v * 10.0);
    return std::to_string(n / 10) + "." + std::to_string(n % 10);
}

std::string colourText(Colour c) {
    return std::to_string(c.r) + " " + std::to_string(c.g) + " " + std::to_string(c.b);
}

int countWhite(const Image& image) {
    int count = 0;
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            count += (image.getPixel(x, y).r == 255) ? 1 : 0;
        }
    }
    return count;
}

void report(const std::string& label, const Image& image) {
    std::cout << label << " " << countWhite(image) << " of " << image.width() * image.height()
              << " white, looks like grey " << static_cast<int>(averageColour(image).r) << "\n";
}

void printDots(const std::string& label, const Image& image, int rows) {
    std::cout << label << "\n";
    for (int y = 0; y < rows; ++y) {
        std::cout << "    ";
        for (int x = 0; x < image.width(); ++x) {
            std::cout << ((image.getPixel(x, y).r == 255) ? "#" : ".");
        }
        std::cout << "\n";
    }
}

Image makeColourRamp() {
    Image ramp(64, 16);
    for (int x = 0; x < 64; ++x) {
        const Colour c = lerpColour(Colour{200, 100, 50}, Colour{40, 160, 220}, x / 63.0);
        fillRect(ramp, makeRect(x, 0, 1, 16), c);
    }
    return ramp;
}

Image makeScene() {
    Image scene(160, 110);
    for (int y = 0; y < 110; ++y) {
        const Colour c = lerpColour(Colour{70, 120, 190}, Colour{235, 190, 140}, y / 109.0);
        fillRect(scene, makeRect(0, y, 160, 1), c);
    }
    fillCircleAA(scene, 118.0, 38.0, 16.0, Colour{255, 230, 120});
    const std::vector<PointF> hills = {{0.0, 80.0},    {30.0, 62.0},   {65.0, 78.0}, {100.0, 58.0},
                                       {160.0, 84.0},  {160.0, 110.0}, {0.0, 110.0}};
    fillPolygonAA(scene, hills, Colour{60, 110, 60});
    fillRect(scene, makeRect(28, 70, 26, 22), Colour{200, 80, 60});
    fillPolygonAA(scene, {{24.0, 71.0}, {41.0, 56.0}, {58.0, 71.0}}, Colour{110, 50, 40});
    fillRect(scene, makeRect(37, 80, 8, 12), Colour{70, 45, 30});
    return scene;
}

int main() {
    std::cout << "Bayer 4 x 4:\n";
    for (int y = 0; y < 4; ++y) {
        std::cout << "   ";
        for (int x = 0; x < 4; ++x) {
            const int v = kBayer4[y * 4 + x];
            std::cout << ((v < 10) ? "  " : " ") << v;
        }
        std::cout << "\n";
    }
    std::cout << "thresholds of the top row: " << bayerThreshold(0, 0) << " " << bayerThreshold(1, 0)
              << " " << bayerThreshold(2, 0) << " " << bayerThreshold(3, 0) << "\n";

    const Image grey(16, 16, Colour{128, 128, 128});
    const std::vector<Colour> blackWhite = {colours::black, colours::white};
    const Image orderedLinear = orderedDither(grey, 2, true);
    const Image diffusedLinear = floydSteinberg(grey, blackWhite, true);
    std::cout << "\ngrey 128 as black and white dots:\n";
    report("  the grey itself:         ", grey);
    report("  threshold:               ", posterise(grey, 2));
    report("  ordered, sRGB values:    ", orderedDither(grey, 2, false));
    report("  ordered, linear light:   ", orderedLinear);
    report("  Floyd-Steinberg, sRGB:   ", floydSteinberg(grey, blackWhite, false));
    report("  Floyd-Steinberg, linear: ", diffusedLinear);
    printDots("ordered, linear light, top rows:", orderedLinear, 4);
    printDots("Floyd-Steinberg, linear light, top rows:", diffusedLinear, 4);

    const std::vector<Colour> corners = cubePalette(2);
    const ColourF orange = toColourF(Colour{200, 100, 50});
    std::vector<ColourF> cornerValues;
    for (Colour c : corners) {
        cornerValues.push_back(toColourF(c));
    }
    const int k = nearestIndex(orange, cornerValues);
    std::cout << "\nnearest of the 8 corner colours to 200 100 50: " << colourText(corners[k])
              << ", distance " << oneDecimal(255.0 * std::sqrt(distanceSquared(orange, cornerValues[k])))
              << "\n";

    const Image ramp = makeColourRamp();
    std::cout << "\ncolour ramp, average colour seen from far away:\n";
    std::cout << "  original:               " << colourText(averageColour(ramp)) << "\n";
    std::cout << "  nearest corner colour:  " << colourText(averageColour(posterise(ramp, 2))) << "\n";
    std::cout << "  ordered, 8 colours:     " << colourText(averageColour(orderedDither(ramp, 2)))
              << "\n";
    std::cout << "  Floyd-Steinberg, 8:     "
              << colourText(averageColour(floydSteinberg(ramp, corners))) << "\n";

    const Image scene = makeScene();
    Image greyScene = scene;
    makeGrey(greyScene);
    const Image tiles[8] = {scene,
                            posterise(scene, 2),
                            orderedDither(scene, 2),
                            floydSteinberg(scene, corners),
                            greyScene,
                            posterise(greyScene, 2),
                            orderedDither(greyScene, 2),
                            floydSteinberg(greyScene, blackWhite)};
    const std::string names[8] = {"original",   "8 colours",   "ordered, 8",  "Floyd-St., 8",
                                  "grey",       "threshold",   "ordered, b/w", "Floyd-St., b/w"};
    Image sheet(4 * 170 + 10, 2 * 134 + 10, colours::white);
    for (int i = 0; i < 8; ++i) {
        const int left = 10 + (i % 4) * 170;
        const int top = 10 + (i / 4) * 134;
        for (int y = 0; y < 110; ++y) {
            for (int x = 0; x < 160; ++x) {
                sheet.setPixel(left + x, top + y, tiles[i].getPixel(x, y));
            }
        }
        drawText(sheet, left, top + 114, names[i], colours::black);
    }
    if (!savePNGCompressed(sheet, "dither.png")) {
        std::cout << "could not write dither.png\n";
        return 1;
    }
    std::cout << "wrote dither.png\n";
    return 0;
}
