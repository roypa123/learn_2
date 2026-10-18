#include <cmath>
#include <iostream>
#include <string>
#include <vector>
#include "blur.h"
#include "deflate.h"

std::string fourDecimals(double v) {
    const long long n = std::llround(v * 10000.0);
    std::string digits = std::to_string(n % 10000);
    while (digits.size() < 4) {
        digits = "0" + digits;
    }
    return std::to_string(n / 10000) + "." + digits;
}

void printRow(const std::string& label, const Image& image) {
    std::cout << label;
    for (int x = 0; x < image.width(); ++x) {
        std::cout << " " << static_cast<int>(image.getPixel(x, 0).r);
    }
    std::cout << "\n";
}

std::string colourText(Colour c) {
    return std::to_string(c.r) + " " + std::to_string(c.g) + " " + std::to_string(c.b);
}

Image makeTest() {
    Image test(96, 64);
    for (int y = 0; y < 64; ++y) {
        for (int x = 0; x < 96; ++x) {
            const std::uint8_t v = ((x / 8 + y / 8) % 2 == 0) ? 40 : 200;
            Colour c{v, static_cast<std::uint8_t>(v / 2), static_cast<std::uint8_t>(255 - v)};
            if (x >= 60 && x < 80 && y >= 20 && y < 40) {
                c = colours::white;
            }
            test.setPixel(x, y, c);
        }
    }
    return test;
}

void compare(const std::string& label, const Image& a, const Image& b) {
    int different = 0;
    int largest = 0;
    for (int y = 0; y < a.height(); ++y) {
        for (int x = 0; x < a.width(); ++x) {
            const Colour p = a.getPixel(x, y);
            const Colour q = b.getPixel(x, y);
            const int d[3] = {std::abs(p.r - q.r), std::abs(p.g - q.g), std::abs(p.b - q.b)};
            for (int v : d) {
                different += (v > 0) ? 1 : 0;
                largest = std::max(largest, v);
            }
        }
    }
    std::cout << label << ": " << different << " of " << a.width() * a.height() * 3
              << " values differ, by at most " << largest << "\n";
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
    const double sigmas[2] = {0.5, 1.0};
    for (double s : sigmas) {
        const std::vector<double> w = gaussianWeights(s);
        std::cout << "Gaussian weights, sigma " << s << ":";
        double sum = 0.0;
        for (double v : w) {
            std::cout << " " << fourDecimals(v);
            sum += v;
        }
        std::cout << "  (sum " << sum << ")\n";
    }

    const Image test = makeTest();
    compare("sigma 1.5: 11 x 11 kernel vs separable",
            convolve(test, kernelFromWeights(gaussianWeights(1.5)), EdgeMode::Clamp, false),
            gaussianBlur(test, 1.5, EdgeMode::Clamp, false));
    compare("box radius 3: separable vs running sum", separableBlur(test, boxWeights(3)),
            boxBlurFast(test, 3));
    const int n = static_cast<int>(gaussianWeights(5.0).size());
    std::cout << "sigma 5: kernel " << n << " x " << n << ", multiplications per value: 2D " << n * n
              << ", separable " << 2 * n << "\n";

    Image spike(15, 1);
    spike.setPixel(7, 0, colours::white);
    Image boxed = spike;
    for (int pass = 0; pass < 3; ++pass) {
        boxed = separableBlur(boxed, boxWeights(1), EdgeMode::Clamp, false);
    }
    printRow("\nspike, three box blurs (radius 1):", boxed);
    printRow("spike, one Gaussian (sigma 1.41):  ",
             gaussianBlur(spike, std::sqrt(2.0), EdgeMode::Clamp, false));

    Image redGreen(4, 1);
    redGreen.setPixel(0, 0, colours::red);
    redGreen.setPixel(1, 0, colours::red);
    redGreen.setPixel(2, 0, colours::green);
    redGreen.setPixel(3, 0, colours::green);
    const Image blurredSrgb = separableBlur(redGreen, boxWeights(1), EdgeMode::Clamp, false);
    const Image blurredLinear = separableBlur(redGreen, boxWeights(1), EdgeMode::Clamp, true);
    std::cout << "\nred red green green, pixel 1 blurred: sRGB values "
              << colourText(blurredSrgb.getPixel(1, 0)) << ", linear light "
              << colourText(blurredLinear.getPixel(1, 0)) << "\n";

    Image stripes(48, 4);
    for (int y = 0; y < 4; ++y) {
        for (int x = 0; x < 48; ++x) {
            stripes.setPixel(x, y, (x % 4 < 2) ? colours::white : colours::black);
        }
    }
    printRow("\nstripes shrunk 3 times:          ", resizeNearest(stripes, 16, 1));
    printRow("blurred (sigma 1.5), then shrunk:",
             resizeNearest(gaussianBlur(stripes, 1.5), 16, 1));

    const Image scene = makeScene();
    const Image tiles[6] = {scene,
                            gaussianBlur(scene, 1.0),
                            gaussianBlur(scene, 3.0),
                            gaussianBlur(scene, 8.0),
                            boxBlurFast(scene, 8),
                            gaussianBlur(scene, 3.0, EdgeMode::Clamp, false)};
    const std::string names[6] = {"original",    "Gaussian sigma 1", "Gaussian sigma 3",
                                  "Gaussian sigma 8", "box radius 8", "sigma 3, sRGB values"};
    Image sheet(3 * 170 + 10, 2 * 134 + 10, colours::white);
    for (int i = 0; i < 6; ++i) {
        const int left = 10 + (i % 3) * 170;
        const int top = 10 + (i / 3) * 134;
        for (int y = 0; y < 110; ++y) {
            for (int x = 0; x < 160; ++x) {
                sheet.setPixel(left + x, top + y, tiles[i].getPixel(x, y));
            }
        }
        drawText(sheet, left, top + 114, names[i], colours::black);
    }
    if (!savePNGCompressed(sheet, "blur.png")) {
        std::cout << "could not write blur.png\n";
        return 1;
    }
    std::cout << "wrote blur.png\n";
    return 0;
}
