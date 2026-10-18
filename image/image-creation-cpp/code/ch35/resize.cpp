#include <cmath>
#include <iostream>
#include <string>
#include "resize.h"

void paste(Image& dest, const Image& source, int ox, int oy) {
    for (int y = 0; y < source.height(); ++y) {
        for (int x = 0; x < source.width(); ++x) {
            dest.setPixel(ox + x, oy + y, source.getPixel(x, y));
        }
    }
}

Image makeSprite() {
    const std::string rows[8] = {"  ####  ", " #yyyy# ", "#y#yy#y#", "#yyyyyy#",
                                 "#y#yy#y#", "#yy##yy#", " #yyyy# ", "  ####  "};
    Image sprite(8, 8);
    for (int y = 0; y < 8; ++y) {
        for (int x = 0; x < 8; ++x) {
            char ch = rows[y][x];
            Colour c{120, 180, 240};
            if (ch == '#') {
                c = Colour{40, 40, 60};
            } else if (ch == 'y') {
                c = Colour{250, 210, 60};
            }
            sprite.setPixel(x, y, c);
        }
    }
    return sprite;
}

void printRow(const char* label, const Image& image) {
    std::cout << label;
    for (int x = 0; x < image.width(); ++x) {
        std::cout << " " << static_cast<int>(image.getPixel(x, 0).r);
    }
    std::cout << "\n";
}

int main() {
    std::cout << "3 to 7 pixels, source pixel for each new pixel:";
    for (int x = 0; x < 7; ++x) {
        std::cout << " " << static_cast<int>(std::floor((x + 0.5) * 3.0 / 7.0));
    }
    std::cout << "\nwithout the + 0.5:";
    for (int x = 0; x < 7; ++x) {
        std::cout << " " << static_cast<int>(std::floor(x * 3.0 / 7.0));
    }
    std::cout << "\n";

    Image strip(2, 1);
    strip.setPixel(0, 0, colours::black);
    strip.setPixel(1, 0, colours::white);
    printRow("black, white to 4, nearest:", resizeNearest(strip, 4, 1));
    printRow("black, white to 4, bilinear (linear light):", resizeBilinear(strip, 4, 1));
    printRow("black, white to 4, bilinear (sRGB bytes):", resizeBilinear(strip, 4, 1, false));

    Image stripes(4, 1);
    for (int x = 0; x < 4; ++x) {
        stripes.setPixel(x, 0, (x % 2 == 0) ? colours::black : colours::white);
    }
    printRow("black, white, black, white to 2, nearest:", resizeNearest(stripes, 2, 1));
    printRow("black, white, black, white to 2, box:", resizeBox(stripes, 2, 1));

    Image redGreen(2, 1);
    redGreen.setPixel(0, 0, colours::red);
    redGreen.setPixel(1, 0, colours::green);
    Image blendLinear = resizeBilinear(redGreen, 400, 40);
    Image blendBytes = resizeBilinear(redGreen, 400, 40, false);
    Colour m1 = blendLinear.getPixel(200, 0);
    Colour m2 = blendBytes.getPixel(200, 0);
    std::cout << "middle of red to green: linear light (" << static_cast<int>(m1.r) << ", "
              << static_cast<int>(m1.g) << ", " << static_cast<int>(m1.b) << "), sRGB bytes ("
              << static_cast<int>(m2.r) << ", " << static_cast<int>(m2.g) << ", "
              << static_cast<int>(m2.b) << ")\n";

    Image sprite = makeSprite();
    Image zoom(266, 128, colours::white);
    paste(zoom, resizeNearest(sprite, 128, 128), 0, 0);
    paste(zoom, resizeBilinear(sprite, 128, 128), 138, 0);

    Image blend(400, 80);
    paste(blend, blendBytes, 0, 0);
    paste(blend, blendLinear, 0, 40);

    Image rings(300, 300);
    for (int y = 0; y < 300; ++y) {
        for (int x = 0; x < 300; ++x) {
            double dx = x + 0.5 - 150.0;
            double dy = y + 0.5 - 150.0;
            double v = 0.5 + 0.5 * std::cos((dx * dx + dy * dy) / 150.0);
            std::uint8_t g = toByte(v);
            rings.setPixel(x, y, Colour{g, g, g});
        }
    }
    Image small(320, 100, colours::white);
    paste(small, resizeNearest(rings, 100, 100), 0, 0);
    paste(small, resizeBilinear(rings, 100, 100), 110, 0);
    paste(small, resizeBox(rings, 100, 100), 220, 0);

    Image turned(400, 200, colours::white);
    Mat3 place = rotation(degreesToRadians(30.0)) * scaling(10.0, 10.0) * translation(-4.0, -4.0);
    drawImageTransformed(turned, sprite, translation(100.0, 100.0) * place);
    drawImageTransformedSmooth(turned, sprite, translation(300.0, 100.0) * place);

    bool ok = zoom.savePPM("zoom.ppm");
    ok = ok && blend.savePPM("blend.ppm");
    ok = ok && rings.savePPM("rings.ppm");
    ok = ok && small.savePPM("small.ppm");
    ok = ok && turned.savePPM("turned.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
