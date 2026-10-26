#include <cmath>
#include <iostream>
#include <string>
#include <vector>
#include "warp.h"
#include "deflate.h"

std::string twoDecimals(double v) {
    const long long n = std::llround(v * 100.0);
    const std::string digits = std::to_string(n % 100);
    return std::to_string(n / 100) + "." + ((digits.size() < 2) ? "0" + digits : digits);
}

std::string pointText(PointF p) {
    return "(" + twoDecimals(p.x) + ", " + twoDecimals(p.y) + ")";
}

void showSource(const std::string& label, const Warp& w, PointF p) {
    std::cout << label << pointText(p) << " reads from " << pointText(warpSource(p, w)) << "\n";
}

Image makeGrid() {
    Image grid(160, 110);
    for (int y = 0; y < 110; ++y) {
        for (int x = 0; x < 160; ++x) {
            const bool light = (x / 10 + y / 10) % 2 == 0;
            grid.setPixel(x, y, light ? Colour{230, 230, 230} : Colour{40, 40, 40});
        }
    }
    return grid;
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
    const PointF middle{80.0, 55.0};
    const Warp none{};
    const Warp wave{WarpKind::Wave, middle, 6.0, 40.0};
    const Warp ripple{WarpKind::Ripple, middle, 3.0, 20.0};
    const Warp swirl{WarpKind::Swirl, middle, kPi / 2.0, 50.0};
    const Warp bulge{WarpKind::Bulge, middle, 2.0, 50.0};
    const Warp pinch{WarpKind::Bulge, middle, 0.5, 50.0};

    showSource("none:   the new point ", none, PointF{105.0, 55.0});
    showSource("wave:   the new point ", wave, PointF{50.0, 10.0});
    showSource("        the new point ", wave, PointF{50.0, 30.0});
    showSource("ripple: the new point ", ripple, PointF{85.0, 55.0});
    showSource("swirl:  the new point ", swirl, PointF{105.0, 55.0});
    showSource("        the new point ", swirl, PointF{80.0, 55.0});
    showSource("bulge:  the new point ", bulge, PointF{105.0, 55.0});
    showSource("pinch:  the new point ", pinch, PointF{105.0, 55.0});

    const Image grid = makeGrid();
    int holes = 0;
    const Image forward = warpForward(grid, swirl, colours::red, holes);
    std::cout << "\nswirl done forwards: " << holes << " of " << grid.width() * grid.height()
              << " pixels never painted\n";

    const Image scene = makeScene();
    const Colour black = colours::black;
    const Image tiles[8] = {scene,
                            warpImage(scene, wave, black),
                            warpImage(scene, swirl, black),
                            warpImage(scene, bulge, black),
                            grid,
                            warpImage(grid, ripple, black),
                            warpImage(grid, pinch, black),
                            forward};
    const std::string names[8] = {"original", "wave",  "swirl",          "bulge",
                                  "grid",     "ripple", "pinch",         "swirl, forwards"};
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
    if (!savePNGCompressed(sheet, "warp.png")) {
        std::cout << "could not write warp.png\n";
        return 1;
    }
    std::cout << "wrote warp.png\n";
    return 0;
}
