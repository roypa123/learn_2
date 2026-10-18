#include <iostream>
#include <string>
#include <vector>
#include "pointops.h"
#include "deflate.h"

std::string padLeft(const std::string& text, int width) {
    std::string s = text;
    while (static_cast<int>(s.size()) < width) {
        s = " " + s;
    }
    return s;
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

void paste(Image& dest, const Image& src, int left, int top) {
    for (int y = 0; y < src.height(); ++y) {
        for (int x = 0; x < src.width(); ++x) {
            dest.setPixel(left + x, top + y, src.getPixel(x, y));
        }
    }
}

int main() {
    const std::string names[8] = {"brightness +40", "contrast x1.5", "invert",    "threshold 128",
                                  "gamma 0.5",      "gamma 2.0",     "exposure x2", "levels 50-200"};
    const LookupTable tables[8] = {brightnessTable(40), contrastTable(1.5), invertTable(),
                                   thresholdTable(128), gammaTable(0.5),     gammaTable(2.0),
                                   exposureTable(2.0),  levelsTable(50, 200)};
    const int samples[6] = {0, 50, 100, 128, 200, 255};

    std::cout << "input:          ";
    for (int v : samples) {
        std::cout << padLeft(std::to_string(v), 5);
    }
    std::cout << "   average\n";
    for (int i = 0; i < 8; ++i) {
        std::cout << names[i] << std::string(16 - names[i].size(), ' ');
        for (int v : samples) {
            std::cout << padLeft(std::to_string(tables[i][v]), 5);
        }
        std::cout << "   " << tableAverage(tables[i]) << "\n";
    }

    const int v = 230;
    std::cout << "\n230 + 40 with clamping: " << static_cast<int>(clampByte(v + 40))
              << ", with wrap-around: " << static_cast<int>(static_cast<std::uint8_t>(v + 40)) << "\n";
    const LookupTable brightThenContrast = combineTables(tables[0], tables[1]);
    const LookupTable contrastThenBright = combineTables(tables[1], tables[0]);
    std::cout << "100: brightness then contrast = " << static_cast<int>(brightThenContrast[100])
              << ", contrast then brightness = " << static_cast<int>(contrastThenBright[100]) << "\n";
    const LookupTable twice = combineTables(invertTable(), invertTable());
    std::cout << "invert twice is the identity: " << (twice == identityTable() ? "yes" : "no") << "\n";

    const Image scene = makeScene();
    Image sheet(3 * 170 + 10, 3 * 134 + 10, colours::white);
    for (int i = 0; i < 9; ++i) {
        Image tile = scene;
        std::string label = "original";
        if (i > 0) {
            if (i == 4) {
                makeGrey(tile);
            }
            applyTable(tile, tables[i - 1]);
            label = names[i - 1];
        }
        const int left = 10 + (i % 3) * 170;
        const int top = 10 + (i / 3) * 134;
        paste(sheet, tile, left, top);
        drawText(sheet, left, top + 114, label, colours::black);
    }

    Image curves(4 * 150 + 10, 2 * 160 + 10, colours::white);
    for (int i = 0; i < 8; ++i) {
        const int left = 20 + (i % 4) * 150;
        const int top = 10 + (i / 4) * 160;
        drawCurve(curves, left, top, 120, tables[i], Colour{200, 40, 40});
        drawText(curves, left, top + 128, names[i], colours::black);
    }

    if (!savePNGCompressed(sheet, "operations.png") || !savePNGCompressed(curves, "curves.png")) {
        std::cout << "could not write the files\n";
        return 1;
    }
    std::cout << "wrote operations.png and curves.png\n";
    return 0;
}
