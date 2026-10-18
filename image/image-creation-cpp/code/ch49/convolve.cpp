#include <iostream>
#include <string>
#include <vector>
#include "convolve.h"
#include "deflate.h"

std::string padLeft(const std::string& text, int width) {
    std::string s = text;
    while (static_cast<int>(s.size()) < width) {
        s = " " + s;
    }
    return s;
}

Image greyGrid(int width, int height, const std::vector<int>& values) {
    Image grid(width, height);
    for (int i = 0; i < width * height; ++i) {
        const std::uint8_t g = static_cast<std::uint8_t>(values[i]);
        grid.setPixel(i % width, i / width, Colour{g, g, g});
    }
    return grid;
}

void printGrid(const std::string& title, const Image& grid) {
    std::cout << title << "\n";
    for (int y = 0; y < grid.height(); ++y) {
        std::cout << "  ";
        for (int x = 0; x < grid.width(); ++x) {
            std::cout << padLeft(std::to_string(grid.getPixel(x, y).r), 4);
        }
        std::cout << "\n";
    }
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
    const Image dot = greyGrid(5, 5, {0, 0, 0,  0, 0,
                                      0, 0, 0,  0, 0,
                                      0, 0, 90, 0, 0,
                                      0, 0, 0,  0, 0,
                                      0, 0, 0,  0, 0});
    printGrid("a dot:", dot);
    printGrid("3 x 3 box (average):", convolve(dot, boxKernel(3)));

    const Image edge = greyGrid(5, 5, {0, 0, 90, 90, 90,
                                       0, 0, 90, 90, 90,
                                       0, 0, 90, 90, 90,
                                       0, 0, 90, 90, 90,
                                       0, 0, 90, 90, 90});
    printGrid("an edge:", edge);
    printGrid("3 x 3 box:", convolve(edge, boxKernel(3)));
    const Kernel shiftRight{3, {0, 0, 0, 1, 0, 0, 0, 0, 0}};
    printGrid("shift kernel (weight 1 on the left neighbour):", convolve(edge, shiftRight));
    const Kernel difference{3, {0, 0, 0, -1, 0, 1, 0, 0, 0}};
    printGrid("difference kernel (right - left):", convolve(edge, difference));
    std::cout << "weights add up to: box " << kernelSum(boxKernel(3)) << ", identity "
              << kernelSum(identityKernel()) << ", difference " << kernelSum(difference) << "\n";

    const Image row = greyGrid(5, 1, {100, 80, 60, 40, 20});
    const Kernel across{3, {0, 0, 0, 1.0 / 3, 1.0 / 3, 1.0 / 3, 0, 0, 0}};
    const EdgeMode modes[4] = {EdgeMode::Zero, EdgeMode::Clamp, EdgeMode::Mirror, EdgeMode::Wrap};
    const std::string modeNames[4] = {"zero", "clamp", "mirror", "wrap"};
    std::cout << "\nthe row 100 80 60 40 20, averaged across:\n";
    for (int m = 0; m < 4; ++m) {
        const Image result = convolve(row, across, modes[m]);
        std::cout << "  " << modeNames[m] << std::string(8 - modeNames[m].size(), ' ');
        for (int x = 0; x < 5; ++x) {
            std::cout << padLeft(std::to_string(result.getPixel(x, 0).r), 4);
        }
        std::cout << "\n";
    }
    std::cout << "  index -2 with mirror: " << edgeIndex(-2, 5, EdgeMode::Mirror) << ", with clamp: "
              << edgeIndex(-2, 5, EdgeMode::Clamp) << ", with wrap: " << edgeIndex(-2, 5, EdgeMode::Wrap)
              << "\n";

    const Image spike = greyGrid(7, 1, {0, 0, 90, 0, 0, 0, 0});
    Image inPlace = spike;
    for (int x = 0; x < 7; ++x) {
        inPlace.setPixel(x, 0, convolvePixel(inPlace, x, 0, across, EdgeMode::Clamp, false));
    }
    printGrid("\nthe row 0 0 90 0 0 0 0, averaged into a new picture:", convolve(spike, across));
    printGrid("averaged in place (wrong):", inPlace);

    const Image scene = makeScene();
    const Kernel kernels[6] = {identityKernel(), boxKernel(3), boxKernel(9),
                               Kernel{3, {0, -1, 0, -1, 5, -1, 0, -1, 0}},
                               Kernel{3, {-1, 0, 1, -2, 0, 2, -1, 0, 1}}, shiftRight};
    const std::string names[6] = {"identity", "box 3 x 3", "box 9 x 9", "sharpen", "edges (x)", "shift"};
    Image sheet(3 * 170 + 10, 2 * 134 + 10, colours::white);
    for (int i = 0; i < 6; ++i) {
        const Image result = convolve(scene, kernels[i]);
        const int left = 10 + (i % 3) * 170;
        const int top = 10 + (i / 3) * 134;
        for (int y = 0; y < result.height(); ++y) {
            for (int x = 0; x < result.width(); ++x) {
                sheet.setPixel(left + x, top + y, result.getPixel(x, y));
            }
        }
        drawText(sheet, left, top + 114, names[i], colours::black);
    }
    if (!savePNGCompressed(sheet, "kernels.png")) {
        std::cout << "could not write kernels.png\n";
        return 1;
    }
    const long long photo = 1920LL * 1080 * 3;
    std::cout << "\nmultiplications for a 1920 x 1080 photo: 3 x 3 kernel " << photo * 9
              << ", 15 x 15 kernel " << photo * 225 << "\n";
    std::cout << "wrote kernels.png\n";
    return 0;
}
