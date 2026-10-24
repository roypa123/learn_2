#include <cmath>
#include <iostream>
#include <string>
#include <vector>
#include "edges.h"
#include "deflate.h"

std::string oneDecimal(double v) {
    const long long n = std::llround(v * 10.0);
    return std::to_string(n / 10) + "." + std::to_string(n % 10);
}

void printRow(const std::string& label, const Image& image) {
    std::cout << label;
    for (int x = 0; x < image.width(); ++x) {
        std::cout << " " << static_cast<int>(image.getPixel(x, 0).r);
    }
    std::cout << "\n";
}

void printGreyRow(const std::string& label, const GreyF& g, int y) {
    std::cout << label;
    for (int x = 0; x < g.width; ++x) {
        std::cout << " " << std::llround(g.data[y * g.width + x]);
    }
    std::cout << "\n";
}

Image makeRow(const std::vector<int>& values) {
    Image row(static_cast<int>(values.size()), 1);
    for (int x = 0; x < row.width(); ++x) {
        const std::uint8_t v = static_cast<std::uint8_t>(values[x]);
        row.setPixel(x, 0, Colour{v, v, v});
    }
    return row;
}

double gridValue(const std::string& kind, int x, int y) {
    if (kind == "dot") {
        return (x == 2 && y == 2) ? 90.0 : 0.0;
    }
    if (kind == "edge") {
        return (x >= 2) ? 90.0 : 0.0;
    }
    if (kind == "flipped") {
        return (x >= 2) ? 0.0 : 90.0;
    }
    return (x + y >= 5) ? 90.0 : 0.0;
}

GreyF makeGrid(const std::string& kind) {
    GreyF g = makeGreyF(5, 5);
    for (int y = 0; y < 5; ++y) {
        for (int x = 0; x < 5; ++x) {
            g.data[y * 5 + x] = gridValue(kind, x, y);
        }
    }
    return g;
}

Image makeNoisy() {
    Image noisy(64, 64);
    for (int y = 0; y < 64; ++y) {
        for (int x = 0; x < 64; ++x) {
            const int base = (x < 32) ? 80 : 160;
            const int noise = ((x * 37 + y * 53 + x * y) % 7 - 3) * 6;
            const std::uint8_t v = static_cast<std::uint8_t>(base + noise);
            noisy.setPixel(x, y, Colour{v, v, v});
        }
    }
    return noisy;
}

int countAtLeast(const GreyF& g, double level) {
    int count = 0;
    for (double v : g.data) {
        count += (v >= level) ? 1 : 0;
    }
    return count;
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
    std::cout << "weights add up to: sharpen " << kernelSum(sharpenKernel()) << ", Laplacian "
              << kernelSum(laplacianKernel()) << ", Sobel x " << kernelSum(sobelX()) << "\n";

    const Image gentle = makeRow({100, 100, 100, 160, 160, 160});
    printRow("\nedge 100 -> 160, sharpen kernel:  ", convolve(gentle, sharpenKernel()));
    printRow("unsharp mask, sigma 1, amount 1:  ", unsharpMask(gentle, 1.0, 1.0));
    printRow("the same in linear light:         ", unsharpMask(gentle, 1.0, 1.0, true));
    const Image strong = makeRow({50, 50, 50, 200, 200, 200});
    printRow("edge 50 -> 200, sharpen kernel:   ", convolve(strong, sharpenKernel()));

    const GreyF edge = makeGrid("edge");
    const GreyF flipped = makeGrid("flipped");
    printGreyRow("\nedge grid, Sobel x:       ", convolveGrey(edge, sobelX()), 2);
    printGreyRow("edge grid, Sobel y:       ", convolveGrey(edge, sobelY()), 2);
    printGreyRow("flipped edge, Sobel x:    ", convolveGrey(flipped, sobelX()), 2);
    printRow("the same, kept as bytes:  ", greyFToImage(convolveGrey(flipped, sobelX()), 1.0));

    const GreyF diagonal = makeGrid("diagonal");
    const double gx = convolveGrey(diagonal, sobelX()).data[2 * 5 + 2];
    const double gy = convolveGrey(diagonal, sobelY()).data[2 * 5 + 2];
    std::cout << "diagonal edge, centre: gx " << gx << ", gy " << gy << ", strength "
              << oneDecimal(std::sqrt(gx * gx + gy * gy)) << ", direction "
              << directionDegrees(gx, gy) << " degrees\n";
    std::cout << "directions: edge grid " << directionDegrees(360.0, 0.0) << ", flipped "
              << directionDegrees(-360.0, 0.0) << "\n";

    printGreyRow("\ndot grid, Laplacian:      ", convolveGrey(makeGrid("dot"), laplacianKernel()), 2);
    printGreyRow("edge grid, Laplacian:     ", convolveGrey(edge, laplacianKernel()), 2);

    const Image noisy = makeNoisy();
    const int plain = countAtLeast(sobelMagnitude(toGreyF(noisy)), 100.0);
    const Image smooth = gaussianBlur(noisy, 1.0, EdgeMode::Clamp, false);
    const int blurred = countAtLeast(sobelMagnitude(toGreyF(smooth)), 100.0);
    std::cout << "\nnoisy edge, pixels with strength >= 100: " << plain << " without blur, "
              << blurred << " after a blur (the real edge: 2 x 64 = 128)\n";

    const Image scene = makeScene();
    const GreyF grey = toGreyF(scene);
    const GreyF sx = convolveGrey(grey, sobelX());
    const GreyF sy = convolveGrey(grey, sobelY());
    const GreyF strength = magnitudeOf(sx, sy);
    const double largest = largestValue(strength);
    const Image tiles[8] = {scene,
                            unsharpMask(scene, 1.0, 1.5),
                            unsharpMask(scene, 2.0, 5.0),
                            greyFToImage(sx, 0.25, 128.0),
                            greyFToImage(strength, 255.0 / largest),
                            edgeMap(strength, 0.25 * largest),
                            directionColours(sx, sy, largest),
                            greyFToImage(convolveGrey(grey, laplacianKernel()), 1.0, 128.0)};
    const std::string names[8] = {"original",   "sharpened",  "far too sharp", "Sobel x",
                                  "strength",   "edge map",   "direction",     "Laplacian"};
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
    if (!savePNGCompressed(sheet, "edges.png")) {
        std::cout << "could not write edges.png\n";
        return 1;
    }
    std::cout << "wrote edges.png\n";
    return 0;
}
